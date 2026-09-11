from typing import Protocol

from app.processing.application.dependency_failure_policy import DependencyFailureOutcome
from app.processing.application.job_service import ProcessingJob, ProcessingJobService


class ServiceBusMessage(Protocol):
    async def defer(self, retry_delay_seconds: int) -> None: ...

    async def dead_letter(self, reason: str) -> None: ...


class ServiceBusWorker:
    def __init__(self, job_service: ProcessingJobService) -> None:
        self._job_service = job_service

    async def handle_dependency_failure(
        self, message: ServiceBusMessage, job: ProcessingJob, error: Exception
    ) -> DependencyFailureOutcome:
        outcome = await self._job_service.handle_dependency_failure(job, error)
        if outcome.disposition == 'retry':
            if outcome.retry_delay_seconds is None:
                raise RuntimeError('Retry outcome is missing a retry delay.')
            await message.defer(outcome.retry_delay_seconds)
        elif outcome.disposition == 'dead_letter':
            await message.dead_letter(outcome.reason)
        return outcome