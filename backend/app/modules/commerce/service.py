"""Course registration (BR-PAY-01..03, 07, 08). Talks to payments only through
payments.service and the payments.* events, so payments can become a separate service."""

from datetime import UTC, datetime, time, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import events
from app.core.errors import Conflict, Forbidden, NotFound
from app.core.timeutil import IST, now_utc
from app.modules.audit import service as audit
from app.modules.commerce import models as cm
from app.modules.commerce.models import Course, Registration
from app.modules.enrolment import service as enrolment
from app.modules.enrolment.models import Enrolment
from app.modules.payments import service as payments
from app.modules.users.models import PENDING_GUARDIAN, User

PURPOSE = "course_registration"


async def course_by_code(session: AsyncSession, code: str, *, public: bool = True) -> Course:
    c = await session.scalar(select(Course).where(Course.code == code))
    if c is None or (public and c.status == "draft"):
        raise NotFound("Course not found.")
    return c


async def seats_taken(session: AsyncSession, course_id: UUID) -> int:
    return await session.scalar(select(func.count()).select_from(Registration).where(
        Registration.course_id == course_id, Registration.status == cm.ACTIVE)) or 0


def access_window(course: Course, start: datetime) -> tuple[datetime, datetime]:
    if course.access_ends_on:
        end = datetime.combine(course.access_ends_on, time(23, 59, 59), IST).astimezone(UTC)
    else:
        end = start + timedelta(days=course.validity_days or 365)
    return start, end


async def start_registration(session: AsyncSession, user: User, code: str, form: dict[str, Any]) -> dict:
    course = await course_by_code(session, code)
    if course.status != "open":
        raise Conflict("Registrations for this course are closed.", code="course_closed")
    if user.status == PENDING_GUARDIAN:  # BR-PAY-07
        raise Forbidden("A parent or guardian must give consent before you can register.",
                        code="guardian_consent_required")
    reg = await session.scalar(select(Registration).where(
        Registration.user_id == user.id, Registration.course_id == course.id,
        Registration.status.in_([cm.PENDING_PAYMENT, cm.ACTIVE])).with_for_update())
    if reg and reg.status == cm.ACTIVE:
        raise Conflict("You are already registered for this course.", code="already_registered")
    if course.seat_limit and await seats_taken(session, course.id) >= course.seat_limit:
        raise Conflict("This course is full.", code="course_full")

    # Save registration profile fields on the user too (used for receipts and staff reports).
    for k in ("city", "qualification", "target_exam"):
        if form.get(k):
            setattr(user, k, form[k])
    if form.get("email") and not user.email:
        user.email = form["email"].lower()

    if reg is None:
        reg = Registration(user_id=user.id, course_id=course.id, form=form)
        session.add(reg)
        await session.flush()
        await audit.record(session, "registration.created", actor=user, target_type="registration",
                           target_id=reg.id, subject_user_id=user.id, metadata={"course": course.code})
    else:
        reg.form = form

    order = await payments.open_order_for(session, reg.id, course.fee_paise)
    if order is not None:
        checkout = order.notes.get("checkout", {})
    else:
        order, checkout = await payments.create_order(
            session, user=user, purpose=PURPOSE, reference_id=reg.id, amount_paise=course.fee_paise,
            description=f"{course.title} — course fee")
    reg.current_order_id = order.id
    return {"registration_id": reg.id, "order_id": order.id, "order_number": order.number,
            "amount_paise": order.amount_paise, "currency": order.currency, "provider": order.provider,
            "checkout": checkout}


async def activate(session: AsyncSession, reg: Registration, actor=None) -> None:
    if reg.status == cm.ACTIVE:
        return
    course = await session.get(Course, reg.course_id)
    start, end = access_window(course, now_utc())
    await enrolment.grant(session, user_id=reg.user_id, subject_ids=[s.subject_id for s in course.subjects],
                          source="registration", source_id=reg.id, starts_at=start, ends_at=end)
    if course.batch_id and not await session.scalar(select(Enrolment.id).where(
            Enrolment.user_id == reg.user_id, Enrolment.batch_id == course.batch_id)):
        session.add(Enrolment(user_id=reg.user_id, batch_id=course.batch_id, enrolled_by=getattr(actor, "id", None)))
    reg.status, reg.activated_at = cm.ACTIVE, now_utc()
    await audit.record(session, "registration.activated", actor=actor, actor_type=None if actor else "system",
                       target_type="registration", target_id=reg.id, subject_user_id=reg.user_id,
                       metadata={"course": course.code, "access_until": end.isoformat()})


async def cancel(session: AsyncSession, reg: Registration, reason: str, actor=None) -> None:
    if reg.status == cm.CANCELLED:
        return
    await enrolment.revoke_source(session, "registration", reg.id)
    reg.status, reg.cancelled_at, reg.cancel_reason = cm.CANCELLED, now_utc(), reason
    await audit.record(session, "registration.cancelled", actor=actor, actor_type=None if actor else "system",
                       target_type="registration", target_id=reg.id, subject_user_id=reg.user_id, reason=reason)


@events.subscribe("payments.order_paid")
async def _on_paid(session: AsyncSession, ev: dict) -> None:
    if ev["purpose"] != PURPOSE:
        return
    reg = await session.get(Registration, UUID(ev["reference_id"]), with_for_update=True)
    if reg is not None:
        reg.current_order_id = UUID(ev["order_id"])
        await activate(session, reg)


@events.subscribe("payments.order_refunded")
async def _on_refunded(session: AsyncSession, ev: dict) -> None:
    if ev["purpose"] != PURPOSE or not ev.get("full"):
        return  # BR-PAY-08: partial refunds keep access
    reg = await session.get(Registration, UUID(ev["reference_id"]), with_for_update=True)
    if reg is not None:
        await cancel(session, reg, "Full refund")


async def register_offline(session: AsyncSession, *, user: User, course: Course, reference: str,
                           amount_paise: int | None, actor) -> Registration:
    reg = await session.scalar(select(Registration).where(
        Registration.user_id == user.id, Registration.course_id == course.id,
        Registration.status.in_([cm.PENDING_PAYMENT, cm.ACTIVE])))
    if reg and reg.status == cm.ACTIVE:
        raise Conflict("Student is already registered for this course.")
    if reg is None:
        reg = Registration(user_id=user.id, course_id=course.id, form={"source": "admin_offline"})
        session.add(reg)
        await session.flush()
    order = await payments.record_offline(session, user=user, purpose=PURPOSE, reference_id=reg.id,
                                          amount_paise=amount_paise or course.fee_paise,
                                          description=f"{course.title} — course fee (offline)",
                                          reference=reference, actor=actor)
    reg.current_order_id = order.id
    return reg
