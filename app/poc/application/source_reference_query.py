from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class PocSourceReference:
    source_id: str
    version: str
    cited: bool


@dataclass(frozen=True)
class PocSourceReview:
    draft_id: str
    source_set_version: str
    sources: tuple[PocSourceReference, ...]
    citation_status: Literal["complete", "blocked"]
    missing_citation_source_ids: tuple[str, ...]


class PocSourceReferenceRepository(Protocol):
    async def get_source_review(self, draft_id: str) -> PocSourceReview | None: ...


class PocSourceReferenceQuery:
    def __init__(self, repository: PocSourceReferenceRepository) -> None:
        self._repository = repository

    async def get(self, draft_id: str) -> PocSourceReview | None:
        review = await self._repository.get_source_review(draft_id)
        if review is None:
            return None
        missing = tuple(source.source_id for source in review.sources if not source.cited)
        return PocSourceReview(
            draft_id=review.draft_id,
            source_set_version=review.source_set_version,
            sources=review.sources,
            citation_status="blocked" if missing else "complete",
            missing_citation_source_ids=missing,
        )