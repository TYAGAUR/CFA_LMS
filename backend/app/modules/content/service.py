"""Notes block schema `notes/v1` (A-03 §5) and versioned publishing (ADR-007)."""

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import Conflict, Invalid, NotFound
from app.core.timeutil import now_utc
from app.modules.audit import service as audit
from app.modules.content.models import ContentItem, ContentVersion

ALLOWED_LINK_PREFIXES = ("https://",)


class _B(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Inline(_B):
    t: str = Field(max_length=5000)
    b: bool | None = None
    i: bool | None = None
    sub: bool | None = None
    sup: bool | None = None
    link: str | None = None

    @field_validator("link")
    @classmethod
    def _https(cls, v: str | None) -> str | None:
        if v and not v.startswith(ALLOWED_LINK_PREFIXES):
            raise ValueError("links must be https")
        return v


class Heading(_B):
    type: Literal["heading"]
    level: Literal[2, 3, 4] = 3
    text: str = Field(max_length=300)


class Paragraph(_B):
    type: Literal["paragraph"]
    inline: list[Inline]


class ListBlock(_B):
    type: Literal["list"]
    ordered: bool = False
    items: list[list[Inline]]


class Table(_B):
    type: Literal["table"]
    header: list[str]
    rows: list[list[str]]


class Callout(_B):
    type: Literal["callout"]
    variant: Literal["example", "watch_out", "formula", "fun", "note"]
    title: str = Field(max_length=120)
    inline: list[Inline]


class InfographicRow(_B):
    label: str
    text: str
    pct: int = Field(ge=0, le=100)


class Infographic(_B):
    type: Literal["infographic"]
    kind: Literal["waterfall"]
    data: list[InfographicRow]
    alt: str = Field(min_length=3)


class Image(_B):
    type: Literal["image"]
    resource_id: UUID
    alt: str = Field(min_length=3)
    caption: str = ""


Block = Annotated[Heading | Paragraph | ListBlock | Table | Callout | Infographic | Image,
                  Field(discriminator="type")]


class NotesDoc(_B):
    schema_: Literal["notes/v1"] = Field(alias="schema")
    blocks: list[Block]


def validate_body(body: dict[str, Any]) -> dict[str, Any]:
    try:
        doc = NotesDoc.model_validate(body)
    except ValidationError as exc:
        errors = [{"loc": list(map(str, e["loc"])), "msg": e["msg"]} for e in exc.errors()]
        raise Invalid("Content does not match the notes/v1 schema.", code="invalid_content",
                      meta={"errors": errors}) from exc
    return doc.model_dump(by_alias=True, exclude_none=True, mode="json")


def plain_text(body: dict[str, Any]) -> str:
    parts: list[str] = []
    for b in body.get("blocks", []):
        if "text" in b:
            parts.append(b["text"])
        if "title" in b:
            parts.append(b["title"])
        for il in b.get("inline", []):
            parts.append(il["t"])
        for item in b.get("items", []):
            parts.extend(il["t"] for il in item)
        if b.get("type") == "table":
            parts.extend(b["header"])
            parts.extend(c for row in b["rows"] for c in row)
        for d in b.get("data", []):
            parts.extend([d["label"], d["text"]])
    return " ".join(parts)


async def save_draft(session: AsyncSession, item: ContentItem, body: dict, actor, provenance: str,
                     licence_ref: str | None, note: str | None) -> ContentVersion:
    body = validate_body(body)
    if provenance == "licensed_third_party" and not licence_ref:
        raise Invalid("Licensed content needs a licence reference (C-06).", code="licence_required")
    n = (await session.scalar(select(func.max(ContentVersion.version_no)).where(ContentVersion.item_id == item.id))
         or 0) + 1
    v = ContentVersion(item_id=item.id, version_no=n, body=body, plain_text=plain_text(body), status="draft",
                       provenance=provenance, licence_ref=licence_ref, author_id=getattr(actor, "id", None),
                       created_at=now_utc(), note=note)
    session.add(v)
    await session.flush()
    await audit.record(session, "content_version.created", actor=actor, target_type="content_item",
                       target_id=item.id, metadata={"version_no": n})
    return v


async def publish(session: AsyncSession, item: ContentItem, version_id: UUID, actor) -> ContentVersion:
    v = await session.get(ContentVersion, version_id)
    if v is None or v.item_id != item.id:
        raise NotFound()
    if v.status == "published":
        raise Conflict("This version is already published.")
    if item.current_published_version_id:
        old = await session.get(ContentVersion, item.current_published_version_id)
        if old:
            old.status = "retired"
    v.status, v.published_at = "published", now_utc()
    v.reviewer_id = getattr(actor, "id", None)
    item.current_published_version_id = v.id
    await audit.record(session, "content_version.published", actor=actor, target_type="content_item",
                       target_id=item.id, metadata={"version_no": v.version_no})
    return v
