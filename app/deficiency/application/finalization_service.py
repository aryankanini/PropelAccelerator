from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import NAMESPACE_URL, uuid5

from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.poc.application.deficiency_eligibility import DeficiencyEligibilityService
from app.processing.ports.idempotent_job_repository import JobOutcome
from app.processing.ports.poc_command_publisher import (
    PocCommandPublisher,
    PocGenerationCommand,
)


class PocJobRepository(Protocol):
    async def persist_or_return(
        self,
        *,
        processing_record_id: str,
        attempt_id: str,
        correlation_id: str,
        state: str,
        retry_count: int,
        failure_reason: str | None,
    ) -> JobOutcome: ...


@dataclass(frozen=True)
class FinalizationOutcome:
    status: Literal["published", "blocked"]
    commands: tuple[PocGenerationCommand, ...]


class DeficiencyFinalizationService:
    def __init__(
        self,
        eligibility_service: DeficiencyEligibilityService,
        job_repository: PocJobRepository,
        publisher: PocCommandPublisher,
    ) -> None:
        self._eligibility_service = eligibility_service
        self._job_repository = job_repository
        self._publisher = publisher

    async def finalize(
        self,
        *,
        processing_record_id: str,
        finalization_id: str,
        correlation_id: str,
        candidates: tuple[DeficiencyCandidate, ...],
    ) -> FinalizationOutcome:
        eligibility = await self._eligibility_service.evaluate(
            processing_record_id,
            candidates,
        )
        if not eligibility.poc_generation_available or any(
            candidate.segmentation_status != "confirmed" for candidate in candidates
        ):
            return FinalizationOutcome(status="blocked", commands=())

        published_commands = []
        for candidate in candidates:
            command = self._command_for(
                processing_record_id,
                finalization_id,
                correlation_id,
                candidate.deficiency_id,
            )
            outcome = await self._job_repository.persist_or_return(
                processing_record_id=processing_record_id,
                attempt_id=command.attempt_id,
                correlation_id=correlation_id,
                state="pending",
                retry_count=0,
                failure_reason=None,
            )
            if outcome.disposition != "created":
                continue
            await self._publisher.publish(command)
            published_commands.append(command)

        return FinalizationOutcome(
            status="published",
            commands=tuple(published_commands),
        )

    @staticmethod
    def _command_for(
        processing_record_id: str,
        finalization_id: str,
        correlation_id: str,
        deficiency_id: str,
    ) -> PocGenerationCommand:
        attempt_id = str(
            uuid5(
                NAMESPACE_URL,
                f"poc:{processing_record_id}:{deficiency_id}:{finalization_id}",
            )
        )
        return PocGenerationCommand(
            job_id=attempt_id,
            attempt_id=attempt_id,
            processing_record_id=processing_record_id,
            deficiency_id=deficiency_id,
            correlation_id=correlation_id,
        )