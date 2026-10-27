"""Subjects → Learning Modules → Topics, plus LOS (A-03 §3.4)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin, TimestampMixin


class Subject(IdMixin, TimestampMixin, Base):
    __tablename__ = "subjects"

    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    icon: Mapped[str] = mapped_column(String(8), default="◆")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="published")
    exam_weight: Mapped[str | None] = mapped_column(String(20))

    lms: Mapped[list["LearningModule"]] = relationship(
        back_populates="subject", order_by="LearningModule.lm_no", lazy="selectin"
    )


class LearningModule(IdMixin, TimestampMixin, Base):
    __tablename__ = "learning_modules"
    __table_args__ = (UniqueConstraint("subject_id", "lm_no"),)

    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True)
    lm_no: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str | None] = mapped_column(Text)
    source_ref: Mapped[str | None] = mapped_column(String(40))  # INTERNAL ONLY (BR-CAT-03)
    status: Mapped[str] = mapped_column(String(20), default="published")
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    subject: Mapped[Subject] = relationship(back_populates="lms")
    topics: Mapped[list["Topic"]] = relationship(order_by="Topic.sort_order", lazy="selectin")


class Topic(IdMixin, TimestampMixin, Base):
    __tablename__ = "topics"

    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="published")
    los_ids: Mapped[list | None] = mapped_column(JSONB)


class Los(IdMixin, TimestampMixin, Base):
    __tablename__ = "los"
    __table_args__ = (UniqueConstraint("lm_id", "code"),)

    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(30))
    statement: Mapped[str] = mapped_column(Text)
    command_word: Mapped[str] = mapped_column(String(30))
