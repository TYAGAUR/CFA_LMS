import json

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.security import hmac_sha256_hex
from app.modules.payments.models import Order
from app.modules.payments.providers.mock import MockProvider
from app.modules.progress.service import covered_seconds, merge_intervals
from tests.conftest import make_client, pay, signup, staff_login


async def test_not_entitled_before_payment(client, world):
    await signup(client, "9711111111")
    r = await client.get(f"/lms/{world['lm1']}")
    assert r.status_code == 403 and r.json()["code"] == "not_entitled"
    subj = (await client.get("/subjects/eq")).json()
    assert subj["entitled"] is False and subj["courses"][0]["code"] == "EQ-ONLY"  # outline + how to buy


async def test_paid_registration_opens_every_lm(client, world):
    await signup(client, "9722222222")
    reg = await pay(client, world["course"])
    order = (await client.get(f"/payments/orders/{reg['order_id']}")).json()
    assert order["status"] == "paid" and order["payments"][0]["status"] == "captured"
    regs = (await client.get("/me/registrations")).json()
    assert regs[0]["status"] == "active"
    # No chapter locking: LM2 opens without touching LM1 (BR-OPN-01)
    lm2 = await client.get(f"/lms/{world['lm2']}")
    assert lm2.status_code == 200
    lm1 = (await client.get(f"/lms/{world['lm1']}")).json()
    assert "source_ref" not in json.dumps(lm1) and "R39-SECRET" not in json.dumps(lm1)  # BR-CAT-03
    body = (await client.get(f"/content/{world['item']}")).json()
    assert body["body"]["blocks"][0]["type"] == "paragraph"
    # Subject not in the course stays closed
    assert (await client.get(f"/lms/{world['fi1']}")).status_code == 403


async def test_failed_payment_grants_nothing_and_can_retry(client, world):
    await signup(client, "9733333333")
    reg = await pay(client, world["course"], outcome="failure")
    assert (await client.get(f"/payments/orders/{reg['order_id']}")).json()["status"] == "created"
    assert (await client.get(f"/lms/{world['lm1']}")).status_code == 403
    again = await pay(client, world["course"])
    assert again["order_id"] == reg["order_id"]  # open order reused (BR-PAY-03)
    assert (await client.get(f"/lms/{world['lm1']}")).status_code == 200


async def test_cannot_register_twice(client, world):
    await signup(client, "9744444444")
    await pay(client, world["course"])
    r = await client.post(f"/courses/{world['course']}/register", json={
        "city": "Pune", "qualification": "B.Com", "target_exam": "2027-05", "accept_course_terms": True})
    assert r.status_code == 409 and r.json()["code"] == "already_registered"


async def test_webhook_signature_and_idempotency(client, world):
    await signup(client, "9755555555")
    r = await client.post(f"/courses/{world['course']}/register", json={
        "city": "Pune", "qualification": "B.Com", "target_exam": "2027-05", "accept_course_terms": True})
    poid = r.json()["checkout"]["url"].split("order_id=")[1].split("&")[0]
    mock = MockProvider()
    info, _ = mock.simulate(poid, 500_00, True)
    headers, body = mock.webhook_for(info)
    async with make_client() as gw:
        bad = await gw.post("/payments/webhooks/mock", content=body, headers={**headers, "x-mock-signature": "x"})
        assert bad.status_code == 400
        first = await gw.post("/payments/webhooks/mock", content=body, headers=headers)
        assert first.json()["status"] == "processed"
        again = await gw.post("/payments/webhooks/mock", content=body, headers=headers)
        assert again.json()["status"] == "duplicate"
    async with SessionLocal() as s:
        orders = (await s.scalars(select(Order))).all()
    assert len(orders) == 1 and orders[0].status == "paid"


