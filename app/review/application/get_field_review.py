from typing import Protocol

from app.review.contracts.field_review import (
    ExtractedFieldDraft,
    FieldReviewField,
    FieldReviewOutcome,
    FieldReviewResponse,
)


class EvidenceRetrievalError(RuntimeError):
    """Raised when stored evidence cannot be resolved for staff review."""


class FieldReviewAuthorizer(Protocol):
    async def can_view(self, actor_id: str, processing_record_id: str) -> bool: ...


class ExtractedFieldReviewRepository(Protocol):
    async def get_for_review(
        self, processing_record_id: str
    ) -> tuple[ExtractedFieldDraft, ...] | None: ...


class EvidenceResolver(Protocol):
    async def resolve(self, locator: str) -> str: ...


class FieldReviewQuery:
    def __init__(
        self,
        authorizer: FieldReviewAuthorizer,
        repository: ExtractedFieldReviewRepository,
        evidence_resolver: EvidenceResolver,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository
        self._evidence_resolver = evidence_resolver

    async def get(
        self, *, actor_id: str, processing_record_id: str
    ) -> FieldReviewOutcome:
        if not await self._authorizer.can_view(actor_id, processing_record_id):
            return FieldReviewOutcome(status="access_denied")

        drafts = await self._repository.get_for_review(processing_record_id)
        if drafts is None:
            return FieldReviewOutcome(status="not_found")

        fields = tuple([await self._build_field(draft) for draft in drafts])
        return FieldReviewOutcome(
            status="authorized",
            review=FieldReviewResponse(
                processing_record_id=processing_record_id,
                fields=fields,
            ),
        )

    async def _build_field(self, draft: ExtractedFieldDraft) -> FieldReviewField:
        if draft.evidence_locator is None:
            return self._unresolved_field(draft)

        try:
            source_evidence_locator = await self._evidence_resolver.resolve(
                draft.evidence_locator
            )
        except EvidenceRetrievalError:
            return self._unresolved_field(draft)

        return FieldReviewField(
            field_name=draft.field_name,
            value=draft.value,
            confidence_state=draft.confidence_state,
            evidence_state="resolved",
            source_evidence_locator=source_evidence_locator,
            approval_eligible=True,
        )

    @staticmethod
    def _unresolved_field(draft: ExtractedFieldDraft) -> FieldReviewField:
        return FieldReviewField(
            field_name=draft.field_name,
            value=draft.value,
            confidence_state=draft.confidence_state,
            evidence_state="unresolved",
            source_evidence_locator=None,
            approval_eligible=False,
        )