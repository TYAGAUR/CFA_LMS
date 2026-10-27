"""Tests and quizzes (student) + question bank (staff). A-04 §4."""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field, field_validator
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import Forbidden, Invalid, NotFound
from app.core.schemas import In
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.catalog.models import LearningModule, Subject
from app.modules.enrolment import service as enrolment
from app.modules.qbank import service as svc
from app.modules.qbank.models import AttemptItem, Question, TestAttempt

router = APIRouter(tags=["tests"])
LETTERS = "ABC"


# ---------- serialisation (never leaks keys early: ADR-010) ----------

def item_out(a: TestAttempt, it: AttemptItem) -> dict:
    s = it.snapshot
    out = {"position": it.position, "stem": s["stem"], "options": s["options"], "difficulty": s["difficulty"],
           "answer_index": it.answer_index, "flagged": it.flagged}
    reveal = a.status == "submitted" or (a.mode == "practice" and it.answer_index is not None)
    if reveal:
        out.update(correct_index=s["correct_index"], explanation=s["explanation"],
                   is_correct=it.answer_index is not None and it.answer_index == s["correct_index"])
    return out


def attempt_out(a: TestAttempt, its: list[AttemptItem] | None = None) -> dict:
    left = None
    if a.status == "in_progress" and a.timed and a.deadline_at:
        left = max(0, int((a.deadline_at - now_utc()).total_seconds()))
    out = {"id": a.id, "kind": a.kind, "title": a.title, "mode": a.mode, "timed": a.timed,
           "time_limit_s": a.time_limit_s, "seconds_left": left, "status": a.status, "started_at": a.started_at,
           "submitted_at": a.submitted_at, "submit_reason": a.submit_reason, "total": a.total, "correct": a.correct,
           "score_pct": a.score_pct, "pass_mark": a.pass_mark, "lm_id": a.lm_id,
           "passed": (a.score_pct >= a.pass_mark) if a.score_pct is not None and a.pass_mark else None}
    if its is not None:
        out["items"] = [item_out(a, it) for it in its]
        out["answered"] = sum(1 for it in its if it.answer_index is not None)
    return out


# ---------- builder ----------

class FilterIn(In):
    subject_codes: list[str] = Field(min_length=1, max_length=10)
    lm_ids: list[UUID] = []
    difficulty: Literal["all", "E", "M", "H"] = "all"
    qtype: Literal["all", "conceptual", "numerical"] = "all"


class CustomTestIn(FilterIn):
    count: int = Field(ge=1, le=100)
    mode: Literal["practice", "assessment"] = "practice"
    timed: bool = False


async def _filters(session: AsyncSession, body: FilterIn) -> svc.Filters:
    subs = (await session.scalars(select(Subject).where(Subject.code.in_(body.subject_codes)))).all()
    if len(subs) != len(set(body.subject_codes)):
        raise Invalid("Unknown subject")
    return svc.Filters(subject_ids=[s.id for s in subs], lm_ids=body.lm_ids, difficulty=body.difficulty,
                       qtype=body.qtype)


@router.get("/practice/options")
async def practice_options(user: CurrentUser = Depends(require("test:take")),
                           session: AsyncSession = Depends(get_session)) -> list[dict]:
    """Subjects (and LMs) the student can build tests from, with question counts."""
    ent = None if user.is_staff else await enrolment.entitled_subject_ids(session, user.id)
    subs = (await session.scalars(select(Subject).where(Subject.status == "published")
                                  .order_by(Subject.sort_order))).all()
    counts = dict((await session.execute(select(Question.lm_id, func.count()).where(
        Question.status == "published").group_by(Question.lm_id))).all())
    subj_counts = dict((await session.execute(select(Question.subject_id, func.count()).where(
        Question.status == "published").group_by(Question.subject_id))).all())
    return [{"code": s.code, "name": s.name, "icon": s.icon, "entitled": ent is None or s.id in ent,
             "questions": subj_counts.get(s.id, 0),
             "lms": [{"id": lm.id, "lm_no": lm.lm_no, "title": lm.title, "questions": counts.get(lm.id, 0)}
                     for lm in s.lms if lm.status == "published"]} for s in subs]


