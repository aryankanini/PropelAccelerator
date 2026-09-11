from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.review.application.get_field_history import FieldHistoryQuery
from app.review.contracts.field_history import FieldHistoryResponse


def create_field_history_router(
    query: FieldHistoryQuery,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/review", tags=["review"])

    @router.get(
        "/processing-records/{processing_record_id}/fields/{field_name}/history",
        response_model=FieldHistoryResponse,
    )
    async def get_field_history(
        processing_record_id: str,
        field_name: str,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> FieldHistoryResponse:
        outcome = await query.get(
            actor_id=actor_id,
            processing_record_id=processing_record_id,
            field_name=field_name,
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "not_found" or outcome.history is None:
            raise HTTPException(status_code=404, detail="Field not found.")

        return outcome.history

    return router