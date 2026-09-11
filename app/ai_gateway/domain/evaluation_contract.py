from dataclasses import dataclass
from typing import Literal


EvaluationCategory = Literal[
    "extraction",
    "sod_recall",
    "citation_support",
    "poc_quality",
    "refusal",
    "conditional_fields",
]

REQUIRED_EVALUATION_CATEGORIES: tuple[EvaluationCategory, ...] = (
    "extraction",
    "sod_recall",
    "citation_support",
    "poc_quality",
    "refusal",
    "conditional_fields",
)


@dataclass(frozen=True)
class EvaluationResult:
    category: EvaluationCategory
    score: float


@dataclass(frozen=True)
class ReleaseDecision:
    status: Literal["eligible", "blocked"]
    missing_categories: tuple[EvaluationCategory, ...]
    test_set_version: str
    candidate_identity: str