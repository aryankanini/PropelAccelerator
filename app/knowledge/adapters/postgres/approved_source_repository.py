from typing import Any, Protocol

from app.poc.domain.grounded_request import ApprovedCmsSource


class ApprovedSourceConnection(Protocol):
    async def fetch(self, query: str, *parameters: object) -> list[dict[str, Any]]: ...


class ApprovedSourceRepository:
    _LIST_APPROVED_FOR_TAG = """
        SELECT canonical_id, effective_version, content
        FROM cms_knowledge_sources
        WHERE approval_state = 'approved'
                    AND indexing_state = 'indexed'
          AND applicable_tag = $1
        ORDER BY canonical_id, effective_version DESC;
    """

    def __init__(self, connection: ApprovedSourceConnection) -> None:
        self._connection = connection

    async def list_approved_for_tag(self, tag: str) -> tuple[ApprovedCmsSource, ...]:
        rows = await self._connection.fetch(self._LIST_APPROVED_FOR_TAG, tag)
        return tuple(
            ApprovedCmsSource(
                source_id=row["canonical_id"],
                version=row["effective_version"],
                content=row["content"],
            )
            for row in rows
        )