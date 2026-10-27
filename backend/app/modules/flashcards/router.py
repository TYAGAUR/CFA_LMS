"""Flashcard decks, review sessions, and staff card management (BR-FC)."""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import Invalid, NotFound
from app.core.schemas import In
from app.core.timeutil import now_utc, today_ist
from app.modules.audit import service as audit
from app.modules.catalog.models import LearningModule, Subject
from app.modules.enrolment import service as enrolment
from app.modules.flashcards.models import CardReview, Flashcard
from app.modules.flashcards.service import SrsState, schedule

router = APIRouter(tags=["flashcards"])


@router.get("/flashcards/decks")
async def decks(user: CurrentUser = Depends(require("flashcard:review")),
                session: AsyncSession = Depends(get_session)) -> list[dict]:
    ent = None if user.is_staff else await enrolment.entitled_subject_ids(session, user.id)
    today = today_ist()
    subs = (await session.scalars(select(Subject).order_by(Subject.sort_order))).all()
    totals = dict((await session.execute(select(Flashcard.subject_id, func.count()).where(
        Flashcard.status == "published").group_by(Flashcard.subject_id))).all())
    rows = (await session.execute(
        select(Flashcard.subject_id, CardReview.due_on, CardReview.reps, CardReview.interval_days)
        .join(CardReview, CardReview.card_id == Flashcard.id)
        .where(CardReview.user_id == user.id, Flashcard.status == "published"))).all()
    out = []
    for s in subs:
        total = totals.get(s.id, 0)
        if not total:
            continue
        mine = [r for r in rows if r[0] == s.id]
        due = sum(1 for r in mine if r[1] <= today)
        mastered = sum(1 for r in mine if r[3] >= 21)
        out.append({"code": s.code, "name": s.name, "icon": s.icon, "entitled": ent is None or s.id in ent,
                    "total": total, "new": total - len(mine), "due": due, "learning": len(mine) - mastered,
                    "mastered": mastered})
    return out


@router.get("/flashcards/session")
async def session_cards(subject: str, lm_id: UUID | None = None, limit: int = Query(20, ge=1, le=100),
                        include_future: bool = False,
                        user: CurrentUser = Depends(require("flashcard:review")),
                        session: AsyncSession = Depends(get_session)) -> dict:
    """Due cards first (oldest due first, BR-FC-04), then new cards. `include_future` adds cards not yet due
    (cram mode) when nothing else is left."""
    s = await session.scalar(select(Subject).where(Subject.code == subject))
    if s is None:
        raise NotFound()
    await enrolment.assert_entitled(session, user, s.id)
    today = today_ist()
    stmt = select(Flashcard, CardReview).outerjoin(CardReview, (CardReview.card_id == Flashcard.id) &
                                                   (CardReview.user_id == user.id)).where(
        Flashcard.subject_id == s.id, Flashcard.status == "published")
    if lm_id:
        stmt = stmt.where(Flashcard.lm_id == lm_id)
    rows = (await session.execute(stmt.order_by(Flashcard.sort_order, Flashcard.created_at))).all()
    due = sorted([(c, r) for c, r in rows if r and r.due_on <= today], key=lambda x: x[1].due_on)
    new = [(c, r) for c, r in rows if r is None]
    later = sorted([(c, r) for c, r in rows if r and r.due_on > today], key=lambda x: x[1].due_on)
    picked = (due + new + (later if include_future else []))[:limit]
    return {
        "subject": {"code": s.code, "name": s.name},
        "counts": {"due": len(due), "new": len(new), "later": len(later)},
        "cards": [{"id": c.id, "front": c.front, "back": c.back, "lm_id": c.lm_id,
                   "state": None if r is None else {"due_on": r.due_on, "interval_days": r.interval_days,
                                                    "last_rating": r.last_rating}} for c, r in picked],
    }


class ReviewIn(In):
    rating: Literal["known", "needs_revision", "difficult"]


@router.post("/flashcards/{card_id}/review")
async def review(card_id: UUID, body: ReviewIn, user: CurrentUser = Depends(require("flashcard:review")),
                 session: AsyncSession = Depends(get_session)) -> dict:
    c = await session.get(Flashcard, card_id)
    if c is None or c.status != "published":
        raise NotFound()
    await enrolment.assert_entitled(session, user, c.subject_id)
    r = await session.get(CardReview, (user.id, c.id), with_for_update=True)
    state = SrsState() if r is None else SrsState(r.ease, r.interval_days, r.reps, r.lapses)
    new, due = schedule(state, body.rating, today_ist())
    if r is None:
        r = CardReview(user_id=user.id, card_id=c.id, total_reviews=0, known_reviews=0)
        session.add(r)
    r.ease, r.interval_days, r.reps, r.lapses = new.ease, new.interval_days, new.reps, new.lapses
    r.due_on, r.last_rating, r.last_reviewed_at = due, body.rating, now_utc()
    r.total_reviews = (r.total_reviews or 0) + 1
    r.known_reviews = (r.known_reviews or 0) + (1 if body.rating == "known" else 0)
    return {"card_id": c.id, "due_on": due, "interval_days": new.interval_days}


# ---------- staff ----------

class CardIn(In):
    subject_code: str
    lm_id: UUID | None = None
    front: str = Field(min_length=2, max_length=500)
    back: str = Field(min_length=1, max_length=1500)
    status: Literal["draft", "published", "retired"] = "published"


def card_out(c: Flashcard) -> dict:
    return {"id": c.id, "subject_id": c.subject_id, "lm_id": c.lm_id, "front": c.front, "back": c.back,
            "status": c.status}


@router.get("/admin/flashcards")
async def admin_cards(subject: str | None = None, _: CurrentUser = Depends(require("catalog:read_admin")),
                      session: AsyncSession = Depends(get_session)) -> list[dict]:
    stmt = select(Flashcard)
    if subject:
        stmt = stmt.join(Subject, Subject.id == Flashcard.subject_id).where(Subject.code == subject)
    return [card_out(c) for c in (await session.scalars(stmt.order_by(Flashcard.created_at))).all()]


async def _apply(session: AsyncSession, c: Flashcard, body: CardIn) -> None:
    s = await session.scalar(select(Subject).where(Subject.code == body.subject_code))
    if s is None:
        raise Invalid("Unknown subject")
    if body.lm_id:
        lm = await session.get(LearningModule, body.lm_id)
        if lm is None or lm.subject_id != s.id:
            raise Invalid("The LM does not belong to that subject.")
    c.subject_id, c.lm_id, c.front, c.back, c.status = s.id, body.lm_id, body.front, body.back, body.status


@router.post("/admin/flashcards", status_code=201)
async def create_card(body: CardIn, actor: CurrentUser = Depends(require("flashcard:write")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    c = Flashcard(created_by=actor.id)
    await _apply(session, c, body)
    session.add(c)
    await session.flush()
    await audit.record(session, "flashcard.created", actor=actor, target_type="flashcard", target_id=c.id)
    return card_out(c)


@router.patch("/admin/flashcards/{cid}")
async def update_card(cid: UUID, body: CardIn, actor: CurrentUser = Depends(require("flashcard:write")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    c = await session.get(Flashcard, cid)
    if c is None:
        raise NotFound()
    await _apply(session, c, body)
    await audit.record(session, "flashcard.updated", actor=actor, target_type="flashcard", target_id=c.id)
    return card_out(c)
