from datetime import UTC, datetime

import pytest

from app.review.application.approve_poc import (
    ApprovePocService,
    PocApprovalAuditEntry,
    PocApprovalEligibility,
)
from app.review.application.authorized_poc_access import AuthorizedPocAccess, StoredPoc


class ApprovalAuthorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_approve(self, actor_id: str, poc_id: str) -> bool:
        return self._allowed


class ApprovalRepository:
    def __init__(self, eligibility: PocApprovalEligibility | None) -> None:
        self._eligibility = eligibility
        self.lookups: list[str] = []
        self.audit_entries: list[PocApprovalAuditEntry] = []

    async def get_eligibility(self, poc_id: str) -> PocApprovalEligibility | None:
        self.lookups.append(poc_id)
        return self._eligibility

    async def approve_with_audit(self, entry: PocApprovalAuditEntry) -> None:
        self.audit_entries.append(entry)


class AccessAuthorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_use(self, actor_id: str, poc_id: str) -> bool:
        return self._allowed


class AccessRepository:
    def __init__(self, poc: StoredPoc | None) -> None:
        self._poc = poc
        self.lookups: list[str] = []

    async def get(self, poc_id: str) -> StoredPoc | None:
        self.lookups.append(poc_id)
        return self._poc


def eligible_poc() -> PocApprovalEligibility:
    return PocApprovalEligibility("poc-1", True, True, True, "pending")


@pytest.mark.asyncio
async def test_poc_approval_denies_access_before_loading_eligibility() -> None:
    repository = ApprovalRepository(eligible_poc())
    outcome = await ApprovePocService(ApprovalAuthorizer(False), repository).approve(
        actor_id="staff-1", poc_id="poc-1", occurred_at=datetime.now(UTC)
    )

    assert outcome.status == "access_denied"
    assert repository.lookups == []


@pytest.mark.asyncio
async def test_poc_approval_records_an_audit_entry_only_when_eligible() -> None:
    repository = ApprovalRepository(eligible_poc())
    occurred_at = datetime(2026, 9, 11, 10, 0, tzinfo=UTC)
    outcome = await ApprovePocService(ApprovalAuthorizer(True), repository).approve(
        actor_id="staff-1", poc_id="poc-1", occurred_at=occurred_at
    )

    assert outcome.status == "approved"
    assert repository.audit_entries == [PocApprovalAuditEntry("poc-1", "staff-1", occurred_at)]


@pytest.mark.asyncio
async def test_incomplete_or_rejected_poc_remains_unavailable() -> None:
    repository = ApprovalRepository(
        PocApprovalEligibility("poc-1", True, False, True, "rejected")
    )
    outcome = await ApprovePocService(ApprovalAuthorizer(True), repository).approve(
        actor_id="staff-1", poc_id="poc-1", occurred_at=datetime.now(UTC)
    )

    access_repository = AccessRepository(StoredPoc("poc-1", "Draft", "rejected"))
    access = await AuthorizedPocAccess(AccessAuthorizer(True), access_repository).get(
        actor_id="staff-1", poc_id="poc-1"
    )

    assert outcome.status == "ineligible"
    assert repository.audit_entries == []
    assert access.status == "unavailable"