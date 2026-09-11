from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.review.application.record_field_decision import FieldDecisionService
from app.review.contracts.field_decision import (
    FieldDecisionRequest,
    FieldDecisionResponse,
)


def create_field_decision_router(
    service: FieldDecisionService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/review", tags=["review"])

    @router.post(
        "/processing-records/{processing_record_id}/fields/{field_name}/decisions",
        response_model=FieldDecisionResponse,
    )
    async def record_field_decision(
        processing_record_id: str,
        field_name: str,
        request: FieldDecisionRequest,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> FieldDecisionResponse:
        outcome = await service.record(
            actor_id=actor_id,
            processing_record_id=processing_record_id,
            field_name=field_name,
            decision=request.decision,
            corrected_value=request.corrected_value,
            occurred_at=request.occurred_at,
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "not_found":
            raise HTTPException(status_code=404, detail="Field not found.")
        if outcome.status == "missing_evidence":
            raise HTTPException(
                status_code=422,
                detail="Source evidence is required before a field can be reviewed.",
            )
        if outcome.decision is None:
            raise RuntimeError("Recorded field decision is missing.")

        return FieldDecisionResponse(
            processing_record_id=outcome.decision.processing_record_id,
            field_name=outcome.decision.field_name,
            review_state=outcome.decision.review_state,
            reviewer_id=outcome.decision.reviewer_id,
            reviewed_at=outcome.decision.reviewed_at,
        )

    return router