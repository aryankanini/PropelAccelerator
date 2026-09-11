from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ProcessingStatus:
    detected_format: str | None
    processing_state: str


@dataclass(frozen=True)
class StatusOutcome:
    status: Literal["authorized", "access_denied", "not_found"]
    processing_status: ProcessingStatus | None = None