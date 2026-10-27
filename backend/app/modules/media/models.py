"""Learning resources: videos, PDFs, class notes, links (A-03 §3.5)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin

RESOURCE_KINDS = ("video", "pdf", "class_note", "link")


class Resource(IdMixin, TimestampMixin, Base):
    __tablename__ = "resources"

    lm_id: Mapped[UUID] = mapped_column(ForeignKey("learning_modules.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[UUID | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    downloadable: Mapped[bool] = mapped_column(Boolean, default=False)
    provenance: Mapped[str] = mapped_column(String(30), default="original")
    licence_ref: Mapped[str | None] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(20), default="draft")
    storage_key: Mapped[str | None] = mapped_column(Text)
    mime_type: Mapped[str | None] = mapped_column(String(80))
    url: Mapped[str | None] = mapped_column(Text)
    duration_s: Mapped[int | None] = mapped_column(Integer)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    chapters: Mapped[list | None] = mapped_column(JSONB)  # [{start_s, title}]
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
