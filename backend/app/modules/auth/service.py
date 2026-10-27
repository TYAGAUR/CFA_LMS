"""OTP sign-in, staff login + TOTP, sessions with rotating refresh tokens (ADR-003, US-1.01..1.03)."""

import re
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

import pyotp
from fastapi import Response
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.context import client_ip_var, user_agent_var
from app.core.errors import AppError, Forbidden, Invalid, RateLimited, Unauthenticated
from app.core.ids import uuid7
from app.core.notify import email as email_provider
from app.core.notify import sms as sms_provider
from app.core.security import (
    encode_token,
    keyed_hash,
    otp_code,
    random_token,
    sha256,
    verify_password,
)
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.auth.models import OtpChallenge, UserSession
from app.modules.users.models import DEACTIVATED, DELETED, User

MOBILE_RE = re.compile(r"^(?:\+?91)?([6-9]\d{9})$")


def normalise_mobile(raw: str) -> str:
    m = MOBILE_RE.match(re.sub(r"[\s-]", "", raw or ""))
    if not m:
        raise Invalid("Enter a valid 10-digit Indian mobile number.", code="invalid_mobile")
    return "+91" + m.group(1)


def normalise_destination(channel: str, destination: str) -> str:
    if channel == "sms":
        return normalise_mobile(destination)
    d = (destination or "").strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", d):
        raise Invalid("Enter a valid email address.", code="invalid_email")
    return d


# ---------- OTP ----------

async def request_otp(session: AsyncSession, channel: str, destination: str, purpose: str) -> dict:
    s = get_settings()
    dest = normalise_destination(channel, destination)
    dhash = keyed_hash(dest)
    since = now_utc() - timedelta(hours=1)
    recent = await session.scalar(
        select(func.count()).select_from(OtpChallenge)
        .where(OtpChallenge.destination_hash == dhash, OtpChallenge.created_at >= since)
    )
    if (recent or 0) >= s.otp_max_requests_per_hour:
        raise RateLimited("Too many codes requested. Please try again in an hour.")
    code = otp_code()
    ch = OtpChallenge(
        id=uuid7(), channel=channel, destination_hash=dhash, purpose=purpose,
        code_hash=b"", expires_at=now_utc() + timedelta(seconds=s.otp_ttl_seconds),
    )
    ch.code_hash = sha256(f"{ch.id}:{code}")
    session.add(ch)
    text = (f"{code} is your Karan Sir Classes verification code. "
            f"It expires in {s.otp_ttl_seconds // 60} minutes. Do not share it.")
    if channel == "sms":
        await sms_provider().send(dest, text)
    else:
        await email_provider().send(dest, "Your verification code", text)
    out = {"challenge_id": str(ch.id), "expires_in": s.otp_ttl_seconds, "destination": dest}
    if s.otp_debug_echo and s.dev_tools:
        out["debug_code"] = code
    return out


async def check_otp(session: AsyncSession, challenge_id: UUID, code: str, channel: str, destination: str) -> None:
    s = get_settings()
    ch = await session.get(OtpChallenge, challenge_id, with_for_update=True)
    if ch is None or ch.consumed_at is not None or ch.expires_at < now_utc():
        raise Invalid("This code has expired. Request a new one.", code="otp_expired")
    if ch.channel != channel or ch.destination_hash != keyed_hash(normalise_destination(channel, destination)):
        raise Invalid("This code was not sent to that number.", code="otp_mismatch")
    if ch.attempts >= s.otp_max_attempts:
        raise Invalid("Too many wrong attempts. Request a new code.", code="otp_locked")
    ch.attempts += 1
    if sha256(f"{ch.id}:{code.strip()}") != ch.code_hash:
        await session.commit()  # keep the attempt count even though we raise
        left = s.otp_max_attempts - ch.attempts
        raise Invalid(f"Wrong code. {left} attempt(s) left.", code="otp_invalid", meta={"attempts_left": left})
    ch.consumed_at = now_utc()


