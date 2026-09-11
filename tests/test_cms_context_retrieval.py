import pytest

from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.knowledge.application.cms_context_retrieval import CmsContextRetrievalService
from app.poc.domain.grounded_request import ApprovedCmsSource


class ApprovedSourceRepository:
    def __init__(self, sources: tuple[ApprovedCmsSource, ...]) -> None:
        self._sources = sources
        self.tags: list[str] = []

    async def list_approved_for_tag(self, tag: str) -> tuple[ApprovedCmsSource, ...]:
        self.tags.append(tag)
        return self._sources


def confirmed_deficiency(status: str = "confirmed") -> DeficiencyCandidate:
    return DeficiencyCandidate(
        deficiency_id="deficiency-1",
        processing_record_id="record-1",
        sod_text="Deficiency text.",
        tag="F600",
        evidence_references=("evidence-1",),
        segmentation_status=status,  # type: ignore[arg-type]
    )


@pytest.mark.asyncio
async def test_retrieval_attaches_only_approved_source_identifiers_and_versions() -> None:
    repository = ApprovedSourceRepository(
        (ApprovedCmsSource("cms-1", "2026.1", "Applicable CMS guidance."),)
    )

    outcome = await CmsContextRetrievalService(repository).retrieve(confirmed_deficiency())

    assert outcome.status == "grounded"
    assert outcome.request is not None
    assert outcome.request.sources[0].source_id == "cms-1"
    assert outcome.request.sources[0].version == "2026.1"
    assert outcome.request.source_set_version
    assert repository.tags == ["F600"]


@pytest.mark.asyncio
async def test_retrieval_blocks_an_ungrounded_request_when_no_approved_source_exists() -> None:
    outcome = await CmsContextRetrievalService(ApprovedSourceRepository(())).retrieve(
        confirmed_deficiency()
    )

    assert outcome.status == "blocked"
    assert outcome.reason == "no_approved_sources"
    assert outcome.request is None