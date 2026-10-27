"""Application settings (12-factor, environment variables). See D-01 §3."""

import re
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_DIR / ".env", BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["local", "test", "staging", "production"] = "local"
    # Staging only: allow on-screen OTP codes and the mock payment gateway until SMS/Razorpay are connected.
    demo_mode: bool = False
    app_name: str = "Karan Sir Classes · CFA Learning Hub"
    # Render sets RENDER_EXTERNAL_URL automatically; PUBLIC_BASE_URL (e.g. a custom domain) wins.
    public_base_url: str = Field(default="http://localhost:3000",
                                 validation_alias=AliasChoices("PUBLIC_BASE_URL", "RENDER_EXTERNAL_URL"))

    database_url: str = "postgresql+asyncpg://cfa_lms:cfa_lms_local@localhost:5432/cfa_lms"

    secret_key: str = Field(default="change-me-local-only-secret-key-0123456789abcdef", min_length=32)
    access_token_ttl_minutes: int = 15
    student_refresh_ttl_days: int = 30
    staff_refresh_ttl_hours: int = 12
    student_max_sessions: int = 2
    cookie_secure: bool = False

    # OTP (BR-ACC-01). In local/test the code is echoed back so the UI can show it.
    otp_ttl_seconds: int = 300
    otp_max_attempts: int = 5
    otp_max_requests_per_hour: int = 5
    otp_debug_echo: bool = True
    sms_provider: Literal["console", "msg91"] = "console"
    email_provider: Literal["console", "ses"] = "console"

    # Staff MFA (S-02 §3.2). Can only be disabled in local/test.
    staff_mfa_required: bool = False

    # Payments (A-08)
    payment_provider: Literal["mock", "razorpay"] = "mock"
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""
    mock_webhook_secret: str = "mock-webhook-secret-local"
    order_reuse_minutes: int = 30

    # Events: optional HTTP sink so other services/teams can consume domain events (A-08 §6)
    event_sink_url: str = ""

    # Seeded staff password; required outside local/test (scripts/seed.py).
    seed_staff_password: str = ""

    storage_dir: Path = BACKEND_DIR / "var" / "storage"
    max_upload_mb: int = 500

    @field_validator("database_url")
    @classmethod
    def _asyncpg_url(cls, v: str) -> str:
        # Hosts such as Render hand out postgres:// or postgresql:// URLs; the app needs the asyncpg driver.
        return re.sub(r"^postgres(ql)?://", "postgresql+asyncpg://", v)

    @property
    def is_dev(self) -> bool:
        return self.app_env in ("local", "test")

    @property
    def dev_tools(self) -> bool:
        """On-screen OTP, mock gateway and debug links: local/test, or staging with DEMO_MODE."""
        return self.is_dev or (self.app_env == "staging" and self.demo_mode)


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if not s.is_dev:
        # Guard rails: never allow dev conveniences outside local/test.
        assert s.app_env == "staging" or not s.demo_mode, "DEMO_MODE is not allowed in production"
        assert s.dev_tools or not s.otp_debug_echo, "OTP_DEBUG_ECHO must be false outside local/test/demo"
        assert s.staff_mfa_required, "STAFF_MFA_REQUIRED must be true outside local/test"
        assert s.cookie_secure, "COOKIE_SECURE must be true outside local/test"
        assert "change-me" not in s.secret_key, "SECRET_KEY must be set"
    return s