async def verify_otp_login(session: AsyncSession, response: Response, challenge_id: UUID, code: str,
                           channel: str, destination: str) -> dict:
    await check_otp(session, challenge_id, code, channel, destination)
    dest = normalise_destination(channel, destination)
    col = User.mobile_e164 if channel == "sms" else User.email
    user = await session.scalar(select(User).where(col == dest))
    if user is None:
        token = encode_token("signup", {"ch": channel, "dest": dest}, timedelta(minutes=20))
        return {"status": "signup_required", "signup_token": token}
    if user.status in (DEACTIVATED, DELETED):
        raise Forbidden("This account is not active. Please contact support.", code="account_inactive")
    if user.is_staff and not any(r == "student" for r in user.role_names):
        raise Forbidden("Staff accounts sign in with email and password.", code="use_staff_login")
    await start_session(session, response, user)
    await audit.record(session, "auth.login_succeeded", actor=user, target_type="user", target_id=user.id,
                       metadata={"method": f"otp_{channel}"}, with_ip=True)
    return {"status": "signed_in"}


# ---------- sessions ----------

def _device_label(ua: str | None) -> str:
    ua = ua or ""
    os_ = next((n for k, n in [("Android", "Android"), ("iPhone", "iPhone"), ("iPad", "iPad"),
                               ("Windows", "Windows"), ("Mac OS", "Mac"), ("Linux", "Linux")] if k in ua), "Device")
    br = next((n for k, n in [("Edg/", "Edge"), ("Chrome/", "Chrome"), ("Firefox/", "Firefox"),
                              ("Safari/", "Safari")] if k in ua), "Browser")
    return f"{br} on {os_}"


def set_auth_cookies(response: Response, user: User, sess: UserSession, refresh: str) -> None:
    s = get_settings()
    access = encode_token("access", {"sub": str(user.id), "sid": str(sess.id), "roles": user.role_names},
                          timedelta(minutes=s.access_token_ttl_minutes))
    max_age = int((sess.expires_at - now_utc()).total_seconds())
    common = {"secure": s.cookie_secure, "samesite": "lax"}
    response.set_cookie("access_token", access, httponly=True, path="/", max_age=max_age, **common)
    response.set_cookie("refresh_token", refresh, httponly=True, path="/api/v1/auth", max_age=max_age, **common)
    response.set_cookie("csrf_token", random_token(16), httponly=False, path="/", max_age=max_age, **common)


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/auth")
    response.delete_cookie("csrf_token", path="/")


async def start_session(session: AsyncSession, response: Response, user: User) -> UserSession:
    s = get_settings()
    now = now_utc()
    if not user.is_staff:
        active = (await session.scalars(
            select(UserSession).where(UserSession.user_id == user.id, UserSession.revoked_at.is_(None),
                                      UserSession.expires_at > now).order_by(UserSession.created_at)
        )).all()
        while len(active) >= s.student_max_sessions:  # BR-ACC-05: oldest session ends
            oldest = active.pop(0)
            oldest.revoked_at, oldest.revoke_reason = now, "limit"
    ttl = timedelta(hours=s.staff_refresh_ttl_hours) if user.is_staff else timedelta(days=s.student_refresh_ttl_days)
    refresh = random_token()
    ua = user_agent_var.get()
    sess = UserSession(
        id=uuid7(), user_id=user.id, family_id=uuid7(), refresh_token_hash=sha256(refresh),
        device_label=_device_label(ua), ip_address=client_ip_var.get(), user_agent=ua,
        last_seen_at=now, expires_at=now + ttl,
    )
    session.add(sess)
    user.last_login_at = now
    await session.flush()
    set_auth_cookies(response, user, sess, refresh)
    return sess


async def refresh_session(session: AsyncSession, response: Response, refresh: str | None) -> None:
    if not refresh:
        raise Unauthenticated()
    h = sha256(refresh)
    now = now_utc()
    sess = await session.scalar(select(UserSession).where(UserSession.refresh_token_hash == h))
    if sess is None:
        reused = await session.scalar(select(UserSession).where(UserSession.prev_refresh_token_hash == h))
        if reused is not None and reused.revoked_at is None:  # token replay: kill the session
            reused.revoked_at, reused.revoke_reason = now, "reuse_detected"
            await audit.record(session, "auth.session_revoked", actor_type="system", target_type="session",
                               target_id=reused.id, subject_user_id=reused.user_id,
                               metadata={"reason": "reuse_detected"}, with_ip=True)
            await session.commit()
        clear_auth_cookies(response)
        raise Unauthenticated("Your session has ended. Please sign in again.")
    if sess.revoked_at is not None or sess.expires_at < now:
        clear_auth_cookies(response)
        raise Unauthenticated("Your session has ended. Please sign in again.")
    user = await session.get(User, sess.user_id)
    if user is None or user.status in (DEACTIVATED, DELETED):
        raise Unauthenticated()
    new = random_token()
    sess.prev_refresh_token_hash, sess.refresh_token_hash, sess.last_seen_at = h, sha256(new), now
    set_auth_cookies(response, user, sess, new)


