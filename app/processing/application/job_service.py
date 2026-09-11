from dataclasses import dataclass
from typing import Literal, Protocol

from app.processing.application.dependency_failure_policy import (
    DependencyFailureOutcome,
    DependencyFailurePolicy,
)


@dataclass(frozen=True)
class ProcessingJob:
    job_id: str
    state: str
    retry_count: int
    approval_state: Literal['unapproved', 'approved']


class ProcessingJobRepository(Protocol):
    async def record_recoverable_failure(
        self, job_id: str, retry_count: int, reason: str
    ) -> None: ...


class ProcessingJobService:
    def __init__(
        self,
        repository: ProcessingJobRepository,
        policy: DependencyFailurePolicy | None = None,
    ) -> None:
        self._repository = repository
        self._policy = policy or DependencyFailurePolicy()

    async def handle_dependency_failure(
        self, job: ProcessingJob, error: Exception
    ) -> DependencyFailureOutcome:
        outcome = self._policy.evaluate(error, job.retry_count)
        if outcome.disposition == 'retry':
            await self._repository.record_recoverable_failure(
                job.job_id, outcome.retry_count, outcome.reason
            )
        return outcome