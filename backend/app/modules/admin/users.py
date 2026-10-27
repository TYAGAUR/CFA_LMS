"""Admin: users, roles, sessions, batches, entitlements (A-04 §2.4)."""

from datetime import date, datetime, time
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr, Field
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import Conflict, Forbidden, Invalid, NotFound
from app.core.schemas import In
from app.core.security import hash_password
from app.core.timeutil import IST, now_utc
from app.modules.audit import service as audit
from app.modules.auth.models import UserSession
from app.modules.auth.service import revoke_all
from app.modules.catalog.models import Subject
from app.modules.commerce.models import Course, Registration
from app.modules.enrolment import service as enrolment
from app.modules.enrolment.models import Batch, Enrolment, Entitlement
from app.modules.payments.models import Order
from app.modules.users.models import ROLES, User, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])


def user_row(u: User) -> dict:
    return {"id": u.id, "full_name": u.full_name, "mobile_e164": u.mobile_e164, "email": u.email,
            "student_code": u.student_code, "status": u.status, "is_minor": u.is_minor, "roles": u.role_names,
            "city": u.city, "created_at": u.created_at, "last_login_at": u.last_login_at}


@router.get("/users")
async def list_users(q: str | None = None, role: str | None = None, status: str | None = None,
                     limit: int = Query(50, le=200), offset: int = 0,
                     _: CurrentUser = Depends(require("user:read")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    stmt = select(User)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(User.full_name.ilike(like), User.mobile_e164.ilike(like), User.email.ilike(like),
                              User.student_code.ilike(like)))
    if role:
        stmt = stmt.where(User.roles.any(UserRole.role == role))
    if status:
        stmt = stmt.where(User.status == status)
    total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = (await session.scalars(stmt.order_by(User.created_at.desc()).limit(limit).offset(offset))).all()
    return {"total": total, "items": [user_row(u) for u in rows]}


@router.get("/users/{uid}")
async def get_user(uid: UUID, _: CurrentUser = Depends(require("user:read")),
                   session: AsyncSession = Depends(get_session)) -> dict:
    u = await session.get(User, uid)
    if u is None:
        raise NotFound()
    regs = (await session.execute(select(Registration, Course).join(Course).where(Registration.user_id == uid)
                                  .order_by(Registration.created_at.desc()))).all()
    orders = (await session.scalars(select(Order).where(Order.user_id == uid).order_by(Order.created_at.desc()))).all()
    ents = (await session.execute(select(Entitlement, Subject).join(Subject).where(Entitlement.user_id == uid)
                                  .order_by(Entitlement.created_at.desc()))).all()
    sessions = await session.scalar(select(func.count()).select_from(UserSession).where(
        UserSession.user_id == uid, UserSession.revoked_at.is_(None), UserSession.expires_at > now_utc()))
    return {
        **user_row(u), "dob": u.dob, "qualification": u.qualification, "target_exam": u.target_exam,
        "active_sessions": sessions,
        "registrations": [{"id": r.id, "status": r.status, "course": c.title, "course_code": c.code,
                           "created_at": r.created_at, "activated_at": r.activated_at} for r, c in regs],
        "orders": [{"id": o.id, "number": o.number, "amount_paise": o.amount_paise, "status": o.status,
                    "provider": o.provider, "created_at": o.created_at, "paid_at": o.paid_at} for o in orders],
        "entitlements": [{"id": e.id, "subject": s.name, "source": e.source, "starts_at": e.starts_at,
                          "ends_at": e.ends_at, "revoked_at": e.revoked_at} for e, s in ents],
    }


class StaffIn(In):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    roles: list[Literal["author", "reviewer", "admin", "super_admin"]] = Field(min_length=1)
    temporary_password: str = Field(min_length=12, max_length=200)


@router.post("/users", status_code=201)
async def create_staff(body: StaffIn, actor: CurrentUser = Depends(require("user:write")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    if {"admin", "super_admin"} & set(body.roles) and not actor.can("role:assign_admin"):
        raise Forbidden("Only a super admin can create admin accounts.")  # SoD-02
    if await session.scalar(select(User.id).where(User.email == body.email.lower())):
        raise Conflict("A user with this email exists.")
    u = User(full_name=body.full_name, email=body.email.lower(), password_hash=hash_password(body.temporary_password))
    u.roles = [UserRole(role=r, granted_by=actor.id, granted_at=now_utc()) for r in body.roles]
    session.add(u)
    await session.flush()
    await audit.record(session, "user.created", actor=actor, target_type="user", target_id=u.id,
                       metadata={"roles": body.roles, "staff": True})
    return user_row(u)


class RolesIn(In):
    roles: list[str]


@router.put("/users/{uid}/roles")
async def set_roles(uid: UUID, body: RolesIn, actor: CurrentUser = Depends(require("user:write")),
                    session: AsyncSession = Depends(get_session)) -> dict:
    u = await session.get(User, uid)
    if u is None:
        raise NotFound()
    new = set(body.roles)
    if not new <= set(ROLES):
        raise Invalid("Unknown role")
    old = set(u.role_names)
    if ({"admin", "super_admin"} & (new ^ old)) and not actor.can("role:assign_admin"):
        raise Forbidden("Only a super admin can grant or remove admin roles.")
    if u.id == actor.id and "super_admin" in (new - old):
        raise Forbidden("You cannot grant yourself super admin.")  # SoD-02
    u.roles = [r for r in u.roles if r.role in new] + [
        UserRole(role=r, granted_by=actor.id, granted_at=now_utc()) for r in new - old]
    for r in new - old:
        await audit.record(session, "user.role_granted", actor=actor, target_type="user", target_id=u.id,
                           metadata={"role": r})
    for r in old - new:
        await audit.record(session, "user.role_revoked", actor=actor, target_type="user", target_id=u.id,
                           metadata={"role": r})
    await session.flush()
    return user_row(u)


class StatusIn(In):
    reason: str = Field(min_length=3, max_length=500)


@router.post("/users/{uid}/deactivate")
async def deactivate(uid: UUID, body: StatusIn, actor: CurrentUser = Depends(require("user:write")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    u = await session.get(User, uid)
    if u is None:
        raise NotFound()
    if u.id == actor.id:
        raise Forbidden("You cannot deactivate yourself.")
    u.status = "deactivated"
    await revoke_all(session, u.id, "deactivated")
    await audit.record(session, "user.deactivated", actor=actor, target_type="user", target_id=u.id,
                       subject_user_id=u.id, reason=body.reason)
    return user_row(u)


@router.post("/users/{uid}/reactivate")
async def reactivate(uid: UUID, body: StatusIn, actor: CurrentUser = Depends(require("user:write")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    u = await session.get(User, uid)
    if u is None or u.status != "deactivated":
        raise NotFound()
    u.status = "active"
    await audit.record(session, "user.reactivated", actor=actor, target_type="user", target_id=u.id,
                       subject_user_id=u.id, reason=body.reason)
    return user_row(u)


@router.delete("/users/{uid}/sessions")
async def revoke_sessions(uid: UUID, actor: CurrentUser = Depends(require("session:revoke")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    await revoke_all(session, uid, "admin")
    await audit.record(session, "auth.session_revoked", actor=actor, target_type="user", target_id=uid,
                       subject_user_id=uid, metadata={"reason": "admin"})
    return {"status": "revoked"}


# ---------- entitlements ----------

class GrantIn(In):
    user_id: UUID
    subject_codes: list[str] = Field(min_length=1)
    ends_on: date
    reason: str = Field(min_length=3, max_length=500)


@router.post("/entitlements")
async def grant(body: GrantIn, actor: CurrentUser = Depends(require("entitlement:grant")),
                session: AsyncSession = Depends(get_session)) -> dict:
    subs = (await session.scalars(select(Subject).where(Subject.code.in_(body.subject_codes)))).all()
    if len(subs) != len(set(body.subject_codes)):
        raise Invalid("Unknown subject code")
    ends = datetime.combine(body.ends_on, time(23, 59, 59), IST)
    n = await enrolment.grant(session, user_id=body.user_id, subject_ids=[s.id for s in subs], source="grant",
                              source_id=actor.id, starts_at=now_utc(), ends_at=ends)
    await audit.record(session, "entitlement.granted", actor=actor, target_type="user", target_id=body.user_id,
                       subject_user_id=body.user_id, reason=body.reason,
                       metadata={"subjects": body.subject_codes, "ends_on": str(body.ends_on)})
    return {"granted": n}


@router.post("/entitlements/{eid}/revoke")
async def revoke_entitlement(eid: UUID, body: StatusIn, actor: CurrentUser = Depends(require("entitlement:grant")),
                             session: AsyncSession = Depends(get_session)) -> dict:
    e = await session.get(Entitlement, eid)
    if e is None:
        raise NotFound()
    e.revoked_at = now_utc()
    await audit.record(session, "entitlement.revoked", actor=actor, target_type="entitlement", target_id=e.id,
                       subject_user_id=e.user_id, reason=body.reason)
    return {"status": "revoked"}


# ---------- batches ----------

class BatchIn(In):
    code: str = Field(min_length=2, max_length=20, pattern=r"^[A-Z0-9-]+$")
    name: str = Field(min_length=2, max_length=120)
    exam_window: str | None = Field(default=None, max_length=20)
    starts_on: date
    ends_on: date
    status: Literal["planned", "active", "closed"] = "active"


def batch_row(b: Batch, n: int = 0) -> dict:
    return {"id": b.id, "code": b.code, "name": b.name, "exam_window": b.exam_window, "starts_on": b.starts_on,
            "ends_on": b.ends_on, "status": b.status, "students": n}


@router.get("/batches")
async def batches(_: CurrentUser = Depends(require("batch:manage")),
                  session: AsyncSession = Depends(get_session)) -> list[dict]:
    rows = (await session.execute(select(Batch, func.count(Enrolment.id)).outerjoin(Enrolment)
                                  .group_by(Batch.id).order_by(Batch.starts_on.desc()))).all()
    return [batch_row(b, n) for b, n in rows]


@router.post("/batches", status_code=201)
async def create_batch(body: BatchIn, actor: CurrentUser = Depends(require("batch:manage")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    if body.ends_on < body.starts_on:
        raise Invalid("End date must be after the start date.")
    if await session.scalar(select(Batch.id).where(Batch.code == body.code)):
        raise Conflict("Batch code already used.")
    b = Batch(**body.model_dump())
    session.add(b)
    await session.flush()
    await audit.record(session, "batch.created", actor=actor, target_type="batch", target_id=b.id,
                       metadata=body.model_dump(mode="json"))
    return batch_row(b)


@router.patch("/batches/{bid}")
async def update_batch(bid: UUID, body: BatchIn, actor: CurrentUser = Depends(require("batch:manage")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    b = await session.get(Batch, bid)
    if b is None:
        raise NotFound()
    for k, v in body.model_dump().items():
        setattr(b, k, v)
    await audit.record(session, "batch.updated", actor=actor, target_type="batch", target_id=b.id,
                       metadata=body.model_dump(mode="json"))
    return batch_row(b)
