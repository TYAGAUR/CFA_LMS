from pydantic import BaseModel, ConfigDict


class In(BaseModel):
    """Base for request bodies: unknown fields are rejected (S-03 §3 rule 5)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)
