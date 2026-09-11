from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from app.poc.application.source_reference_query import PocSourceReferenceQuery


class PocCitationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_id: str
    version: str
    cited: bool


class PocReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    draft_id: str
    source_set_version: str
    citations: tuple[PocCitationResponse, ...]
    citation_status: str
    missing_citation_source_ids: tuple[str, ...]


def create_poc_review_router(query: PocSourceReferenceQuery) -> APIRouter:
    router = APIRouter(prefix="/poc-drafts", tags=["poc-review"])

    @router.get("/{draft_id}/sources", response_model=PocReviewResponse)
    async def get_poc_sources(draft_id: str) -> PocReviewResponse:
        review = await query.get(draft_id)
        if review is None:
            raise HTTPException(status_code=404, detail="POC draft not found.")
        return PocReviewResponse(
            draft_id=review.draft_id,
            source_set_version=review.source_set_version,
            citations=tuple(
                PocCitationResponse(
                    source_id=source.source_id,
                    version=source.version,
                    cited=source.cited,
                )
                for source in review.sources
            ),
            citation_status=review.citation_status,
            missing_citation_source_ids=review.missing_citation_source_ids,
        )

    return router