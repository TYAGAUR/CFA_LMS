from functools import lru_cache

from app.core.config import get_settings
from app.modules.payments.providers.base import PaymentProvider


@lru_cache
def get_provider(name: str | None = None) -> PaymentProvider:
    name = name or get_settings().payment_provider
    if name == "razorpay":
        from app.modules.payments.providers.razorpay import RazorpayProvider
        return RazorpayProvider()
    if name == "mock":
        from app.modules.payments.providers.mock import MockProvider
        return MockProvider()
    raise ValueError(f"Unknown payment provider {name}")
