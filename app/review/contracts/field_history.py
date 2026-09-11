from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


ContentAttribution = Literal["ai", "staff"]
ApprovalStatus = Literal["approved", "rejected", "pending"]


class FieldRevisionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    revision_id: str
    attribution: ContentAttribution
    reviewer_id: str | None
    reviewed_at: datetime
    content_change: str
    approval_status: ApprovalStatus


class FieldHistoryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    processing_record_id: str
    field_name: str
    revisions: tuple[FieldRevisionResponse, ...]