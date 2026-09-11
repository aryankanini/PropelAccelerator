from dataclasses import dataclass
from uuid import NAMESPACE_URL, uuid5

from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.deficiency.ports.deficiency_repository import DeficiencyRepository


@dataclass(frozen=True)
class SegmentationRequest:
    processing_record_id: str
    tag: str
    sod_text: str
    evidence_references: tuple[str, ...]
    correlation_id: str


class DeficiencySegmentationService:
    def __init__(self, repository: DeficiencyRepository) -> None:
        self._repository = repository

    async def segment(
        self,
        request: SegmentationRequest,
    ) -> tuple[DeficiencyCandidate, ...]:
        candidates = tuple(
            self._create_candidate(request, segment)
            for segment in self._segments(request.sod_text)
        )
        await self._repository.save_all(candidates, request.correlation_id)
        return candidates

    @staticmethod
    def _segments(sod_text: str) -> tuple[str, ...]:
        return tuple(segment.strip() for segment in sod_text.split("\n\n") if segment.strip())

    @staticmethod
    def _create_candidate(
        request: SegmentationRequest,
        segment: str,
    ) -> DeficiencyCandidate:
        status = "correction_required" if segment.endswith("?") else "confirmed"
        return DeficiencyCandidate(
            deficiency_id=str(
                uuid5(
                    NAMESPACE_URL,
                    f"deficiency:{request.processing_record_id}:{request.tag}:{segment}",
                )
            ),
            processing_record_id=request.processing_record_id,
            sod_text=segment,
            tag=request.tag,
            evidence_references=request.evidence_references,
            segmentation_status=status,
        )
