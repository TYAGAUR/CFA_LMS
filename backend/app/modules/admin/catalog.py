"""Admin: subjects, LMs, topics, LOS, notes content, resources (A-04 §2.5)."""

from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import get_session
from app.core.deps import CurrentUser, require
from app.core.errors import Conflict, Invalid, NotFound
from app.core.schemas import In
from app.core.storage import storage
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.catalog.models import LearningModule, Los, Subject, Topic
from app.modules.content import service as content
from app.modules.content.models import ContentItem, ContentVersion
from app.modules.media.models import Resource

router = APIRouter(prefix="/admin", tags=["admin"])

ALLOWED_MIME = {
    "video": {"video/mp4", "video/webm"},
    "pdf": {"application/pdf"},
    "class_note": {"application/pdf"},
}


# ---------- subjects / LMs ----------

@router.get("/catalog")
async def catalog(_: CurrentUser = Depends(require("catalog:read_admin")),
                  session: AsyncSession = Depends(get_session)) -> list[dict]:
    subs = (await session.scalars(select(Subject).order_by(Subject.sort_order))).all()
    res_counts = dict((await session.execute(select(Resource.lm_id, func.count()).group_by(Resource.lm_id))).all())
    item_counts = dict((await session.execute(
        select(ContentItem.lm_id, func.count()).where(ContentItem.current_published_version_id.is_not(None))
        .group_by(ContentItem.lm_id))).all())
    return [{"id": s.id, "code": s.code, "name": s.name, "icon": s.icon, "status": s.status,
             "sort_order": s.sort_order, "exam_weight": s.exam_weight,
             "lms": [{"id": lm.id, "lm_no": lm.lm_no, "title": lm.title, "status": lm.status,
                      "source_ref": lm.source_ref, "resources": res_counts.get(lm.id, 0),
                      "notes": item_counts.get(lm.id, 0)} for lm in s.lms]} for s in subs]


class SubjectIn(In):
    code: str = Field(min_length=2, max_length=10, pattern=r"^[a-z0-9]+$")
    name: str = Field(min_length=2, max_length=120)
    icon: str = Field(default="◆", max_length=8)
    sort_order: int = 0
    status: Literal["draft", "published"] = "published"
    exam_weight: str | None = Field(default=None, max_length=20)


@router.post("/subjects", status_code=201)
async def create_subject(body: SubjectIn, actor: CurrentUser = Depends(require("catalog:write")),
                         session: AsyncSession = Depends(get_session)) -> dict:
    if await session.scalar(select(Subject.id).where(Subject.code == body.code)):
        raise Conflict("Subject code exists.")
    s = Subject(**body.model_dump())
    session.add(s)
    await session.flush()
    await audit.record(session, "subject.created", actor=actor, target_type="subject", target_id=s.id,
                       metadata=body.model_dump())
    return {"id": s.id}


@router.patch("/subjects/{sid}")
async def update_subject(sid: UUID, body: SubjectIn, actor: CurrentUser = Depends(require("catalog:write")),
                         session: AsyncSession = Depends(get_session)) -> dict:
    s = await session.get(Subject, sid)
    if s is None:
        raise NotFound()
    for k, v in body.model_dump().items():
        setattr(s, k, v)
    await audit.record(session, "subject.updated", actor=actor, target_type="subject", target_id=s.id,
                       metadata=body.model_dump())
    return {"id": s.id}


class LmIn(In):
    subject_id: UUID
    lm_no: int = Field(ge=1, le=99)
    title: str = Field(min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=2000)
    source_ref: str | None = Field(default=None, max_length=40)
    status: Literal["draft", "published", "retired"] = "draft"


