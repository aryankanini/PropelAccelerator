from dataclasses import dataclass
from typing import Literal, Protocol

from app.deficiency.domain.segmentation_result import DeficiencyCandidate


PocEligibilityState = Literal["incomplete", "eligible"]


@dataclass(frozen=True)
class PocEligibilityOutcome:
    state: PocEligibilityState
    poc_generation_available: bool
    invalidated_jobs: int


class PocEligibilityRepository(Protocol):
    async def set_eligibility(
        self,
        processing_record_id: str,
        state: PocEligibilityState,
    ) -> None: ...

    async def invalidate_pending_jobs(self, processing_record_id: str) -> int: ...


class DeficiencyEligibilityService:
    def __init__(self, repository: PocEligibilityRepository) -> None:
        self._repository = repository

    async def evaluate(
        self,
        processing_record_id: str,
        candidates: tuple[DeficiencyCandidate, ...],
    ) -> PocEligibilityOutcome:
        if any(candidate.segmentation_status == "confirmed" for candidate in candidates):
            await self._repository.set_eligibility(processing_record_id, "eligible")
            return PocEligibilityOutcome(
                state="eligible",
                poc_generation_available=True,
                invalidated_jobs=0,
            )

        await self._repository.set_eligibility(processing_record_id, "incomplete")
        invalidated_jobs = await self._repository.invalidate_pending_jobs(processing_record_id)
        return PocEligibilityOutcome(
            state="incomplete",
            poc_generation_available=False,
            invalidated_jobs=invalidated_jobs,
        )