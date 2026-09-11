from typing import Protocol
from uuid import NAMESPACE_URL, uuid5

from app.intake.contracts.extraction_command import ExtractionCommand
from app.intake.domain.format_classifier import DetectedFormat
from app.intake.domain.scheduling_state import SchedulingState


class ExtractionScheduleRepository(Protocol):
    async def persist(
        self,
        command: ExtractionCommand,
        state: SchedulingState,
    ) -> None: ...

    async def transition(
        self,
        job_id: str,
        state: SchedulingState,
    ) -> None: ...


class ExtractionQueue(Protocol):
    async def publish(self, command: ExtractionCommand) -> None: ...


class ExtractionSchedulingService:
    def __init__(
        self,
        repository: ExtractionScheduleRepository,
        queue: ExtractionQueue,
    ) -> None:
        self._repository = repository
        self._queue = queue

    async def schedule(
        self,
        *,
        processing_record_id: str,
        correlation_id: str,
        detected_format: DetectedFormat | None,
    ) -> SchedulingState:
        if detected_format is None:
            return SchedulingState.RETRYABLE

        command = ExtractionCommand(
            job_id=str(uuid5(NAMESPACE_URL, f"extraction:{processing_record_id}")),
            processing_record_id=processing_record_id,
            correlation_id=correlation_id,
        )
        await self._repository.persist(command, SchedulingState.PENDING)
        try:
            await self._queue.publish(command)
        except Exception:
            await self._repository.transition(command.job_id, SchedulingState.RETRYABLE)
            return SchedulingState.RETRYABLE

        await self._repository.transition(command.job_id, SchedulingState.PUBLISHED)
        return SchedulingState.PUBLISHED