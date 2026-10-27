"""Spaced repetition: modified SM-2 with three ratings (BR-FC-02/03)."""

from dataclasses import dataclass
from datetime import date, timedelta

RATINGS = ("known", "needs_revision", "difficult")
MIN_EASE = 1.3


@dataclass
class SrsState:
    ease: float = 2.5
    interval_days: int = 0
    reps: int = 0
    lapses: int = 0


def schedule(state: SrsState, rating: str, today: date) -> tuple[SrsState, date]:
    """Known → 1 d, 3 d, then interval × ease. Needs revision → interval × 1.2, ease −0.15.
    Difficult → back to 1 d, ease −0.2, counts a lapse."""
    s = SrsState(state.ease, state.interval_days, state.reps, state.lapses)
    if rating == "known":
        s.interval_days = 1 if s.reps == 0 else 3 if s.reps == 1 else max(s.interval_days + 1,
                                                                          round(s.interval_days * s.ease))
        s.reps += 1
    elif rating == "needs_revision":
        s.interval_days = max(1, round(max(s.interval_days, 1) * 1.2))
        s.ease = max(MIN_EASE, s.ease - 0.15)
    elif rating == "difficult":
        s.interval_days, s.reps, s.lapses = 1, 0, s.lapses + 1
        s.ease = max(MIN_EASE, s.ease - 0.2)
    else:
        raise ValueError(rating)
    return s, today + timedelta(days=s.interval_days)
