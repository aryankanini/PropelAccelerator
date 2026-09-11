from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Protocol

from app.knowledge.application.approve_cms_source import PendingCmsSource
from app.knowledge.application.detect_source_conflicts import SourceScope
from app.knowledge.contracts.cms_source_inventory import (
    CmsSourceInventoryFilter,
    CmsSourceInventoryItem,
)


class CmsSourceConnection(Protocol):
    async def execute(self, query: str, *parameters: object) -> None: ...

    async def fetchrow(self, query: str, *parameters: object) -> dict[str, Any] | None: ...

    async def fetch(self, query: str, *parameters: object) -> list[dict[str, Any]]: ...


@dataclass(frozen=True)
class CmsSourceRecord:
    canonical_id: str
    canonical_reference: str
    content_hash: str
    effective_version: str | None
    applicable_tag: str
    content: str
    approval_state: Literal['pending', 'approved', 'conflict', 'retired']
    indexing_state: Literal['ineligible', 'indexed']


class CmsSourceRepository:
    _INSERT_SOURCE = """
        INSERT INTO cms_knowledge_sources (
            canonical_id, canonical_reference, content_hash, effective_version,
            applicable_tag, content, approval_state, indexing_state
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
    """
    _GET_PENDING_SOURCE = """
        SELECT canonical_id, effective_version, canonical_reference, content_hash
        FROM cms_knowledge_sources
        WHERE canonical_id = $1 AND approval_state = 'pending';
    """
    _APPROVE_SOURCE = """
        UPDATE cms_knowledge_sources
        SET approval_state = 'approved', indexing_state = 'indexed',
            approved_by = $2, approved_at = $3
        WHERE canonical_id = $1 AND approval_state = 'pending';
    """
    _LIST_APPROVED_SOURCES = """
        SELECT canonical_id, applicable_tag, canonical_reference
        FROM cms_knowledge_sources
        WHERE applicable_tag = $1 AND approval_state = 'approved'
          AND indexing_state = 'indexed';
    """
    _HOLD_FOR_CONFLICT = """
        UPDATE cms_knowledge_sources
        SET approval_state = 'conflict', indexing_state = 'ineligible'
        WHERE canonical_id = $1 AND approval_state = 'pending';
    """
    _APPEND_CONFLICT_DECISION = """
        WITH recorded AS (
            INSERT INTO cms_source_conflict_decisions (
                source_id, decision, decided_by, decided_at
            ) VALUES ($1, $2, $3, $4)
        )
        UPDATE cms_knowledge_sources
        SET approval_state = CASE WHEN $2 = 'approve' THEN 'approved' ELSE 'pending' END,
            indexing_state = CASE WHEN $2 = 'approve' THEN 'indexed' ELSE 'ineligible' END,
            approved_by = CASE WHEN $2 = 'approve' THEN $3 ELSE NULL END,
            approved_at = CASE WHEN $2 = 'approve' THEN $4 ELSE NULL END
        WHERE canonical_id = $1;
    """
    _SEARCH = """
        SELECT canonical_id, canonical_reference, effective_version, approval_state
        FROM cms_knowledge_sources
        WHERE ($1::TEXT IS NULL OR canonical_reference ILIKE '%' || $1 || '%')
          AND ($2::TEXT IS NULL OR effective_version = $2)
          AND ($3::TEXT IS NULL OR approval_state = $3)
        ORDER BY canonical_reference, effective_version NULLS LAST, canonical_id
        LIMIT $4 OFFSET $5;
    """

    def __init__(self, connection: CmsSourceConnection) -> None:
        self._connection = connection

    async def save(self, source: CmsSourceRecord) -> None:
        await self._connection.execute(
            self._INSERT_SOURCE,
            source.canonical_id,
            source.canonical_reference,
            source.content_hash,
            source.effective_version,
            source.applicable_tag,
            source.content,
            source.approval_state,
            source.indexing_state,
        )

    async def get_pending_source(self, source_id: str) -> PendingCmsSource | None:
        row = await self._connection.fetchrow(self._GET_PENDING_SOURCE, source_id)
        if row is None:
            return None
        return PendingCmsSource(
            source_id=str(row['canonical_id']),
            effective_version=row['effective_version'],
            canonical_reference=row['canonical_reference'],
            content_hash=row['content_hash'],
        )

    async def approve_source(
        self, source_id: str, approver_id: str, approved_at: datetime
    ) -> None:
        await self._connection.execute(self._APPROVE_SOURCE, source_id, approver_id, approved_at)

    async def list_approved_sources(self, applicable_tag: str) -> tuple[SourceScope, ...]:
        rows = await self._connection.fetch(self._LIST_APPROVED_SOURCES, applicable_tag)
        return tuple(
            SourceScope(
                source_id=str(row['canonical_id']),
                applicable_tag=row['applicable_tag'],
                canonical_reference=row['canonical_reference'],
            )
            for row in rows
        )

    async def hold_for_conflict(
        self, source_id: str, conflicting_source_ids: tuple[str, ...]
    ) -> None:
        await self._connection.execute(self._HOLD_FOR_CONFLICT, source_id)

    async def append_conflict_decision(
        self,
        source_id: str,
        decision: Literal['approve', 'reject'],
        decided_by: str,
        decided_at: datetime,
    ) -> None:
        await self._connection.execute(
            self._APPEND_CONFLICT_DECISION, source_id, decision, decided_by, decided_at
        )

    async def search(
        self, filters: CmsSourceInventoryFilter
    ) -> tuple[CmsSourceInventoryItem, ...]:
        rows = await self._connection.fetch(
            self._SEARCH,
            filters.reference,
            filters.version,
            filters.approval_state,
            filters.limit,
            filters.offset,
        )
        return tuple(
            CmsSourceInventoryItem(
                source_id=str(row['canonical_id']),
                canonical_reference=row['canonical_reference'],
                effective_version=row['effective_version'],
                approval_state=row['approval_state'],
                authoritative=row['approval_state'] == 'approved',
            )
            for row in rows
        )