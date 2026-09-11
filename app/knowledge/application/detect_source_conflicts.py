from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceScope:
    source_id: str
    applicable_tag: str
    canonical_reference: str


class SourceConflictRepository(Protocol):
    async def list_approved_sources(self, applicable_tag: str) -> tuple[SourceScope, ...]: ...

    async def hold_for_conflict(self, source_id: str, conflicting_source_ids: tuple[str, ...]) -> None: ...


class DetectSourceConflictsService:
    def __init__(self, repository: SourceConflictRepository) -> None:
        self._repository = repository

    async def detect(self, submitted_source: SourceScope) -> tuple[str, ...]:
        approved_sources = await self._repository.list_approved_sources(
            submitted_source.applicable_tag
        )
        conflicts = tuple(
            source.source_id
            for source in approved_sources
            if source.canonical_reference == submitted_source.canonical_reference
        )
        if conflicts:
            await self._repository.hold_for_conflict(submitted_source.source_id, conflicts)
        return conflicts