from hashlib import sha256
from typing import Protocol

from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.poc.domain.grounded_request import (
    ApprovedCmsSource,
    GroundedPocRequest,
    GroundedRequestOutcome,
)


class ApprovedCmsSourceRepository(Protocol):
    async def list_approved_for_tag(self, tag: str) -> tuple[ApprovedCmsSource, ...]: ...


class CmsContextRetrievalService:
    def __init__(self, repository: ApprovedCmsSourceRepository) -> None:
        self._repository = repository

    async def retrieve(self, deficiency: DeficiencyCandidate) -> GroundedRequestOutcome:
        if deficiency.segmentation_status != "confirmed":
            return GroundedRequestOutcome(
                status="blocked",
                reason="deficiency_not_confirmed",
            )

        sources = await self._repository.list_approved_for_tag(deficiency.tag)
        if not sources:
            return GroundedRequestOutcome(status="blocked", reason="no_approved_sources")

        return GroundedRequestOutcome(
            status="grounded",
            request=GroundedPocRequest(
                deficiency=deficiency,
                sources=sources,
                source_set_version=self._source_set_version(sources),
            ),
        )

    @staticmethod
    def _source_set_version(sources: tuple[ApprovedCmsSource, ...]) -> str:
        source_versions = "\n".join(
            f"{source.source_id}:{source.version}" for source in sources
        )
        return sha256(source_versions.encode("utf-8")).hexdigest()