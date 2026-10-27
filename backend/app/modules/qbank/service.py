"""Test engine (BR-TST-01..09, BR-SCR-01..04). Grading happens only on the server;
answer keys are never sent before an assessment-mode question is submitted (ADR-010)."""

import random
from dataclasses import dataclass, field
from datetime import timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import Conflict, Invalid, NotFound
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.catalog.models import LearningModule, Subject
from app.modules.enrolment import service as enrolment
from app.modules.qbank.models import AttemptItem, Question, TestAttempt

SECONDS_PER_QUESTION = 90      # BR-TST-07: CFA Level I pace
CHAPTER_QUIZ_SIZE = 10         # BR-TST-09
CHAPTER_QUIZ_MIN = 3
CHAPTER_PASS_MARK = 80         # BR-SCR-02 (advisory: no locking, BR-OPN-04)
MASTER_QUIZ_SIZE = 50          # BR-TST-10
MASTER_PASS_MARK = 75
UNTIMED_RESUME_DAYS = 7        # BR-TST-08
MAX_ITEM_SECONDS = 600         # BR-ANL-03 cap


@dataclass
class Filters:
    subject_ids: list[UUID] = field(default_factory=list)
    lm_ids: list[UUID] = field(default_factory=list)
    difficulty: str = "all"     # all | E | M | H
    qtype: str = "all"          # all | conceptual | numerical


async def _allowed_subjects(session: AsyncSession, user, wanted: list[UUID]) -> list[UUID]:
    if user.is_staff:
        return wanted
    ent = await enrolment.entitled_subject_ids(session, user.id)
    return [s for s in wanted if s in ent]


async def eligible_pool(session: AsyncSession, user, f: Filters) -> list[Question]:
    """BR-TST-01: published questions, inside the filters, in subjects the student is entitled to."""
    subjects = await _allowed_subjects(session, user, f.subject_ids)
    if not subjects:
        return []
    stmt = select(Question).where(Question.status == "published", Question.subject_id.in_(subjects))
    if f.lm_ids:
        stmt = stmt.where(Question.lm_id.in_(f.lm_ids))
    if f.difficulty in ("E", "M", "H"):
        stmt = stmt.where(Question.difficulty == f.difficulty)
    if f.qtype in ("conceptual", "numerical"):
        stmt = stmt.where(Question.qtype == f.qtype)
    return list((await session.scalars(stmt)).all())


async def pool_breakdown(session: AsyncSession, user, f: Filters) -> dict:
    pool = await eligible_pool(session, user, f)
    by = {"E": 0, "M": 0, "H": 0}
    for q in pool:
        by[q.difficulty] = by.get(q.difficulty, 0) + 1
    return {"available": len(pool), "by_difficulty": by,
            "numerical": sum(1 for q in pool if q.qtype == "numerical")}


async def _history(session: AsyncSession, user_id: UUID) -> dict[UUID, tuple]:
    """Latest answer per question for this student: {question_id: (answered_at, is_correct)}."""
    rows = (await session.execute(
        select(AttemptItem.question_id, AttemptItem.answered_at, AttemptItem.is_correct)
        .join(TestAttempt, TestAttempt.id == AttemptItem.attempt_id)
        .where(TestAttempt.user_id == user_id, AttemptItem.answered_at.is_not(None))
    )).all()
    out: dict[UUID, tuple] = {}
    for qid, at, ok in rows:
        if qid not in out or at > out[qid][0]:
            out[qid] = (at, ok)
    return out


async def draw(session: AsyncSession, user_id: UUID, pool: list[Question], n: int) -> list[Question]:
    """BR-TST-03/04: no duplicates; unseen first, then previously wrong, then previously
    correct (least recent first); ties broken at random; final order shuffled."""
    hist = await _history(session, user_id)
    unseen = [q for q in pool if q.id not in hist]
    wrong = [q for q in pool if q.id in hist and not hist[q.id][1]]
    right = [q for q in pool if q.id in hist and hist[q.id][1]]
    random.shuffle(unseen)
    random.shuffle(wrong)
    wrong.sort(key=lambda q: hist[q.id][0])
    right.sort(key=lambda q: hist[q.id][0])
    chosen = (unseen + wrong + right)[:n]
    random.shuffle(chosen)
    return chosen


