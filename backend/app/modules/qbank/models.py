"""Question bank and test attempts (A-03 §6, BR-QB, BR-TST, BR-SCR).

Each attempt item stores a snapshot of the question as served (stem, shuffled options,
correct index, explanation), so later edits never change a past attempt (BR-QB-02)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin

DIFFICULTIES = ("E", "M", "H")
QTYPES = ("conceptual", "numerical")


class Question(IdMixin, TimestampMixin, Base):
    __tablename__ = "questions"

    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True)
    lm_id: Mapped[UUID | None] = mapped_column(ForeignKey("learning_modules.id", ondelete="SET NULL"), index=True)
    los_id: Mapped[UUID | None] = mapped_column(ForeignKey("los.id", ondelete="SET NULL"))
    stem: Mapped[str] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSONB)  # exactly 3 strings (A/B/C)
    correct_index: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)
    distractor_rationale: Mapped[list | None] = mapped_column(JSONB)
    difficulty: Mapped[str] = mapped_column(String(1), index=True)
    qtype: Mapped[str] = mapped_column(String(12), default="conceptual")
    calc_mechanic: Mapped[str | None] = mapped_column(String(80))
    lock_option_order: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    provenance: Mapped[str] = mapped_column(String(30), default="original")
    version: Mapped[int] = mapped_column(Integer, default=1)
    source_ref: Mapped[str | None] = mapped_column(String(40), unique=True)  # e.g. proto-12 (seed import)
    author_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewer_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TestAttempt(IdMixin, TimestampMixin, Base):
    __test__ = False  # not a pytest test class
    __tablename__ = "test_attempts"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(10))  # chapter | master | custom
    title: Mapped[str] = mapped_column(String(200))
    subject_id: Mapped[UUID | None] = mapped_column(ForeignKey("subjects.id", ondelete="SET NULL"))
    lm_id: Mapped[UUID | None] = mapped_column(ForeignKey("learning_modules.id", ondelete="SET NULL"), index=True)
    filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    mode: Mapped[str] = mapped_column(String(12))  # practice | assessment
    timed: Mapped[bool] = mapped_column(Boolean)
    time_limit_s: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(12), default="in_progress", index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    submit_reason: Mapped[str | None] = mapped_column(String(12))  # student | timeout
    total: Mapped[int] = mapped_column(Integer)
    correct: Mapped[int | None] = mapped_column(Integer)
    score_pct: Mapped[float | None] = mapped_column(Float)
    pass_mark: Mapped[int | None] = mapped_column(Integer)


class AttemptItem(Base):
    __tablename__ = "attempt_items"

    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("test_attempts.id", ondelete="CASCADE"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    snapshot: Mapped[dict] = mapped_column(JSONB)  # {stem, options, correct_index, explanation, difficulty, lm_id}
    answer_index: Mapped[int | None] = mapped_column(Integer)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    time_spent_s: Mapped[int] = mapped_column(Integer, default=0)
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
