"""Learning progress (A-03 §3.6). Progress never gates access (BR-OPN-03)."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class ResourceProgress(Base):
    __tablename__ = "resource_progress"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    resource_id: Mapped[UUID] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
    watched: Mapped[list] = mapped_column(JSONB, default=list)  # merged [start_s, end_s] intervals
    last_position_s: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class LmProgress(Base):
    __tablename__ = "lm_progress"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), primary_key=True)
    learned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    learned_undo_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RevisionLog(IdMixin, Base):
    __tablename__ = "revision_logs"
    __table_args__ = (
        Index("uq_revision_counted_per_day", "user_id", "lm_id", "revised_on",
              unique=True, postgresql_where=text("counted")),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"))
    revised_on: Mapped[date] = mapped_column(Date)
    activity: Mapped[str] = mapped_column(String(20))
    counted: Mapped[bool] = mapped_column(Boolean)
    source: Mapped[str] = mapped_column(String(10), default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EocEntry(Base):
    __tablename__ = "eoc_entries"
    __table_args__ = (CheckConstraint("q_correct <= q_attempted", name="correct_le_attempted"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), primary_key=True)
    attempted: Mapped[bool] = mapped_column(Boolean, default=False)
    q_attempted: Mapped[int] = mapped_column(Integer, default=0)
    q_correct: Mapped[int] = mapped_column(Integer, default=0)
    completed_on: Mapped[date | None] = mapped_column(Date)
    weak_topics: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Bookmark(IdMixin, TimestampMixin, Base):
    __tablename__ = "bookmarks"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    target_type: Mapped[str] = mapped_column(String(20))  # content_item | resource | lm
    target_id: Mapped[UUID] = mapped_column()
    position_s: Mapped[int | None] = mapped_column(Integer)
    note: Mapped[str | None] = mapped_column(String(500))
