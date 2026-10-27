from datetime import date

from app.core.db import SessionLocal
from app.modules.audit import service as audit
from tests.conftest import login_otp, make_client, signup, staff_login


async def test_signup_creates_active_adult_with_consents(client):
    u = await signup(client, "9811111111")
    assert u["status"] == "active" and u["role_names"] == ["student"] and u["student_code"].startswith("KS")
    me = (await client.get("/me")).json()
    assert me["mobile_e164"] == "+919811111111"
    consents = (await client.get("/me/consents")).json()["consents"]
    assert consents["service_delivery"]["granted"] is True
    assert consents["product_analytics"]["granted"] is False  # optional purposes default off (C-03)


async def test_wrong_otp_counts_attempts_and_locks(client):
    ch = (await client.post("/auth/otp/request", json={"channel": "sms", "destination": "9822222222"})).json()
    for _ in range(5):
        r = await client.post("/auth/otp/verify", json={"challenge_id": ch["challenge_id"], "code": "000000",
                                                        "channel": "sms", "destination": "9822222222"})
        assert r.status_code == 422
    r = await client.post("/auth/otp/verify", json={"challenge_id": ch["challenge_id"], "code": ch["debug_code"],
                                                    "channel": "sms", "destination": "9822222222"})
    assert r.json()["code"] == "otp_locked"


async def test_otp_request_rate_limited(client):
    for _ in range(5):
        assert (await client.post("/auth/otp/request", json={"destination": "9833333333"})).status_code == 200
    assert (await client.post("/auth/otp/request", json={"destination": "9833333333"})).status_code == 429


async def test_invalid_mobile_rejected(client):
    r = await client.post("/auth/otp/request", json={"destination": "12345"})
    assert r.status_code == 422 and r.json()["code"] == "invalid_mobile"


async def test_minor_needs_guardian_consent(client, world):
    u = await signup(client, "9844444444", dob=date(2010, 1, 1))
    assert u["status"] == "pending_guardian_consent" and u["is_minor"] is True
    r = await client.get("/me/dashboard")
    assert r.status_code == 403 and r.json()["code"] == "guardian_consent_required"
    r = await client.post("/me/guardian", json={"full_name": "Parent", "mobile": "9855555555", "relation": "parent"})
    assert r.status_code == 200, r.text
    token = r.json()["debug_link"].rsplit("/", 1)[1]
    async with make_client() as guardian:
        view = (await guardian.get(f"/guardian-consent/{token}")).json()
        assert view["student_first_name"] == "Test"
        ch = (await guardian.post(f"/guardian-consent/{token}/otp")).json()
        r = await guardian.post(f"/guardian-consent/{token}", json={
            "challenge_id": ch["challenge_id"], "code": ch["debug_code"], "accept": True})
        assert r.status_code == 200, r.text
    assert (await client.get("/me")).json()["status"] == "active"
    # Analytics consent is not available to minors (C-01 PR-2)
    r = await client.post("/me/consents", json={"purpose": "product_analytics", "granted": True})
    assert r.status_code == 403


async def test_csrf_required_for_cookie_requests(client):
    await signup(client, "9866666666")
    r = await client.patch("/me", json={"city": "Delhi"}, headers={"x-csrf-token": "wrong"})
    assert r.status_code == 403 and r.json()["code"] == "csrf_failed"


async def test_session_limit_evicts_oldest(world):
    async with make_client() as a:
        await signup(a, "9877777777")
        async with make_client() as b, make_client() as c:
            await login_otp(b, "9877777777")
            await login_otp(c, "9877777777")  # third device
            assert (await c.get("/me")).status_code == 200
            assert (await a.get("/me")).status_code == 401  # oldest ended (BR-ACC-05)


async def test_refresh_rotation_and_reuse_detection(client):
    await signup(client, "9888888888")
    old = client.cookies.get("refresh_token")
    r = await client.post("/auth/refresh")
    assert r.status_code == 200
    async with make_client() as attacker:
        attacker.cookies.set("refresh_token", old, path="/api/v1/auth")
        assert (await attacker.post("/auth/refresh")).status_code == 401
    # the replay revoked the session
    assert (await client.post("/auth/refresh")).status_code == 401


async def test_staff_login_and_rbac(client, world):
    await staff_login(client, "author@t.test")
    assert (await client.get("/admin/catalog")).status_code == 200
    assert (await client.get("/admin/users")).status_code == 403
    assert (await client.post("/admin/courses", json={})).status_code in (403, 422)


async def test_student_cannot_use_admin_api(client, world):
    await signup(client, "9899999999")
    for path in ("/admin/users", "/admin/orders", "/admin/audit", "/admin/catalog"):
        assert (await client.get(path)).status_code == 403, path


async def test_staff_lockout_after_failed_passwords(client, world):
    for _ in range(5):
        await client.post("/auth/staff/login", json={"email": "admin@t.test", "password": "wrong-password"})
    r = await client.post("/auth/staff/login", json={"email": "admin@t.test", "password": "Test-Password-123!"})
    assert r.json()["code"] == "account_locked"


async def test_data_export_and_audit_chain(client):
    await signup(client, "9700000001")
    data = (await client.get("/me/data-export")).json()
    assert data["profile"]["mobile_e164"] == "+919700000001"
    assert "password_hash" not in data["profile"]
    async with SessionLocal() as s:
        ok, n = await audit.verify_chain(s)
    assert ok and n >= 3
