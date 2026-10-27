"""Student learning API (A-04 §2.3). Every section of an entitled subject is open (BR-OPN-01)."""

from datetime import date, timedelta
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from pydantic import Field
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser, current_user, optional_user, require
from app.core.errors import NotFound
from app.core.schemas import In
from app.core.security import decode_token, encode_token
from app.core.storage import storage
from app.modules.catalog.models import LearningModule, Los, Subject
from app.modules.commerce.models import Course, CourseSubject
from app.modules.content.models import ContentItem, ContentVersion
from app.modules.enrolment import service as enrolment
from app.modules.media.models import Resource
from app.modules.progress import service as progress
from app.modules.progress.models import (
    Bookmark,
    EocEntry,
    LmProgress,
    ResourceProgress,
    RevisionLog,
)
from app.modules.qbank import service as qbank

router = APIRouter(tags=["learning"])


# ---------- helpers ----------

async def _lm(session: AsyncSession, lm_id: UUID) -> LearningModule:
    lm = await session.get(LearningModule, lm_id)
    if lm is None or lm.status != "published":
        raise NotFound()
    return lm


async def _entitled_lm(session: AsyncSession, user: CurrentUser, lm_id: UUID) -> LearningModule:
    lm = await _lm(session, lm_id)
    await enrolment.assert_entitled(session, user, lm.subject_id)
    return lm


async def _published_resources(session: AsyncSession, lm_ids: list[UUID]) -> list[Resource]:
    if not lm_ids:
        return []
    return list((await session.scalars(select(Resource).where(Resource.lm_id.in_(lm_ids),
                                                              Resource.status == "published")
                                       .order_by(Resource.sort_order, Resource.created_at))).all())


async def _lm_stats(session: AsyncSession, user_id: UUID, lms: list[LearningModule]) -> dict[UUID, dict]:
    ids = [lm.id for lm in lms]
    res = await _published_resources(session, ids)
    done = set((await session.scalars(select(ResourceProgress.resource_id).where(
        ResourceProgress.user_id == user_id, ResourceProgress.completed_at.is_not(None)))).all())
    lp = {p.lm_id: p for p in (await session.scalars(select(LmProgress).where(
        LmProgress.user_id == user_id, LmProgress.lm_id.in_(ids)))).all()} if ids else {}
    eoc = {e.lm_id: e for e in (await session.scalars(select(EocEntry).where(
        EocEntry.user_id == user_id, EocEntry.lm_id.in_(ids)))).all()} if ids else {}
    revs = dict((await session.execute(select(RevisionLog.lm_id, func.count()).where(
        RevisionLog.user_id == user_id, RevisionLog.counted, RevisionLog.lm_id.in_(ids))
        .group_by(RevisionLog.lm_id))).all()) if ids else {}
    out = {}
    for lm in lms:
        mand = [r for r in res if r.lm_id == lm.id and r.mandatory]
        comp = sum(1 for r in mand if r.id in done)
        p = lp.get(lm.id)
        e = eoc.get(lm.id)
        out[lm.id] = {
            "resources_total": len(mand), "resources_done": comp,
            "completion_pct": round(comp / len(mand) * 100) if mand else (100 if p and p.learned_at else 0),
            "learned": bool(p and p.learned_at), "learned_at": p.learned_at if p else None,
            "learned_undo_until": p.learned_undo_until if p else None,
            "last_opened_at": p.last_opened_at if p else None,
            "eoc_completed": bool(e and e.attempted and e.completed_on), "revision_count": revs.get(lm.id, 0),
        }
    return out


async def _courses_for_subject(session: AsyncSession, subject_id: UUID) -> list[dict]:
    rows = (await session.scalars(select(Course).join(CourseSubject).where(
        CourseSubject.subject_id == subject_id, Course.status == "open"))).all()
    return [{"code": c.code, "title": c.title, "fee_paise": c.fee_paise} for c in rows]


# ---------- catalogue ----------

@router.get("/subjects")
async def subjects(user: CurrentUser | None = Depends(optional_user),
                   session: AsyncSession = Depends(get_session)) -> list[dict]:
    subs = (await session.scalars(select(Subject).where(Subject.status == "published")
                                  .order_by(Subject.sort_order))).all()
    ent = await enrolment.entitled_subject_ids(session, user.id) if user else set()
    out = []
    for s in subs:
        lms = [lm for lm in s.lms if lm.status == "published"]
        entitled = bool(user and (user.is_staff or s.id in ent))
        stats = await _lm_stats(session, user.id, lms) if user and entitled else {}
        learned = sum(1 for v in stats.values() if v["learned"])
        out.append({"id": s.id, "code": s.code, "name": s.name, "icon": s.icon, "exam_weight": s.exam_weight,
                    "lm_count": len(lms), "entitled": entitled, "learned_count": learned,
                    "completion_pct": round(learned / len(lms) * 100) if lms else 0})
    return out


