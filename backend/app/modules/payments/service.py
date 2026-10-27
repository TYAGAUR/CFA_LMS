"""Order lifecycle, payment confirmation, webhooks, refunds (BR-PAY-03..09, A-08 §4).

Published events (contract in A-08 §6):
  payments.order_paid      {order_id, number, user_id, purpose, reference_id, amount_paise, provider}
  payments.payment_failed  {order_id, user_id, purpose, reference_id, error}
  payments.order_refunded  {order_id, user_id, purpose, reference_id, refund_paise, full}
"""

import json
import logging
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import events
from app.core.config import get_settings
from app.core.errors import AppError, Conflict, Invalid, NotFound
from app.core.ids import uuid7
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.payments import models as m
from app.modules.payments.models import Order, Payment, PaymentEvent, Refund
from app.modules.payments.providers import get_provider
from app.modules.payments.providers.base import OrderIntent, PaymentInfo
from app.modules.users.models import User

log = logging.getLogger("payments")


async def _next_number(session: AsyncSession) -> str:
    n = await session.scalar(text("SELECT nextval('order_number_seq')"))
    return f"KSC-{now_utc().year}-{n:06d}"


async def create_order(session: AsyncSession, *, user: User, purpose: str, reference_id: UUID,
                       amount_paise: int, description: str) -> tuple[Order, dict]:
    if amount_paise <= 0:
        raise Invalid("Amount must be positive")
    provider = get_provider()
    order = Order(number=await _next_number(session), user_id=user.id, purpose=purpose, reference_id=reference_id,
                  description=description, amount_paise=amount_paise, currency="INR", provider=provider.name,
                  expires_at=now_utc() + timedelta(minutes=get_settings().order_reuse_minutes))
    session.add(order)
    await session.flush()
    try:
        po = await provider.create_order(OrderIntent(
            str(order.id), order.number, amount_paise, "INR", description, user.full_name, user.mobile_e164,
            user.email))
    except Exception as exc:
        log.exception("gateway create_order failed")
        raise AppError("The payment gateway is not reachable. Please try again.", code="gateway_unavailable",
                       status=502) from exc
    order.provider_order_id = po.provider_order_id
    order.notes = {"checkout": po.checkout}
    await audit.record(session, "order.created", actor=user, target_type="order", target_id=order.id,
                       subject_user_id=user.id,
                       metadata={"number": order.number, "amount_paise": amount_paise, "purpose": purpose})
    return order, po.checkout


async def open_order_for(session: AsyncSession, reference_id: UUID, amount_paise: int) -> Order | None:
    """An unpaid order for this reference that can be reused (BR-PAY-03)."""
    o = await session.scalar(
        select(Order).where(Order.reference_id == reference_id, Order.status == m.CREATED)
        .order_by(Order.created_at.desc()).limit(1)
    )
    if o and o.expires_at > now_utc() and o.amount_paise == amount_paise and o.provider == get_provider().name:
        return o
    if o:
        o.status = m.EXPIRED
    return None


async def _publish(session: AsyncSession, topic: str, order: Order, **extra) -> None:
    await events.publish(session, topic, {
        "order_id": order.id, "number": order.number, "user_id": order.user_id, "purpose": order.purpose,
        "reference_id": order.reference_id, "amount_paise": order.amount_paise, "provider": order.provider,
        **extra,
    })


async def apply_payment(session: AsyncSession, order: Order, info: PaymentInfo, source: str) -> Order:
    """Idempotent: applying the same captured payment twice changes nothing (BR-PAY-05)."""
    pay = await session.scalar(select(Payment).where(Payment.provider_payment_id == info.provider_payment_id))
    if pay is None:
        pay = Payment(order_id=order.id, provider=order.provider, provider_payment_id=info.provider_payment_id,
                      status=info.status, amount_paise=info.amount_paise)
        session.add(pay)
    pay.status, pay.method, pay.amount_paise = info.status, info.method, info.amount_paise
    pay.error_code, pay.error_description = info.error_code, info.error_description

    if info.status == "authorized":
        info = await get_provider(order.provider).capture(info.provider_payment_id, order.amount_paise,
                                                          order.currency)
        pay.status = info.status

    if info.status == "captured":
        pay.captured_at = pay.captured_at or now_utc()
        if order.status in (m.PAID, m.REFUNDED, m.PARTIALLY_REFUNDED, m.AMOUNT_MISMATCH):
            return order
        if info.amount_paise != order.amount_paise:  # BR-PAY-06
            order.status = m.AMOUNT_MISMATCH
            await audit.record(session, "order.amount_mismatch", actor_type="system", target_type="order",
                               target_id=order.id, subject_user_id=order.user_id,
                               metadata={"expected": order.amount_paise, "captured": info.amount_paise})
            return order
        order.status, order.paid_at = m.PAID, now_utc()
        await audit.record(session, "order.paid", actor_type="system", target_type="order", target_id=order.id,
                           subject_user_id=order.user_id,
                           metadata={"number": order.number, "payment_id": info.provider_payment_id,
                                     "source": source, "method": info.method})
        await _publish(session, "payments.order_paid", order)
    elif info.status == "failed":
        # A failed attempt does not close the order: the student may retry (Razorpay semantics).
        await _publish(session, "payments.payment_failed", order, error=info.error_description)
    return order


