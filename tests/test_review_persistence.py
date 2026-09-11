import pytest

from app.review.application.review_persistence import (
    DatabaseConnectionError,
    ReviewPersistenceService,
)
from app.review.ports.repositories import ContentRevision, PocApprovalState


class RecordingRepository:
    def __init__(self, failure: Exception | None = None) -> None:
        self.items: list[object] = []
        self._failure = failure

    async def save(self, item: object) -> None:
        if self._failure:
            raise self._failure
        self.items.append(item)

    async def append(self, item: object) -> None:
        if self._failure:
            raise self._failure
        self.items.append(item)


class RecordingUnitOfWork:
    def __init__(self, failure: Exception | None = None) -> None:
        self.approval_states = RecordingRepository(failure)
        self.audit_revisions = RecordingRepository(failure)
        self.committed = False
        self.rolled_back = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


class AuditFailureUnitOfWork(RecordingUnitOfWork):
    def __init__(self) -> None:
        super().__init__()
        self.audit_revisions = RecordingRepository(RuntimeError("audit write failed"))


def approval() -> PocApprovalState:
    return PocApprovalState(poc_id="poc-1", status="approved", reviewer_id="reviewer")


def revision() -> ContentRevision:
    return ContentRevision(
        revision_id="revision-1",
        poc_id="poc-1",
        content="Approved response",
        editor_id="reviewer",
    )


@pytest.mark.asyncio
async def test_persist_decision_commits_approval_and_revision_together() -> None:
    unit_of_work = RecordingUnitOfWork()
    service = ReviewPersistenceService(lambda: unit_of_work)

    result = await service.persist_decision(approval(), revision())

    assert result.approval_recorded is True
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


@pytest.mark.asyncio
async def test_persist_decision_returns_recoverable_connection_failure() -> None:
    unit_of_work = RecordingUnitOfWork(DatabaseConnectionError())
    service = ReviewPersistenceService(lambda: unit_of_work)

    result = await service.persist_decision(approval(), revision())

    assert result.status == "connection_failed"
    assert result.approval_recorded is False
    assert unit_of_work.rolled_back is True


@pytest.mark.asyncio
async def test_persist_decision_rolls_back_when_audit_write_fails() -> None:
    unit_of_work = AuditFailureUnitOfWork()
    service = ReviewPersistenceService(lambda: unit_of_work)

    with pytest.raises(RuntimeError, match="audit write failed"):
        await service.persist_decision(approval(), revision())

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True