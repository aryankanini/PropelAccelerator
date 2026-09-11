from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CmsSourceInventoryFilter(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    reference: str | None = None
    version: str | None = None
    approval_state: Literal['pending', 'approved', 'conflict', 'retired'] | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class CmsSourceInventoryItem(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    source_id: str
    canonical_reference: str
    effective_version: str | None
    approval_state: Literal['pending', 'approved', 'conflict', 'retired']
    authoritative: bool


class CmsSourceInventoryPage(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    items: tuple[CmsSourceInventoryItem, ...]
    limit: int
    offset: int