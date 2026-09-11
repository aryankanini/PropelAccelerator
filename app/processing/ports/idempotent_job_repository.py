from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class JobOutcome:
    correlation_id: str
    state: str
    retry_count: int
    failure_reason: str | None
    disposition: Literal["created", "duplicate", "connection_failed"]