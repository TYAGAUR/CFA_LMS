"""Privacy notice, consents, guardian consent, data requests (A-04 §2.2)."""

from datetime import datetime, timedelta
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_session
from app.core.deps import CurrentUser, current_user, current_user_allow_pending
from app.core.errors import Forbidden, Invalid, NotFound
from app.core.notify import sms
from app.core.schemas import In, Out
from app.core.security import decode_token, encode_token
from app.core.timeutil import now_utc
from app.modules.auth import service as auth
from app.modules.privacy import service
from app.modules.privacy.models import DataRequest
from app.modules.privacy.notice import NOTICE
from app.modules.users.models import PENDING_GUARDIAN, Guardian, User

router = APIRouter(tags=["privacy"])


class ConsentIn(In):
    purpose: Literal["product_analytics", "marketing_messages", "leaderboard_display"]
    granted: bool


class GuardianIn(In):
    full_name: str = Field(min_length=2, max_length=120)
    mobile: str
    relation: Literal["parent", "legal_guardian"]


class GuardianConsentIn(In):
    challenge_id: UUID
    code: str
    accept: bool
    marketing_messages: bool = False


class DataRequestIn(In):
    type: Literal["access", "correction", "erasure", "grievance", "nomination"]
    note: str | None = Field(default=None, max_length=2000)
    nominee_name: str | None = Field(default=None, max_length=120)
    nominee_contact: str | None = Field(default=None, max_length=120)


class DataRequestOut(Out):
    id: UUID
    type: str
    status: str
    note: str | None
    due_at: datetime
    created_at: datetime
    closed_at: datetime | None
    resolution_note: str | None


@router.get("/privacy/notice/current")
async def notice() -> dict:
    return NOTICE


@router.get("/me/consents")
async def my_consents(user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> dict:
    return {"is_minor": user.user.is_minor, "consents": await service.current_consents(session, user.id)}


@router.post("/me/consents")
async def set_consent(body: ConsentIn, user: CurrentUser = Depends(current_user),
                      session: AsyncSession = Depends(get_session)) -> dict:
    await service.record_consent(session, user.user, body.purpose, body.granted)
    return {"consents": await service.current_consents(session, user.id)}


# ---------- guardian consent (WF-02) ----------

@router.get("/me/guardian")
async def my_guardian(user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> dict | None:
    g = await session.scalar(select(Guardian).where(Guardian.student_user_id == user.id))
    if not g:
        return None
    return {"full_name": g.full_name, "mobile": f"******{g.mobile_e164[-4:]}", "relation": g.relation,
            "verified_at": g.verified_at}


@router.post("/me/guardian")
async def request_guardian_consent(body: GuardianIn, user: CurrentUser = Depends(current_user_allow_pending),
                                   session: AsyncSession = Depends(get_session)) -> dict:
    u = user.user
    if u.status != PENDING_GUARDIAN:
        raise Forbidden("Guardian consent is not needed for this account.")
    mobile = auth.normalise_mobile(body.mobile)
    if mobile == u.mobile_e164:
        raise Invalid("The guardian's number must be different from yours.", code="same_number")
    g = await session.scalar(select(Guardian).where(Guardian.student_user_id == u.id))
    if g is None:
        g = Guardian(student_user_id=u.id, full_name=body.full_name, mobile_e164=mobile, relation=body.relation)
        session.add(g)
    else:
        g.full_name, g.mobile_e164, g.relation = body.full_name, mobile, body.relation
    await session.flush()
    token = encode_token("guardian", {"gid": str(g.id)}, timedelta(days=7))
    link = f"{get_settings().public_base_url}/guardian-consent/{token}"
    first = u.full_name.split()[0]
    await sms().send(mobile, f"{first} has asked to join Karan Sir Classes. Review and give consent: {link}")
    out: dict = {"status": "sent", "guardian_mobile": f"******{mobile[-4:]}"}
    if get_settings().is_dev:
        out["debug_link"] = link
    return out


async def _guardian(session: AsyncSession, token: str) -> tuple[Guardian, User]:
    p = decode_token(token, "guardian")
    g = await session.get(Guardian, UUID(p["gid"])) if p else None
    if g is None:
        raise NotFound("This consent link is invalid or has expired.")
    student = await session.get(User, g.student_user_id)
    if student is None:
        raise NotFound()
    return g, student


@router.get("/guardian-consent/{token}")
async def guardian_view(token: str, session: AsyncSession = Depends(get_session)) -> dict:
    g, student = await _guardian(session, token)
    return {"student_first_name": student.full_name.split()[0], "guardian_name": g.full_name,
            "relation": g.relation, "already_verified": g.verified_at is not None, "notice": NOTICE}


@router.post("/guardian-consent/{token}/otp")
async def guardian_otp(token: str, session: AsyncSession = Depends(get_session)) -> dict:
    g, _ = await _guardian(session, token)
    return await auth.request_otp(session, "sms", g.mobile_e164, "guardian_consent")


@router.post("/guardian-consent/{token}")
async def guardian_accept(token: str, body: GuardianConsentIn, session: AsyncSession = Depends(get_session)) -> dict:
    g, student = await _guardian(session, token)
    if not body.accept:
        raise Invalid("Consent was not given.", code="consent_declined")
    await auth.check_otp(session, body.challenge_id, body.code, "sms", g.mobile_e164)
    if student.status == PENDING_GUARDIAN:
        await service.activate_with_guardian(session, student, g, body.marketing_messages)
    return {"status": "consent_recorded"}


# ---------- data requests (WF-10) ----------

@router.get("/me/data-requests")
async def my_requests(user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> list[DataRequestOut]:
    rows = (await session.scalars(select(DataRequest).where(DataRequest.user_id == user.id)
                                  .order_by(DataRequest.created_at.desc()))).all()
    return [DataRequestOut.model_validate(r) for r in rows]


@router.post("/me/data-requests", status_code=201)
async def new_request(body: DataRequestIn, user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> DataRequestOut:
    details = None
    if body.type == "nomination":
        if not body.nominee_name or not body.nominee_contact:
            raise Invalid("Enter the nominee's name and contact.")
        details = {"nominee_name": body.nominee_name, "nominee_contact": body.nominee_contact}
    dr = await service.create_data_request(session, user.user, body.type, body.note, details)
    if body.type == "nomination":
        dr.status, dr.closed_at = "completed", now_utc()
    return DataRequestOut.model_validate(dr)


@router.get("/me/data-export")
async def data_export(user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> dict:
    return await service.export_user_data(session, user.user)