@router.post("/tests/preview")
async def preview(body: FilterIn, user: CurrentUser = Depends(require("test:take")),
                  session: AsyncSession = Depends(get_session)) -> dict:
    return await svc.pool_breakdown(session, user, await _filters(session, body))


@router.post("/tests", status_code=201)
async def create_custom(body: CustomTestIn, user: CurrentUser = Depends(require("test:take")),
                        session: AsyncSession = Depends(get_session)) -> dict:
    f = await _filters(session, body)
    pool = await svc.eligible_pool(session, user, f)
    if not pool:
        raise Invalid("No questions match these choices. Widen the subjects or difficulty.", code="empty_pool")
    qs = await svc.draw(session, user.id, pool, body.count)  # BR-TST-02: never padded from outside the filters
    label = {"all": "Mixed", "E": "Easy", "M": "Medium", "H": "Hard"}[body.difficulty]
    a = await svc.create_attempt(session, user, kind="custom", title=f"Custom test · {label} · {len(qs)} questions",
                                 questions=qs, mode=body.mode, timed=body.timed,
                                 filters=body.model_dump(mode="json"))
    out = attempt_out(a)
    out["requested"], out["served"] = body.count, len(qs)
    return out


@router.post("/lms/{lm_id}/quiz", status_code=201)
async def start_chapter_quiz(lm_id: UUID, user: CurrentUser = Depends(require("test:take")),
                             session: AsyncSession = Depends(get_session)) -> dict:
    return attempt_out(await svc.chapter_quiz(session, user, lm_id))


@router.post("/subjects/{code}/test", status_code=201)
async def start_subject_test(code: str, user: CurrentUser = Depends(require("test:take")),
                             session: AsyncSession = Depends(get_session)) -> dict:
    return attempt_out(await svc.master_quiz(session, user, code))


# ---------- taking a test ----------

