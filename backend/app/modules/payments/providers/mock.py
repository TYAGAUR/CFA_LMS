"""Mock gateway for local development and tests. It behaves like Razorpay: same
signature scheme, a hosted "checkout" page (frontend /mock-gateway), and signed
webhooks, so the whole order → payment → webhook → access flow can be exercised
without real money. Disabled outside local/test."""

import json
from typing import Any

from app.core.config import get_settings
from app.core.ids import uuid7
from app.core.security import constant_time_equals, hmac_sha256_hex
from app.modules.payments.providers.base import (
    GatewayEvent,
    OrderIntent,
    PaymentInfo,
    ProviderOrder,
    RefundInfo,
)

# In-memory record of mock payments (enough for a dev server / test process).
_PAYMENTS: dict[str, PaymentInfo] = {}


class MockProvider:
    name = "mock"

    def __init__(self) -> None:
        s = get_settings()
        if not s.dev_tools:
            raise RuntimeError("The mock payment provider is only available in local/test or staging demo mode")
        self.secret = s.mock_webhook_secret

    async def create_order(self, intent: OrderIntent) -> ProviderOrder:
        oid = f"mock_order_{uuid7().hex[:20]}"
        return ProviderOrder(oid, {
            "mode": "redirect",
            "url": f"/mock-gateway?order_id={oid}&amount={intent.amount_paise}&ref={intent.order_id}",
        })

    # --- helpers used by the mock gateway endpoints ---
    def simulate(self, provider_order_id: str, amount_paise: int, success: bool) -> tuple[PaymentInfo, dict]:
        pid = f"mock_pay_{uuid7().hex[:20]}"
        info = PaymentInfo(pid, provider_order_id, "captured" if success else "failed", amount_paise,
                           "upi" if success else "card",
                           None if success else "BAD_REQUEST_ERROR",
                           None if success else "Payment declined by the (mock) bank")
        _PAYMENTS[pid] = info
        checkout = {"mock_order_id": provider_order_id, "mock_payment_id": pid,
                    "mock_signature": hmac_sha256_hex(self.secret, f"{provider_order_id}|{pid}")}
        return info, checkout

    def webhook_for(self, info: PaymentInfo) -> tuple[dict[str, str], bytes]:
        body = json.dumps({
            "event": "payment.captured" if info.status == "captured" else "payment.failed",
            "payload": {"payment": {"entity": {
                "id": info.provider_payment_id, "order_id": info.provider_order_id, "status": info.status,
                "amount": info.amount_paise, "method": info.method, "error_code": info.error_code,
                "error_description": info.error_description,
            }}},
        }).encode()
        return {"x-mock-signature": hmac_sha256_hex(self.secret, body),
                "x-mock-event-id": f"evt_{uuid7().hex[:20]}"}, body

    # --- PaymentProvider ---
    def verify_checkout(self, payload: dict[str, Any]) -> tuple[str, str]:
        oid, pid, sig = (payload.get(k, "") for k in ("mock_order_id", "mock_payment_id", "mock_signature"))
        if not (oid and pid and sig) or not constant_time_equals(hmac_sha256_hex(self.secret, f"{oid}|{pid}"), sig):
            raise ValueError("bad signature")
        return oid, pid

    async def fetch_payment(self, provider_payment_id: str) -> PaymentInfo:
        info = _PAYMENTS.get(provider_payment_id)
        if info is None:
            raise ValueError("unknown payment")
        return info

    async def capture(self, provider_payment_id: str, amount_paise: int, currency: str) -> PaymentInfo:
        return await self.fetch_payment(provider_payment_id)

    def verify_webhook(self, headers: dict[str, str], body: bytes) -> bool:
        sig = headers.get("x-mock-signature", "")
        return bool(sig) and constant_time_equals(hmac_sha256_hex(self.secret, body), sig)

    def parse_webhook(self, headers: dict[str, str], body: bytes) -> GatewayEvent:
        data = json.loads(body)
        p = data["payload"]["payment"]["entity"]
        info = PaymentInfo(p["id"], p.get("order_id"), p["status"], int(p["amount"]), p.get("method"),
                           p.get("error_code"), p.get("error_description"))
        typ = "payment.captured" if data["event"] == "payment.captured" else "payment.failed"
        return GatewayEvent(headers.get("x-mock-event-id", p["id"]), typ, data["event"], payment=info)

    async def refund(self, provider_payment_id: str, amount_paise: int, notes: dict[str, str]) -> RefundInfo:
        return RefundInfo(f"mock_rfnd_{uuid7().hex[:16]}", "processed", amount_paise)
