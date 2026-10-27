"""/auth and /me endpoints (A-04 §2.1)."""

import secrets
from datetime import date, datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, current_user_allow_pending
from app.core.errors import Conflict, Invalid, NotFound, Unauthenticated
from app.core.schemas import In, Out
from app.core.security import decode_token
from app.core.timeutil import age_on, now_utc, today_ist
from app.modules.audit import service as audit
from app.modules.auth import service
from app.modules.auth.models import UserSession
from app.modules.privacy import service as privacy
from app.modules.privacy.notice import NOTICE_VERSION
from app.modules.users.models import PENDING_GUARDIAN, User, UserRole

router = APIRouter(tags=["auth"])


class UserOut(Out):
    id: UUID
    full_name: str
    mobile_e164: str | None
    email: str | None
    student_code: str | None
    status: str
    is_minor: bool
    role_names: list[str]
    is_staff: bool
    city: str | None
    qualification: str | None
    target_exam: str | None


class OtpRequestIn(In):
    channel: Literal["sms", "email"] = "sms"
    destination: str = Field(max_length=120)


class OtpVerifyIn(In):
    challenge_id: UUID
    code: str = Field(min_length=4, max_length=8)
    channel: Literal["sms", "email"] = "sms"
    destination: str = Field(max_length=120)


class SignupIn(In):
    signup_token: str
    full_name: str = Field(min_length=2, max_length=120)
    dob: date
    email: EmailStr | None = None
    city: str | None = Field(default=None, max_length=80)
    accept_terms: bool
    notice_version: str
    product_analytics: bool = False
    marketing_messages: bool = False


class StaffLoginIn(In):
    email: str = Field(min_length=3, max_length=254)  # match only; no deliverability check on login
    password: str = Field(min_length=1, max_length=200)


class MfaIn(In):
    mfa_token: str
    code: str = Field(default="", max_length=10)


class ProfilePatch(In):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    city: str | None = Field(default=None, max_length=80)
    qualification: str | None = Field(default=None, max_length=120)
    target_exam: str | None = Field(default=None, max_length=20)


class SessionOut(Out):
    id: UUID
    device_label: str | None
    created_at: datetime
    last_seen_at: datetime
    current: bool = False


@router.post("/auth/otp/request")
async def otp_request(body: OtpRequestIn, session: AsyncSession = Depends(get_session)) -> dict:
    return await service.request_otp(session, body.channel, body.destination, "login")


@router.post("/auth/otp/verify")
async def otp_verify(body: OtpVerifyIn, response: Response, session: AsyncSession = Depends(get_session)) -> dict:
    return await service.verify_otp_login(session, response, body.challenge_id, body.code, body.channel,
                                          body.destination)


async def _new_student_code(session: AsyncSession) -> str:
    yy = today_ist().strftime("%y")
    for _ in range(20):
        code = f"KS{yy}-{secrets.randbelow(100000):05d}"
        if not await session.scalar(select(User.id).where(User.student_code == code)):
            return code
    raise Conflict("Could not allocate a student code")


@router.post("/auth/signup", status_code=201)
async def signup(body: SignupIn, response: Response, session: AsyncSession = Depends(get_session)) -> UserOut:
    tok = decode_token(body.signup_token, "signup")
    if not tok:
        raise Invalid("Your verification has expired. Please verify your number again.", code="signup_expired")
    if not body.accept_terms or body.notice_version != NOTICE_VERSION:
        raise Invalid("Please accept the privacy notice and terms to continue.", code="consent_required")
    today = today_ist()
    age = age_on(body.dob, today)
    if age < 10 or body.dob > today:
        raise Invalid("Please enter a valid date of birth.", code="invalid_dob")
    ch, dest = tok["ch"], tok["dest"]
    mobile = dest if ch == "sms" else None
    email = dest if ch == "email" else (body.email.lower() if body.email else None)
    if mobile and await session.scalar(select(User.id).where(User.mobile_e164 == mobile)):
        raise Conflict("An account with this mobile number already exists.", code="account_exists")
    if email and await session.scalar(select(User.id).where(User.email == email)):
        raise Conflict("An account with this email already exists.", code="email_taken")
    minor = age < 18
    user = User(full_name=body.full_name, mobile_e164=mobile, email=email, dob=body.dob, is_minor=minor,
                city=body.city, student_code=await _new_student_code(session),
                status=PENDING_GUARDIAN if minor else "active")
    user.roles = [UserRole(role="student", granted_at=now_utc())]
    session.add(user)
    await session.flush()
    await audit.record(session, "user.created", actor=user, target_type="user", target_id=user.id,
                       subject_user_id=user.id, metadata={"via": f"signup_{ch}", "is_minor": minor})
    # Adult gives service consent now; for a minor the guardian does (C-03 §5).
    if not minor:
        await privacy.record_consent(session, user, "service_delivery", True)
        await privacy.record_consent(session, user, "product_analytics", body.product_analytics)
    await privacy.record_consent(session, user, "marketing_messages", body.marketing_messages and not minor)
    await service.start_session(session, response, user)
    await session.refresh(user, ["roles"])
    return UserOut.model_validate(user)


