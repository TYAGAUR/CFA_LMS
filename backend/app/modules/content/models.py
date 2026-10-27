"""Versioned content (ADR-007, ADR-012). Notes are JSON blocks, never HTML."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin

KINDS = ("note", "revision_sheet", "infographic")
PROVENANCE = ("original", "faculty_recording", "licensed_third_party", "reference_only")


class ContentItem(IdMixin, TimestampMixin, Base):
    __tablename__ = "content_items"

    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[UUID | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(20), default="note")
    title: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    current_published_version_id: Mapped[UUID | None] = mapped_column()


class ContentVersion(IdMixin, Base):
    __tablename__ = "content_versions"
    __table_args__ = (UniqueConstraint("item_id", "version_no"),)

    item_id: Mapped[UUID] = mapped_column(ForeignKey("content_items.id", ondelete="CASCADE"), index=True)
    version_no: Mapped[int] = mapped_column(Integer)
    body: Mapped[dict] = mapped_column(JSONB)
    plain_text: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="draft")
    provenance: Mapped[str] = mapped_column(String(30), default="original")
    licence_ref: Mapped[str | None] = mapped_column(String(60))
    author_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewer_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)
