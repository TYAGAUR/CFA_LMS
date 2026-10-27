"""Admin: courses, registrations, orders, refunds, offline payments."""

from datetime import date
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import Conflict, Invalid, NotFound
from app.core.schemas import In
from app.modules.audit import service as audit
from app.modules.auth.service import normalise_mobile
from app.modules.catalog.models import Subject
from app.modules.commerce import service as commerce
from app.modules.commerce.models import Course, CourseSubject, Registration
from app.modules.payments import service as payments
from app.modules.payments.models import Order, Payment, Refund
from app.modules.users.models import User

router = APIRouter(prefix="/admin", tags=["admin"])


class CourseIn(In):
    code: str = Field(min_length=2, max_length=30, pattern=r"^[A-Z0-9-]+$")
    title: str = Field(min_length=3, max_length=200)
    tagline: str | None = Field(default=None, max_length=300)
    description: str | None = Field(default=None, max_length=5000)
    fee_paise: int = Field(gt=0, le=100_000_000)
    validity_days: int | None = Field(default=None, gt=0, le=1500)
    access_ends_on: date | None = None
    seat_limit: int | None = Field(default=None, gt=0)
    batch_id: UUID | None = None
    exam_window: str | None = Field(default=None, max_length=20)
    status: Literal["draft", "open", "closed"] = "draft"
    sort_order: int = 0
    subject_codes: list[str] = Field(min_length=1)


async def course_row(session: AsyncSession, c: Course) -> dict:
    ids = [s.subject_id for s in c.subjects]
    subs = (await session.scalars(select(Subject).where(Subject.id.in_(ids)).order_by(Subject.sort_order))).all() \
        if ids else []
    active = await commerce.seats_taken(session, c.id)
    return {"id": c.id, "code": c.code, "title": c.title, "tagline": c.tagline, "description": c.description,
            "fee_paise": c.fee_paise, "validity_days": c.validity_days, "access_ends_on": c.access_ends_on,
            "seat_limit": c.seat_limit, "batch_id": c.batch_id, "exam_window": c.exam_window, "status": c.status,
            "sort_order": c.sort_order, "subject_codes": [s.code for s in subs], "active_registrations": active}


async def _apply(session: AsyncSession, c: Course, body: CourseIn) -> None:
    if not body.validity_days and not body.access_ends_on:
        raise Invalid("Set either validity days or an access end date.")
    subs = (await session.scalars(select(Subject).where(Subject.code.in_(body.subject_codes)))).all()
    if len(subs) != len(set(body.subject_codes)):
        raise Invalid("Unknown subject code")
    for k, v in body.model_dump(exclude={"subject_codes"}).items():
        setattr(c, k, v)
    wanted = {s.id for s in subs}
    c.subjects = [cs for cs in c.subjects if cs.subject_id in wanted] + [
        CourseSubject(subject_id=sid) for sid in wanted - {cs.subject_id for cs in c.subjects}]


@router.get("/courses")
async def courses(_: CurrentUser = Depends(require("course:manage")),
                  session: AsyncSession = Depends(get_session)) -> list[dict]:
    rows = (await session.scalars(select(Course).order_by(Course.sort_order, Course.created_at))).all()
    return [await course_row(session, c) for c in rows]


@router.post("/courses", status_code=201)
async def create_course(body: CourseIn, actor: CurrentUser = Depends(require("course:manage")),
                        session: AsyncSession = Depends(get_session)) -> dict:
    if await session.scalar(select(Course.id).where(Course.code == body.code)):
        raise Conflict("Course code already used.")
    c = Course(code=body.code, title=body.title, fee_paise=body.fee_paise)
    await _apply(session, c, body)
    session.add(c)
    await session.flush()
    await audit.record(session, "course.created", actor=actor, target_type="course", target_id=c.id,
                       metadata=body.model_dump(mode="json"))
    return await course_row(session, c)


@router.patch("/courses/{cid}")
async def update_course(cid: UUID, body: CourseIn, actor: CurrentUser = Depends(require("course:manage")),
                        session: AsyncSession = Depends(get_session)) -> dict:
    c = await session.get(Course, cid)
    if c is None:
        raise NotFound()
    before = await course_row(session, c)
    await _apply(session, c, body)
    await session.flush()
    after = await course_row(session, c)
    changes = {k: {"old": before[k], "new": after[k]} for k in after if before.get(k) != after[k]
               and k != "active_registrations"}
    await audit.record(session, "course.updated", actor=actor, target_type="course", target_id=c.id, changes=changes)
    return after


# ---------- registrations ----------

@router.get("/registrations")
async def registrations(course: str | None = None, status: str | None = None, q: str | None = None,
                        limit: int = Query(100, le=500), _: CurrentUser = Depends(require("order:read")),
                        session: AsyncSession = Depends(get_session)) -> list[dict]:
    stmt = select(Registration, Course, User).join(Course).join(User, User.id == Registration.user_id)
    if course:
        stmt = stmt.where(Course.code == course)
    if status:
        stmt = stmt.where(Registration.status == status)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(User.full_name.ilike(like), User.mobile_e164.ilike(like), User.student_code.ilike(like)))
    rows = (await session.execute(stmt.order_by(Registration.created_at.desc()).limit(limit))).all()
    return [{"id": r.id, "status": r.status, "created_at": r.created_at, "activated_at": r.activated_at,
             "course_code": c.code, "course": c.title, "user_id": u.id, "student": u.full_name,
             "student_code": u.student_code, "mobile": u.mobile_e164, "form": r.form,
             "order_id": r.current_order_id} for r, c, u in rows]


