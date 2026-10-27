"""Time helpers: store UTC, business days in IST (A-01 §6)."""

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def now_utc() -> datetime:
    return datetime.now(UTC)


def today_ist() -> date:
    return datetime.now(IST).date()


def age_on(dob: date, on: date) -> int:
    return on.year - dob.year - ((on.month, on.day) < (dob.month, dob.day))
