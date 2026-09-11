from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol

from app.review.contracts.field_decision import FieldDecision, FieldReviewState


class FieldDecisionAuthorizer(Protocol):
    async def can_review(self, actor_id: str, processing_record_id: str) -> bool: ...


@dataclass(frozen=True)
class ReviewableField:
    field_name: str
    has_source_evidence: bool


@dataclass(frozen=True)
class RecordedFieldDecision:
    processing_record_id: str
    field_name: str
    decision: FieldDecision
    corrected_value: str | None
    reviewer_id: str
    reviewed_at: datetime
    review_state: FieldReviewState


class FieldDecisionRepository(Protocol):
    async def get_field(
        self, processing_record_id: str, field_name: str
    ) -> ReviewableField | None: ...

    async def record(self, decision: RecordedFieldDecision) -> None: ...


@dataclass(frozen=True)
class FieldDecisionOutcome:
    status: Literal["recorded", "access_denied", "not_found", "missing_evidence"]
    decision: RecordedFieldDecision | None = None


class FieldDecisionService:
    def __init__(
        self,
        authorizer: FieldDecisionAuthorizer,
        repository: FieldDecisionRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def record(
        self,
        *,
        actor_id: str,
        processing_record_id: str,
        field_name: str,
        decision: FieldDecision,
        corrected_value: str | None,
        occurred_at: datetime,
    ) -> FieldDecisionOutcome:
        if not await self._authorizer.can_review(actor_id, processing_record_id):
            return FieldDecisionOutcome(status="access_denied")

        field = await self._repository.get_field(processing_record_id, field_name)
        if field is None:
            return FieldDecisionOutcome(status="not_found")
        if not field.has_source_evidence:
            return FieldDecisionOutcome(status="missing_evidence")

        recorded_decision = RecordedFieldDecision(
            processing_record_id=processing_record_id,
            field_name=field_name,
            decision=decision,
            corrected_value=corrected_value,
            reviewer_id=actor_id,
            reviewed_at=occurred_at,
            review_state="verified",
        )
        await self._repository.record(recorded_decision)
        return FieldDecisionOutcome(status="recorded", decision=recorded_decision)