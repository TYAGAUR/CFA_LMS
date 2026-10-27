"""Entitlements decide who may see which subject (BR-ENR-01, BR-OPN-01/05)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotEntitled
from app.core.timeutil import now_utc
from app.modules.enrolment.models import Entitlement


def _active(now: datetime):
    return (Entitlement.revoked_at.is_(None), Entitlement.starts_at <= now, Entitlement.ends_at > now)


async def entitled_subject_ids(session: AsyncSession, user_id: UUID) -> set[UUID]:
    now = now_utc()
    rows = await session.scalars(select(Entitlement.subject_id).where(Entitlement.user_id == user_id, *_active(now)))
    return set(rows.all())


async def is_entitled(session: AsyncSession, user, subject_id: UUID) -> bool:
    if user is not None and getattr(user, "is_staff", False):
        return True  # staff can preview all content
    if user is None:
        return False
    return subject_id in await entitled_subject_ids(session, user.id)


async def assert_entitled(session: AsyncSession, user, subject_id: UUID) -> None:
    if not await is_entitled(session, user, subject_id):
        raise NotEntitled("Register for a course that includes this subject to open it.")


async def grant(session: AsyncSession, *, user_id: UUID, subject_ids: list[UUID], source: str,
                source_id: UUID | None, starts_at: datetime, ends_at: datetime) -> int:
    n = 0
    for sid in subject_ids:
        exists = await session.scalar(select(Entitlement.id).where(
            Entitlement.user_id == user_id, Entitlement.subject_id == sid, Entitlement.source == source,
            Entitlement.source_id == source_id, Entitlement.revoked_at.is_(None)))
        if exists:
            continue  # idempotent
        session.add(Entitlement(user_id=user_id, subject_id=sid, source=source, source_id=source_id,
                                starts_at=starts_at, ends_at=ends_at))
        n += 1
    return n


async def revoke_source(session: AsyncSession, source: str, source_id: UUID) -> None:
    await session.execute(update(Entitlement).where(
        Entitlement.source == source, Entitlement.source_id == source_id, Entitlement.revoked_at.is_(None)
    ).values(revoked_at=now_utc()))
