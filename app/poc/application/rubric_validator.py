from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class PocRubricResult:
    quality_score: float
    required_element_results: dict[str, bool]
    status: Literal["ready_for_review", "blocked"]
    missing_elements: tuple[str, ...]


class PocRubricValidator:
    def __init__(self, required_elements: tuple[str, ...]) -> None:
        self._required_elements = required_elements

    def validate(self, elements: dict[str, str]) -> PocRubricResult:
        results = {
            element: bool(elements.get(element, "").strip())
            for element in self._required_elements
        }
        missing_elements = tuple(element for element, present in results.items() if not present)
        quality_score = sum(results.values()) / len(results) if results else 1.0
        return PocRubricResult(
            quality_score=quality_score,
            required_element_results=results,
            status="blocked" if missing_elements else "ready_for_review",
            missing_elements=missing_elements,
        )