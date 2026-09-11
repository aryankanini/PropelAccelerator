from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, Protocol

from app.platform.ports.unit_of_work import UnitOfWork
from app.review.ports.repositories import (
    ApprovalStateRepository,
    AuditRevisionRepository,
    ContentRevision,
    PocApprovalState,
)


class DatabaseConnectionError(ConnectionError):
    """A transient database connectivity failure that callers may retry."""


class ReviewUnitOfWork(UnitOfWork, Protocol):
    approval_states: ApprovalStateRepository
    audit_revisions: AuditRevisionRepository


@dataclass(frozen=True)
class ReviewPersistenceResult:
    status: Literal["persisted", "connection_failed"]
    approval_recorded: bool


class ReviewPersistenceService:
    def __init__(self, unit_of_work_factory: Callable[[], ReviewUnitOfWork]) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    async def persist_decision(
        self,
        approval_state: PocApprovalState,
        revision: ContentRevision,
    ) -> ReviewPersistenceResult:
        if approval_state.poc_id != revision.poc_id:
            raise ValueError("Approval state and revision must belong to the same POC")

        unit_of_work = self._unit_of_work_factory()
        try:
            await unit_of_work.approval_states.save(approval_state)
            await unit_of_work.audit_revisions.append(revision)
            await unit_of_work.commit()
        except DatabaseConnectionError:
            await unit_of_work.rollback()
            return ReviewPersistenceResult(
                status="connection_failed",
                approval_recorded=False,
            )
        except Exception:
            await unit_of_work.rollback()
            raise

        return ReviewPersistenceResult(status="persisted", approval_recorded=True)