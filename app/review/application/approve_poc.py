from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


class PocApprovalAuthorizer(Protocol):
    async def can_approve(self, actor_id: str, poc_id: str) -> bool: ...


@dataclass(frozen=True)
class PocApprovalEligibility:
    poc_id: str
    review_completed: bool
    required_elements_complete: bool
    cms_support_complete: bool
    review_state: Literal["pending", "rejected", "approved"]

    @property
    def is_eligible(self) -> bool:
        return (
            self.review_completed
            and self.required_elements_complete
            and self.cms_support_complete
            and self.review_state != "rejected"
        )


@dataclass(frozen=True)
class PocApprovalAuditEntry:
    poc_id: str
    reviewer_id: str
    approved_at: datetime


class PocApprovalRepository(Protocol):
    async def get_eligibility(self, poc_id: str) -> PocApprovalEligibility | None: ...

    async def approve_with_audit(self, entry: PocApprovalAuditEntry) -> None: ...


@dataclass(frozen=True)
class PocApprovalOutcome:
    status: Literal["approved", "access_denied", "not_found", "ineligible"]
    audit_entry: PocApprovalAuditEntry | None = None


class ApprovePocService:
    def __init__(
        self,
        authorizer: PocApprovalAuthorizer,
        repository: PocApprovalRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def approve(
        self, *, actor_id: str, poc_id: str, occurred_at: datetime
    ) -> PocApprovalOutcome:
        if not await self._authorizer.can_approve(actor_id, poc_id):
            return PocApprovalOutcome(status="access_denied")

        eligibility = await self._repository.get_eligibility(poc_id)
        if eligibility is None:
            return PocApprovalOutcome(status="not_found")
        if not eligibility.is_eligible:
            return PocApprovalOutcome(status="ineligible")

        audit_entry = PocApprovalAuditEntry(
            poc_id=poc_id,
            reviewer_id=actor_id,
            approved_at=occurred_at,
        )
        await self._repository.approve_with_audit(audit_entry)
        return PocApprovalOutcome(status="approved", audit_entry=audit_entry)