from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CmsSourceApprovalCommand(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    source_id: str
    occurred_at: datetime


class CmsSourceApprovalResult(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    source_id: str
    status: Literal['approved', 'access_denied', 'not_found', 'incomplete']
    approver_id: str | None = None
    approved_at: datetime | None = None