"""Consents and data requests (A-03 §3.2, C-03)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin

PURPOSES = ("service_delivery", "product_analytics", "marketing_messages", "leaderboard_display")
MINOR_BLOCKED_PURPOSES = ("product_analytics", "leaderboard_display")  # C-01 PR-2
DATA_REQUEST_TYPES = ("access", "correction", "erasure", "grievance", "nomination")


class Consent(IdMixin, Base):
    """Append-only: the latest row per (user, purpose) is the current state."""

    __tablename__ = "consents"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    purpose: Mapped[str] = mapped_column(String(30))
    granted: Mapped[bool] = mapped_column(Boolean)
    notice_version: Mapped[str] = mapped_column(String(20))
    actor: Mapped[str] = mapped_column(String(10))  # self | guardian
    guardian_id: Mapped[UUID | None] = mapped_column(ForeignKey("guardians.id", ondelete="SET NULL"))
    method: Mapped[str] = mapped_column(String(20))
    ip_address: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class DataRequest(IdMixin, TimestampMixin, Base):
    __tablename__ = "data_requests"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="open")
    note: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict | None] = mapped_column(JSONB)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    handled_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    resolution_note: Mapped[str | None] = mapped_column(Text)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
