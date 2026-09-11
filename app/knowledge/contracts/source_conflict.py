from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class SourceConflictResolution(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    source_id: str
    decision: Literal['approve', 'reject']
    occurred_at: datetime


class SourceConflictDecision(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    source_id: str
    decision: Literal['pending', 'approve', 'reject']
    decided_by: str | None = None
    decided_at: datetime | None = None