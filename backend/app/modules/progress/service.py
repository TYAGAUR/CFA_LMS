"""Progress rules (BR-PRG, BR-REV). Progress is informational only (BR-OPN-03)."""

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import Conflict, Invalid
from app.core.timeutil import now_utc, today_ist
from app.modules.audit import service as audit
from app.modules.media.models import Resource
from app.modules.progress.models import (
    EocEntry,
    LmProgress,
    ResourceProgress,
    RevisionLog,
)

COMPLETION_THRESHOLD = 0.90  # BR-PRG-01
MAX_HEARTBEAT_SPAN_S = 60


def merge_intervals(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """Merge [start, end] second ranges; counts each second once (seeking ahead doesn't count)."""
    items = sorted([*intervals, new])
    out: list[list[int]] = []
    for s, e in items:
        if out and s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def covered_seconds(intervals: list[list[int]]) -> int:
    return sum(e - s for s, e in intervals)


async def _get_rp(session: AsyncSession, user_id: UUID, resource_id: UUID) -> ResourceProgress:
    await session.execute(insert(ResourceProgress).values(
        user_id=user_id, resource_id=resource_id, watched=[], last_position_s=0, updated_at=now_utc()
    ).on_conflict_do_nothing())
    return await session.get(ResourceProgress, (user_id, resource_id), with_for_update=True,
                             populate_existing=True)


async def record_progress(session: AsyncSession, user_id: UUID, res: Resource, *, from_s: int | None,
                          to_s: int | None, position_s: int | None, mark_complete: bool) -> dict:
    rp = await _get_rp(session, user_id, res.id)
    if res.kind == "video" and from_s is not None and to_s is not None:
        if not (0 <= from_s <= to_s) or to_s - from_s > MAX_HEARTBEAT_SPAN_S:
            raise Invalid("Invalid progress interval", code="invalid_interval")
        if res.duration_s:
            to_s = min(to_s, res.duration_s)
        rp.watched = merge_intervals([list(x) for x in rp.watched or []], [from_s, to_s])
    if position_s is not None:
        rp.last_position_s = max(0, position_s)
    coverage = 0.0
    if res.kind == "video" and res.duration_s:
        coverage = covered_seconds(rp.watched) / res.duration_s
        if coverage >= COMPLETION_THRESHOLD and rp.completed_at is None:
            rp.completed_at = now_utc()
    # Videos without a known duration, and documents/links, can be marked done manually.
    if mark_complete and rp.completed_at is None and (res.kind != "video" or not res.duration_s):
        rp.completed_at = now_utc()
    rp.updated_at = now_utc()
    return {"completed": rp.completed_at is not None, "coverage_pct": round(min(coverage, 1) * 100),
            "last_position_s": rp.last_position_s}


async def _lmp(session: AsyncSession, user_id: UUID, lm_id: UUID) -> LmProgress:
    await session.execute(insert(LmProgress).values(user_id=user_id, lm_id=lm_id).on_conflict_do_nothing())
    return await session.get(LmProgress, (user_id, lm_id), with_for_update=True, populate_existing=True)


async def touch_lm(session: AsyncSession, user_id: UUID, lm_id: UUID) -> None:
    (await _lmp(session, user_id, lm_id)).last_opened_at = now_utc()


async def mark_learned(session: AsyncSession, user, lm_id: UUID) -> LmProgress:
    p = await _lmp(session, user.id, lm_id)
    if p.learned_at is None:
        p.learned_at, p.learned_undo_until = now_utc(), now_utc() + timedelta(hours=24)
        await audit.record(session, "lm.marked_learned", actor=user, target_type="learning_module", target_id=lm_id,
                           subject_user_id=user.id)
    return p


async def undo_learned(session: AsyncSession, user, lm_id: UUID) -> LmProgress:
    p = await _lmp(session, user.id, lm_id)
    if p.learned_at is None:
        return p
    if p.learned_undo_until and p.learned_undo_until < now_utc():
        raise Conflict("The 24-hour undo window has passed. Ask an admin to change this.", code="undo_expired")
    p.learned_at = p.learned_undo_until = None
    await audit.record(session, "lm.learned_undone", actor=user, target_type="learning_module", target_id=lm_id,
                       subject_user_id=user.id)
    return p


async def log_revision(session: AsyncSession, user, lm_id: UUID, activity: str, revised_on: date | None) -> dict:
    day = revised_on or today_ist()
    if day > today_ist():
        raise Invalid("Revision date cannot be in the future.")
    already = await session.scalar(select(RevisionLog.id).where(
        RevisionLog.user_id == user.id, RevisionLog.lm_id == lm_id, RevisionLog.revised_on == day,
        RevisionLog.counted))
    counted = already is None  # BR-REV-02: one counted revision per LM per IST day
    session.add(RevisionLog(user_id=user.id, lm_id=lm_id, revised_on=day, activity=activity, counted=counted,
                            created_at=now_utc()))
    await session.flush()
    await audit.record(session, "revision.logged", actor=user, target_type="learning_module", target_id=lm_id,
                       subject_user_id=user.id, metadata={"activity": activity, "counted": counted})
    return {"counted": counted, "revision_count": await revision_count(session, user.id, lm_id)}


async def revision_count(session: AsyncSession, user_id: UUID, lm_id: UUID) -> int:
    return await session.scalar(select(func.count()).select_from(RevisionLog).where(
        RevisionLog.user_id == user_id, RevisionLog.lm_id == lm_id, RevisionLog.counted)) or 0


async def save_eoc(session: AsyncSession, user, lm_id: UUID, data: dict) -> EocEntry:
    if data["q_correct"] > data["q_attempted"]:
        raise Invalid("Correct answers cannot exceed questions attempted.")
    if data.get("completed_on") and data["completed_on"] > today_ist():
        raise Invalid("Date cannot be in the future.")
    if not data["attempted"] and data.get("completed_on"):
        raise Invalid("Mark the EOC questions as attempted before setting a completion date.")
    e = await session.get(EocEntry, (user.id, lm_id), with_for_update=True)
    if e is None:
        e = EocEntry(user_id=user.id, lm_id=lm_id)
        session.add(e)
    for k, v in data.items():
        setattr(e, k, v)
    e.updated_at = now_utc()
    await audit.record(session, "eoc.updated", actor=user, target_type="learning_module", target_id=lm_id,
                       subject_user_id=user.id, metadata={k: str(v) for k, v in data.items() if k != "weak_topics"})
    return e
