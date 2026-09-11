from typing import Protocol

from app.intake.contracts.status import StatusOutcome


class ProcessingStatusAuthorizer(Protocol):
    async def can_view(self, actor_id: str, processing_record_id: str) -> bool: ...


class ProcessingStatusRepository(Protocol):
    async def get(self, processing_record_id: str) -> StatusOutcome | None: ...


class ProcessingStatusQuery:
    def __init__(
        self,
        authorizer: ProcessingStatusAuthorizer,
        repository: ProcessingStatusRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def get(self, *, actor_id: str, processing_record_id: str) -> StatusOutcome:
        if not await self._authorizer.can_view(actor_id, processing_record_id):
            return StatusOutcome(status="access_denied")

        return await self._repository.get(processing_record_id) or StatusOutcome(
            status="not_found"
        )