@router.get("/attempts/{attempt_id}")
async def get_attempt(attempt_id: UUID, user: CurrentUser = Depends(require("test:take")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    a = await svc.get_attempt(session, user, attempt_id)
    return attempt_out(a, await svc.items(session, a.id))


class AnswerIn(In):
    answer_index: int | None = Field(default=None, ge=0, le=2)
    time_spent_s: int = Field(default=0, ge=0, le=3600)
    flagged: bool | None = None


@router.put("/attempts/{attempt_id}/items/{position}")
async def save_answer(attempt_id: UUID, position: int, body: AnswerIn,
                      user: CurrentUser = Depends(require("test:take")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    a, it = await svc.answer(session, user, attempt_id, position, body.answer_index, body.time_spent_s, body.flagged)
    return item_out(a, it)


@router.post("/attempts/{attempt_id}/submit")
async def submit(attempt_id: UUID, user: CurrentUser = Depends(require("test:take")),
                 session: AsyncSession = Depends(get_session)) -> dict:
    a = await svc.get_attempt(session, user, attempt_id, lock=True)
    await svc.finish(session, a, "student")
    return attempt_out(a, await svc.items(session, a.id))


@router.get("/me/attempts")
async def my_attempts(kind: str | None = None, limit: int = Query(50, le=200),
                      user: CurrentUser = Depends(require("test:take")),
                      session: AsyncSession = Depends(get_session)) -> list[dict]:
    stmt = select(TestAttempt).where(TestAttempt.user_id == user.id)
    if kind:
        stmt = stmt.where(TestAttempt.kind == kind)
    rows = (await session.scalars(stmt.order_by(TestAttempt.started_at.desc()).limit(limit))).all()
    return [attempt_out(a) for a in rows]


@router.get("/me/test-stats")
async def test_stats(user: CurrentUser = Depends(require("test:take")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    """Accuracy by subject and difficulty across submitted attempts (BR-ANL-01)."""
    rows = (await session.execute(
        select(AttemptItem.snapshot, AttemptItem.answer_index, AttemptItem.is_correct)
        .join(TestAttempt, TestAttempt.id == AttemptItem.attempt_id)
        .where(TestAttempt.user_id == user.id, TestAttempt.status == "submitted"))).all()
    subjects = {str(s.id): s for s in (await session.scalars(select(Subject))).all()}
    by_s: dict[str, list[int]] = {}
    by_d: dict[str, list[int]] = {"E": [0, 0], "M": [0, 0], "H": [0, 0]}
    for snap, ans, ok in rows:
        if ans is None:
            continue
        s = by_s.setdefault(snap.get("subject_id", ""), [0, 0])
        s[0] += 1
        s[1] += 1 if ok else 0
        d = by_d.setdefault(snap["difficulty"], [0, 0])
        d[0] += 1
        d[1] += 1 if ok else 0

    def pct(v):
        return round(v[1] / v[0] * 100) if v[0] else None

    return {
        "answered": sum(v[0] for v in by_s.values()),
        "by_subject": sorted([{"code": subjects[k].code, "name": subjects[k].name, "answered": v[0],
                               "accuracy_pct": pct(v)} for k, v in by_s.items() if k in subjects],
                             key=lambda x: x["accuracy_pct"] if x["accuracy_pct"] is not None else 101),
        "by_difficulty": [{"difficulty": k, "answered": v[0], "accuracy_pct": pct(v)} for k, v in by_d.items()],
    }


# ---------- staff: question bank ----------

class QuestionIn(In):
    subject_code: str
    lm_id: UUID | None = None
    stem: str = Field(min_length=10, max_length=4000)
    options: list[str] = Field(min_length=3, max_length=3)
    correct_index: int = Field(ge=0, le=2)
    explanation: str = Field(min_length=5, max_length=6000)
    difficulty: Literal["E", "M", "H"]
    qtype: Literal["conceptual", "numerical"] = "conceptual"
    lock_option_order: bool = False
    provenance: Literal["original", "licensed_third_party"] = "original"

    @field_validator("options")
    @classmethod
    def _opts(cls, v: list[str]) -> list[str]:
        v = [o.strip() for o in v]
        if any(not o for o in v) or len({o.lower() for o in v}) != 3:
            raise ValueError("three different, non-empty options are required")
        return v


def q_out(q: Question) -> dict:
    return {"id": q.id, "subject_id": q.subject_id, "lm_id": q.lm_id, "stem": q.stem, "options": q.options,
            "correct_index": q.correct_index, "explanation": q.explanation, "difficulty": q.difficulty,
            "qtype": q.qtype, "lock_option_order": q.lock_option_order, "status": q.status, "version": q.version,
            "provenance": q.provenance, "author_id": q.author_id, "updated_at": q.updated_at}


@router.get("/admin/questions")
async def list_questions(subject: str | None = None, lm_id: UUID | None = None, status: str | None = None,
                         difficulty: str | None = None, q: str | None = None, limit: int = Query(200, le=500),
                         _: CurrentUser = Depends(require("catalog:read_admin")),
                         session: AsyncSession = Depends(get_session)) -> dict:
    stmt = select(Question)
    if subject:
        stmt = stmt.join(Subject, Subject.id == Question.subject_id).where(Subject.code == subject)
    if lm_id:
        stmt = stmt.where(Question.lm_id == lm_id)
    if status:
        stmt = stmt.where(Question.status == status)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)
    if q:
        stmt = stmt.where(or_(Question.stem.ilike(f"%{q}%"), Question.explanation.ilike(f"%{q}%")))
    total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = (await session.scalars(stmt.order_by(Question.created_at).limit(limit))).all()
    return {"total": total, "items": [q_out(x) for x in rows]}


async def _apply(session: AsyncSession, qn: Question, body: QuestionIn) -> None:
    s = await session.scalar(select(Subject).where(Subject.code == body.subject_code))
    if s is None:
        raise Invalid("Unknown subject")
    if body.lm_id:
        lm = await session.get(LearningModule, body.lm_id)
        if lm is None or lm.subject_id != s.id:
            raise Invalid("The LM does not belong to that subject.")
    data = body.model_dump(exclude={"subject_code"})
    for k, v in data.items():
        setattr(qn, k, v)
    qn.subject_id = s.id


@router.post("/admin/questions", status_code=201)
async def create_question(body: QuestionIn, actor: CurrentUser = Depends(require("qbank:write")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    qn = Question(author_id=actor.id, status="draft")
    await _apply(session, qn, body)
    session.add(qn)
    await session.flush()
    await audit.record(session, "question.created", actor=actor, target_type="question", target_id=qn.id)
    return q_out(qn)


@router.patch("/admin/questions/{qid}")
async def update_question(qid: UUID, body: QuestionIn, actor: CurrentUser = Depends(require("qbank:write")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    qn = await session.get(Question, qid)
    if qn is None:
        raise NotFound()
    before = q_out(qn)
    await _apply(session, qn, body)
    qn.version += 1  # past attempts keep their own snapshot (BR-QB-02)
    if qn.status == "published":
        qn.status = "draft"  # edited questions go back through review before students see them
    await session.flush()
    changes = {k: {"old": before[k], "new": v} for k, v in q_out(qn).items()
               if k not in ("updated_at", "version") and before[k] != v}
    await audit.record(session, "question.updated", actor=actor, target_type="question", target_id=qn.id,
                       changes=changes, metadata={"version": qn.version})
    return q_out(qn)


@router.post("/admin/questions/{qid}/{action}")
async def set_question_status(qid: UUID, action: Literal["publish", "retire", "draft"],
                              actor: CurrentUser = Depends(require("qbank:publish")),
                              session: AsyncSession = Depends(get_session)) -> dict:
    qn = await session.get(Question, qid)
    if qn is None:
        raise NotFound()
    if action == "publish" and qn.author_id == actor.id and not actor.can("role:assign_admin"):
        raise Forbidden("Another person must publish a question you wrote (BR-CNT-03).", code="sod_violation")
    qn.status = {"publish": "published", "retire": "retired", "draft": "draft"}[action]
    if action == "publish":
        qn.published_at, qn.reviewer_id = now_utc(), actor.id
    await audit.record(session, f"question.{qn.status}", actor=actor, target_type="question", target_id=qn.id)
    return q_out(qn)


@router.get("/admin/questions/validate")
async def validate_set(lm_id: UUID, _: CurrentUser = Depends(require("catalog:read_admin")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    """Release checks for an LM's question set (BR-QB-05)."""
    qs = list((await session.scalars(select(Question).where(Question.lm_id == lm_id, Question.status != "retired")
                                     .order_by(Question.created_at))).all())
    n = len(qs)
    counts = {LETTERS[i]: sum(1 for q in qs if q.correct_index == i) for i in range(3)}
    issues = []
    if n:
        for letter, c in counts.items():
            share = c / n * 100
            if not 25 <= share <= 42:
                issues.append(f"Answer {letter} is correct in {share:.0f}% of questions (target 25–42%).")
        run, longest = 1, 1
        for a, b in zip(qs, qs[1:], strict=False):
            run = run + 1 if a.correct_index == b.correct_index else 1
            longest = max(longest, run)
        if longest > 3:
            issues.append(f"{longest} questions in a row have the same answer letter (max 3).")
        seen: dict[str, Question] = {}
        for q in qs:
            key = " ".join(q.stem.lower().split())
            if key in seen:
                issues.append(f"Duplicate stem: “{q.stem[:70]}…”")
            seen[key] = q
    return {"questions": n, "answer_distribution": counts, "issues": issues, "ok": n > 0 and not issues}

