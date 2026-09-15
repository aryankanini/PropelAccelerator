from dataclasses import dataclass
from typing import Literal, Protocol


QueueStageKey = Literal["verification", "blocked"]


@dataclass(frozen=True)
class ProcessingQueueItem:
    processing_record_id: str
    provider: str
    format: str
    stage: str
    stage_key: QueueStageKey
    action: str
    review_url: str


class ProcessingQueueRepository(Protocol):
    async def list_requiring_review(self) -> tuple[ProcessingQueueItem, ...]: ...


class ProcessingQueueQuery:
    def __init__(self, repository: ProcessingQueueRepository) -> None:
        self._repository = repository

    async def get(self) -> tuple[ProcessingQueueItem, ...]:
        return await self._repository.list_requiring_review()