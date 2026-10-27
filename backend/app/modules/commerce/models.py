"""Courses and student registrations (BR-PAY-01..03). Payments live in the payments module."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin, TimestampMixin

# registration.status
PENDING_PAYMENT = "pending_payment"
ACTIVE = "active"
CANCELLED = "cancelled"
EXPIRED = "expired"


class Course(IdMixin, TimestampMixin, Base):
    __tablename__ = "courses"

    code: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    tagline: Mapped[str | None] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    fee_paise: Mapped[int] = mapped_column(Integer)  # GST-inclusive
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    validity_days: Mapped[int | None] = mapped_column(Integer)
    access_ends_on: Mapped[date | None] = mapped_column(Date)
    seat_limit: Mapped[int | None] = mapped_column(Integer)
    batch_id: Mapped[UUID | None] = mapped_column(ForeignKey("batches.id", ondelete="SET NULL"))
    exam_window: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft | open | closed
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    subjects: Mapped[list["CourseSubject"]] = relationship(lazy="selectin", cascade="all, delete-orphan")


class CourseSubject(Base):
    __tablename__ = "course_subjects"

    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)


class Registration(IdMixin, TimestampMixin, Base):
    __tablename__ = "registrations"
    __table_args__ = (
        # BR-PAY-03: one open registration per course per student
        Index("uq_registration_open", "user_id", "course_id", unique=True,
              postgresql_where=text("status in ('pending_payment','active')")),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(20), default=PENDING_PAYMENT)
    form: Mapped[dict] = mapped_column(JSONB, default=dict)
    current_order_id: Mapped[UUID | None] = mapped_column()
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancel_reason: Mapped[str | None] = mapped_column(Text)
