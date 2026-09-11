import pytest
from pydantic import ValidationError

from app.ai_gateway.application.grounded_request_guard import GroundedRequestGuard
from app.ai_gateway.application.release_evaluator import ReleaseEvaluator
from app.ai_gateway.domain.evaluation_contract import EvaluationResult
from app.ai_gateway.domain.poc_response_schema import PocResponseSchema
from app.deficiency.domain.segmentation_result import DeficiencyCandidate
from app.knowledge.application.cms_context_retrieval import CmsContextRetrievalService
from app.poc.application.generation_worker import PocGenerationWorker
from app.poc.application.rubric_validator import PocRubricValidator
from app.poc.application.source_reference_query import (
    PocSourceReference,
    PocSourceReferenceQuery,
    PocSourceReview,
)
from app.poc.domain.grounded_request import ApprovedCmsSource


class SourceRepository:
    async def list_approved_for_tag(self, tag: str) -> tuple[ApprovedCmsSource, ...]:
        return (ApprovedCmsSource("cms-1", "v1", "CMS guidance"),)


class ModelGateway:
    async def generate(self, request: object) -> str:
        return "Draft content"


class DraftRepository:
    def __init__(self) -> None:
        self.persisted: list[tuple[str, str, str]] = []
        self.errors: list[tuple[str, str]] = []

    async def persist_draft(self, deficiency_id: str, source_set_version: str, content: str) -> str:
        self.persisted.append((deficiency_id, source_set_version, content))
        return "draft-1"

    async def record_generation_error(self, deficiency_id: str, error: str) -> None:
        self.errors.append((deficiency_id, error))


class SourceReviewRepository:
    async def get_source_review(self, draft_id: str) -> PocSourceReview:
        return PocSourceReview(
            draft_id=draft_id,
            source_set_version="source-set-1",
            sources=(PocSourceReference("cms-1", "v1", False),),
            citation_status="complete",
            missing_citation_source_ids=(),
        )


def deficiency() -> DeficiencyCandidate:
    return DeficiencyCandidate(
        deficiency_id="deficiency-1",
        processing_record_id="record-1",
        sod_text="Deficiency text.",
        tag="F600",
        evidence_references=("evidence-1",),
        segmentation_status="confirmed",
    )


@pytest.mark.asyncio
async def test_worker_persists_a_grounded_draft_with_its_source_set_version() -> None:
    repository = DraftRepository()
    worker = PocGenerationWorker(CmsContextRetrievalService(SourceRepository()), ModelGateway(), repository)

    outcome = await worker.generate(deficiency())

    assert outcome.status == "persisted"
    assert outcome.draft_id == "draft-1"
    assert repository.persisted[0][0] == "deficiency-1"
    assert repository.persisted[0][1]


def test_rubric_blocks_review_and_identifies_all_missing_elements() -> None:
    result = PocRubricValidator(("root_cause", "corrective_action")).validate({"root_cause": "Cause"})

    assert result.status == "blocked"
    assert result.missing_elements == ("corrective_action",)
    assert result.quality_score == 0.5


def test_source_review_marks_missing_citations_as_blocking() -> None:
    review = __import__("asyncio").run(PocSourceReferenceQuery(SourceReviewRepository()).get("draft-1"))

    assert review is not None
    assert review.citation_status == "blocked"
    assert review.missing_citation_source_ids == ("cms-1",)


def test_release_evaluation_blocks_a_candidate_with_missing_categories() -> None:
    decision = ReleaseEvaluator().evaluate(
        test_set_version="2026.1",
        candidate_identity="model-1",
        results=(EvaluationResult(category="extraction", score=1),),
    )

    assert decision.status == "blocked"
    assert "citation_support" in decision.missing_categories


def test_poc_response_schema_rejects_unknown_properties() -> None:
    with pytest.raises(ValidationError):
        PocResponseSchema.model_validate({"status": "refused", "unexpected": "value"})


def test_poc_response_schema_rejects_completed_responses_without_elements() -> None:
    with pytest.raises(ValidationError, match="at least one element"):
        PocResponseSchema.model_validate({"status": "completed"})


def test_guard_refuses_empty_source_context() -> None:
    request = __import__("asyncio").run(CmsContextRetrievalService(SourceRepository()).retrieve(deficiency())).request
    assert request is not None
    blocked = GroundedRequestGuard().create(request.__class__(request.deficiency, (), request.source_set_version))
    assert blocked.status == "blocked"


def test_guard_refuses_an_explicitly_unapproved_source() -> None:
    request = __import__("asyncio").run(CmsContextRetrievalService(SourceRepository()).retrieve(deficiency())).request
    assert request is not None
    unapproved = ApprovedCmsSource("cms-1", "v1", "CMS guidance", approved=False)
    blocked = GroundedRequestGuard().create(
        request.__class__(request.deficiency, (unapproved,), request.source_set_version)
    )
    assert blocked.status == "blocked"