@router.post("/auth/staff/login")
async def staff_login(body: StaffLoginIn, response: Response, session: AsyncSession = Depends(get_session)) -> dict:
    res = await service.staff_login(session, response, body.email, body.password)
    return {"status": res.status, "mfa_token": res.mfa_token}


async def _mfa_user(session: AsyncSession, token: str) -> User:
    p = decode_token(token, "mfa")
    user = await session.get(User, UUID(p["sub"])) if p else None
    if user is None:
        raise Unauthenticated("Please sign in again.")
    return user


@router.post("/auth/staff/mfa/setup")
async def staff_mfa_setup(body: MfaIn, session: AsyncSession = Depends(get_session)) -> dict:
    return await service.staff_mfa_setup(session, await _mfa_user(session, body.mfa_token))


@router.post("/auth/staff/mfa")
async def staff_mfa(body: MfaIn, response: Response, session: AsyncSession = Depends(get_session)) -> dict:
    await service.staff_mfa_verify(session, response, await _mfa_user(session, body.mfa_token), body.code)
    return {"status": "signed_in"}


@router.post("/auth/refresh")
async def refresh(request: Request, response: Response, session: AsyncSession = Depends(get_session)) -> dict:
    await service.refresh_session(session, response, request.cookies.get("refresh_token"))
    return {"status": "refreshed"}


@router.post("/auth/logout")
async def logout(response: Response, user: CurrentUser = Depends(current_user_allow_pending),
                 session: AsyncSession = Depends(get_session)) -> dict:
    await service.revoke_session(session, user.session_id, "logout")
    service.clear_auth_cookies(response)
    return {"status": "signed_out"}


@router.get("/me")
async def me(user: CurrentUser = Depends(current_user_allow_pending)) -> dict:
    return {**UserOut.model_validate(user.user).model_dump(), "permissions": sorted(user.permissions)}


@router.patch("/me")
async def update_me(body: ProfilePatch, user: CurrentUser = Depends(current_user_allow_pending),
                    session: AsyncSession = Depends(get_session)) -> UserOut:
    u = user.user
    changes = {}
    for k, v in body.model_dump(exclude_unset=True).items():
        if k == "email" and v:
            v = v.lower()
            if await session.scalar(select(User.id).where(User.email == v, User.id != u.id)):
                raise Conflict("This email is already in use.", code="email_taken")
        if getattr(u, k) != v:
            changes[k] = {"old": "***" if k == "email" else getattr(u, k), "new": "***" if k == "email" else v}
            setattr(u, k, v)
            if k == "email":
                u.email_verified_at = None
    if changes:
        await audit.record(session, "user.updated", actor=user, target_type="user", target_id=u.id,
                           subject_user_id=u.id, changes=changes)
    return UserOut.model_validate(u)


@router.get("/me/sessions")
async def my_sessions(user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> list[SessionOut]:
    rows = (await session.scalars(
        select(UserSession).where(UserSession.user_id == user.id, UserSession.revoked_at.is_(None),
                                  UserSession.expires_at > now_utc()).order_by(UserSession.last_seen_at.desc())
    )).all()
    return [SessionOut.model_validate(r).model_copy(update={"current": r.id == user.session_id}) for r in rows]


@router.delete("/me/sessions/{session_id}")
async def end_session(session_id: UUID, user: CurrentUser = Depends(current_user_allow_pending),
                      session: AsyncSession = Depends(get_session)) -> dict:
    s = await session.get(UserSession, session_id)
    if s is None or s.user_id != user.id:
        raise NotFound()
    await service.revoke_session(session, s.id, "logout")
    await audit.record(session, "auth.session_revoked", actor=user, target_type="session", target_id=s.id,
                       subject_user_id=user.id, metadata={"reason": "user"})
    return {"status": "ended"}
