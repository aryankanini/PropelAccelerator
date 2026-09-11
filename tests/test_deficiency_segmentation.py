import pytest

from app.deficiency.application.segmentation_service import (
    DeficiencySegmentationService,
    SegmentationRequest,
)
from app.deficiency.domain.segmentation_result import DeficiencyCandidate


class RecordingDeficiencyRepository:
    def __init__(self) -> None:
        self.candidates: tuple[DeficiencyCandidate, ...] = ()
        self.correlation_id = ""

    async def save_all(
        self,
        candidates: tuple[DeficiencyCandidate, ...],
        correlation_id: str,
    ) -> None:
        self.candidates = candidates
        self.correlation_id = correlation_id


@pytest.mark.asyncio
async def test_segmentation_creates_a_distinct_confirmed_candidate_per_boundary() -> None:
    repository = RecordingDeficiencyRepository()
    service = DeficiencySegmentationService(repository)

    candidates = await service.segment(
        SegmentationRequest(
            processing_record_id="record-1",
            tag="F600",
            sod_text="First deficiency.\n\nSecond deficiency.",
            evidence_references=("evidence-1",),
            correlation_id="correlation-1",
        )
    )

    assert [candidate.sod_text for candidate in candidates] == [
        "First deficiency.",
        "Second deficiency.",
    ]
    assert all(candidate.segmentation_status == "confirmed" for candidate in candidates)
    assert len({candidate.deficiency_id for candidate in candidates}) == 2
    assert repository.correlation_id == "correlation-1"


@pytest.mark.asyncio
async def test_segmentation_marks_an_ambiguous_boundary_for_correction() -> None:
    repository = RecordingDeficiencyRepository()
    service = DeficiencySegmentationService(repository)

    candidates = await service.segment(
        SegmentationRequest(
            processing_record_id="record-1",
            tag="F600",
            sod_text="Uncertain boundary?",
            evidence_references=("evidence-1",),
            correlation_id="correlation-1",
        )
    )

    assert candidates[0].segmentation_status == "correction_required"