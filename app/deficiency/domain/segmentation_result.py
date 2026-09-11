from dataclasses import dataclass
from typing import Literal


SegmentationStatus = Literal["confirmed", "correction_required"]


@dataclass(frozen=True)
class DeficiencyCandidate:
    deficiency_id: str
    processing_record_id: str
    sod_text: str
    tag: str
    evidence_references: tuple[str, ...]
    segmentation_status: SegmentationStatus
