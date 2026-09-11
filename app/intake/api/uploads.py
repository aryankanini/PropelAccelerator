from collections.abc import Callable
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.intake.application.accept_upload import UploadAcceptanceService, UploadCommand
from app.intake.contracts.uploads import UploadAcknowledgement


class UploadAcknowledgementResponse(BaseModel):
    processing_record_id: str


def create_upload_router(
    service: UploadAcceptanceService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix="/intake", tags=["intake"])

    @router.post("/uploads", response_model=UploadAcknowledgementResponse)
    async def upload_survey(
        file: Annotated[UploadFile, File()],
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> UploadAcknowledgementResponse:
        acknowledgement = await service.accept(
            UploadCommand(
                actor_id=actor_id,
                processing_record_id=str(uuid4()),
                content=await file.read(),
                media_type=file.content_type or "",
            )
        )
        if acknowledgement is None:
            raise HTTPException(status_code=400, detail="Upload could not be accepted.")

        return _to_response(acknowledgement)

    return router


def _to_response(acknowledgement: UploadAcknowledgement) -> UploadAcknowledgementResponse:
    return UploadAcknowledgementResponse(
        processing_record_id=acknowledgement.processing_record_id
    )