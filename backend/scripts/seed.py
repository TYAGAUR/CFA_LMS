"""Seed local/staging data from seed/*.json (prototype content) plus demo accounts and courses.

Idempotent: safe to run repeatedly.   uv run python scripts/seed.py
Never run against production (refuses unless APP_ENV is local/test/staging).
"""

import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

import app.models  # noqa: E402,F401
import app.modules.commerce.service  # noqa: E402,F401  (event subscribers)
from app.core.config import REPO_DIR, get_settings  # noqa: E402
from app.core.db import SessionLocal  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.core.timeutil import now_utc  # noqa: E402
from app.modules.catalog.models import LearningModule, Subject, Topic  # noqa: E402
from app.modules.commerce import service as commerce  # noqa: E402
from app.modules.commerce.models import Course, CourseSubject  # noqa: E402
from app.modules.content import service as content  # noqa: E402
from app.modules.content.models import ContentItem  # noqa: E402
from app.modules.enrolment.models import Batch  # noqa: E402
from app.modules.flashcards.models import Flashcard  # noqa: E402
from app.modules.privacy import service as privacy  # noqa: E402
from app.modules.qbank.models import Question  # noqa: E402
from app.modules.users.models import User, UserRole  # noqa: E402

SEED = REPO_DIR / "seed"
WEIGHTS = {"eth": "15–20%", "qm": "6–9%", "ec": "6–9%", "cf": "6–9%", "fsa": "11–14%", "eq": "11–14%",
           "fi": "11–14%", "dv": "5–8%", "ai": "7–10%", "pm": "8–12%"}
STAFF_PASSWORD = "LocalDev#2026!"
STAFF = [("super@local.test", "Super Admin", ["super_admin"]), ("admin@local.test", "Ops Admin", ["admin"]),
         ("author@local.test", "Karan Singh, CFA", ["author"]), ("reviewer@local.test", "Academic Reviewer",
                                                                 ["reviewer"])]
DEMO_STUDENT = ("+919876543210", "Aarav Mehta")


async def seed_catalog(session) -> dict[str, Subject]:
    subjects = json.loads((SEED / "subjects.json").read_text(encoding="utf-8"))
    out = {}
    for i, s in enumerate(subjects):
        subj = await session.scalar(select(Subject).where(Subject.code == s["code"]))
        if subj is None:
            subj = Subject(code=s["code"], name=s["name"], icon=s["icon"], sort_order=i, status="published",
                           exam_weight=WEIGHTS.get(s["code"]))
            session.add(subj)
            await session.flush()
        for n, title in enumerate(s["lms"], start=1):
            lm = await session.scalar(select(LearningModule).where(LearningModule.subject_id == subj.id,
                                                                   LearningModule.lm_no == n))
            if lm is None:
                session.add(LearningModule(subject_id=subj.id, lm_no=n, title=title, status="published",
                                           published_at=now_utc()))
        out[s["code"]] = subj
    await session.flush()
    return out


async def seed_notes(session, subjects: dict[str, Subject], author: User) -> int:
    notes = json.loads((SEED / "notes.json").read_text(encoding="utf-8"))
    created = 0
    for n in notes:
        subj = subjects[n["subject"]]
        lm = await session.scalar(select(LearningModule).where(LearningModule.subject_id == subj.id,
                                                               LearningModule.lm_no == n["lm_index"] + 1))
        if await session.scalar(select(ContentItem.id).where(ContentItem.lm_id == lm.id)):
            continue
        items = [(t["title"], "note", t["body"]) for t in n["topics"]]
        if "infographic" in n["extra"]:
            items.append(("Infographic · Who gets paid first?", "infographic", n["extra"]["infographic"]))
        if "revision_sheet" in n["extra"]:
            items.append(("Revision sheet", "revision_sheet", n["extra"]["revision_sheet"]))
        for order, (title, kind, body) in enumerate(items):
            topic = None
            if kind == "note":
                topic = Topic(lm_id=lm.id, title=title, sort_order=order)
                session.add(topic)
                await session.flush()
            item = ContentItem(lm_id=lm.id, topic_id=topic.id if topic else None, kind=kind, title=title,
                               sort_order=order)
            session.add(item)
            await session.flush()
            v = await content.save_draft(session, item, body, author, "original", None, "Imported from prototype")
            await content.publish(session, item, v.id, author)
            created += 1
    return created


NUMERIC = re.compile(r"₹|\d+(?:\.\d+)?%|\d[\d,]{2,}")


async def seed_questions(session, subjects: dict[str, Subject], author: User, reviewer: User) -> int:
    """Prototype MCQs → question bank (published). `c` is the 0-based chapter index (BR-QB-06 qtype inferred)."""
    data = json.loads((SEED / "questions.json").read_text(encoding="utf-8"))
    n = 0
    for q in data:
        ref = f"proto-{q['id']}"
        if await session.scalar(select(Question.id).where(Question.source_ref == ref)):
            continue
        subj = subjects[q["s"]]
        lm = await session.scalar(select(LearningModule).where(LearningModule.subject_id == subj.id,
                                                               LearningModule.lm_no == q["c"] + 1))
        session.add(Question(
            subject_id=subj.id, lm_id=lm.id if lm else None, stem=q["q"], options=q["o"], correct_index=q["a"],
            explanation=q["e"], difficulty=q["d"], qtype="numerical" if NUMERIC.search(q["q"]) else "conceptual",
            status="published", provenance="original", source_ref=ref, author_id=author.id,
            reviewer_id=reviewer.id, published_at=now_utc()))
        n += 1
    return n


