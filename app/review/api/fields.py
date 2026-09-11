from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.review.application.get_field_review import FieldReviewQuery
from app.review.contracts.field_review import FieldReviewResponse


def create_field_review_router(
    query: FieldReviewQuery,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/review", tags=["review"])

    @router.get(
        "/processing-records/{processing_record_id}/fields",
        response_model=FieldReviewResponse,
    )
    async def get_field_review(
        processing_record_id: str,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> FieldReviewResponse:
        outcome = await query.get(
            actor_id=actor_id,
            processing_record_id=processing_record_id,
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "not_found" or outcome.review is None:
            raise HTTPException(status_code=404, detail="Processing record not found.")

        return outcome.review

    return router