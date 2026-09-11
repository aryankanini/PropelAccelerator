from datetime import UTC, datetime

import pytest

from app.knowledge.application.approve_cms_source import (
    ApproveCmsSourceService,
    PendingCmsSource,
)
from app.knowledge.application.detect_source_conflicts import (
    DetectSourceConflictsService,
    SourceScope,
)
from app.knowledge.application.resolve_source_conflict import (
    ResolveSourceConflictService,
)
from app.knowledge.application.search_cms_sources import SearchCmsSourcesService
from app.knowledge.contracts.cms_source_inventory import (
    CmsSourceInventoryFilter,
    CmsSourceInventoryItem,
)


class Authorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_approve_source(self, actor_id: str) -> bool:
        return self._allowed

    async def can_view_sources(self, actor_id: str) -> bool:
        return self._allowed


class ApprovalRepository:
    def __init__(self, source: PendingCmsSource | None) -> None:
        self._source = source
        self.lookups: list[str] = []
        self.approvals: list[tuple[str, str, datetime]] = []

    async def get_pending_source(self, source_id: str) -> PendingCmsSource | None:
        self.lookups.append(source_id)
        return self._source

    async def approve_source(
        self, source_id: str, approver_id: str, approved_at: datetime
    ) -> None:
        self.approvals.append((source_id, approver_id, approved_at))


class ConflictRepository:
    def __init__(self, sources: tuple[SourceScope, ...]) -> None:
        self._sources = sources
        self.held: list[tuple[str, tuple[str, ...]]] = []
        self.decisions: list[tuple[str, str, str, datetime]] = []

    async def list_approved_sources(self, applicable_tag: str) -> tuple[SourceScope, ...]:
        return self._sources

    async def hold_for_conflict(self, source_id: str, conflicts: tuple[str, ...]) -> None:
        self.held.append((source_id, conflicts))

    async def append_conflict_decision(
        self, source_id: str, decision: str, decided_by: str, decided_at: datetime
    ) -> None:
        self.decisions.append((source_id, decision, decided_by, decided_at))


class InventoryRepository:
    async def search(
        self, filters: CmsSourceInventoryFilter
    ) -> tuple[CmsSourceInventoryItem, ...]:
        return (
            CmsSourceInventoryItem(
                source_id='source-1',
                canonical_reference='cms:F600',
                effective_version='2026.1',
                approval_state='approved',
                authoritative=True,
            ),
        )


@pytest.mark.asyncio
async def test_approval_denies_access_before_loading_the_source() -> None:
    repository = ApprovalRepository(PendingCmsSource('source-1', 'v1', 'cms:F600', 'a'))

    outcome = await ApproveCmsSourceService(Authorizer(False), repository).approve(
        actor_id='staff-1', source_id='source-1', occurred_at=datetime.now(UTC)
    )

    assert outcome.status == 'access_denied'
    assert repository.lookups == []


@pytest.mark.asyncio
async def test_approval_requires_complete_source_metadata() -> None:
    repository = ApprovalRepository(PendingCmsSource('source-1', None, 'cms:F600', 'a'))

    outcome = await ApproveCmsSourceService(Authorizer(True), repository).approve(
        actor_id='staff-1', source_id='source-1', occurred_at=datetime.now(UTC)
    )

    assert outcome.status == 'incomplete'
    assert repository.approvals == []


@pytest.mark.asyncio
async def test_conflicting_source_is_held_and_resolution_history_is_appended() -> None:
    repository = ConflictRepository((SourceScope('approved-1', 'F600', 'cms:F600'),))
    conflicts = await DetectSourceConflictsService(repository).detect(
        SourceScope('submitted-1', 'F600', 'cms:F600')
    )
    occurred_at = datetime(2026, 9, 11, tzinfo=UTC)
    await ResolveSourceConflictService(repository).resolve(
        source_id='submitted-1', decision='reject', actor_id='staff-1', occurred_at=occurred_at
    )

    assert conflicts == ('approved-1',)
    assert repository.held == [('submitted-1', ('approved-1',))]
    assert repository.decisions == [('submitted-1', 'reject', 'staff-1', occurred_at)]


@pytest.mark.asyncio
async def test_inventory_search_is_authorized_and_preserves_requested_page_bounds() -> None:
    filters = CmsSourceInventoryFilter(limit=25, offset=50)
    page = await SearchCmsSourcesService(Authorizer(True), InventoryRepository()).search(
        actor_id='staff-1', filters=filters
    )

    assert page is not None
    assert page.limit == 25
    assert page.offset == 50
    assert page.items[0].authoritative is True