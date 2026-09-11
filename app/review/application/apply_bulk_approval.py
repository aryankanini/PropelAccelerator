from collections.abc import Callable
from datetime import datetime

from app.review.application.approve_poc import ApprovePocService
from app.review.contracts.bulk_approval import BulkApprovalRecord


class BulkApprovalService:
    def __init__(
        self,
        approval_service: ApprovePocService,
        clock: Callable[[], datetime],
    ) -> None:
        self._approval_service = approval_service
        self._clock = clock

    async def apply(
        self, *, actor_id: str, poc_ids: tuple[str, ...]
    ) -> tuple[BulkApprovalRecord, ...]:
        records = []
        for poc_id in poc_ids:
            outcome = await self._approval_service.approve(
                actor_id=actor_id,
                poc_id=poc_id,
                occurred_at=self._clock(),
            )
            if outcome.status == "approved" and outcome.audit_entry is not None:
                records.append(
                    BulkApprovalRecord(
                        poc_id=poc_id,
                        status="approved",
                        reviewer_id=outcome.audit_entry.reviewer_id,
                        approved_at=outcome.audit_entry.approved_at,
                    )
                )
                continue

            records.append(
                BulkApprovalRecord(
                    poc_id=poc_id,
                    status="ineligible",
                    reason=outcome.status,
                )
            )

        return tuple(records)