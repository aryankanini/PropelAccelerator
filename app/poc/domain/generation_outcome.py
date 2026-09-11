from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class PocGenerationOutcome:
    status: Literal["persisted", "blocked", "failed"]
    deficiency_id: str
    draft_id: str | None = None
    error: str | None = None
    manual_drafting_available: bool = False