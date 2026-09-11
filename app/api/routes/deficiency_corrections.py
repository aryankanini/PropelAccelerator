from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from app.deficiency.application.correction_service import (
    CorrectionCommand,
    DeficiencyCorrectionService,
)


class CorrectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    operation: Literal["merge", "split", "create"]
    source_deficiency_ids: tuple[str, ...] = ()
    source_boundary: str | None = None
    occurred_at: datetime
    correlation_id: str


class CorrectionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["applied"]


def create_deficiency_correction_router(
    service: DeficiencyCorrectionService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/deficiencies", tags=["deficiencies"])

    @router.post(
        "/processing-records/{processing_record_id}/corrections",
        response_model=CorrectionResponse,
    )
    async def correct_deficiency(
        processing_record_id: str,
        request: CorrectionRequest,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> CorrectionResponse:
        outcome = await service.correct(
            CorrectionCommand(
                processing_record_id=processing_record_id,
                operation=request.operation,
                source_deficiency_ids=request.source_deficiency_ids,
                source_boundary=request.source_boundary,
                actor_id=actor_id,
                occurred_at=request.occurred_at,
                correlation_id=request.correlation_id,
            )
        )
        if outcome.status == "access_denied":
            raise HTTPException(status_code=403, detail="Access denied.")
        if outcome.status == "invalid_split":
            raise HTTPException(status_code=422, detail="A split requires a source boundary.")

        return CorrectionResponse(status="applied")

    return router