@router.get("/subjects/{code}")
async def subject_detail(code: str, user: CurrentUser | None = Depends(optional_user),
                         session: AsyncSession = Depends(get_session)) -> dict:
    s = await session.scalar(select(Subject).where(Subject.code == code, Subject.status == "published"))
    if s is None:
        raise NotFound()
    lms = [lm for lm in s.lms if lm.status == "published"]
    entitled = await enrolment.is_entitled(session, user, s.id)
    stats = await _lm_stats(session, user.id, lms) if user and entitled else {}
    return {
        "id": s.id, "code": s.code, "name": s.name, "icon": s.icon, "entitled": entitled,
        "courses": [] if entitled else await _courses_for_subject(session, s.id),
        "lms": [{"id": lm.id, "lm_no": lm.lm_no, "title": lm.title, "summary": lm.summary,
                 **(stats.get(lm.id, {}))} for lm in lms],
    }


@router.get("/lms/{lm_id}")
async def lm_detail(lm_id: UUID, user: CurrentUser = Depends(current_user),
                    session: AsyncSession = Depends(get_session)) -> dict:
    lm = await _entitled_lm(session, user, lm_id)
    subject = await session.get(Subject, lm.subject_id)
    items = (await session.scalars(select(ContentItem).where(
        ContentItem.lm_id == lm.id, ContentItem.current_published_version_id.is_not(None))
        .order_by(ContentItem.sort_order))).all()
    res = await _published_resources(session, [lm.id])
    rp = {p.resource_id: p for p in (await session.scalars(select(ResourceProgress).where(
        ResourceProgress.user_id == user.id, ResourceProgress.resource_id.in_([r.id for r in res])))).all()} \
        if res else {}
    los = (await session.scalars(select(Los).where(Los.lm_id == lm.id).order_by(Los.code))).all()
    eoc = await session.get(EocEntry, (user.id, lm.id))
    await progress.touch_lm(session, user.id, lm.id)
    stats = (await _lm_stats(session, user.id, [lm]))[lm.id]
    qcount = (await qbank.question_counts(session, [lm.id])).get(lm.id, 0)
    best = await qbank.best_scores(session, user.id, [lm.id])
    siblings = [x for x in subject.lms if x.status == "published"]
    idx = next(i for i, x in enumerate(siblings) if x.id == lm.id)
    return {
        "id": lm.id, "lm_no": lm.lm_no, "title": lm.title, "summary": lm.summary,
        "subject": {"id": subject.id, "code": subject.code, "name": subject.name},
        "prev_lm_id": siblings[idx - 1].id if idx > 0 else None,
        "next_lm_id": siblings[idx + 1].id if idx + 1 < len(siblings) else None,
        "topics": [{"id": t.id, "title": t.title} for t in lm.topics if t.status == "published"],
        "content": [{"id": c.id, "title": c.title, "kind": c.kind, "topic_id": c.topic_id} for c in items],
        "resources": [{"id": r.id, "kind": r.kind, "title": r.title, "mandatory": r.mandatory,
                       "duration_s": r.duration_s, "downloadable": r.downloadable, "topic_id": r.topic_id,
                       "completed": bool(rp.get(r.id) and rp[r.id].completed_at),
                       "last_position_s": rp[r.id].last_position_s if r.id in rp else 0} for r in res],
        "los": [{"code": x.code, "statement": x.statement, "command_word": x.command_word} for x in los],
        "eoc": None if eoc is None else {"attempted": eoc.attempted, "q_attempted": eoc.q_attempted,
                                         "q_correct": eoc.q_correct, "completed_on": eoc.completed_on,
                                         "weak_topics": eoc.weak_topics},
        "progress": stats,
        "quiz": {"questions": qcount, "available": qcount >= qbank.CHAPTER_QUIZ_MIN,
                 "size": min(qcount, qbank.CHAPTER_QUIZ_SIZE), "pass_mark": qbank.CHAPTER_PASS_MARK,
                 **best.get(lm.id, {"best_pct": None, "attempts": 0})},
    }