async def seed_flashcards(session, subjects: dict[str, Subject], author: User) -> int:
    data = json.loads((SEED / "flashcards.json").read_text(encoding="utf-8"))
    n = 0
    for code, cards in data.items():
        for i, c in enumerate(cards):
            ref = f"proto-{code}-{i}"
            if await session.scalar(select(Flashcard.id).where(Flashcard.source_ref == ref)):
                continue
            session.add(Flashcard(subject_id=subjects[code].id, front=c["front"], back=c["back"], sort_order=i,
                                  status="published", source_ref=ref, created_by=author.id))
            n += 1
    return n


async def seed_staff(session) -> dict[str, User]:
    out = {}
    for email, name, roles in STAFF:
        u = await session.scalar(select(User).where(User.email == email))
        if u is None:
            u = User(email=email, full_name=name, password_hash=hash_password(STAFF_PASSWORD), status="active")
            u.roles = [UserRole(role=r, granted_at=now_utc()) for r in roles]
            session.add(u)
            await session.flush()
        out[email] = u
    return out


async def seed_courses(session, subjects: dict[str, Subject]) -> dict[str, Course]:
    batch = await session.scalar(select(Batch).where(Batch.code == "KSC-27"))
    if batch is None:
        batch = Batch(code="KSC-27", name="CFA Level I · May 2027", exam_window="2027-05",
                      starts_on=date(2026, 11, 1), ends_on=date(2027, 5, 31))
        session.add(batch)
        await session.flush()
    specs = [
        dict(code="CFA-L1-MAY27", title="CFA Level I · Complete Course (May 2027)",
             tagline="All 10 subjects: class videos, notes, revision sheets and progress tracking.",
             description="Structured preparation for the May 2027 CFA Level I window with Karan Singh, CFA. "
                         "Access runs until 31 May 2027.",
             fee_paise=44_999_00, access_ends_on=date(2027, 5, 31), batch_id=batch.id, exam_window="2027-05",
             status="open", sort_order=0, subjects=list(subjects)),
        dict(code="CFA-L1-EQFI", title="Equity & Fixed Income · Focus Module",
             tagline="Two high-weight subjects in depth, 180 days of access.",
             description="For candidates who want extra depth in Equity Investments and Fixed Income.",
             fee_paise=9_999_00, validity_days=180, status="open", sort_order=1, subjects=["eq", "fi"]),
    ]
    out = {}
    for spec in specs:
        codes = spec.pop("subjects")
        c = await session.scalar(select(Course).where(Course.code == spec["code"]))
        if c is None:
            c = Course(**spec)
            c.subjects = [CourseSubject(subject_id=subjects[k].id) for k in codes]
            session.add(c)
            await session.flush()
        out[c.code] = c
    return out


async def seed_demo_student(session, courses: dict[str, Course], admin: User) -> User:
    mobile, name = DEMO_STUDENT
    u = await session.scalar(select(User).where(User.mobile_e164 == mobile))
    if u is None:
        u = User(mobile_e164=mobile, full_name=name, dob=date(2000, 4, 12), student_code="KS26-00001",
                 city="Mumbai", qualification="B.Com", target_exam="2027-05", status="active")
        u.roles = [UserRole(role="student", granted_at=now_utc())]
        session.add(u)
        await session.flush()
        await privacy.record_consent(session, u, "service_delivery", True)
        await commerce.register_offline(session, user=u, course=courses["CFA-L1-MAY27"], reference="SEED-DEMO",
                                        amount_paise=None, actor=admin)
    return u


async def main() -> None:
    s = get_settings()
    if s.app_env not in ("local", "test", "staging"):
        raise SystemExit("Refusing to seed outside local/test/staging")
    global STAFF_PASSWORD
    if s.seed_staff_password:
        STAFF_PASSWORD = s.seed_staff_password
    elif not s.is_dev:
        raise SystemExit("Set SEED_STAFF_PASSWORD to seed staff accounts outside local/test")
    async with SessionLocal() as session:
        subjects = await seed_catalog(session)
        staff = await seed_staff(session)
        notes = await seed_notes(session, subjects, staff["author@local.test"])
        questions = await seed_questions(session, subjects, staff["author@local.test"], staff["reviewer@local.test"])
        cards = await seed_flashcards(session, subjects, staff["author@local.test"])
        courses = await seed_courses(session, subjects)
        await seed_demo_student(session, courses, staff["admin@local.test"])
        await session.commit()
    personas = {
        "staff_password": STAFF_PASSWORD if s.is_dev else "(SEED_STAFF_PASSWORD)",
        "staff": [{"email": e, "roles": r} for e, _, r in STAFF],
        "demo_student_mobile": DEMO_STUDENT[0][3:],
        "note": "Local only. OTP codes are printed in the API console and shown on screen (OTP_DEBUG_ECHO).",
    }
    (SEED / "personas.json").write_text(json.dumps(personas, indent=2), encoding="utf-8")
    print(f"Seeded: {len(subjects)} subjects, {notes} new note items, {questions} new questions, "
          f"{cards} new flashcards, {len(courses)} courses, {len(staff)} staff.")
    pw = STAFF_PASSWORD if s.is_dev else "(SEED_STAFF_PASSWORD)"
    print(f"Staff logins: {', '.join(e for e, _, _ in STAFF)} / password {pw}")
    print(f"Demo student mobile: {DEMO_STUDENT[0][3:]} (registered for CFA-L1-MAY27)")


if __name__ == "__main__":
    asyncio.run(main())
