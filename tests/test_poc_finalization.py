import pytest

from app.deficiency.application.finalization_service import DeficiencyFinalizationService
from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.poc.application.deficiency_eligibility import DeficiencyEligibilityService
from app.processing.adapters.postgres.idempotent_job_repository import JobOutcome


class EligibilityRepository:
    def __init__(self) -> None:
        self.states: list[str] = []
        self.invalidations = 0

    async def set_eligibility(self, processing_record_id: str, state: str) -> None:
        self.states.append(state)

    async def invalidate_pending_jobs(self, processing_record_id: str) -> int:
        self.invalidations += 1
        return 1


class IdempotentJobStore:
    def __init__(self) -> None:
        self.attempt_ids: set[str] = set()

    async def persist_or_return(self, **kwargs: object) -> JobOutcome:
        attempt_id = str(kwargs["attempt_id"])
        created = attempt_id not in self.attempt_ids
        self.attempt_ids.add(attempt_id)
        return JobOutcome(
            correlation_id=str(kwargs["correlation_id"]),
            state="pending",
            retry_count=0,
            failure_reason=None,
            disposition="created" if created else "duplicate",
        )


class Publisher:
    def __init__(self) -> None:
        self.commands: list[object] = []

    async def publish(self, command: object) -> None:
        self.commands.append(command)


def candidate(status: str = "confirmed") -> DeficiencyCandidate:
    return DeficiencyCandidate(
        deficiency_id="deficiency-1",
        processing_record_id="record-1",
        sod_text="Deficiency text.",
        tag="F600",
        evidence_references=("evidence-1",),
        segmentation_status=status,  # type: ignore[arg-type]
    )


@pytest.mark.asyncio
async def test_finalization_publishes_each_confirmed_deficiency_only_once() -> None:
    eligibility_repository = EligibilityRepository()
    publisher = Publisher()
    service = DeficiencyFinalizationService(
        DeficiencyEligibilityService(eligibility_repository),
        IdempotentJobStore(),
        publisher,
    )

    first = await service.finalize(
        processing_record_id="record-1",
        finalization_id="finalization-1",
        correlation_id="correlation-1",
        candidates=(candidate(),),
    )
    repeated = await service.finalize(
        processing_record_id="record-1",
        finalization_id="finalization-1",
        correlation_id="correlation-1",
        candidates=(candidate(),),
    )

    assert len(first.commands) == 1
    assert repeated.commands == ()
    assert len(publisher.commands) == 1


@pytest.mark.asyncio
async def test_ineligible_finalization_invalidates_pending_work_without_publishing() -> None:
    eligibility_repository = EligibilityRepository()
    publisher = Publisher()
    service = DeficiencyFinalizationService(
        DeficiencyEligibilityService(eligibility_repository),
        IdempotentJobStore(),
        publisher,
    )

    outcome = await service.finalize(
        processing_record_id="record-1",
        finalization_id="finalization-1",
        correlation_id="correlation-1",
        candidates=(candidate("correction_required"),),
    )

    assert outcome.status == "blocked"
    assert publisher.commands == []
    assert eligibility_repository.states == ["incomplete"]
    assert eligibility_repository.invalidations == 1