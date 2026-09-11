from datetime import datetime
from typing import Literal, Protocol


class SourceConflictResolutionRepository(Protocol):
    async def append_conflict_decision(
        self,
        source_id: str,
        decision: Literal['approve', 'reject'],
        decided_by: str,
        decided_at: datetime,
    ) -> None: ...


class ResolveSourceConflictService:
    def __init__(self, repository: SourceConflictResolutionRepository) -> None:
        self._repository = repository

    async def resolve(
        self,
        *,
        source_id: str,
        decision: Literal['approve', 'reject'],
        actor_id: str,
        occurred_at: datetime,
    ) -> None:
        await self._repository.append_conflict_decision(
            source_id, decision, actor_id, occurred_at
        )