async def confirm_checkout(session: AsyncSession, user: User, order_id: UUID, payload: dict) -> Order:
    order = await session.get(Order, order_id, with_for_update=True)
    if order is None or order.user_id != user.id:
        raise NotFound()
    if order.status == m.PAID:
        return order
    provider = get_provider(order.provider)
    try:
        oid, pid = provider.verify_checkout(payload)
    except ValueError as exc:
        await audit.record(session, "order.checkout_signature_invalid", actor=user, target_type="order",
                           target_id=order.id, with_ip=True)
        raise Invalid("We could not verify this payment.", code="payment_unverified") from exc
    if oid != order.provider_order_id:
        raise Invalid("Payment does not belong to this order.", code="payment_mismatch")
    info = await provider.fetch_payment(pid)  # never trust the browser alone (BR-PAY-04)
    return await apply_payment(session, order, info, "checkout")


async def handle_webhook(session: AsyncSession, provider_name: str, headers: dict[str, str], body: bytes) -> str:
    provider = get_provider(provider_name)
    if not provider.verify_webhook(headers, body):
        await audit.record(session, "payment.webhook_rejected", actor_type="webhook", with_ip=True,
                           metadata={"provider": provider_name})
        await session.commit()
        raise AppError("Invalid signature", code="invalid_signature", status=400)
    ev = provider.parse_webhook(headers, body)
    inserted = await session.scalar(
        insert(PaymentEvent).values(
            id=uuid7(), provider=provider_name,
            event_id=ev.event_id, event_type=ev.raw_type, payload=json.loads(body), signature_valid=True,
            received_at=now_utc(),
        ).on_conflict_do_nothing(index_elements=["provider", "event_id"]).returning(PaymentEvent.id)
    )
    if inserted is None:
        return "duplicate"
    row = await session.get(PaymentEvent, inserted)
    try:
        if ev.payment and ev.type in ("payment.captured", "payment.failed"):
            order = await session.scalar(select(Order).where(Order.provider_order_id == ev.payment.provider_order_id)
                                         .with_for_update())
            if order is None:
                row.error = "order not found"
            else:
                await apply_payment(session, order, ev.payment, "webhook")
        elif ev.type == "refund.processed" and ev.refund_id:
            rf = await session.scalar(select(Refund).where(Refund.provider_refund_id == ev.refund_id))
            if rf:
                rf.status = "processed"
        row.processed_at = now_utc()
    except Exception as exc:  # keep the event for replay; the gateway will retry
        log.exception("webhook processing failed")
        row.error = str(exc)[:500]
        raise
    return "processed"


async def refund(session: AsyncSession, order_id: UUID, amount_paise: int | None, reason: str, actor) -> Refund:
    order = await session.get(Order, order_id, with_for_update=True)
    if order is None:
        raise NotFound()
    if order.status not in (m.PAID, m.PARTIALLY_REFUNDED):
        raise Conflict("Only paid orders can be refunded.")
    remaining = order.amount_paise - order.refunded_paise
    amount = amount_paise or remaining
    if amount <= 0 or amount > remaining:
        raise Invalid(f"Refund must be between ₹0.01 and ₹{remaining / 100:,.2f}.")
    pay = await session.scalar(select(Payment).where(Payment.order_id == order.id, Payment.status == "captured"))
    if order.provider == "offline":
        info_id, status = None, "processed"
    else:
        if pay is None:
            raise Conflict("No captured payment found for this order.")
        ri = await get_provider(order.provider).refund(pay.provider_payment_id, amount, {"order": order.number})
        info_id, status = ri.provider_refund_id, ri.status
    rf = Refund(order_id=order.id, payment_id=pay.id if pay else None, amount_paise=amount, status=status,
                provider_refund_id=info_id, reason=reason, created_by=getattr(actor, "id", None))
    session.add(rf)
    order.refunded_paise += amount
    full = order.refunded_paise >= order.amount_paise
    order.status = m.REFUNDED if full else m.PARTIALLY_REFUNDED
    await audit.record(session, "order.refunded", actor=actor, target_type="order", target_id=order.id,
                       subject_user_id=order.user_id, reason=reason,
                       metadata={"amount_paise": amount, "full": full})
    await _publish(session, "payments.order_refunded", order, refund_paise=amount, full=full)
    await session.flush()
    return rf


async def record_offline(session: AsyncSession, *, user: User, purpose: str, reference_id: UUID,
                         amount_paise: int, description: str, reference: str, actor) -> Order:
    """BR-PAY-09: cash / bank transfer recorded by an admin."""
    order = Order(number=await _next_number(session), user_id=user.id, purpose=purpose, reference_id=reference_id,
                  description=description, amount_paise=amount_paise, currency="INR", provider="offline",
                  status=m.PAID, paid_at=now_utc(), expires_at=now_utc(), offline_reference=reference)
    session.add(order)
    await session.flush()
    await audit.record(session, "order.offline_recorded", actor=actor, target_type="order", target_id=order.id,
                       subject_user_id=user.id, metadata={"amount_paise": amount_paise, "reference": reference})
    await _publish(session, "payments.order_paid", order)
    return order
