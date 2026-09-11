from dataclasses import dataclass
from typing import Literal

from app.deficiency.domain.segmentation_result import DeficiencyCandidate


@dataclass(frozen=True)
class ApprovedCmsSource:
    source_id: str
    version: str
    content: str
    approved: bool = True


@dataclass(frozen=True)
class GroundedPocRequest:
    deficiency: DeficiencyCandidate
    sources: tuple[ApprovedCmsSource, ...]
    source_set_version: str


@dataclass(frozen=True)
class GroundedRequestOutcome:
    status: Literal["grounded", "blocked"]
    request: GroundedPocRequest | None = None
    reason: Literal["no_approved_sources", "deficiency_not_confirmed"] | None = None