@router.get("/content/{item_id}")
async def content(item_id: UUID, user: CurrentUser = Depends(current_user),
                  session: AsyncSession = Depends(get_session)) -> dict:
    item = await session.get(ContentItem, item_id)
    if item is None or item.current_published_version_id is None:
        raise NotFound()
    await _entitled_lm(session, user, item.lm_id)
    v = await session.get(ContentVersion, item.current_published_version_id)
    return {"id": item.id, "title": item.title, "kind": item.kind, "version_no": v.version_no, "body": v.body}


# ---------- resources ----------

async def _resource(session: AsyncSession, user: CurrentUser, rid: UUID) -> Resource:
    r = await session.get(Resource, rid)
    if r is None or (r.status != "published" and not user.is_staff):
        raise NotFound()
    await _entitled_lm(session, user, r.lm_id)
    return r


@router.get("/resources/{rid}/playback")
async def playback(rid: UUID, user: CurrentUser = Depends(current_user),
                   session: AsyncSession = Depends(get_session)) -> dict:
    r = await _resource(session, user, rid)
    rp = await session.get(ResourceProgress, (user.id, r.id))
    mobile = user.user.mobile_e164 or ""
    watermark = f"{user.user.student_code or 'STAFF'} · ••••{mobile[-4:]}" if mobile else \
        (user.user.student_code or "STAFF")
    url = r.url
    if r.storage_key:
        token = encode_token("media", {"rid": str(r.id), "uid": str(user.id)}, timedelta(hours=2))
        url = f"/api/v1/media/stream/{token}"
    return {"id": r.id, "kind": r.kind, "title": r.title, "url": url, "mime_type": r.mime_type,
            "duration_s": r.duration_s, "chapters": r.chapters or [], "watermark": watermark,
            "downloadable": r.downloadable, "last_position_s": rp.last_position_s if rp else 0,
            "completed": bool(rp and rp.completed_at)}


@router.get("/media/stream/{token}")
async def stream(token: str, session: AsyncSession = Depends(get_session)) -> FileResponse:
    """Signed, expiring media URL (US-5.04). Range requests are supported for seeking."""
    p = decode_token(token, "media")
    if not p:
        raise NotFound("This link has expired. Reload the page.")
    r = await session.get(Resource, UUID(p["rid"]))
    if r is None or not r.storage_key:
        raise NotFound()
    path = storage().path(r.storage_key)
    if not path.exists():
        raise NotFound("File missing")
    disposition = "attachment" if r.downloadable and r.kind != "video" else "inline"
    return FileResponse(path, media_type=r.mime_type or "application/octet-stream",
                        headers={"Content-Disposition": f'{disposition}; filename="{path.name.split("_", 1)[-1]}"',
                                 "Cache-Control": "private, max-age=3600"})


class ProgressIn(In):
    from_s: int | None = Field(default=None, ge=0)
    to_s: int | None = Field(default=None, ge=0)
    position_s: int | None = Field(default=None, ge=0)
    mark_complete: bool = False


@router.post("/resources/{rid}/progress")
async def resource_progress(rid: UUID, body: ProgressIn, user: CurrentUser = Depends(require("progress:write")),
                            session: AsyncSession = Depends(get_session)) -> dict:
    r = await _resource(session, user, rid)
    return await progress.record_progress(session, user.id, r, from_s=body.from_s, to_s=body.to_s,
                                          position_s=body.position_s, mark_complete=body.mark_complete)


# ---------- LM progress ----------

@router.post("/lms/{lm_id}/learned")
async def learned(lm_id: UUID, user: CurrentUser = Depends(require("progress:write")),
                  session: AsyncSession = Depends(get_session)) -> dict:
    lm = await _entitled_lm(session, user, lm_id)
    await progress.mark_learned(session, user, lm.id)
    return (await _lm_stats(session, user.id, [lm]))[lm.id]


@router.delete("/lms/{lm_id}/learned")
async def unlearned(lm_id: UUID, user: CurrentUser = Depends(require("progress:write")),
                    session: AsyncSession = Depends(get_session)) -> dict:
    lm = await _entitled_lm(session, user, lm_id)
    await progress.undo_learned(session, user, lm.id)
    return (await _lm_stats(session, user.id, [lm]))[lm.id]


class RevisionIn(In):
    activity: Literal["notes", "revision_sheet", "flashcards", "questions", "other"] = "notes"
    revised_on: date | None = None


