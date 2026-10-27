"""Payment gateway port (A-08 §3). Add a gateway by implementing this protocol and
registering it in `providers/__init__.py`; nothing else in the codebase changes."""

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

EventType = Literal["payment.captured", "payment.failed", "refund.processed", "ignored"]


@dataclass
class OrderIntent:
    order_id: str          # our order UUID (string)
    number: str            # human order number, used as the gateway receipt
    amount_paise: int
    currency: str
    description: str
    customer_name: str
    customer_mobile: str | None
    customer_email: str | None


@dataclass
class ProviderOrder:
    provider_order_id: str
    checkout: dict[str, Any]   # parameters the browser needs to open the gateway's checkout


@dataclass
class PaymentInfo:
    provider_payment_id: str
    provider_order_id: str | None
    status: Literal["captured", "authorized", "failed", "pending"]
    amount_paise: int
    method: str | None = None
    error_code: str | None = None
    error_description: str | None = None


@dataclass
class GatewayEvent:
    event_id: str
    type: EventType
    raw_type: str
    payment: PaymentInfo | None = None
    refund_id: str | None = None
    refund_amount_paise: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RefundInfo:
    provider_refund_id: str
    status: Literal["pending", "processed", "failed"]
    amount_paise: int


class PaymentProvider(Protocol):
    name: str

    async def create_order(self, intent: OrderIntent) -> ProviderOrder: ...

    def verify_checkout(self, payload: dict[str, Any]) -> tuple[str, str]:
        """Verify the browser's success callback. Returns (provider_order_id, provider_payment_id)
        or raises ValueError. A valid signature is NOT proof of capture: always fetch_payment()."""
        ...

    async def fetch_payment(self, provider_payment_id: str) -> PaymentInfo: ...

    async def capture(self, provider_payment_id: str, amount_paise: int, currency: str) -> PaymentInfo: ...

    def verify_webhook(self, headers: dict[str, str], body: bytes) -> bool: ...

    def parse_webhook(self, headers: dict[str, str], body: bytes) -> GatewayEvent: ...

    async def refund(self, provider_payment_id: str, amount_paise: int, notes: dict[str, str]) -> RefundInfo: ...
