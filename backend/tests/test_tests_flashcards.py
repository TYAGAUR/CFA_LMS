import json
from datetime import date, timedelta

import pytest
from sqlalchemy import update

from app.core.db import SessionLocal
from app.core.timeutil import now_utc
from app.modules.flashcards.models import Flashcard
from app.modules.flashcards.service import SrsState, schedule
from app.modules.qbank.models import Question, TestAttempt
from tests.conftest import make_client, pay, signup, staff_login


@pytest.fixture
async def bank(world):
    async with SessionLocal() as s:
        for i in range(12):
            s.add(Question(subject_id=world["eq"], lm_id=world["lm1"], stem=f"Question {i} about equity?",
                           options=[f"A{i}", f"B{i}", f"C{i}"], correct_index=i % 3, explanation=f"Because {i}.",
                           difficulty="EMH"[i % 3], qtype="numerical" if i % 2 else "conceptual",
                           status="published"))
        s.add(Question(subject_id=world["eq"], lm_id=world["lm1"], stem="Draft question not visible?",
                       options=["x", "y", "z"], correct_index=0, explanation="n/a", difficulty="E", status="draft"))
        s.add(Question(subject_id=world["fi"], lm_id=world["fi1"], stem="Fixed income question?",
                       options=["x", "y", "z"], correct_index=0, explanation="n/a", difficulty="E",
                       status="published"))
        for i in range(4):
            s.add(Flashcard(subject_id=world["eq"], front=f"Front {i}", back=f"Back {i}", sort_order=i))
        await s.commit()
    return world


async def _student(c, mobile, world):
    await signup(c, mobile)
    await pay(c, world["course"])


async def test_chapter_quiz_hides_answers_until_submit(client, bank):
    await _student(client, "9611111111", bank)
    lm = (await client.get(f"/lms/{bank['lm1']}")).json()
    assert lm["quiz"]["available"] and lm["quiz"]["size"] == 10 and lm["quiz"]["questions"] == 12
    a = (await client.post(f"/lms/{bank['lm1']}/quiz")).json()
    assert a["total"] == 10 and a["mode"] == "assessment" and a["timed"] and a["time_limit_s"] == 900
    full = (await client.get(f"/attempts/{a['id']}")).json()
    assert "correct_index" not in json.dumps(full) and "explanation" not in json.dumps(full)  # ADR-010
    assert all("Draft" not in it["stem"] for it in full["items"])
    stems = [it["stem"] for it in full["items"]]
    assert len(set(stems)) == 10  # BR-TST-03
    for it in full["items"]:
        r = await client.put(f"/attempts/{a['id']}/items/{it['position']}",
                             json={"answer_index": 0, "time_spent_s": 20})
        assert "correct_index" not in r.json()
    # assessment mode: answers may change before submit
    assert (await client.put(f"/attempts/{a['id']}/items/0", json={"answer_index": 1})).status_code == 200
    res = (await client.post(f"/attempts/{a['id']}/submit")).json()
    assert res["status"] == "submitted" and res["pass_mark"] == 80
    assert all("correct_index" in it and "explanation" in it for it in res["items"])
    assert res["correct"] == sum(1 for it in res["items"] if it["is_correct"])
    assert (await client.put(f"/attempts/{a['id']}/items/0", json={"answer_index": 2})).status_code == 409
    lm = (await client.get(f"/lms/{bank['lm1']}")).json()
    assert lm["quiz"]["attempts"] == 1 and lm["quiz"]["best_pct"] == res["score_pct"]


async def test_retake_prefers_unseen_questions(client, bank):
    await _student(client, "9622222222", bank)
    a1 = (await client.post(f"/lms/{bank['lm1']}/quiz")).json()
    first = {it["stem"] for it in (await client.get(f"/attempts/{a1['id']}")).json()["items"]}
    for it in range(10):
        await client.put(f"/attempts/{a1['id']}/items/{it}", json={"answer_index": 0})
    await client.post(f"/attempts/{a1['id']}/submit")
    a2 = (await client.post(f"/lms/{bank['lm1']}/quiz")).json()
    second = {it["stem"] for it in (await client.get(f"/attempts/{a2['id']}")).json()["items"]}
    assert len(second - first) == 2  # both never-seen questions are included (BR-TST-04)


