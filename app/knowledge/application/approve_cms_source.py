from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


@dataclass(frozen=True)
class PendingCmsSource:
    source_id: str
    effective_version: str | None
    canonical_reference: str
    content_hash: str

    @property
    def is_complete(self) -> bool:
        return bool(self.effective_version and self.canonical_reference and self.content_hash)


class CmsSourceApprovalAuthorizer(Protocol):
    async def can_approve_source(self, actor_id: str) -> bool: ...


class CmsSourceApprovalRepository(Protocol):
    async def get_pending_source(self, source_id: str) -> PendingCmsSource | None: ...

    async def approve_source(
        self, source_id: str, approver_id: str, approved_at: datetime
    ) -> None: ...


@dataclass(frozen=True)
class CmsSourceApprovalOutcome:
    status: Literal['approved', 'access_denied', 'not_found', 'incomplete']
    approver_id: str | None = None
    approved_at: datetime | None = None


class ApproveCmsSourceService:
    def __init__(
        self,
        authorizer: CmsSourceApprovalAuthorizer,
        repository: CmsSourceApprovalRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def approve(
        self, *, actor_id: str, source_id: str, occurred_at: datetime
    ) -> CmsSourceApprovalOutcome:
        if not await self._authorizer.can_approve_source(actor_id):
            return CmsSourceApprovalOutcome(status='access_denied')

        source = await self._repository.get_pending_source(source_id)
        if source is None:
            return CmsSourceApprovalOutcome(status='not_found')
        if not source.is_complete:
            return CmsSourceApprovalOutcome(status='incomplete')

        await self._repository.approve_source(source_id, actor_id, occurred_at)
        return CmsSourceApprovalOutcome(
            status='approved', approver_id=actor_id, approved_at=occurred_at
        )