from typing import Protocol

from app.deficiency.contracts.inventory import (
    DeficiencyInventoryResponse,
    InventoryCandidate,
)
from app.deficiency.domain.segmentation_result import DeficiencyCandidate


class DeficiencyInventoryRepository(Protocol):
    async def list_for_record(
        self,
        processing_record_id: str,
    ) -> tuple[DeficiencyCandidate, ...]: ...


class DeficiencyInventoryQuery:
    def __init__(self, repository: DeficiencyInventoryRepository) -> None:
        self._repository = repository

    async def get(self, processing_record_id: str) -> DeficiencyInventoryResponse:
        candidates = await self._repository.list_for_record(processing_record_id)
        return DeficiencyInventoryResponse(
            processing_record_id=processing_record_id,
            status="complete" if candidates else "incomplete",
            candidates=tuple(
                InventoryCandidate(
                    deficiency_id=candidate.deficiency_id,
                    sod_text=candidate.sod_text,
                    tag=candidate.tag,
                    evidence_references=candidate.evidence_references,
                    segmentation_status=candidate.segmentation_status,
                )
                for candidate in candidates
            ),
            poc_generation_available=bool(candidates),
        )