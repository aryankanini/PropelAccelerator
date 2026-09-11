from dataclasses import dataclass
from typing import Any, Protocol


class PocSourceVersionConnection(Protocol):
    async def execute(self, query: str, *parameters: object) -> None: ...

    async def fetch(self, query: str, *parameters: object) -> list[dict[str, Any]]: ...


@dataclass(frozen=True)
class PocSourceVersion:
    source_id: str
    effective_version: str
    source_set_version: str


class PocSourceVersionRepository:
    _INSERT = """
        INSERT INTO poc_source_set_versions (
            poc_draft_id, source_id, effective_version, source_set_version
        ) VALUES ($1, $2, $3, $4);
    """
    _LIST_FOR_AUDIT = """
        SELECT source_id, effective_version, source_set_version
        FROM poc_source_set_versions
        WHERE poc_draft_id = $1
        ORDER BY source_id, effective_version;
    """

    def __init__(self, connection: PocSourceVersionConnection) -> None:
        self._connection = connection

    async def persist(self, poc_draft_id: str, source: PocSourceVersion) -> None:
        await self._connection.execute(
            self._INSERT,
            poc_draft_id,
            source.source_id,
            source.effective_version,
            source.source_set_version,
        )

    async def list_for_audit(self, poc_draft_id: str) -> tuple[PocSourceVersion, ...]:
        rows = await self._connection.fetch(self._LIST_FOR_AUDIT, poc_draft_id)
        return tuple(
            PocSourceVersion(
                source_id=str(row['source_id']),
                effective_version=row['effective_version'],
                source_set_version=row['source_set_version'],
            )
            for row in rows
        )