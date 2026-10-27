"""Cryptographic helpers. All crypto goes through this module (S-03 §3 rule 9)."""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings

_hasher = PasswordHasher(time_cost=3, memory_cost=64 * 1024, parallelism=2)


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    if not password_hash:
        return False
    try:
        return _hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def random_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def sha256(value: str) -> bytes:
    return hashlib.sha256(value.encode()).digest()


def hmac_sha256_hex(secret: str, message: bytes | str) -> str:
    if isinstance(message, str):
        message = message.encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def keyed_hash(value: str) -> str:
    """Deterministic keyed hash for lookups without storing the raw value (e.g. OTP destination)."""
    return hmac_sha256_hex(get_settings().secret_key, value.lower().strip())


def constant_time_equals(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())


def otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def encode_token(purpose: str, data: dict[str, Any], ttl: timedelta) -> str:
    now = datetime.now(UTC)
    payload = {**data, "pur": purpose, "iat": now, "exp": now + ttl}
    return jwt.encode(payload, get_settings().secret_key, algorithm="HS256")


def decode_token(token: str, purpose: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
    if payload.get("pur") != purpose:
        return None
    return payload
