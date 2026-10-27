"""Flashcards and per-student spaced-repetition state (BR-FC)."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class Flashcard(IdMixin, TimestampMixin, Base):
    __tablename__ = "flashcards"

    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True)
    lm_id: Mapped[UUID | None] = mapped_column(ForeignKey("learning_modules.id", ondelete="SET NULL"), index=True)
    front: Mapped[str] = mapped_column(Text)
    back: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="published")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    source_ref: Mapped[str | None] = mapped_column(String(40), unique=True)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))


class CardReview(Base):
    __tablename__ = "card_reviews"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    card_id: Mapped[UUID] = mapped_column(ForeignKey("flashcards.id", ondelete="CASCADE"), primary_key=True)
    ease: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    reps: Mapped[int] = mapped_column(Integer, default=0)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    due_on: Mapped[date] = mapped_column(Date, index=True)
    last_rating: Mapped[str] = mapped_column(String(16))
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    known_reviews: Mapped[int] = mapped_column(Integer, default=0)
