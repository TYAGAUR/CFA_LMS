"""Batches, enrolments and entitlements (A-03 §3.3)."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class Batch(IdMixin, TimestampMixin, Base):
    __tablename__ = "batches"

    code: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    exam_window: Mapped[str | None] = mapped_column(String(20))
    starts_on: Mapped[date] = mapped_column(Date)
    ends_on: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="active")


class Enrolment(IdMixin, TimestampMixin, Base):
    __tablename__ = "enrolments"
    __table_args__ = (UniqueConstraint("user_id", "batch_id"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    batch_id: Mapped[UUID] = mapped_column(ForeignKey("batches.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="active")
    enrolled_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))


class Entitlement(IdMixin, TimestampMixin, Base):
    """Right to access a subject. Source: a paid registration, a batch, or an admin grant."""

    __tablename__ = "entitlements"
    __table_args__ = (Index("ix_entitlements_user_subject", "user_id", "subject_id", "ends_at"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    source: Mapped[str] = mapped_column(String(20))  # registration | batch | grant
    source_id: Mapped[UUID | None] = mapped_column()
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
