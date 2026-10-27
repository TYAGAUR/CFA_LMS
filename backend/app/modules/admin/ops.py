"""Admin: overview, progress report, audit log, data requests."""

from datetime import timedelta
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import NotFound
from app.core.schemas import In
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.audit.models import AuditLog
from app.modules.catalog.models import LearningModule, Subject
from app.modules.commerce.models import Course, CourseSubject, Registration
from app.modules.payments.models import Order
from app.modules.privacy import service as privacy
from app.modules.privacy.models import DataRequest
from app.modules.progress.models import LmProgress
from app.modules.users.models import User, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])

SECURITY_PREFIXES = ("auth.", "user.break_glass")


@router.get("/overview")
async def overview(_: CurrentUser = Depends(require("report:read")),
                   session: AsyncSession = Depends(get_session)) -> dict:
    month_start = now_utc().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    week = now_utc() - timedelta(days=7)
    students = await session.scalar(select(func.count()).select_from(User).where(
        User.roles.any(UserRole.role == "student"), User.status != "deleted"))
    active_regs = await session.scalar(select(func.count()).select_from(Registration).where(
        Registration.status == "active"))
    pending = await session.scalar(select(func.count()).select_from(Registration).where(
        Registration.status == "pending_payment"))
    revenue = await session.scalar(select(func.coalesce(func.sum(Order.amount_paise - Order.refunded_paise), 0))
                                   .where(Order.status.in_(["paid", "partially_refunded"]),
                                          Order.paid_at >= month_start))
    active_week = await session.scalar(select(func.count(func.distinct(LmProgress.user_id))).where(
        LmProgress.last_opened_at >= week))
    mismatches = await session.scalar(select(func.count()).select_from(Order).where(Order.status == "amount_mismatch"))
    open_dr = await session.scalar(select(func.count()).select_from(DataRequest).where(
        DataRequest.status.in_(["open", "in_progress"])))
    return {"students": students, "active_registrations": active_regs, "pending_payments": pending,
            "revenue_this_month_paise": revenue, "active_students_7d": active_week,
            "orders_needing_review": mismatches, "open_data_requests": open_dr}


@router.get("/reports/progress")
async def progress_report(course: str, _: CurrentUser = Depends(require("report:read")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    c = await session.scalar(select(Course).where(Course.code == course))
    if c is None:
        raise NotFound()
    subject_ids = [s.subject_id for s in c.subjects]
    subjects = (await session.scalars(select(Subject).where(Subject.id.in_(subject_ids))
                                      .order_by(Subject.sort_order))).all()
    lm_subject = {lm.id: s.code for s in subjects for lm in s.lms if lm.status == "published"}
    totals = {s.code: sum(1 for lm in s.lms if lm.status == "published") for s in subjects}
    regs = (await session.execute(select(Registration, User).join(User, User.id == Registration.user_id).where(
        Registration.course_id == c.id, Registration.status == "active"))).all()
    rows = []
    for _reg, u in regs:
        prog = (await session.scalars(select(LmProgress).where(LmProgress.user_id == u.id,
                                                               LmProgress.lm_id.in_(lm_subject.keys())))).all()
        learned = {code: 0 for code in totals}
        last = None
        for p in prog:
            if p.learned_at:
                learned[lm_subject[p.lm_id]] += 1
            if p.last_opened_at and (last is None or p.last_opened_at > last):
                last = p.last_opened_at
        rows.append({"student": u.full_name, "student_code": u.student_code, "user_id": u.id, "last_active": last,
                     "subjects": {k: {"learned": learned[k], "total": totals[k]} for k in totals}})
    return {"course": c.title, "subjects": [{"code": s.code, "name": s.name} for s in subjects], "rows": rows}


@router.get("/audit")
async def audit_log(action: str | None = None, actor: UUID | None = None, subject: UUID | None = None,
                    before_id: int | None = None, limit: int = Query(100, le=500),
                    user: CurrentUser = Depends(require("audit:read")),
                    session: AsyncSession = Depends(get_session)) -> list[dict]:
    stmt = select(AuditLog)
    if action:
        stmt = stmt.where(AuditLog.action.ilike(f"{action}%"))
    if actor:
        stmt = stmt.where(AuditLog.actor_user_id == actor)
    if subject:
        stmt = stmt.where(AuditLog.subject_user_id == subject)
    if before_id:
        stmt = stmt.where(AuditLog.id < before_id)
    if not user.can("audit:read_security"):
        for p in SECURITY_PREFIXES:
            stmt = stmt.where(~AuditLog.action.startswith(p))
    rows = (await session.scalars(stmt.order_by(AuditLog.id.desc()).limit(limit))).all()
    names = {u.id: u.full_name for u in (await session.scalars(select(User).where(
        User.id.in_({r.actor_user_id for r in rows if r.actor_user_id})))).all()} if rows else {}
    return [{"id": r.id, "occurred_at": r.occurred_at, "actor": names.get(r.actor_user_id, r.actor_type),
             "actor_user_id": r.actor_user_id, "action": r.action, "target_type": r.target_type,
             "target_id": r.target_id, "reason": r.reason, "changes": r.changes, "metadata": r.metadata_}
            for r in rows]


@router.get("/audit/verify")
async def verify(_: CurrentUser = Depends(require("audit:read")),
                 session: AsyncSession = Depends(get_session)) -> dict:
    ok, n = await audit.verify_chain(session)
    return {"ok": ok, "rows_checked": n}


@router.get("/data-requests")
async def data_requests(_: CurrentUser = Depends(require("data_request:process")),
                        session: AsyncSession = Depends(get_session)) -> list[dict]:
    rows = (await session.execute(select(DataRequest, User).join(User, User.id == DataRequest.user_id)
                                  .order_by(DataRequest.created_at.desc()).limit(200))).all()
    return [{"id": d.id, "type": d.type, "status": d.status, "note": d.note, "details": d.details,
             "due_at": d.due_at, "created_at": d.created_at, "closed_at": d.closed_at,
             "resolution_note": d.resolution_note, "student": u.full_name, "user_id": u.id} for d, u in rows]


class DataRequestUpdate(In):
    status: Literal["in_progress", "completed", "rejected"]
    resolution_note: str = Field(min_length=3, max_length=2000)


@router.post("/data-requests/{did}")
async def update_request(did: UUID, body: DataRequestUpdate,
                         actor: CurrentUser = Depends(require("data_request:process")),
                         session: AsyncSession = Depends(get_session)) -> dict:
    d = await session.get(DataRequest, did)
    if d is None:
        raise NotFound()
    d.status, d.resolution_note, d.handled_by = body.status, body.resolution_note, actor.id
    if body.status in ("completed", "rejected"):
        d.closed_at = now_utc()
    await audit.record(session, "data_request.status_changed", actor=actor, target_type="data_request",
                       target_id=d.id, subject_user_id=d.user_id, metadata={"status": body.status})
    return {"status": d.status}


@router.post("/data-requests/{did}/erase")
async def erase(did: UUID, actor: CurrentUser = Depends(require("data_request:process")),
                session: AsyncSession = Depends(get_session)) -> dict:
    d = await session.get(DataRequest, did)
    if d is None or d.type != "erasure":
        raise NotFound()
    counts = await privacy.erase_user(session, d.user_id, actor)
    return {"status": "completed", "rows_deleted": counts}


__all__ = ["CourseSubject", "LearningModule", "router"]
