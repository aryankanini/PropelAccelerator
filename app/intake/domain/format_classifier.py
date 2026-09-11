from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class DetectedFormat(StrEnum):
    FORMAT_1 = "format_1"
    FORMAT_2 = "format_2"
    OPEN_SOURCE = "open_source"


@dataclass(frozen=True)
class ClassificationResult:
    detected_format: DetectedFormat | None
    processing_state: str


class FormatClassifier:
    """Classifies a survey from supplied deterministic marker rules."""

    def __init__(self, marker_rules: Mapping[DetectedFormat, frozenset[str]]) -> None:
        self._marker_rules = marker_rules

    def classify(self, content: str) -> ClassificationResult:
        matches = [
            detected_format
            for detected_format, markers in self._marker_rules.items()
            if any(marker in content for marker in markers)
        ]
        if len(matches) != 1:
            return ClassificationResult(
                detected_format=None,
                processing_state="classification_error",
            )

        return ClassificationResult(
            detected_format=matches[0],
            processing_state="classified",
        )