import pytest

from app.processing.adapters.service_bus_worker import ServiceBusWorker
from app.processing.application.dependency_failure_policy import (
    MAX_RETRY_ATTEMPTS,
    TransientLlmFailure,
)
from app.processing.application.job_service import ProcessingJob, ProcessingJobService


class JobRepository:
    def __init__(self) -> None:
        self.records: list[tuple[str, int, str]] = []

    async def record_recoverable_failure(
        self, job_id: str, retry_count: int, reason: str
    ) -> None:
        self.records.append((job_id, retry_count, reason))


class Message:
    def __init__(self) -> None:
        self.deferred: list[int] = []
        self.dead_lettered: list[str] = []

    async def defer(self, retry_delay_seconds: int) -> None:
        self.deferred.append(retry_delay_seconds)

    async def dead_letter(self, reason: str) -> None:
        self.dead_lettered.append(reason)


@pytest.mark.asyncio
async def test_retryable_failure_preserves_unapproved_state_and_records_recovery() -> None:
    repository = JobRepository()
    message = Message()
    job = ProcessingJob('job-1', 'processing', 0, 'unapproved')

    outcome = await ServiceBusWorker(ProcessingJobService(repository)).handle_dependency_failure(
        message, job, TransientLlmFailure('provider outage')
    )

    assert outcome.disposition == 'retry'
    assert job.approval_state == 'unapproved'
    assert repository.records == [('job-1', 1, 'transient_llm_failure')]
    assert message.deferred == [1]
    assert message.dead_lettered == []


@pytest.mark.asyncio
async def test_exhausted_retry_is_dead_lettered_without_approval() -> None:
    repository = JobRepository()
    message = Message()
    job = ProcessingJob('job-1', 'processing', MAX_RETRY_ATTEMPTS, 'unapproved')

    outcome = await ServiceBusWorker(ProcessingJobService(repository)).handle_dependency_failure(
        message, job, TransientLlmFailure('provider outage')
    )

    assert outcome.disposition == 'dead_letter'
    assert job.approval_state == 'unapproved'
    assert repository.records == []
    assert message.dead_lettered == ['transient_llm_retry_exhausted']