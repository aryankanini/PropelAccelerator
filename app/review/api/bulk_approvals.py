from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends

from app.review.application.apply_bulk_approval import BulkApprovalService
from app.review.contracts.bulk_approval import BulkApprovalRequest, BulkApprovalResponse


def create_bulk_approval_router(
    service: BulkApprovalService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/review", tags=["review"])

    @router.post("/pocs/bulk-approval", response_model=BulkApprovalResponse)
    async def apply_bulk_approval(
        request: BulkApprovalRequest,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> BulkApprovalResponse:
        records = await service.apply(actor_id=actor_id, poc_ids=request.poc_ids)
        return BulkApprovalResponse(records=records)

    return router