import os

os.environ.update({
    "APP_ENV": "test",
    "DATABASE_URL": os.environ.get("TEST_DATABASE_URL",
                                   "postgresql+asyncpg://cfa_lms:cfa_lms_local@localhost:5432/cfa_lms_test"),
    "PAYMENT_PROVIDER": "mock",
    "OTP_DEBUG_ECHO": "true",
    "STAFF_MFA_REQUIRED": "false",
    "COOKIE_SECURE": "false",
    "STORAGE_DIR": os.path.join(os.path.dirname(__file__), "..", "var", "test-storage"),
})

from datetime import date  # noqa: E402

import httpx  # noqa: E402
import pytest  # noqa: E402
from sqlalchemy import text  # noqa: E402

import app.models  # noqa: E402,F401
from app.core.db import Base, SessionLocal, engine  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.core.timeutil import now_utc  # noqa: E402
from app.main import app  # noqa: E402
from app.modules.catalog.models import LearningModule, Subject  # noqa: E402
from app.modules.commerce.models import Course, CourseSubject  # noqa: E402
from app.modules.content import service as content  # noqa: E402
from app.modules.content.models import ContentItem  # noqa: E402
from app.modules.users.models import User, UserRole  # noqa: E402

STAFF_PW = "Test-Password-123!"


@pytest.fixture(scope="session", autouse=True)
async def schema():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("DROP SEQUENCE IF EXISTS order_number_seq"))
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture(autouse=True)
async def clean():
    async with engine.begin() as conn:
        tables = ", ".join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
async def world():
    """Two subjects, LMs, published notes, one open course covering subject eq only."""
    async with SessionLocal() as s:
        eq = Subject(code="eq", name="Equity Investments", sort_order=1)
        fi = Subject(code="fi", name="Fixed Income", sort_order=2)
        s.add_all([eq, fi])
        await s.flush()
        lm1 = LearningModule(subject_id=eq.id, lm_no=1, title="Equity Instrument Features", status="published",
                             source_ref="R39-SECRET")
        lm2 = LearningModule(subject_id=eq.id, lm_no=2, title="Market Organization", status="published")
        fi1 = LearningModule(subject_id=fi.id, lm_no=1, title="Instrument Features", status="published")
        s.add_all([lm1, lm2, fi1])
        author = User(email="author@t.test", full_name="Author", password_hash=hash_password(STAFF_PW))
        author.roles = [UserRole(role="author", granted_at=now_utc())]
        admin = User(email="admin@t.test", full_name="Admin", password_hash=hash_password(STAFF_PW))
        admin.roles = [UserRole(role="admin", granted_at=now_utc())]
        s.add_all([author, admin])
        await s.flush()
        item = ContentItem(lm_id=lm1.id, title="What is equity?", kind="note")
        s.add(item)
        await s.flush()
        v = await content.save_draft(s, item, {"schema": "notes/v1", "blocks": [
            {"type": "paragraph", "inline": [{"t": "Limited liability caps the loss."}]}]}, author, "original",
            None, None)
        await content.publish(s, item, v.id, admin)
        course = Course(code="EQ-ONLY", title="Equity course", fee_paise=500_00, validity_days=30, status="open")
        course.subjects = [CourseSubject(subject_id=eq.id)]
        s.add(course)
        await s.commit()
        return {"eq": eq.id, "fi": fi.id, "lm1": lm1.id, "lm2": lm2.id, "fi1": fi1.id, "item": item.id,
                "course": course.code}


class Client(httpx.AsyncClient):
    """Test client that adds the CSRF header automatically, like the web app does."""

    async def request(self, method, url, **kw):
        if method.upper() in ("POST", "PUT", "PATCH", "DELETE") and self.cookies.get("csrf_token"):
            kw["headers"] = {"x-csrf-token": self.cookies.get("csrf_token"), **dict(kw.get("headers") or {})}
        return await super().request(method, url, **kw)


def make_client() -> Client:
    return Client(transport=httpx.ASGITransport(app=app), base_url="http://test/api/v1")


@pytest.fixture
async def client():
    async with make_client() as c:
        yield c


async def signup(c: Client, mobile: str, *, dob: date = date(1998, 5, 1), name: str = "Test Student") -> dict:
    r = await c.post("/auth/otp/request", json={"channel": "sms", "destination": mobile})
    assert r.status_code == 200, r.text
    ch = r.json()
    r = await c.post("/auth/otp/verify", json={"challenge_id": ch["challenge_id"], "code": ch["debug_code"],
                                               "channel": "sms", "destination": mobile})
    assert r.status_code == 200, r.text
    tok = r.json()["signup_token"]
    notice = (await c.get("/privacy/notice/current")).json()["version"]
    r = await c.post("/auth/signup", json={"signup_token": tok, "full_name": name, "dob": dob.isoformat(),
                                           "accept_terms": True, "notice_version": notice})
    assert r.status_code == 201, r.text
    return r.json()


async def login_otp(c: Client, mobile: str) -> None:
    ch = (await c.post("/auth/otp/request", json={"channel": "sms", "destination": mobile})).json()
    r = await c.post("/auth/otp/verify", json={"challenge_id": ch["challenge_id"], "code": ch["debug_code"],
                                               "channel": "sms", "destination": mobile})
    assert r.json()["status"] == "signed_in", r.text


async def staff_login(c: Client, email: str) -> None:
    r = await c.post("/auth/staff/login", json={"email": email, "password": STAFF_PW})
    assert r.json()["status"] == "signed_in", r.text


async def pay(c: Client, course: str, outcome: str = "success") -> dict:
    r = await c.post(f"/courses/{course}/register", json={
        "city": "Pune", "qualification": "B.Com", "target_exam": "2027-05", "accept_course_terms": True})
    assert r.status_code == 200, r.text
    reg = r.json()
    poid = reg["checkout"]["url"].split("order_id=")[1].split("&")[0]
    r = await c.post("/payments/mock/complete", json={"provider_order_id": poid, "outcome": outcome})
    assert r.status_code == 200, r.text
    done = r.json()
    if done["checkout_payload"]:
        r = await c.post(f"/payments/orders/{reg['order_id']}/confirm", json={"payload": done["checkout_payload"]})
        assert r.status_code == 200, r.text
    return {**reg, "provider_order_id": poid}