async def test_amount_mismatch_blocks_access(client, world):
    await signup(client, "9766666666")
    r = await client.post(f"/courses/{world['course']}/register", json={
        "city": "Pune", "qualification": "B.Com", "target_exam": "2027-05", "accept_course_terms": True})
    poid = r.json()["checkout"]["url"].split("order_id=")[1].split("&")[0]
    mock = MockProvider()
    info, _ = mock.simulate(poid, 1_00, True)  # captured ₹1 instead of ₹500
    headers, body = mock.webhook_for(info)
    await client.post("/payments/webhooks/mock", content=body, headers=headers)
    async with SessionLocal() as s:
        assert (await s.scalar(select(Order.status))) == "amount_mismatch"
    assert (await client.get(f"/lms/{world['lm1']}")).status_code == 403


async def test_full_refund_revokes_access(client, world):
    await signup(client, "9777777777")
    reg = await pay(client, world["course"])
    async with make_client() as admin:
        await staff_login(admin, "admin@t.test")
        r = await admin.post(f"/admin/orders/{reg['order_id']}/refund", json={"reason": "Student request"})
        assert r.status_code == 200, r.text
    assert (await client.get(f"/lms/{world['lm1']}")).status_code == 403
    assert (await client.get("/me/registrations")).json()[0]["status"] == "cancelled"


async def test_offline_registration_by_admin(world):
    async with make_client() as student:
        await signup(student, "9788888888")
        async with make_client() as admin:
            await staff_login(admin, "admin@t.test")
            r = await admin.post("/admin/registrations/offline", json={
                "mobile": "9788888888", "course_code": world["course"], "reference": "NEFT-123"})
            assert r.status_code == 201, r.text
        assert (await student.get(f"/lms/{world['lm1']}")).status_code == 200


def test_razorpay_signatures():
    from app.core.config import get_settings
    from app.modules.payments.providers.razorpay import RazorpayProvider

    s = get_settings()
    s.razorpay_key_id, s.razorpay_key_secret, s.razorpay_webhook_secret = "rzp_test_x", "secret", "whsec"
    p = RazorpayProvider()
    sig = hmac_sha256_hex("secret", "order_1|pay_1")
    assert p.verify_checkout({"razorpay_order_id": "order_1", "razorpay_payment_id": "pay_1",
                              "razorpay_signature": sig}) == ("order_1", "pay_1")
    try:
        p.verify_checkout({"razorpay_order_id": "order_1", "razorpay_payment_id": "pay_1",
                           "razorpay_signature": "nope"})
        raise AssertionError("bad signature accepted")
    except ValueError:
        pass
    body = json.dumps({"event": "payment.captured", "payload": {"payment": {"entity": {
        "id": "pay_1", "order_id": "order_1", "status": "captured", "amount": 50000, "method": "upi"}}}}).encode()
    headers = {"x-razorpay-signature": hmac_sha256_hex("whsec", body), "x-razorpay-event-id": "evt_1"}
    assert p.verify_webhook(headers, body)
    ev = p.parse_webhook(headers, body)
    assert ev.type == "payment.captured" and ev.payment.amount_paise == 50000 and ev.event_id == "evt_1"


def test_interval_merge():
    iv = merge_intervals([], [0, 15])
    iv = merge_intervals(iv, [10, 30])
    iv = merge_intervals(iv, [100, 115])
    assert iv == [[0, 30], [100, 115]] and covered_seconds(iv) == 45


async def test_progress_revision_and_learned(client, world):
    await signup(client, "9799999999")
    await pay(client, world["course"])
    r = await client.post(f"/lms/{world['lm1']}/revisions", json={"activity": "notes"})
    assert r.json() == {"counted": True, "revision_count": 1}
    r = await client.post(f"/lms/{world['lm1']}/revisions", json={"activity": "flashcards"})
    assert r.json() == {"counted": False, "revision_count": 1}  # one per IST day (BR-REV-02)
    r = await client.post(f"/lms/{world['lm2']}/learned")
    assert r.json()["learned"] is True
    r = await client.delete(f"/lms/{world['lm2']}/learned")
    assert r.json()["learned"] is False
    r = await client.put(f"/lms/{world['lm1']}/eoc", json={"attempted": True, "q_attempted": 10, "q_correct": 12})
    assert r.status_code == 422
    dash = (await client.get("/me/dashboard")).json()
    assert dash["next_action"]["type"] in ("continue", "mark_learned")
