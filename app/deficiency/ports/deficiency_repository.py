from typing import Protocol

from app.deficiency.domain.segmentation_result import DeficiencyCandidate


class DeficiencyRepository(Protocol):
    async def save_all(
        self,
        candidates: tuple[DeficiencyCandidate, ...],
        correlation_id: str,
    ) -> None: ...
