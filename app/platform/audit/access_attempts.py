from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DeniedUploadAttempt:
    actor_id: str


class AccessAttemptRepository(Protocol):
    async def append(self, attempt: DeniedUploadAttempt) -> None: ...


class AccessAttemptAuditService:
    """Records denied upload attempts without retaining document metadata."""

    def __init__(self, repository: AccessAttemptRepository) -> None:
        self._repository = repository

    async def record_denied_upload(self, actor_id: str) -> None:
        await self._repository.append(DeniedUploadAttempt(actor_id=actor_id))