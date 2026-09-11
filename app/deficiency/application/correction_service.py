from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


CorrectionOperation = Literal["merge", "split", "create"]


@dataclass(frozen=True)
class CorrectionCommand:
    processing_record_id: str
    operation: CorrectionOperation
    source_deficiency_ids: tuple[str, ...]
    source_boundary: str | None
    actor_id: str
    occurred_at: datetime
    correlation_id: str


@dataclass(frozen=True)
class CorrectionOutcome:
    status: Literal["applied", "access_denied", "invalid_split"]


class DeficiencyCorrectionAuthorizer(Protocol):
    async def can_review(self, actor_id: str) -> bool: ...


class DeficiencyCorrectionRepository(Protocol):
    async def apply_correction(self, command: CorrectionCommand) -> None: ...


class DeficiencyCorrectionService:
    def __init__(
        self,
        authorizer: DeficiencyCorrectionAuthorizer,
        repository: DeficiencyCorrectionRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def correct(self, command: CorrectionCommand) -> CorrectionOutcome:
        if not await self._authorizer.can_review(command.actor_id):
            return CorrectionOutcome(status="access_denied")
        if command.operation == "split" and not command.source_boundary:
            return CorrectionOutcome(status="invalid_split")

        await self._repository.apply_correction(command)
        return CorrectionOutcome(status="applied")