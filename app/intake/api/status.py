from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.intake.application.get_processing_status import ProcessingStatusQuery


class ProcessingStatusResponse(BaseModel):
    detected_format: str | None
    processing_state: str


def create_status_router(
    query: ProcessingStatusQuery,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/intake", tags=["intake"])

    @router.get("/processing-records/{processing_record_id}", response_model=ProcessingStatusResponse)
    async def get_processing_status(
        processing_record_id: str,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> ProcessingStatusResponse:
        outcome = await query.get(
            actor_id=actor_id,
            processing_record_id=processing_record_id,
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "not_found" or outcome.processing_status is None:
            raise HTTPException(status_code=404, detail="Processing record not found.")

        return ProcessingStatusResponse(
            detected_format=outcome.processing_status.detected_format,
            processing_state=outcome.processing_status.processing_state,
        )

    return router