"""Razorpay adapter (Orders API + Standard Checkout + webhooks).

Docs: https://razorpay.com/docs/api/orders/ · https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/
- Checkout signature  = HMAC_SHA256(order_id + "|" + payment_id, key_secret)
- Webhook signature   = HMAC_SHA256(raw_body, webhook_secret) in header X-Razorpay-Signature
- Event id            = header X-Razorpay-Event-Id (used for idempotency)
"""

import json
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.security import constant_time_equals, hmac_sha256_hex
from app.modules.payments.providers.base import (
    GatewayEvent,
    OrderIntent,
    PaymentInfo,
    ProviderOrder,
    RefundInfo,
)

API = "https://api.razorpay.com/v1"


class RazorpayProvider:
    name = "razorpay"

    def __init__(self) -> None:
        s = get_settings()
        if not (s.razorpay_key_id and s.razorpay_key_secret):
            raise RuntimeError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set when PAYMENT_PROVIDER=razorpay")
        self.key_id, self.key_secret, self.webhook_secret = s.razorpay_key_id, s.razorpay_key_secret, \
            s.razorpay_webhook_secret

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=API, auth=(self.key_id, self.key_secret), timeout=15)

    async def create_order(self, intent: OrderIntent) -> ProviderOrder:
        async with self._client() as c:
            r = await c.post("/orders", json={
                "amount": intent.amount_paise, "currency": intent.currency, "receipt": intent.number,
                "notes": {"order_id": intent.order_id},
            })
            r.raise_for_status()
            data = r.json()
        return ProviderOrder(data["id"], {
            "mode": "razorpay_checkout",
            "script": "https://checkout.razorpay.com/v1/checkout.js",
            "options": {
                "key": self.key_id, "order_id": data["id"], "amount": intent.amount_paise,
                "currency": intent.currency, "name": "Karan Sir Classes", "description": intent.description,
                "prefill": {"name": intent.customer_name, "email": intent.customer_email or "",
                            "contact": intent.customer_mobile or ""},
                "notes": {"order_number": intent.number},
                "theme": {"color": "#211C84"},
            },
        })

    def verify_checkout(self, payload: dict[str, Any]) -> tuple[str, str]:
        oid, pid, sig = (payload.get(k, "") for k in ("razorpay_order_id", "razorpay_payment_id",
                                                       "razorpay_signature"))
        if not (oid and pid and sig):
            raise ValueError("missing fields")
        if not constant_time_equals(hmac_sha256_hex(self.key_secret, f"{oid}|{pid}"), sig):
            raise ValueError("bad signature")
        return oid, pid

    @staticmethod
    def _info(p: dict[str, Any]) -> PaymentInfo:
        status = {"captured": "captured", "authorized": "authorized", "failed": "failed"}.get(p.get("status"),
                                                                                             "pending")
        return PaymentInfo(p["id"], p.get("order_id"), status, int(p.get("amount", 0)), p.get("method"),
                           p.get("error_code"), p.get("error_description"))

    async def fetch_payment(self, provider_payment_id: str) -> PaymentInfo:
        async with self._client() as c:
            r = await c.get(f"/payments/{provider_payment_id}")
            r.raise_for_status()
            return self._info(r.json())

    async def capture(self, provider_payment_id: str, amount_paise: int, currency: str) -> PaymentInfo:
        async with self._client() as c:
            r = await c.post(f"/payments/{provider_payment_id}/capture",
                             json={"amount": amount_paise, "currency": currency})
            r.raise_for_status()
            return self._info(r.json())

    def verify_webhook(self, headers: dict[str, str], body: bytes) -> bool:
        sig = headers.get("x-razorpay-signature", "")
        return bool(self.webhook_secret and sig) and constant_time_equals(
            hmac_sha256_hex(self.webhook_secret, body), sig)

    def parse_webhook(self, headers: dict[str, str], body: bytes) -> GatewayEvent:
        data = json.loads(body)
        raw_type = data.get("event", "")
        event_id = headers.get("x-razorpay-event-id") or f"{raw_type}:{data.get('created_at')}"
        payload = data.get("payload", {})
        if raw_type in ("payment.captured", "payment.failed", "order.paid"):
            p = payload.get("payment", {}).get("entity", {})
            info = self._info(p)
            typ = "payment.failed" if raw_type == "payment.failed" else "payment.captured"
            return GatewayEvent(event_id, typ, raw_type, payment=info)
        if raw_type == "refund.processed":
            rf = payload.get("refund", {}).get("entity", {})
            return GatewayEvent(event_id, "refund.processed", raw_type, refund_id=rf.get("id"),
                                refund_amount_paise=int(rf.get("amount", 0)),
                                extra={"payment_id": rf.get("payment_id")})
        return GatewayEvent(event_id, "ignored", raw_type)

    async def refund(self, provider_payment_id: str, amount_paise: int, notes: dict[str, str]) -> RefundInfo:
        async with self._client() as c:
            r = await c.post(f"/payments/{provider_payment_id}/refund",
                             json={"amount": amount_paise, "speed": "normal", "notes": notes})
            r.raise_for_status()
            d = r.json()
        return RefundInfo(d["id"], "processed" if d.get("status") == "processed" else "pending",
                          int(d.get("amount", amount_paise)))
