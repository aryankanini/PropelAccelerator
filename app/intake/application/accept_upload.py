from dataclasses import dataclass
from typing import Protocol

from app.intake.application.validate_upload import UploadValidator
from app.intake.contracts.uploads import UploadAcknowledgement
from app.intake.domain.content_inspection import ContentInspector


class AcceptedUploadRepository(Protocol):
    async def create(self, *, processing_record_id: str, content: bytes, media_type: str) -> None: ...


@dataclass(frozen=True)
class UploadCommand:
    actor_id: str
    processing_record_id: str
    content: bytes
    media_type: str


class UploadAcceptanceService:
    def __init__(
        self,
        validator: UploadValidator,
        repository: AcceptedUploadRepository,
    ) -> None:
        self._validator = validator
        self._repository = repository

    async def accept(self, command: UploadCommand) -> UploadAcknowledgement | None:
        validation = await self._validator.validate(
            actor_id=command.actor_id,
            content=command.content,
            declared_media_type=command.media_type,
        )
        if validation.status == "rejected":
            return None

        await self._repository.create(
            processing_record_id=command.processing_record_id,
            content=command.content,
            media_type=command.media_type,
        )
        return UploadAcknowledgement(processing_record_id=command.processing_record_id)