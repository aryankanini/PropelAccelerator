from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PocGenerationCommand:
    job_id: str
    attempt_id: str
    processing_record_id: str
    deficiency_id: str
    correlation_id: str


class PocCommandPublisher(Protocol):
    async def publish(self, command: PocGenerationCommand) -> None: ...