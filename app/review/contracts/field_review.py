from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict


ConfidenceState = Literal["high_confidence", "low_confidence", "incomplete"]
EvidenceState = Literal["resolved", "unresolved"]


@dataclass(frozen=True)
class ExtractedFieldDraft:
    field_name: str
    value: str | None
    confidence_state: ConfidenceState
    evidence_locator: str | None


class FieldReviewField(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    field_name: str
    value: str | None
    confidence_state: ConfidenceState
    evidence_state: EvidenceState
    source_evidence_locator: str | None
    approval_eligible: bool


class FieldReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    processing_record_id: str
    fields: tuple[FieldReviewField, ...]


@dataclass(frozen=True)
class FieldReviewOutcome:
    status: Literal["authorized", "access_denied", "not_found"]
    review: FieldReviewResponse | None = None