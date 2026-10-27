"""Provider-neutral payment records (A-08). This module knows nothing about courses:
an order has a `purpose` and a `reference_id` owned by the calling module."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin

order_number_seq = Sequence("order_number_seq", start=1001, metadata=Base.metadata)

# order.status
CREATED = "created"
PAID = "paid"
FAILED = "failed"
EXPIRED = "expired"
REFUNDED = "refunded"
PARTIALLY_REFUNDED = "partially_refunded"
AMOUNT_MISMATCH = "amount_mismatch"


class Order(IdMixin, TimestampMixin, Base):
    __tablename__ = "orders"

    number: Mapped[str] = mapped_column(String(30), unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    purpose: Mapped[str] = mapped_column(String(40))
    reference_id: Mapped[UUID] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(String(200))
    amount_paise: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    status: Mapped[str] = mapped_column(String(20), default=CREATED, index=True)
    provider: Mapped[str] = mapped_column(String(20))
    provider_order_id: Mapped[str | None] = mapped_column(String(80), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    refunded_paise: Mapped[int] = mapped_column(Integer, default=0)
    offline_reference: Mapped[str | None] = mapped_column(String(120))
    notes: Mapped[dict] = mapped_column(JSONB, default=dict)


class Payment(IdMixin, TimestampMixin, Base):
    __tablename__ = "payments"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(20))
    provider_payment_id: Mapped[str] = mapped_column(String(80), unique=True)
    status: Mapped[str] = mapped_column(String(20))  # captured | failed | authorized
    amount_paise: Mapped[int] = mapped_column(Integer)
    method: Mapped[str | None] = mapped_column(String(30))
    error_code: Mapped[str | None] = mapped_column(String(80))
    error_description: Mapped[str | None] = mapped_column(Text)
    captured_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PaymentEvent(IdMixin, Base):
    """Webhook inbox. The unique (provider, event_id) makes processing idempotent (BR-PAY-05)."""

    __tablename__ = "payment_events"
    __table_args__ = (UniqueConstraint("provider", "event_id"),)

    provider: Mapped[str] = mapped_column(String(20))
    event_id: Mapped[str] = mapped_column(String(120))
    event_type: Mapped[str] = mapped_column(String(60))
    payload: Mapped[dict] = mapped_column(JSONB)
    signature_valid: Mapped[bool] = mapped_column(Boolean)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error: Mapped[str | None] = mapped_column(Text)


class Refund(IdMixin, TimestampMixin, Base):
    __tablename__ = "refunds"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    payment_id: Mapped[UUID | None] = mapped_column(ForeignKey("payments.id"))
    amount_paise: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20))  # pending | processed | failed
    provider_refund_id: Mapped[str | None] = mapped_column(String(80))
    reason: Mapped[str] = mapped_column(Text)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))

