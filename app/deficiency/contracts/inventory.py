from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.deficiency.domain.segmentation_result import SegmentationStatus


class InventoryCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    deficiency_id: str
    sod_text: str
    tag: str
    evidence_references: tuple[str, ...]
    segmentation_status: SegmentationStatus


class DeficiencyInventoryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    processing_record_id: str
    status: Literal["complete", "incomplete"]
    candidates: tuple[InventoryCandidate, ...]
    poc_generation_available: bool