"""Database engine, session and declarative base. Conventions: A-03 §1."""

from collections.abc import AsyncIterator
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import get_settings
from app.core.ids import uuid7
from app.core.timeutil import now_utc

NAMING = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING)


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)


class TimestampMixin:
    # Python-side defaults so values are available right after flush (no async lazy load).
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc,
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc,
                                                 server_default=func.now(), onupdate=now_utc)


def to_dict(obj: object, exclude: tuple[str, ...] = ("password_hash", "totp_secret")) -> dict:
    """Column attributes of an ORM object as a plain dict."""
    from sqlalchemy import inspect

    return {a.key: getattr(obj, a.key) for a in inspect(obj).mapper.column_attrs if a.key not in exclude}


engine = create_async_engine(get_settings().database_url, pool_pre_ping=True, pool_size=10)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """One transaction per request (unit of work, A-01 §6)."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
