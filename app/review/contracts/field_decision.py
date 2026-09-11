from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator


FieldDecision = Literal["accepted", "corrected"]
FieldReviewState = Literal["verified", "unresolved"]


class FieldDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    decision: FieldDecision
    corrected_value: str | None = None
    occurred_at: datetime

    @model_validator(mode="after")
    def require_value_for_correction(self) -> "FieldDecisionRequest":
        if self.decision == "corrected" and not self.corrected_value:
            raise ValueError("A corrected decision requires a replacement value.")
        return self


class FieldDecisionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    processing_record_id: str
    field_name: str
    review_state: FieldReviewState
    reviewer_id: str
    reviewed_at: datetime