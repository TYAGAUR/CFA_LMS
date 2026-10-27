"""Public course catalogue and student registration (BR-PAY-01..03)."""

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, optional_user, require
from app.core.errors import Invalid
from app.core.schemas import In
from app.modules.catalog.models import Subject
from app.modules.commerce import service
from app.modules.commerce.models import Course, Registration

router = APIRouter(tags=["courses"])


class RegisterIn(In):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    city: str = Field(min_length=2, max_length=80)
    qualification: str = Field(min_length=2, max_length=120)
    target_exam: str = Field(min_length=4, max_length=20)
    accept_course_terms: bool


async def _course_dict(session: AsyncSession, c: Course, with_outline: bool = False) -> dict:
    subject_ids = [s.subject_id for s in c.subjects]
    subjects = (await session.scalars(select(Subject).where(Subject.id.in_(subject_ids))
                                      .order_by(Subject.sort_order))).all() if subject_ids else []
    taken = await service.seats_taken(session, c.id)
    out = {
        "id": c.id, "code": c.code, "title": c.title, "tagline": c.tagline, "description": c.description,
        "fee_paise": c.fee_paise, "currency": c.currency, "validity_days": c.validity_days,
        "access_ends_on": c.access_ends_on, "exam_window": c.exam_window, "status": c.status,
        "seats_left": (c.seat_limit - taken) if c.seat_limit else None,
        "subjects": [{"id": s.id, "code": s.code, "name": s.name, "icon": s.icon, "lm_count": len(s.lms),
                      **({"lms": [{"lm_no": lm.lm_no, "title": lm.title} for lm in s.lms
                                  if lm.status == "published"]} if with_outline else {})}
                     for s in subjects],
    }
    return out


@router.get("/courses")
async def list_courses(session: AsyncSession = Depends(get_session)) -> list[dict]:
    rows = (await session.scalars(select(Course).where(Course.status.in_(["open", "closed"]))
                                  .order_by(Course.sort_order, Course.title))).all()
    return [await _course_dict(session, c) for c in rows]


@router.get("/courses/{code}")
async def get_course(code: str, user: CurrentUser | None = Depends(optional_user),
                     session: AsyncSession = Depends(get_session)) -> dict:
    c = await service.course_by_code(session, code)
    out = await _course_dict(session, c, with_outline=True)
    out["my_registration"] = None
    if user:
        reg = await session.scalar(select(Registration).where(
            Registration.user_id == user.id, Registration.course_id == c.id)
            .order_by(Registration.created_at.desc()).limit(1))
        if reg:
            out["my_registration"] = {"id": reg.id, "status": reg.status, "order_id": reg.current_order_id}
    return out


@router.post("/courses/{code}/register")
async def register(code: str, body: RegisterIn, user: CurrentUser = Depends(require("course:register")),
                   session: AsyncSession = Depends(get_session)) -> dict:
    if not body.accept_course_terms:
        raise Invalid("Please accept the course terms.", code="terms_required")
    if body.full_name and body.full_name != user.user.full_name:
        user.user.full_name = body.full_name
    form = body.model_dump(exclude={"accept_course_terms", "full_name"}, mode="json")
    form["accepted_terms_at"] = datetime.now().isoformat()
    return await service.start_registration(session, user.user, code, form)


@router.get("/me/registrations")
async def my_registrations(user: CurrentUser = Depends(require("course:register")),
                           session: AsyncSession = Depends(get_session)) -> list[dict]:
    regs = (await session.scalars(select(Registration).where(Registration.user_id == user.id)
                                  .order_by(Registration.created_at.desc()))).all()
    out = []
    for r in regs:
        c = await session.get(Course, r.course_id)
        start, end = service.access_window(c, r.activated_at) if r.activated_at else (None, None)
        out.append({"id": r.id, "status": r.status, "created_at": r.created_at, "activated_at": r.activated_at,
                    "access_until": end, "order_id": r.current_order_id,
                    "course": {"code": c.code, "title": c.title, "fee_paise": c.fee_paise}})
    return out

