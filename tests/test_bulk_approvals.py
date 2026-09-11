from datetime import UTC, datetime

import pytest

from app.review.application.apply_bulk_approval import BulkApprovalService
from app.review.application.approve_poc import (
    ApprovePocService,
    PocApprovalAuditEntry,
    PocApprovalEligibility,
)


class Authorizer:
    async def can_approve(self, actor_id: str, poc_id: str) -> bool:
        return poc_id != "poc-denied"


class Repository:
    def __init__(self) -> None:
        self.audit_entries: list[PocApprovalAuditEntry] = []

    async def get_eligibility(self, poc_id: str) -> PocApprovalEligibility | None:
        if poc_id == "poc-ineligible":
            return PocApprovalEligibility(poc_id, True, False, True, "pending")
        return PocApprovalEligibility(poc_id, True, True, True, "pending")

    async def approve_with_audit(self, entry: PocApprovalAuditEntry) -> None:
        self.audit_entries.append(entry)


@pytest.mark.asyncio
async def test_bulk_approval_records_each_eligible_poc_and_reports_each_ineligible_poc() -> None:
    repository = Repository()
    service = BulkApprovalService(
        ApprovePocService(Authorizer(), repository),
        lambda: datetime(2026, 9, 11, 10, 0, tzinfo=UTC),
    )

    records = await service.apply(
        actor_id="staff-1",
        poc_ids=("poc-1", "poc-ineligible", "poc-denied", "poc-2"),
    )

    assert [record.status for record in records] == [
        "approved",
        "ineligible",
        "ineligible",
        "approved",
    ]
    assert [record.reason for record in records[1:3]] == ["ineligible", "access_denied"]
    assert [(entry.poc_id, entry.reviewer_id) for entry in repository.audit_entries] == [
        ("poc-1", "staff-1"),
        ("poc-2", "staff-1"),
    ]