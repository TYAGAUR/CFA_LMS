"""Consent records, guardian consent, data requests, export and erasure (C-01, C-03, C-05)."""

from datetime import timedelta
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context import client_ip_var, user_agent_var
from app.core.db import to_dict
from app.core.errors import Forbidden, Invalid, NotFound
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.privacy.models import (
    MINOR_BLOCKED_PURPOSES,
    PURPOSES,
    Consent,
    DataRequest,
)
from app.modules.privacy.notice import NOTICE_VERSION
from app.modules.users.models import ACTIVE, DELETED, Guardian, User

DUE_DAYS = {"access": 15, "correction": 7, "erasure": 30, "grievance": 15, "nomination": 7}


async def record_consent(session: AsyncSession, user: User, purpose: str, granted: bool, *, actor: str = "self",
                         method: str = "checkbox", guardian_id: UUID | None = None) -> None:
    if purpose not in PURPOSES:
        raise Invalid(f"Unknown purpose {purpose}")
    if granted and user.is_minor and purpose in MINOR_BLOCKED_PURPOSES:
        raise Forbidden("This option is not available for students under 18.", code="minor_restricted")
    session.add(Consent(
        user_id=user.id, purpose=purpose, granted=granted, notice_version=NOTICE_VERSION, actor=actor,
        guardian_id=guardian_id, method=method, ip_address=client_ip_var.get(), user_agent=user_agent_var.get(),
        created_at=now_utc(),
    ))
    await audit.record(session, "consent.changed", actor=user if actor == "self" else None,
                       actor_type="user" if actor == "self" else "guardian",
                       target_type="user", target_id=user.id, subject_user_id=user.id,
                       metadata={"purpose": purpose, "granted": granted, "notice_version": NOTICE_VERSION,
                                 "actor": actor})


async def current_consents(session: AsyncSession, user_id: UUID) -> dict[str, dict]:
    rows = (await session.scalars(
        select(Consent).where(Consent.user_id == user_id).order_by(Consent.created_at)
    )).all()
    state: dict[str, dict] = {p: {"granted": False, "updated_at": None, "actor": None} for p in PURPOSES}
    for r in rows:
        state[r.purpose] = {"granted": r.granted, "updated_at": r.created_at, "actor": r.actor}
    return state


async def has_consent(session: AsyncSession, user: User, purpose: str) -> bool:
    if user.is_minor and purpose in MINOR_BLOCKED_PURPOSES:
        return False
    return (await current_consents(session, user.id))[purpose]["granted"]


async def activate_with_guardian(session: AsyncSession, student: User, guardian: Guardian,
                                 marketing: bool) -> None:
    guardian.verified_at, guardian.verification_method = now_utc(), "sms_otp"
    await record_consent(session, student, "service_delivery", True, actor="guardian", method="sms_otp",
                         guardian_id=guardian.id)
    await record_consent(session, student, "marketing_messages", marketing, actor="guardian", method="sms_otp",
                         guardian_id=guardian.id)
    student.status = ACTIVE
    await audit.record(session, "guardian.consent_verified", actor_type="guardian", target_type="user",
                       target_id=student.id, subject_user_id=student.id, metadata={"method": "sms_otp"},
                       with_ip=True)


async def create_data_request(session: AsyncSession, user: User, type_: str, note: str | None,
                              details: dict | None) -> DataRequest:
    if type_ not in DUE_DAYS:
        raise Invalid("Unknown request type")
    dr = DataRequest(user_id=user.id, type=type_, note=note, details=details,
                     due_at=now_utc() + timedelta(days=DUE_DAYS[type_]))
    session.add(dr)
    await session.flush()
    await session.refresh(dr)
    await audit.record(session, "data_request.created", actor=user, target_type="data_request", target_id=dr.id,
                       subject_user_id=user.id, metadata={"type": type_})
    return dr


async def export_user_data(session: AsyncSession, user: User) -> dict:
    """Machine-readable summary for the right to access (C-01 §3 row 12)."""
    from app.modules.commerce.models import Registration
    from app.modules.payments.models import Order
    from app.modules.progress.models import (
        EocEntry,
        LmProgress,
        ResourceProgress,
        RevisionLog,
    )

    async def rows(model, *where):
        return [to_dict(r) for r in (await session.scalars(select(model).where(*where))).all()]

    profile = {k: getattr(user, k) for k in
               ("id", "full_name", "mobile_e164", "email", "student_code", "dob", "is_minor", "status", "city",
                "qualification", "target_exam", "created_at", "last_login_at")}
    return {
        "generated_at": now_utc(),
        "profile": profile,
        "consents": await current_consents(session, user.id),
        "registrations": await rows(Registration, Registration.user_id == user.id),
        "orders": await rows(Order, Order.user_id == user.id),
        "lm_progress": await rows(LmProgress, LmProgress.user_id == user.id),
        "resource_progress": await rows(ResourceProgress, ResourceProgress.user_id == user.id),
        "revisions": await rows(RevisionLog, RevisionLog.user_id == user.id),
        "eoc_entries": await rows(EocEntry, EocEntry.user_id == user.id),
    }


async def erase_user(session: AsyncSession, user_id: UUID, actor) -> dict:
    """Erasure (C-05 §3). Orders are kept as business records with the user pseudonymised."""
    from app.modules.auth.service import revoke_all
    from app.modules.progress.models import (
        Bookmark,
        EocEntry,
        LmProgress,
        ResourceProgress,
        RevisionLog,
    )

    user = await session.get(User, user_id)
    if user is None:
        raise NotFound()
    await revoke_all(session, user.id, "deactivated")
    counts = {}
    for model in (ResourceProgress, LmProgress, RevisionLog, EocEntry, Bookmark):
        res = await session.execute(delete(model).where(model.user_id == user.id))
        counts[model.__tablename__] = res.rowcount
    await session.execute(delete(Guardian).where(Guardian.student_user_id == user.id))
    user.full_name, user.mobile_e164, user.email, user.dob = "Deleted user", None, None, None
    user.city = user.qualification = user.target_exam = None
    user.status, user.deleted_at = DELETED, now_utc()
    await session.execute(update(DataRequest).where(DataRequest.user_id == user.id, DataRequest.type == "erasure",
                                                    DataRequest.status != "completed")
                          .values(status="completed", closed_at=now_utc(), handled_by=getattr(actor, "id", None)))
    await audit.record(session, "privacy.erasure_completed", actor=actor, target_type="user", target_id=user.id,
                       metadata={"rows_deleted": counts})
    return counts
