from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BulkApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    poc_ids: tuple[str, ...] = Field(min_length=1)


class BulkApprovalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    poc_id: str
    status: Literal["approved", "ineligible"]
    reason: str | None = None
    reviewer_id: str | None = None
    approved_at: datetime | None = None


class BulkApprovalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    records: tuple[BulkApprovalRecord, ...]