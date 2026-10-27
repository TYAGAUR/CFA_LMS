"""Identity tables (A-03 §3.1)."""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin, TimestampMixin

ROLES = ("student", "author", "reviewer", "admin", "super_admin")
STAFF_ROLES = ("author", "reviewer", "admin", "super_admin")

# user.status values
ACTIVE = "active"
PENDING_GUARDIAN = "pending_guardian_consent"
SUSPENDED = "suspended"
DEACTIVATED = "deactivated"
DELETED = "deleted"


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    mobile_e164: Mapped[str | None] = mapped_column(String(16), unique=True)
    email: Mapped[str | None] = mapped_column(CITEXT, unique=True)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    full_name: Mapped[str] = mapped_column(String(120))
    student_code: Mapped[str | None] = mapped_column(String(20), unique=True)
    dob: Mapped[date | None] = mapped_column(Date)
    is_minor: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(32), default=ACTIVE, index=True)
    password_hash: Mapped[str | None] = mapped_column(Text)
    totp_secret: Mapped[bytes | None] = mapped_column(LargeBinary)
    mfa_enrolled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    failed_login_count: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Registration profile (BR-PAY-02)
    city: Mapped[str | None] = mapped_column(String(80))
    qualification: Mapped[str | None] = mapped_column(String(120))
    target_exam: Mapped[str | None] = mapped_column(String(20))

    roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan", foreign_keys="UserRole.user_id"
    )

    @property
    def role_names(self) -> list[str]:
        return sorted(r.role for r in self.roles)

    @property
    def is_staff(self) -> bool:
        return any(r.role in STAFF_ROLES for r in self.roles)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String(20), primary_key=True)
    granted_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="roles", foreign_keys=[user_id])


class Guardian(IdMixin, TimestampMixin, Base):
    __tablename__ = "guardians"

    student_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name: Mapped[str] = mapped_column(String(120))
    mobile_e164: Mapped[str] = mapped_column(String(16))
    relation: Mapped[str] = mapped_column("relationship", String(20))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    verification_method: Mapped[str | None] = mapped_column(String(20))
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