@router.post("/lms", status_code=201)
async def create_lm(body: LmIn, actor: CurrentUser = Depends(require("catalog:write")),
                    session: AsyncSession = Depends(get_session)) -> dict:
    if await session.scalar(select(LearningModule.id).where(LearningModule.subject_id == body.subject_id,
                                                            LearningModule.lm_no == body.lm_no)):
        raise Conflict("That LM number already exists in this subject.")
    if body.status == "published" and not actor.can("catalog:publish"):
        body.status = "draft"
    lm = LearningModule(**body.model_dump(), published_at=now_utc() if body.status == "published" else None)
    session.add(lm)
    await session.flush()
    await audit.record(session, "lm.created", actor=actor, target_type="learning_module", target_id=lm.id,
                       metadata=body.model_dump(mode="json"))
    return {"id": lm.id}


@router.get("/lms/{lm_id}")
async def lm_admin(lm_id: UUID, _: CurrentUser = Depends(require("catalog:read_admin")),
                   session: AsyncSession = Depends(get_session)) -> dict:
    lm = await session.get(LearningModule, lm_id)
    if lm is None:
        raise NotFound()
    subject = await session.get(Subject, lm.subject_id)
    items = (await session.scalars(select(ContentItem).where(ContentItem.lm_id == lm.id)
                                   .order_by(ContentItem.sort_order))).all()
    versions = (await session.scalars(select(ContentVersion).where(ContentVersion.item_id.in_([i.id for i in items]))
                                      .order_by(ContentVersion.version_no.desc()))).all() if items else []
    res = (await session.scalars(select(Resource).where(Resource.lm_id == lm.id)
                                 .order_by(Resource.sort_order, Resource.created_at))).all()
    los = (await session.scalars(select(Los).where(Los.lm_id == lm.id).order_by(Los.code))).all()
    return {
        "id": lm.id, "lm_no": lm.lm_no, "title": lm.title, "summary": lm.summary, "source_ref": lm.source_ref,
        "status": lm.status, "subject": {"id": subject.id, "code": subject.code, "name": subject.name},
        "topics": [{"id": t.id, "title": t.title, "sort_order": t.sort_order, "status": t.status} for t in lm.topics],
        "los": [{"id": x.id, "code": x.code, "statement": x.statement, "command_word": x.command_word} for x in los],
        "content": [{"id": i.id, "title": i.title, "kind": i.kind, "topic_id": i.topic_id, "sort_order": i.sort_order,
                     "current_published_version_id": i.current_published_version_id,
                     "versions": [{"id": v.id, "version_no": v.version_no, "status": v.status,
                                   "created_at": v.created_at, "published_at": v.published_at,
                                   "provenance": v.provenance, "note": v.note}
                                  for v in versions if v.item_id == i.id]} for i in items],
        "resources": [{"id": r.id, "kind": r.kind, "title": r.title, "status": r.status, "mandatory": r.mandatory,
                       "downloadable": r.downloadable, "provenance": r.provenance, "duration_s": r.duration_s,
                       "size_bytes": r.size_bytes, "url": r.url, "sort_order": r.sort_order,
                       "has_file": bool(r.storage_key), "topic_id": r.topic_id} for r in res],
    }


@router.patch("/lms/{lm_id}")
async def update_lm(lm_id: UUID, body: LmIn, actor: CurrentUser = Depends(require("catalog:write")),
                    session: AsyncSession = Depends(get_session)) -> dict:
    lm = await session.get(LearningModule, lm_id)
    if lm is None:
        raise NotFound()
    if body.status != lm.status and not actor.can("catalog:publish"):
        raise Invalid("Only an admin can change the publication status.")
    if body.status == "published" and lm.status != "published":
        lm.published_at = now_utc()
    for k, v in body.model_dump().items():
        setattr(lm, k, v)
    await audit.record(session, "lm.updated", actor=actor, target_type="learning_module", target_id=lm.id,
                       metadata=body.model_dump(mode="json"))
    return {"id": lm.id}


class TopicIn(In):
    lm_id: UUID
    title: str = Field(min_length=2, max_length=200)
    sort_order: int = 0


