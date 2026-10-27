"""Audit writer with hash chain (G-01 §4–§5)."""

import hashlib
import json
from typing import Any
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context import client_ip_var, request_id_var
from app.core.timeutil import now_utc
from app.modules.audit.models import AuditLog

_LOCK_KEY = 7_420_001  # advisory lock id serialising audit inserts


def mask_mobile(m: str | None) -> str | None:
    return None if not m else f"{m[:3]}******{m[-4:]}"


def _canonical(row: AuditLog) -> bytes:
    data = {
        "occurred_at": row.occurred_at.isoformat(),
        "actor_user_id": str(row.actor_user_id) if row.actor_user_id else None,
        "actor_type": row.actor_type,
        "action": row.action,
        "target_type": row.target_type,
        "target_id": row.target_id,
        "subject_user_id": str(row.subject_user_id) if row.subject_user_id else None,
        "reason": row.reason,
        "changes": row.changes,
        "metadata": row.metadata_,
    }
    return json.dumps(data, sort_keys=True, default=str).encode()


async def record(
    session: AsyncSession,
    action: str,
    *,
    actor: Any = None,
    target_type: str | None = None,
    target_id: Any = None,
    subject_user_id: UUID | None = None,
    changes: dict | None = None,
    reason: str | None = None,
    metadata: dict | None = None,
    actor_type: str | None = None,
    with_ip: bool = False,
) -> None:
    """`actor` is a CurrentUser, a User, or None for system/job/webhook events."""
    user = getattr(actor, "user", actor)
    await session.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": _LOCK_KEY})
    prev = await session.scalar(select(AuditLog.hash).order_by(AuditLog.id.desc()).limit(1))
    row = AuditLog(
        occurred_at=now_utc(),
        actor_user_id=getattr(user, "id", None),
        actor_type=actor_type or ("user" if user is not None else "system"),
        actor_roles=list(getattr(user, "role_names", []) or []),
        action=action,
        target_type=target_type,
        target_id=str(target_id) if target_id is not None else None,
        subject_user_id=subject_user_id,
        request_id=request_id_var.get(),
        ip_address=client_ip_var.get() if with_ip else None,
        reason=reason,
        changes=json.loads(json.dumps(changes, default=str)) if changes else None,
        metadata_=json.loads(json.dumps(metadata, default=str)) if metadata else None,
        prev_hash=prev,
    )
    row.hash = hashlib.sha256((prev or b"") + _canonical(row)).digest()
    session.add(row)
    await session.flush()


async def verify_chain(session: AsyncSession) -> tuple[bool, int]:
    """Recompute the chain; returns (ok, rows_checked)."""
    prev: bytes | None = None
    n = 0
    for row in (await session.scalars(select(AuditLog).order_by(AuditLog.id))).all():
        expected = hashlib.sha256((prev or b"") + _canonical(row)).digest()
        if row.prev_hash != prev or row.hash != expected:
            return False, n
        prev = row.hash
        n += 1
    return True, n