@router.post("/lms/{lm_id}/revisions")
async def revision(lm_id: UUID, body: RevisionIn, user: CurrentUser = Depends(require("progress:write")),
                   session: AsyncSession = Depends(get_session)) -> dict:
    lm = await _entitled_lm(session, user, lm_id)
    return await progress.log_revision(session, user, lm.id, body.activity, body.revised_on)


class EocIn(In):
    attempted: bool
    q_attempted: int = Field(ge=0, le=500)
    q_correct: int = Field(ge=0, le=500)
    completed_on: date | None = None
    weak_topics: str | None = Field(default=None, max_length=500)


@router.put("/lms/{lm_id}/eoc")
async def eoc(lm_id: UUID, body: EocIn, user: CurrentUser = Depends(require("progress:write")),
              session: AsyncSession = Depends(get_session)) -> dict:
    lm = await _entitled_lm(session, user, lm_id)
    e = await progress.save_eoc(session, user, lm.id, body.model_dump())
    return {"attempted": e.attempted, "q_attempted": e.q_attempted, "q_correct": e.q_correct,
            "completed_on": e.completed_on, "weak_topics": e.weak_topics}


# ---------- dashboard ----------

@router.get("/me/dashboard")
async def dashboard(user: CurrentUser = Depends(current_user), session: AsyncSession = Depends(get_session)) -> dict:
    ent = await enrolment.entitled_subject_ids(session, user.id)
    subs = (await session.scalars(select(Subject).where(Subject.id.in_(ent)).order_by(Subject.sort_order))).all() \
        if ent else []
    summary, all_lms, stats = [], [], {}
    for s in subs:
        lms = [lm for lm in s.lms if lm.status == "published"]
        st = await _lm_stats(session, user.id, lms)
        stats.update(st)
        all_lms += [(s, lm) for lm in lms]
        learned = sum(1 for v in st.values() if v["learned"])
        summary.append({"code": s.code, "name": s.name, "icon": s.icon, "lm_count": len(lms),
                        "learned_count": learned, "completion_pct": round(learned / len(lms) * 100) if lms else 0})

    next_action = {"type": "register", "title": "Register for a course", "href": "/courses"}
    if all_lms:
        opened = [(s, lm) for s, lm in all_lms if stats[lm.id]["last_opened_at"] and not stats[lm.id]["learned"]]
        opened.sort(key=lambda x: stats[x[1].id]["last_opened_at"], reverse=True)
        pick = opened[0] if opened else next(((s, lm) for s, lm in all_lms if not stats[lm.id]["learned"]), None)
        if pick:
            s, lm = pick
            st = stats[lm.id]
            kind = "continue" if st["resources_done"] < st["resources_total"] else "mark_learned"
            next_action = {"type": kind, "title": f"{s.name} · LM{lm.lm_no} {lm.title}",
                           "subtitle": f"{st['resources_done']} of {st['resources_total']} resources done",
                           "completion_pct": st["completion_pct"], "href": f"/learn/{s.code}?lm={lm.id}"}
        else:
            next_action = {"type": "revise", "title": "Every LM is marked learned — time to revise",
                           "href": f"/learn/{all_lms[0][0].code}"}
    learned = [(s, lm) for s, lm in all_lms if stats[lm.id]["learned"]]
    qcounts = await qbank.question_counts(session, [lm.id for _, lm in learned])
    best = await qbank.best_scores(session, user.id, [lm.id for _, lm in learned])
    pending = [{"title": f"{s.name} · LM{lm.lm_no} {lm.title}", "reason": "Chapter quiz not taken yet",
                "href": f"/learn/{s.code}?lm={lm.id}&tab=quiz"}
               for s, lm in learned
               if qcounts.get(lm.id, 0) >= qbank.CHAPTER_QUIZ_MIN and lm.id not in best][:5]
    recent = (await session.execute(select(LmProgress.lm_id, LmProgress.last_opened_at).where(
        LmProgress.user_id == user.id, LmProgress.last_opened_at.is_not(None))
        .order_by(LmProgress.last_opened_at.desc()).limit(5))).all()
    by_id = {lm.id: (s, lm) for s, lm in all_lms}
    recent_out = [{"title": f"{by_id[r[0]][0].name} · LM{by_id[r[0]][1].lm_no} {by_id[r[0]][1].title}",
                   "at": r[1], "href": f"/learn/{by_id[r[0]][0].code}?lm={r[0]}"} for r in recent if r[0] in by_id]
    return {"user": {"full_name": user.user.full_name, "student_code": user.user.student_code,
                     "target_exam": user.user.target_exam},
            "next_action": next_action, "subjects": summary, "pending": pending, "recent": recent_out}