@router.post("/topics", status_code=201)
async def create_topic(body: TopicIn, actor: CurrentUser = Depends(require("catalog:write")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    t = Topic(**body.model_dump())
    session.add(t)
    await session.flush()
    await audit.record(session, "topic.created", actor=actor, target_type="topic", target_id=t.id,
                       metadata=body.model_dump(mode="json"))
    return {"id": t.id}


@router.delete("/topics/{tid}")
async def delete_topic(tid: UUID, actor: CurrentUser = Depends(require("catalog:write")),
                       session: AsyncSession = Depends(get_session)) -> dict:
    t = await session.get(Topic, tid)
    if t is None:
        raise NotFound()
    await session.delete(t)
    await audit.record(session, "topic.deleted", actor=actor, target_type="topic", target_id=tid)
    return {"status": "deleted"}


class LosIn(In):
    lm_id: UUID
    code: str = Field(min_length=1, max_length=30)
    statement: str = Field(min_length=5, max_length=1000)
    command_word: str = Field(min_length=3, max_length=30)


@router.post("/los", status_code=201)
async def create_los(body: LosIn, actor: CurrentUser = Depends(require("catalog:write")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    x = Los(**body.model_dump())
    session.add(x)
    await session.flush()
    await audit.record(session, "los.created", actor=actor, target_type="los", target_id=x.id,
                       metadata=body.model_dump(mode="json"))
    return {"id": x.id}


@router.delete("/los/{lid}")
async def delete_los(lid: UUID, actor: CurrentUser = Depends(require("catalog:write")),
                     session: AsyncSession = Depends(get_session)) -> dict:
    x = await session.get(Los, lid)
    if x is None:
        raise NotFound()
    await session.delete(x)
    await audit.record(session, "los.deleted", actor=actor, target_type="los", target_id=lid)
    return {"status": "deleted"}


# ---------- notes content ----------

class ContentItemIn(In):
    lm_id: UUID
    title: str = Field(min_length=2, max_length=200)
    kind: Literal["note", "revision_sheet", "infographic"] = "note"
    topic_id: UUID | None = None
    sort_order: int = 0


@router.post("/content-items", status_code=201)
async def create_item(body: ContentItemIn, actor: CurrentUser = Depends(require("content:write")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    i = ContentItem(**body.model_dump())
    session.add(i)
    await session.flush()
    await audit.record(session, "content_item.created", actor=actor, target_type="content_item", target_id=i.id,
                       metadata=body.model_dump(mode="json"))
    return {"id": i.id}


@router.get("/content-items/{iid}/versions/{vid}")
async def get_version(iid: UUID, vid: UUID, _: CurrentUser = Depends(require("catalog:read_admin")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    v = await session.get(ContentVersion, vid)
    if v is None or v.item_id != iid:
        raise NotFound()
    return {"id": v.id, "version_no": v.version_no, "status": v.status, "body": v.body, "provenance": v.provenance,
            "licence_ref": v.licence_ref, "note": v.note}


class VersionIn(In):
    body: dict[str, Any]
    provenance: Literal["original", "faculty_recording", "licensed_third_party", "reference_only"] = "original"
    licence_ref: str | None = Field(default=None, max_length=60)
    note: str | None = Field(default=None, max_length=500)
    publish: bool = False


@router.post("/content-items/{iid}/versions", status_code=201)
async def new_version(iid: UUID, body: VersionIn, actor: CurrentUser = Depends(require("content:write")),
                      session: AsyncSession = Depends(get_session)) -> dict:
    item = await session.get(ContentItem, iid)
    if item is None:
        raise NotFound()
    v = await content.save_draft(session, item, body.body, actor, body.provenance, body.licence_ref, body.note)
    if body.publish and actor.can("content:publish"):
        await content.publish(session, item, v.id, actor)
    return {"id": v.id, "version_no": v.version_no, "status": v.status}


@router.post("/content-items/{iid}/versions/{vid}/publish")
async def publish_version(iid: UUID, vid: UUID, actor: CurrentUser = Depends(require("content:publish")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    item = await session.get(ContentItem, iid)
    if item is None:
        raise NotFound()
    v = await content.publish(session, item, vid, actor)
    return {"id": v.id, "status": v.status}


# ---------- resources ----------

@router.post("/resources", status_code=201)
async def upload_resource(
    lm_id: UUID = Form(...), kind: Literal["video", "pdf", "class_note", "link"] = Form(...),
    title: str = Form(..., min_length=2, max_length=200), mandatory: bool = Form(True),
    downloadable: bool = Form(False),
    provenance: Literal["original", "faculty_recording", "licensed_third_party", "reference_only"] = Form("original"),
    licence_ref: str | None = Form(None), duration_s: int | None = Form(None), url: str | None = Form(None),
    topic_id: UUID | None = Form(None), sort_order: int = Form(0), file: UploadFile | None = File(None),
    actor: CurrentUser = Depends(require("resource:write")), session: AsyncSession = Depends(get_session),
) -> dict:
    if await session.get(LearningModule, lm_id) is None:
        raise NotFound("LM not found")
    if provenance == "licensed_third_party" and not licence_ref:
        raise Invalid("Licensed material needs a licence reference (C-06).", code="licence_required")
    r = Resource(lm_id=lm_id, kind=kind, title=title, mandatory=mandatory, downloadable=downloadable,
                 provenance=provenance, licence_ref=licence_ref, duration_s=duration_s, topic_id=topic_id,
                 sort_order=sort_order, created_by=actor.id, status="draft")
    if kind == "link":
        if not url or not url.startswith("https://"):
            raise Invalid("Links must start with https://")
        r.url = url
    else:
        if file is None:
            raise Invalid("Attach a file.")
        mime = (file.content_type or "").split(";")[0]
        if mime not in ALLOWED_MIME[kind]:
            raise Invalid(f"File type {mime or 'unknown'} is not allowed for {kind}.", code="bad_file_type")
        head = await file.read(8)
        await file.seek(0)
        if kind != "video" and not head.startswith(b"%PDF"):
            raise Invalid("This does not look like a PDF.", code="bad_file_type")
        st = storage()
        key = st.new_key(f"resources/{lm_id}", file.filename or "upload")
        try:
            r.size_bytes = st.save(key, file.file, get_settings().max_upload_mb * 1024 * 1024)
        except ValueError as exc:
            raise Invalid(f"File is larger than {get_settings().max_upload_mb} MB.") from exc
        r.storage_key, r.mime_type = key, mime
        # TODO(cloud): antivirus scan job (ClamAV) before the resource can be published (S-01 T-08).
    session.add(r)
    await session.flush()
    await audit.record(session, "resource.uploaded", actor=actor, target_type="resource", target_id=r.id,
                       metadata={"kind": kind, "title": title, "provenance": provenance, "size": r.size_bytes})
    return {"id": r.id, "status": r.status}


class ResourcePatch(In):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    mandatory: bool | None = None
    downloadable: bool | None = None
    duration_s: int | None = Field(default=None, ge=1)
    sort_order: int | None = None
    chapters: list[dict] | None = None


@router.patch("/resources/{rid}")
async def update_resource(rid: UUID, body: ResourcePatch, actor: CurrentUser = Depends(require("resource:write")),
                          session: AsyncSession = Depends(get_session)) -> dict:
    r = await session.get(Resource, rid)
    if r is None:
        raise NotFound()
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(r, k, v)
    await audit.record(session, "resource.updated", actor=actor, target_type="resource", target_id=r.id,
                       metadata=data)
    return {"id": r.id}


@router.post("/resources/{rid}/{action}")
async def set_resource_status(rid: UUID, action: Literal["publish", "unpublish"],
                              actor: CurrentUser = Depends(require("resource:publish")),
                              session: AsyncSession = Depends(get_session)) -> dict:
    r = await session.get(Resource, rid)
    if r is None:
        raise NotFound()
    if action == "publish":
        if r.provenance == "licensed_third_party" and not r.licence_ref:
            raise Invalid("Cannot publish licensed material without a licence record.")
        r.status, r.published_at = "published", now_utc()
    else:
        r.status = "retired"
    await audit.record(session, f"resource.{'published' if action == 'publish' else 'retired'}", actor=actor,
                       target_type="resource", target_id=r.id)
    return {"id": r.id, "status": r.status}
