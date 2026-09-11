from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from app.review.application.approve_poc import ApprovePocService


class PocApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    occurred_at: datetime


class PocApprovalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    poc_id: str
    status: Literal["approved"]
    reviewer_id: str
    approved_at: datetime


def create_poc_approval_router(
    service: ApprovePocService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/review", tags=["review"])

    @router.post("/pocs/{poc_id}/approval", response_model=PocApprovalResponse)
    async def approve_poc(
        poc_id: str,
        request: PocApprovalRequest,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> PocApprovalResponse:
        outcome = await service.approve(
            actor_id=actor_id,
            poc_id=poc_id,
            occurred_at=request.occurred_at,
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "not_found":
            raise HTTPException(status_code=404, detail="POC not found.")
        if outcome.status == "ineligible":
            raise HTTPException(status_code=422, detail="POC is not eligible for approval.")
        if outcome.audit_entry is None:
            raise RuntimeError("Approved POC audit entry is missing.")

        return PocApprovalResponse(
            poc_id=outcome.audit_entry.poc_id,
            status="approved",
            reviewer_id=outcome.audit_entry.reviewer_id,
            approved_at=outcome.audit_entry.approved_at,
        )

    return router