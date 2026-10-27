"""UUIDv7 generator (ADR-013): time-ordered, random, not guessable."""

import secrets
import time
import uuid


def uuid7() -> uuid.UUID:
    ms = time.time_ns() // 1_000_000
    rand = secrets.randbits(74)
    value = (
        (ms & ((1 << 48) - 1)) << 80
        | 0x7 << 76
        | ((rand >> 62) & 0xFFF) << 64
        | 0b10 << 62
        | (rand & ((1 << 62) - 1))
    )
    return uuid.UUID(int=value)