class OfflineIn(In):
    mobile: str | None = None
    user_id: UUID | None = None
    course_code: str
    reference: str = Field(min_length=3, max_length=120)
    amount_paise: int | None = Field(default=None, gt=0)


@router.post("/registrations/offline", status_code=201)
async def offline(body: OfflineIn, actor: CurrentUser = Depends(require("order:offline")),
                  session: AsyncSession = Depends(get_session)) -> dict:
    if body.user_id:
        user = await session.get(User, body.user_id)
    elif body.mobile:
        user = await session.scalar(select(User).where(User.mobile_e164 == normalise_mobile(body.mobile)))
    else:
        raise Invalid("Give the student's mobile number or user id.")
    if user is None:
        raise NotFound("No student with that mobile. Ask them to sign up first.")
    course = await commerce.course_by_code(session, body.course_code, public=False)
    reg = await commerce.register_offline(session, user=user, course=course, reference=body.reference,
                                          amount_paise=body.amount_paise, actor=actor)
    return {"registration_id": reg.id, "status": reg.status, "order_id": reg.current_order_id}


class ReasonIn(In):
    reason: str = Field(min_length=3, max_length=500)


@router.post("/registrations/{rid}/cancel")
async def cancel(rid: UUID, body: ReasonIn, actor: CurrentUser = Depends(require("order:refund")),
                 session: AsyncSession = Depends(get_session)) -> dict:
    reg = await session.get(Registration, rid)
    if reg is None:
        raise NotFound()
    await commerce.cancel(session, reg, body.reason, actor)
    return {"status": reg.status}


# ---------- orders ----------

@router.get("/orders")
async def orders(status: str | None = None, q: str | None = None, limit: int = Query(100, le=500),
                 _: CurrentUser = Depends(require("order:read")),
                 session: AsyncSession = Depends(get_session)) -> list[dict]:
    stmt = select(Order, User).join(User, User.id == Order.user_id)
    if status:
        stmt = stmt.where(Order.status == status)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Order.number.ilike(like), User.full_name.ilike(like), User.mobile_e164.ilike(like)))
    rows = (await session.execute(stmt.order_by(Order.created_at.desc()).limit(limit))).all()
    return [{"id": o.id, "number": o.number, "description": o.description, "amount_paise": o.amount_paise,
             "refunded_paise": o.refunded_paise, "status": o.status, "provider": o.provider,
             "created_at": o.created_at, "paid_at": o.paid_at, "student": u.full_name, "user_id": u.id,
             "student_code": u.student_code} for o, u in rows]


@router.get("/orders/{oid}")
async def order_detail(oid: UUID, _: CurrentUser = Depends(require("order:read")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    o = await session.get(Order, oid)
    if o is None:
        raise NotFound()
    u = await session.get(User, o.user_id)
    pays = (await session.scalars(select(Payment).where(Payment.order_id == o.id))).all()
    refunds = (await session.scalars(select(Refund).where(Refund.order_id == o.id))).all()
    return {"id": o.id, "number": o.number, "description": o.description, "purpose": o.purpose,
            "reference_id": o.reference_id, "amount_paise": o.amount_paise, "refunded_paise": o.refunded_paise,
            "status": o.status, "provider": o.provider, "provider_order_id": o.provider_order_id,
            "offline_reference": o.offline_reference, "created_at": o.created_at, "paid_at": o.paid_at,
            "student": {"id": u.id, "name": u.full_name, "code": u.student_code, "mobile": u.mobile_e164},
            "payments": [{"id": p.id, "provider_payment_id": p.provider_payment_id, "status": p.status,
                          "amount_paise": p.amount_paise, "method": p.method, "error": p.error_description,
                          "captured_at": p.captured_at, "created_at": p.created_at} for p in pays],
            "refunds": [{"id": r.id, "amount_paise": r.amount_paise, "status": r.status, "reason": r.reason,
                         "provider_refund_id": r.provider_refund_id, "created_at": r.created_at} for r in refunds]}


class RefundIn(In):
    amount_paise: int | None = Field(default=None, gt=0)
    reason: str = Field(min_length=3, max_length=500)


@router.post("/orders/{oid}/refund")
async def refund(oid: UUID, body: RefundIn, actor: CurrentUser = Depends(require("order:refund")),
                 session: AsyncSession = Depends(get_session)) -> dict:
    rf = await payments.refund(session, oid, body.amount_paise, body.reason, actor)
    return {"refund_id": rf.id, "status": rf.status, "amount_paise": rf.amount_paise}


@router.get("/revenue")
async def revenue(_: CurrentUser = Depends(require("order:read")),
                  session: AsyncSession = Depends(get_session)) -> dict:
    rows = (await session.execute(select(Order.status, func.count(), func.coalesce(func.sum(Order.amount_paise), 0),
                                         func.coalesce(func.sum(Order.refunded_paise), 0))
                                  .group_by(Order.status))).all()
    return {"by_status": [{"status": s, "count": n, "amount_paise": a, "refunded_paise": r} for s, n, a, r in rows]}