def _snapshot(q: Question) -> dict:
    """BR-TST-05: shuffle options unless their order is meaningful."""
    order = [0, 1, 2]
    if not q.lock_option_order:
        random.shuffle(order)
    return {"stem": q.stem, "options": [q.options[i] for i in order], "correct_index": order.index(q.correct_index),
            "explanation": q.explanation, "difficulty": q.difficulty, "qtype": q.qtype,
            "lm_id": str(q.lm_id) if q.lm_id else None, "subject_id": str(q.subject_id)}


async def create_attempt(session: AsyncSession, user, *, kind: str, title: str, questions: list[Question],
                         mode: str, timed: bool, filters: dict, subject_id: UUID | None = None,
                         lm_id: UUID | None = None, pass_mark: int | None = None) -> TestAttempt:
    if not questions:
        raise Invalid("No questions match these choices.", code="empty_pool")
    now = now_utc()
    limit = len(questions) * SECONDS_PER_QUESTION if timed else None
    a = TestAttempt(user_id=user.id, kind=kind, title=title, subject_id=subject_id, lm_id=lm_id, filters=filters,
                    mode=mode, timed=timed, time_limit_s=limit, started_at=now,
                    deadline_at=now + timedelta(seconds=limit) if limit else now + timedelta(days=UNTIMED_RESUME_DAYS),
                    total=len(questions), pass_mark=pass_mark)
    session.add(a)
    await session.flush()
    for pos, q in enumerate(questions):
        session.add(AttemptItem(attempt_id=a.id, position=pos, question_id=q.id, snapshot=_snapshot(q)))
    await session.flush()
    await audit.record(session, "attempt.started", actor=user, target_type="test_attempt", target_id=a.id,
                       subject_user_id=user.id, metadata={"kind": kind, "total": len(questions), "mode": mode})
    return a


async def chapter_quiz(session: AsyncSession, user, lm_id: UUID) -> TestAttempt:
    lm = await session.get(LearningModule, lm_id)
    if lm is None or lm.status != "published":
        raise NotFound()
    await enrolment.assert_entitled(session, user, lm.subject_id)
    pool = list((await session.scalars(select(Question).where(
        Question.lm_id == lm.id, Question.status == "published"))).all())
    if len(pool) < CHAPTER_QUIZ_MIN:
        raise Conflict("This LM doesn't have enough questions for a quiz yet.", code="quiz_unavailable")
    qs = await draw(session, user.id, pool, CHAPTER_QUIZ_SIZE)
    return await create_attempt(session, user, kind="chapter", title=f"Chapter quiz · LM{lm.lm_no} {lm.title}",
                                questions=qs, mode="assessment", timed=True, filters={"lm_id": str(lm.id)},
                                subject_id=lm.subject_id, lm_id=lm.id, pass_mark=CHAPTER_PASS_MARK)


async def master_quiz(session: AsyncSession, user, subject_code: str) -> TestAttempt:
    s = await session.scalar(select(Subject).where(Subject.code == subject_code))
    if s is None:
        raise NotFound()
    await enrolment.assert_entitled(session, user, s.id)
    pool = await eligible_pool(session, user, Filters(subject_ids=[s.id]))
    if len(pool) < CHAPTER_QUIZ_MIN:
        raise Conflict("Not enough questions in this subject yet.", code="quiz_unavailable")
    qs = await draw(session, user.id, pool, MASTER_QUIZ_SIZE)
    return await create_attempt(session, user, kind="master", title=f"Subject test · {s.name}", questions=qs,
                                mode="assessment", timed=True, filters={"subject": s.code}, subject_id=s.id,
                                pass_mark=MASTER_PASS_MARK)


