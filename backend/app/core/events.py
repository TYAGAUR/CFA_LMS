"""Domain events (A-01 §5, A-08 §6).

`publish()` writes the event to the outbox in the caller's transaction and runs the
in-process subscribers in that same transaction, so local consistency is immediate.
The outbox dispatcher then forwards events to an optional HTTP sink (EVENT_SINK_URL),
which lets other services or teams (e.g. a separate payments or CRM service) consume
them without touching this codebase.
"""

import asyncio
import json
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hmac_sha256_hex
from app.core.timeutil import now_utc

log = logging.getLogger("events")

Handler = Callable[[AsyncSession, dict[str, Any]], Awaitable[None]]
_handlers: dict[str, list[Handler]] = defaultdict(list)


def subscribe(topic: str) -> Callable[[Handler], Handler]:
    def deco(fn: Handler) -> Handler:
        _handlers[topic].append(fn)
        return fn

    return deco


async def publish(session: AsyncSession, topic: str, payload: dict[str, Any]) -> None:
    from app.modules.audit.models import OutboxEvent

    safe = json.loads(json.dumps(payload, default=str))
    session.add(OutboxEvent(topic=topic, payload=safe, created_at=now_utc()))
    for handler in _handlers.get(topic, []):
        await handler(session, safe)


async def dispatch_outbox_once(session: AsyncSession, batch: int = 100) -> int:
    from app.modules.audit.models import OutboxEvent

    settings = get_settings()
    rows = (
        await session.scalars(
            select(OutboxEvent).where(OutboxEvent.dispatched_at.is_(None))
            .order_by(OutboxEvent.id).limit(batch).with_for_update(skip_locked=True)
        )
    ).all()
    if not rows:
        return 0
    async with httpx.AsyncClient(timeout=10) as client:
        for ev in rows:
            if settings.event_sink_url:
                body = json.dumps({"id": ev.id, "topic": ev.topic, "payload": ev.payload,
                                   "created_at": ev.created_at.isoformat()}).encode()
                try:
                    r = await client.post(settings.event_sink_url, content=body, headers={
                        "content-type": "application/json",
                        "x-event-signature": hmac_sha256_hex(settings.secret_key, body),
                    })
                    r.raise_for_status()
                except Exception as exc:  # retried on the next cycle
                    ev.attempts += 1
                    ev.last_error = str(exc)[:500]
                    continue
            ev.dispatched_at = now_utc()
    return len(rows)


async def outbox_loop(stop: asyncio.Event, interval: float = 2.0) -> None:
    from app.core.db import SessionLocal

    while not stop.is_set():
        try:
            async with SessionLocal() as session:
                await dispatch_outbox_once(session)
                await session.commit()
        except Exception:
            log.exception("outbox dispatch failed")
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except TimeoutError:
            pass
