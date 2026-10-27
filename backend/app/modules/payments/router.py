"""Payment endpoints: confirm checkout, order status, webhooks, mock gateway (A-08 §5)."""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import NotFound
from app.core.schemas import In, Out
from app.modules.payments import service
from app.modules.payments.models import Order, Payment
from app.modules.payments.providers import get_provider

router = APIRouter(tags=["payments"])


class PaymentOut(Out):
    provider_payment_id: str
    status: str
    method: str | None
    amount_paise: int
    captured_at: datetime | None
    error_description: str | None


class OrderOut(Out):
    id: UUID
    number: str
    purpose: str
    reference_id: UUID
    description: str
    amount_paise: int
    currency: str
    status: str
    provider: str
    created_at: datetime
    paid_at: datetime | None
    refunded_paise: int
    offline_reference: str | None
    payments: list[PaymentOut] = []


class ConfirmIn(In):
    payload: dict[str, Any]


class MockCompleteIn(In):
    provider_order_id: str
    outcome: Literal["success", "failure"]


async def order_out(session: AsyncSession, order: Order) -> OrderOut:
    pays = (await session.scalars(select(Payment).where(Payment.order_id == order.id)
                                  .order_by(Payment.created_at))).all()
    return OrderOut.model_validate(order).model_copy(update={"payments": [PaymentOut.model_validate(p) for p in pays]})


@router.get("/me/orders")
async def my_orders(user: CurrentUser = Depends(require("order:self")),
                    session: AsyncSession = Depends(get_session)) -> list[OrderOut]:
    rows = (await session.scalars(select(Order).where(Order.user_id == user.id, Order.status != "expired")
                                  .order_by(Order.created_at.desc()))).all()
    return [await order_out(session, o) for o in rows]


@router.get("/payments/orders/{order_id}")
async def get_order(order_id: UUID, user: CurrentUser = Depends(require("order:self")),
                    session: AsyncSession = Depends(get_session)) -> OrderOut:
    o = await session.get(Order, order_id)
    if o is None or o.user_id != user.id:
        raise NotFound()
    return await order_out(session, o)


@router.post("/payments/orders/{order_id}/confirm")
async def confirm(order_id: UUID, body: ConfirmIn, user: CurrentUser = Depends(require("order:self")),
                  session: AsyncSession = Depends(get_session)) -> OrderOut:
    order = await service.confirm_checkout(session, user.user, order_id, body.payload)
    return await order_out(session, order)


@router.post("/payments/webhooks/{provider}")
async def webhook(provider: Literal["razorpay", "mock"], request: Request,
                  session: AsyncSession = Depends(get_session)) -> dict:
    body = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}
    return {"status": await service.handle_webhook(session, provider, headers, body)}


# ---------- mock gateway (local/test only) ----------

def _mock():
    if get_settings().payment_provider != "mock" or not get_settings().is_dev:
        raise NotFound()
    return get_provider("mock")


@router.get("/payments/mock/orders/{provider_order_id}")
async def mock_order(provider_order_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    _mock()
    o = await session.scalar(select(Order).where(Order.provider_order_id == provider_order_id))
    if o is None:
        raise NotFound()
    return {"order_id": o.id, "number": o.number, "description": o.description, "amount_paise": o.amount_paise,
            "status": o.status}


@router.post("/payments/mock/complete")
async def mock_complete(body: MockCompleteIn, user: CurrentUser = Depends(require("order:self")),
                        session: AsyncSession = Depends(get_session)) -> dict:
    """Simulates the customer paying on the gateway page: the gateway sends a signed webhook
    to us, then hands the browser a signed success payload (like Razorpay's handler)."""
    mock = _mock()
    o = await session.scalar(select(Order).where(Order.provider_order_id == body.provider_order_id))
    if o is None or o.user_id != user.id:
        raise NotFound()
    info, checkout = mock.simulate(body.provider_order_id, o.amount_paise, body.outcome == "success")
    headers, raw = mock.webhook_for(info)
    await service.handle_webhook(session, "mock", headers, raw)
    return {"order_id": o.id, "outcome": body.outcome, "checkout_payload": checkout if info.status == "captured"
            else None, "error": info.error_description}