# ---------- search & bookmarks ----------

@router.get("/search")
async def search(q: str = Query(min_length=2, max_length=100), user: CurrentUser = Depends(current_user),
                 session: AsyncSession = Depends(get_session)) -> dict:
    ent = None if user.is_staff else await enrolment.entitled_subject_ids(session, user.id)
    like = f"%{q}%"
    lm_q = select(LearningModule, Subject).join(Subject).where(
        LearningModule.status == "published", or_(LearningModule.title.ilike(like),
                                                  LearningModule.summary.ilike(like)))
    lms = (await session.execute(lm_q.limit(20))).all()
    tsq = func.websearch_to_tsquery("english", q)
    content_q = (select(ContentItem, LearningModule, Subject, func.ts_headline(
        "english", ContentVersion.plain_text, tsq, "MaxWords=18, MinWords=8").label("snip"))
        .join(ContentVersion, ContentVersion.id == ContentItem.current_published_version_id)
        .join(LearningModule, LearningModule.id == ContentItem.lm_id).join(Subject)
        .where(or_(func.to_tsvector("english", ContentVersion.plain_text).op("@@")(tsq),
                   ContentItem.title.ilike(like))).limit(30))
    contents = (await session.execute(content_q)).all()

    def visible(subject_id):
        return ent is None or subject_id in ent

    return {
        "lms": [{"id": lm.id, "title": f"LM{lm.lm_no} · {lm.title}", "subject": s.name, "subject_code": s.code,
                 "entitled": visible(s.id)} for lm, s in lms],
        "content": [{"id": c.id, "lm_id": lm.id, "title": c.title, "lm": f"LM{lm.lm_no} · {lm.title}",
                     "subject": s.name, "subject_code": s.code, "entitled": visible(s.id),
                     "snippet": snip if visible(s.id) else None} for c, lm, s, snip in contents],
    }


class BookmarkIn(In):
    target_type: Literal["content_item", "resource", "lm"]
    target_id: UUID
    position_s: int | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=500)


@router.get("/me/bookmarks")
async def bookmarks(user: CurrentUser = Depends(require("bookmark:self")),
                    session: AsyncSession = Depends(get_session)) -> list[dict]:
    rows = (await session.scalars(select(Bookmark).where(Bookmark.user_id == user.id)
                                  .order_by(Bookmark.created_at.desc()))).all()
    out = []
    for b in rows:
        title, lm_id = "Removed item", None
        if b.target_type == "content_item" and (c := await session.get(ContentItem, b.target_id)):
            title, lm_id = c.title, c.lm_id
        elif b.target_type == "resource" and (r := await session.get(Resource, b.target_id)):
            title, lm_id = r.title, r.lm_id
        elif b.target_type == "lm" and (lm := await session.get(LearningModule, b.target_id)):
            title, lm_id = f"LM{lm.lm_no} · {lm.title}", lm.id
        lm = await session.get(LearningModule, lm_id) if lm_id else None
        subj = await session.get(Subject, lm.subject_id) if lm else None
        out.append({"id": b.id, "target_type": b.target_type, "target_id": b.target_id, "title": title,
                    "position_s": b.position_s, "note": b.note, "created_at": b.created_at,
                    "href": f"/learn/{subj.code}?lm={lm.id}" if subj else None,
                    "context": f"{subj.name} · LM{lm.lm_no}" if subj else None})
    return out


@router.post("/me/bookmarks", status_code=201)
async def add_bookmark(body: BookmarkIn, user: CurrentUser = Depends(require("bookmark:self")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    existing = await session.scalar(select(Bookmark).where(
        Bookmark.user_id == user.id, Bookmark.target_type == body.target_type, Bookmark.target_id == body.target_id,
        Bookmark.position_s.is_(None) if body.position_s is None else Bookmark.position_s == body.position_s))
    b = existing or Bookmark(user_id=user.id, **body.model_dump())
    if existing:
        b.note = body.note or b.note
    session.add(b)
    await session.flush()
    return {"id": b.id}


@router.delete("/me/bookmarks/{bid}")
async def delete_bookmark(bid: UUID, user: CurrentUser = Depends(require("bookmark:self")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    b = await session.get(Bookmark, bid)
    if b is None or b.user_id != user.id:
        raise NotFound()
    await session.delete(b)
    return {"status": "deleted"}
