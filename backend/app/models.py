"""Import every model so SQLAlchemy metadata (and Alembic autogenerate) sees all tables."""

from app.modules.audit.models import AuditLog, OutboxEvent, Setting  # noqa: F401
from app.modules.auth.models import OtpChallenge, UserSession  # noqa: F401
from app.modules.catalog.models import LearningModule, Los, Subject, Topic  # noqa: F401
from app.modules.commerce.models import Course, CourseSubject, Registration  # noqa: F401
from app.modules.content.models import ContentItem, ContentVersion  # noqa: F401
from app.modules.enrolment.models import Batch, Enrolment, Entitlement  # noqa: F401
from app.modules.flashcards.models import CardReview, Flashcard  # noqa: F401
from app.modules.media.models import Resource  # noqa: F401
from app.modules.payments.models import Order, Payment, PaymentEvent, Refund  # noqa: F401
from app.modules.privacy.models import Consent, DataRequest  # noqa: F401
from app.modules.progress.models import (  # noqa: F401
    Bookmark,
    EocEntry,
    LmProgress,
    ResourceProgress,
    RevisionLog,
)
from app.modules.qbank.models import AttemptItem, Question, TestAttempt  # noqa: F401
from app.modules.users.models import Guardian, User, UserRole  # noqa: F401