async def test_custom_test_difficulty_filter_and_practice_feedback(client, bank):
    await _student(client, "9633333333", bank)
    pv = (await client.post("/tests/preview", json={"subject_codes": ["eq"], "difficulty": "H"})).json()
    assert pv["available"] == 4 and pv["by_difficulty"]["H"] == 4
    # Subject outside the paid course contributes nothing
    pv2 = (await client.post("/tests/preview", json={"subject_codes": ["fi"]})).json()
    assert pv2["available"] == 0
    a = (await client.post("/tests", json={"subject_codes": ["eq"], "difficulty": "H", "count": 20,
                                           "mode": "practice", "timed": False})).json()
    assert a["served"] == 4 and a["requested"] == 20  # BR-TST-02: no padding
    items = (await client.get(f"/attempts/{a['id']}")).json()["items"]
    assert all(it["difficulty"] == "H" for it in items)
    r = (await client.put(f"/attempts/{a['id']}/items/0", json={"answer_index": 1})).json()
    assert "correct_index" in r and "explanation" in r  # practice shows feedback straight away
    assert (await client.put(f"/attempts/{a['id']}/items/0", json={"answer_index": 2})).status_code == 409
    stats_before = (await client.get("/me/test-stats")).json()
    assert stats_before["answered"] == 0
    await client.post(f"/attempts/{a['id']}/submit")
    stats = (await client.get("/me/test-stats")).json()
    assert stats["answered"] == 1 and stats["by_subject"][0]["code"] == "eq"


async def test_timed_test_auto_submits_after_deadline(client, bank):
    await _student(client, "9644444444", bank)
    a = (await client.post("/tests", json={"subject_codes": ["eq"], "count": 3, "mode": "assessment",
                                           "timed": True})).json()
    assert a["time_limit_s"] == 270
    async with SessionLocal() as s:
        await s.execute(update(TestAttempt).where(TestAttempt.id == a["id"])
                        .values(deadline_at=now_utc() - timedelta(seconds=1)))
        await s.commit()
    r = await client.put(f"/attempts/{a['id']}/items/0", json={"answer_index": 0})
    assert r.status_code == 409
    got = (await client.get(f"/attempts/{a['id']}")).json()
    assert got["status"] == "submitted" and got["submit_reason"] == "timeout" and got["score_pct"] == 0


async def test_cannot_open_other_students_attempt(bank):
    async with make_client() as a, make_client() as b:
        await _student(a, "9655555555", bank)
        await signup(b, "9666666666")
        att = (await a.post(f"/lms/{bank['lm1']}/quiz")).json()
        assert (await b.get(f"/attempts/{att['id']}")).status_code == 404


async def test_quiz_requires_entitlement(client, bank):
    await signup(client, "9677777777")
    assert (await client.post(f"/lms/{bank['lm1']}/quiz")).status_code == 403


def test_srs_schedule():
    today = date(2026, 11, 1)
    s, due = schedule(SrsState(), "known", today)
    assert (s.interval_days, due) == (1, date(2026, 11, 2))
    s, _ = schedule(s, "known", today)
    assert s.interval_days == 3
    s, _ = schedule(s, "known", today)
    assert s.interval_days == round(3 * 2.5)
    s2, due2 = schedule(s, "difficult", today)
    assert s2.interval_days == 1 and s2.reps == 0 and s2.lapses == 1 and abs(s2.ease - 2.3) < 1e-9
    s3, _ = schedule(SrsState(interval_days=10, ease=1.35), "needs_revision", today)
    assert s3.interval_days == 12 and s3.ease == 1.3  # ease floor (BR-FC-03)


async def test_flashcard_session_and_review(client, bank):
    await _student(client, "9688888888", bank)
    decks = (await client.get("/flashcards/decks")).json()
    eq = next(d for d in decks if d["code"] == "eq")
    assert eq["total"] == 4 and eq["new"] == 4 and eq["due"] == 0
    sess = (await client.get("/flashcards/session?subject=eq")).json()
    assert len(sess["cards"]) == 4
    first = sess["cards"][0]["id"]
    r = (await client.post(f"/flashcards/{first}/review", json={"rating": "known"})).json()
    assert r["interval_days"] == 1
    sess2 = (await client.get("/flashcards/session?subject=eq")).json()
    assert first not in [c["id"] for c in sess2["cards"]]  # not due until tomorrow
    assert sess2["counts"] == {"due": 0, "new": 3, "later": 1}
    assert (await client.get("/flashcards/session?subject=fi")).status_code == 403


async def test_question_bank_sod_and_validation(world):
    async with make_client() as author, make_client() as admin:
        await staff_login(author, "author@t.test")
        body = {"subject_code": "eq", "lm_id": str(world["lm2"]), "stem": "Which order guarantees execution?",
                "options": ["Market", "Limit", "Stop"], "correct_index": 0, "explanation": "Market orders execute.",
                "difficulty": "E"}
        q = (await author.post("/admin/questions", json=body)).json()
        assert q["status"] == "draft"
        assert (await author.post(f"/admin/questions/{q['id']}/publish")).status_code == 403  # no qbank:publish
        bad = {**body, "options": ["Same", "same", "Other"]}
        assert (await author.post("/admin/questions", json=bad)).status_code == 422
        await staff_login(admin, "admin@t.test")
        assert (await admin.post(f"/admin/questions/{q['id']}/publish")).json()["status"] == "published"
        v = (await admin.get(f"/admin/questions/validate?lm_id={world['lm2']}")).json()
        assert v["questions"] == 1 and v["answer_distribution"]["A"] == 1 and not v["ok"]
