from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol

from app.review.contracts.field_history import (
    ApprovalStatus,
    ContentAttribution,
    FieldHistoryResponse,
    FieldRevisionResponse,
)


class FieldHistoryAuthorizer(Protocol):
    async def can_view(self, actor_id: str, processing_record_id: str) -> bool: ...


@dataclass(frozen=True)
class FieldRevision:
    revision_id: str
    attribution: ContentAttribution
    reviewer_id: str | None
    reviewed_at: datetime
    content_change: str
    approval_status: ApprovalStatus


class FieldHistoryRepository(Protocol):
    async def list_revisions(
        self, processing_record_id: str, field_name: str
    ) -> tuple[FieldRevision, ...] | None: ...


@dataclass(frozen=True)
class FieldHistoryOutcome:
    status: Literal["authorized", "access_denied", "not_found"]
    history: FieldHistoryResponse | None = None


class FieldHistoryQuery:
    def __init__(
        self,
        authorizer: FieldHistoryAuthorizer,
        repository: FieldHistoryRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def get(
        self, *, actor_id: str, processing_record_id: str, field_name: str
    ) -> FieldHistoryOutcome:
        if not await self._authorizer.can_view(actor_id, processing_record_id):
            return FieldHistoryOutcome(status="access_denied")

        revisions = await self._repository.list_revisions(
            processing_record_id, field_name
        )
        if revisions is None:
            return FieldHistoryOutcome(status="not_found")

        return FieldHistoryOutcome(
            status="authorized",
            history=FieldHistoryResponse(
                processing_record_id=processing_record_id,
                field_name=field_name,
                revisions=tuple(
                    FieldRevisionResponse(
                        revision_id=revision.revision_id,
                        attribution=revision.attribution,
                        reviewer_id=revision.reviewer_id,
                        reviewed_at=revision.reviewed_at,
                        content_change=revision.content_change,
                        approval_status=revision.approval_status,
                    )
                    for revision in revisions
                ),
            ),
        )