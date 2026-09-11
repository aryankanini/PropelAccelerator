from dataclasses import dataclass
from typing import Literal, Protocol

from app.intake.domain.content_inspection import ContentInspector


class IntakeAuthorizer(Protocol):
    async def can_upload(self, actor_id: str) -> bool: ...


class AccessAttemptAudit(Protocol):
    async def record_denied_upload(self, actor_id: str) -> None: ...


@dataclass(frozen=True)
class UploadValidationResult:
    status: Literal["accepted", "rejected"]
    error_code: str | None = None


class UploadValidator:
    def __init__(
        self,
        authorizer: IntakeAuthorizer,
        access_attempt_audit: AccessAttemptAudit,
        content_inspector: ContentInspector,
    ) -> None:
        self._authorizer = authorizer
        self._access_attempt_audit = access_attempt_audit
        self._content_inspector = content_inspector

    async def validate(
        self,
        *,
        actor_id: str,
        content: bytes,
        declared_media_type: str,
    ) -> UploadValidationResult:
        if not await self._authorizer.can_upload(actor_id):
            await self._access_attempt_audit.record_denied_upload(actor_id)
            return UploadValidationResult(status="rejected", error_code="access_denied")

        inspection = self._content_inspector.inspect(content, declared_media_type)
        if not inspection.is_supported:
            return UploadValidationResult(
                status="rejected",
                error_code="unsupported_or_unreadable_content",
            )

        return UploadValidationResult(status="accepted")