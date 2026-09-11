import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.intake.application.accept_upload import UploadAcceptanceService, UploadCommand
from app.intake.application.classify_upload import UploadClassificationService
from app.intake.application.get_processing_status import ProcessingStatusQuery
from app.intake.application.schedule_extraction import ExtractionSchedulingService
from app.intake.application.validate_upload import UploadValidator
from app.intake.api.status import create_status_router
from app.intake.api.uploads import create_upload_router
from app.intake.contracts.status import ProcessingStatus, StatusOutcome
from app.intake.domain.content_inspection import ContentInspector
from app.intake.domain.format_classifier import DetectedFormat, FormatClassifier
from app.intake.domain.scheduling_state import SchedulingState
from app.platform.audit.access_attempts import (
    AccessAttemptAuditService,
    DeniedUploadAttempt,
)


class AllowingAuthorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_upload(self, actor_id: str) -> bool:
        return self._allowed

    async def can_view(self, actor_id: str, processing_record_id: str) -> bool:
        return self._allowed


class RecordingAudit:
    def __init__(self) -> None:
        self.actor_ids: list[str] = []

    async def record_denied_upload(self, actor_id: str) -> None:
        self.actor_ids.append(actor_id)


class AccessAttemptRepository:
    def __init__(self) -> None:
        self.attempts: list[DeniedUploadAttempt] = []

    async def append(self, attempt: DeniedUploadAttempt) -> None:
        self.attempts.append(attempt)


class RecordingUploadRepository:
    def __init__(self) -> None:
        self.items: list[UploadCommand] = []

    async def create(self, **kwargs: object) -> None:
        self.items.append(UploadCommand(actor_id="", **kwargs))


class RecordingClassificationRepository:
    def __init__(self) -> None:
        self.results: list[dict[str, str | None]] = []

    async def set_classification(self, **kwargs: str | None) -> None:
        self.results.append(kwargs)


class StatusRepository:
    async def get(self, processing_record_id: str) -> StatusOutcome | None:
        return StatusOutcome(
            status="authorized",
            processing_status=ProcessingStatus(
                detected_format="format_1",
                processing_state="classification_error",
            ),
        )


class RecordingScheduleRepository:
    def __init__(self) -> None:
        self.events: list[tuple[str, SchedulingState]] = []
        self.command = None

    async def persist(self, command: object, state: SchedulingState) -> None:
        self.command = command
        self.events.append(("persist", state))

    async def transition(self, job_id: str, state: SchedulingState) -> None:
        self.events.append(("transition", state))


class Queue:
    def __init__(self, failure: Exception | None = None) -> None:
        self.failure = failure
        self.commands: list[object] = []

    async def publish(self, command: object) -> None:
        if self.failure:
            raise self.failure
        self.commands.append(command)


def validator(allowed: bool = True) -> tuple[UploadValidator, RecordingAudit]:
    audit = RecordingAudit()
    return (
        UploadValidator(
            AllowingAuthorizer(allowed),
            audit,
            ContentInspector({"application/pdf": b"%PDF-"}),
        ),
        audit,
    )


@pytest.mark.asyncio
async def test_upload_rejects_empty_content_before_repository_persistence() -> None:
    upload_validator, _ = validator()
    repository = RecordingUploadRepository()
    service = UploadAcceptanceService(upload_validator, repository)

    result = await service.accept(
        UploadCommand("staff-1", "record-1", b"", "application/pdf")
    )

    assert result is None
    assert repository.items == []


@pytest.mark.asyncio
async def test_upload_rejects_extension_spoofed_content() -> None:
    upload_validator, _ = validator()

    result = await upload_validator.validate(
        actor_id="staff-1",
        content=b"not-a-pdf",
        declared_media_type="application/pdf",
    )

    assert result.error_code == "unsupported_or_unreadable_content"