async def revoke_session(session: AsyncSession, sess_id: UUID, reason: str) -> None:
    await session.execute(
        update(UserSession).where(UserSession.id == sess_id, UserSession.revoked_at.is_(None))
        .values(revoked_at=now_utc(), revoke_reason=reason)
    )


async def revoke_all(session: AsyncSession, user_id: UUID, reason: str) -> None:
    await session.execute(
        update(UserSession).where(UserSession.user_id == user_id, UserSession.revoked_at.is_(None))
        .values(revoked_at=now_utc(), revoke_reason=reason)
    )


# ---------- staff ----------

@dataclass
class StaffLoginResult:
    status: str  # signed_in | mfa_required | mfa_setup_required
    mfa_token: str | None = None


async def staff_login(session: AsyncSession, response: Response, email: str, password: str) -> StaffLoginResult:
    s = get_settings()
    now = now_utc()
    user = await session.scalar(select(User).where(User.email == email.strip().lower()))
    generic = Unauthenticated("Email or password is incorrect.", code="invalid_credentials")
    if user is None or not user.is_staff:
        raise generic
    if user.locked_until and user.locked_until > now:
        raise AppError("Account locked after failed attempts. Try again in 15 minutes.", code="account_locked",
                       status=423)
    if user.status != "active":
        raise generic
    if not verify_password(user.password_hash, password):
        user.failed_login_count += 1
        if user.failed_login_count >= 5:
            user.locked_until, user.failed_login_count = now + timedelta(minutes=15), 0
            await audit.record(session, "auth.account_locked", actor_type="system", target_type="user",
                               target_id=user.id, with_ip=True)
        await audit.record(session, "auth.login_failed", actor_type="system", target_type="user",
                           target_id=user.id, metadata={"method": "password"}, with_ip=True)
        await session.commit()
        raise generic
    user.failed_login_count = 0
    if user.mfa_enrolled_at or s.staff_mfa_required:
        token = encode_token("mfa", {"sub": str(user.id)}, timedelta(minutes=5))
        return StaffLoginResult("mfa_required" if user.mfa_enrolled_at else "mfa_setup_required", token)
    await start_session(session, response, user)
    await audit.record(session, "auth.login_succeeded", actor=user, target_type="user", target_id=user.id,
                       metadata={"method": "password"}, with_ip=True)
    return StaffLoginResult("signed_in")


async def staff_mfa_setup(session: AsyncSession, user: User) -> dict:
    if user.mfa_enrolled_at:
        raise Forbidden("MFA is already set up.")
    secret = pyotp.random_base32()
    user.totp_secret = secret.encode()  # TODO(cloud): envelope-encrypt with KMS (S-02 §4.4)
    uri = pyotp.TOTP(secret).provisioning_uri(name=user.email or str(user.id), issuer_name="Karan Sir Classes")
    return {"secret": secret, "otpauth_uri": uri}


async def staff_mfa_verify(session: AsyncSession, response: Response, user: User, code: str) -> None:
    if not user.totp_secret or not pyotp.TOTP(user.totp_secret.decode()).verify(code.strip(), valid_window=1):
        raise Invalid("That code is not valid.", code="mfa_invalid")
    first = user.mfa_enrolled_at is None
    user.mfa_enrolled_at = user.mfa_enrolled_at or now_utc()
    await start_session(session, response, user)
    if first:
        await audit.record(session, "auth.mfa_enrolled", actor=user, target_type="user", target_id=user.id)
    await audit.record(session, "auth.login_succeeded", actor=user, target_type="user", target_id=user.id,
                       metadata={"method": "password+totp"}, with_ip=True)
