from typing import Protocol

from app.ai_gateway.application.grounded_request_guard import (
    GroundedRequestGuard,
    ModelInferenceRequest,
)
from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.knowledge.application.cms_context_retrieval import CmsContextRetrievalService
from app.poc.domain.generation_outcome import PocGenerationOutcome
from app.poc.domain.grounded_request import GroundedPocRequest


class PocModelGateway(Protocol):
    async def generate(self, request: ModelInferenceRequest) -> str: ...


class PocDraftRepository(Protocol):
    async def persist_draft(
        self,
        deficiency_id: str,
        source_set_version: str,
        content: str,
    ) -> str: ...

    async def record_generation_error(self, deficiency_id: str, error: str) -> None: ...


class PocGenerationWorker:
    def __init__(
        self,
        retrieval_service: CmsContextRetrievalService,
        model_gateway: PocModelGateway,
        draft_repository: PocDraftRepository,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._model_gateway = model_gateway
        self._draft_repository = draft_repository

    async def generate(self, deficiency: DeficiencyCandidate) -> PocGenerationOutcome:
        context = await self._retrieval_service.retrieve(deficiency)
        if context.request is None:
            return PocGenerationOutcome(
                status="blocked",
                deficiency_id=deficiency.deficiency_id,
                error=context.reason,
                manual_drafting_available=True,
            )

        inference_request = GroundedRequestGuard().create(context.request)
        if not isinstance(inference_request, ModelInferenceRequest):
            return PocGenerationOutcome(
                status="blocked",
                deficiency_id=deficiency.deficiency_id,
                error=inference_request.reason,
                manual_drafting_available=True,
            )

        try:
            content = await self._model_gateway.generate(inference_request)
            draft_id = await self._draft_repository.persist_draft(
                deficiency.deficiency_id,
                context.request.source_set_version,
                content,
            )
        except Exception as error:
            await self._draft_repository.record_generation_error(
                deficiency.deficiency_id, str(error)
            )
            return PocGenerationOutcome(
                status="failed",
                deficiency_id=deficiency.deficiency_id,
                error=str(error),
                manual_drafting_available=True,
            )

        return PocGenerationOutcome(
            status="persisted",
            deficiency_id=deficiency.deficiency_id,
            draft_id=draft_id,
        )