@pytest.mark.asyncio
async def test_unauthorized_upload_is_audited_without_inspection_outcome() -> None:
    upload_validator, audit = validator(allowed=False)

    result = await upload_validator.validate(
        actor_id="staff-1",
        content=b"%PDF-survey",
        declared_media_type="application/pdf",
    )

    assert result.error_code == "access_denied"
    assert audit.actor_ids == ["staff-1"]


@pytest.mark.asyncio
async def test_access_attempt_audit_records_only_the_denied_actor() -> None:
    repository = AccessAttemptRepository()
    audit = AccessAttemptAuditService(repository)

    await audit.record_denied_upload("staff-1")

    assert repository.attempts == [DeniedUploadAttempt(actor_id="staff-1")]


@pytest.mark.asyncio
async def test_classification_persists_an_error_state_for_conflicting_markers() -> None:
    repository = RecordingClassificationRepository()
    service = UploadClassificationService(
        FormatClassifier(
            {
                DetectedFormat.FORMAT_1: frozenset({"one"}),
                DetectedFormat.FORMAT_2: frozenset({"two"}),
            }
        ),
        repository,
    )

    result = await service.classify(processing_record_id="record-1", content="one two")

    assert result.detected_format is None
    assert repository.results[0]["processing_state"] == "classification_error"


@pytest.mark.asyncio
async def test_status_denies_access_without_loading_record_metadata() -> None:
    query = ProcessingStatusQuery(AllowingAuthorizer(False), StatusRepository())

    result = await query.get(actor_id="staff-1", processing_record_id="record-1")

    assert result == StatusOutcome(status="access_denied")


@pytest.mark.asyncio
async def test_status_returns_error_state_without_approved_representation() -> None:
    query = ProcessingStatusQuery(AllowingAuthorizer(True), StatusRepository())

    result = await query.get(actor_id="staff-1", processing_record_id="record-1")

    assert result.processing_status is not None
    assert result.processing_status.processing_state == "classification_error"


@pytest.mark.asyncio
async def test_scheduling_persists_pending_command_before_publication() -> None:
    repository = RecordingScheduleRepository()
    queue = Queue()
    service = ExtractionSchedulingService(repository, queue)

    result = await service.schedule(
        processing_record_id="record-1",
        correlation_id="correlation-1",
        detected_format=DetectedFormat.FORMAT_1,
    )

    assert result == SchedulingState.PUBLISHED
    assert repository.events == [
        ("persist", SchedulingState.PENDING),
        ("transition", SchedulingState.PUBLISHED),
    ]
    assert queue.commands[0].processing_record_id == "record-1"
    assert queue.commands[0].correlation_id == "correlation-1"


@pytest.mark.asyncio
async def test_scheduling_marks_publication_failure_retryable() -> None:
    repository = RecordingScheduleRepository()
    service = ExtractionSchedulingService(repository, Queue(ConnectionError()))

    result = await service.schedule(
        processing_record_id="record-1",
        correlation_id="correlation-1",
        detected_format=DetectedFormat.FORMAT_1,
    )

    assert result == SchedulingState.RETRYABLE
    assert repository.events == [
        ("persist", SchedulingState.PENDING),
        ("transition", SchedulingState.RETRYABLE),
    ]


def test_upload_route_returns_only_the_processing_record_identifier() -> None:
    upload_validator, _ = validator()
    application = FastAPI()
    application.include_router(
        create_upload_router(
            UploadAcceptanceService(upload_validator, RecordingUploadRepository()),
            lambda: "staff-1",
        )
    )

    with TestClient(application) as client:
        response = client.post(
            "/intake/uploads",
            files={"file": ("survey.pdf", b"%PDF-survey", "application/pdf")},
        )

    assert response.status_code == 200
    assert set(response.json()) == {"processing_record_id"}


def test_status_route_hides_metadata_for_an_inaccessible_record() -> None:
    application = FastAPI()
    application.include_router(
        create_status_router(
            ProcessingStatusQuery(AllowingAuthorizer(False), StatusRepository()),
            lambda: "staff-1",
        )
    )

    with TestClient(application) as client:
        response = client.get("/intake/processing-records/record-1")

    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied."}