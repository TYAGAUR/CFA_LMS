"""Request dependencies: current user, permission checks (A-01 §6, P-06)."""

from collections.abc import Callable
from dataclasses import dataclass, field
from uuid import UUID

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.errors import Forbidden, Unauthenticated
from app.core.rbac import permissions_for
from app.core.security import decode_token
from app.modules.auth.models import UserSession
from app.modules.users.models import ACTIVE, PENDING_GUARDIAN, User

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"
CSRF_COOKIE = "csrf_token"


@dataclass
class CurrentUser:
    user: User
    session_id: UUID
    permissions: set[str] = field(default_factory=set)

    @property
    def id(self) -> UUID:
        return self.user.id

    @property
    def is_staff(self) -> bool:
        return self.user.is_staff

    def can(self, perm: str) -> bool:
        return perm in self.permissions


def _token_from(request: Request) -> str | None:
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:]
    return request.cookies.get(ACCESS_COOKIE)


async def _load(request: Request, session: AsyncSession, allow_pending: bool) -> CurrentUser:
    token = _token_from(request)
    payload = decode_token(token, "access") if token else None
    if not payload:
        raise Unauthenticated("Please sign in.", code="token_expired" if token else "unauthenticated")
    sess = await session.get(UserSession, UUID(payload["sid"]))
    if sess is None or sess.revoked_at is not None:
        raise Unauthenticated("Your session has ended. Please sign in again.")
    user = await session.scalar(select(User).where(User.id == UUID(payload["sub"])))
    if user is None:
        raise Unauthenticated()
    allowed = {ACTIVE, PENDING_GUARDIAN} if allow_pending else {ACTIVE}
    if user.status not in allowed:
        if user.status == PENDING_GUARDIAN:
            raise Forbidden("A parent or guardian must give consent before you can continue.",
                            code="guardian_consent_required")
        raise Unauthenticated("This account is not active.")
    return CurrentUser(user=user, session_id=sess.id, permissions=permissions_for(user.role_names))


async def current_user(request: Request, session: AsyncSession = Depends(get_session)) -> CurrentUser:
    return await _load(request, session, allow_pending=False)


async def current_user_allow_pending(
    request: Request, session: AsyncSession = Depends(get_session)
) -> CurrentUser:
    return await _load(request, session, allow_pending=True)


async def optional_user(request: Request, session: AsyncSession = Depends(get_session)) -> CurrentUser | None:
    if not _token_from(request):
        return None
    try:
        return await _load(request, session, allow_pending=True)
    except (Unauthenticated, Forbidden):
        return None


def require(*perms: str) -> Callable:
    """Route dependency: the user must hold every listed permission."""

    async def dep(user: CurrentUser = Depends(current_user)) -> CurrentUser:
        missing = [p for p in perms if p not in user.permissions]
        if missing:
            raise Forbidden("You don't have permission to do this.", meta={"missing": missing})
        return user

    return dep