async def get_attempt(session: AsyncSession, user, attempt_id: UUID, *, lock: bool = False) -> TestAttempt:
    a = await session.get(TestAttempt, attempt_id, with_for_update=lock)
    if a is None or a.user_id != user.id:
        raise NotFound()
    if a.status == "in_progress" and a.deadline_at and now_utc() > a.deadline_at:
        await finish(session, a, "timeout")  # BR-TST-07: auto-submit when time runs out
    return a


async def items(session: AsyncSession, attempt_id: UUID) -> list[AttemptItem]:
    return list((await session.scalars(select(AttemptItem).where(AttemptItem.attempt_id == attempt_id)
                                       .order_by(AttemptItem.position))).all())


async def answer(session: AsyncSession, user, attempt_id: UUID, position: int, answer_index: int | None,
                 time_spent_s: int, flagged: bool | None) -> tuple[TestAttempt, AttemptItem]:
    a = await get_attempt(session, user, attempt_id, lock=True)
    if a.status != "in_progress":
        await session.commit()  # keep a timeout auto-submit even though we refuse the answer
        raise Conflict("This test has already been submitted.", code="attempt_closed")
    it = await session.get(AttemptItem, (a.id, position), with_for_update=True)
    if it is None:
        raise NotFound()
    if answer_index is not None and not 0 <= answer_index <= 2:
        raise Invalid("Choose A, B or C.")
    it.time_spent_s = min(MAX_ITEM_SECONDS, it.time_spent_s + max(0, min(time_spent_s, MAX_ITEM_SECONDS)))
    if flagged is not None:
        it.flagged = flagged
    if answer_index is not None:
        if a.mode == "practice" and it.answer_index is not None:
            raise Conflict("In practice mode an answer is final once checked.", code="answer_locked")  # BR-TST-06
        it.answer_index, it.answered_at = answer_index, now_utc()
        it.is_correct = answer_index == it.snapshot["correct_index"]
    return a, it


async def finish(session: AsyncSession, a: TestAttempt, reason: str) -> TestAttempt:
    if a.status != "in_progress":
        return a
    its = await items(session, a.id)
    for it in its:
        if it.answer_index is None:
            it.is_correct = False
    correct = sum(1 for it in its if it.answer_index is not None and it.is_correct)
    a.correct, a.status, a.submitted_at, a.submit_reason = correct, "submitted", now_utc(), reason
    a.score_pct = round(correct / a.total * 100, 2) if a.total else 0.0  # BR-SCR-01
    await audit.record(session, "attempt.submitted", actor_type="system" if reason == "timeout" else "user",
                       target_type="test_attempt", target_id=a.id, subject_user_id=a.user_id,
                       metadata={"kind": a.kind, "correct": correct, "total": a.total, "reason": reason})
    return a


async def best_scores(session: AsyncSession, user_id: UUID, lm_ids: list[UUID]) -> dict[UUID, dict]:
    if not lm_ids:
        return {}
    rows = (await session.execute(
        select(TestAttempt.lm_id, func.max(TestAttempt.score_pct), func.count())
        .where(TestAttempt.user_id == user_id, TestAttempt.kind == "chapter", TestAttempt.status == "submitted",
               TestAttempt.lm_id.in_(lm_ids)).group_by(TestAttempt.lm_id))).all()
    return {lm: {"best_pct": best, "attempts": n} for lm, best, n in rows}


async def question_counts(session: AsyncSession, lm_ids: list[UUID]) -> dict[UUID, int]:
    if not lm_ids:
        return {}
    rows = (await session.execute(select(Question.lm_id, func.count()).where(
        Question.lm_id.in_(lm_ids), Question.status == "published").group_by(Question.lm_id))).all()
    return dict(rows)
