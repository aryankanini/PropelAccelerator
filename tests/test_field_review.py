import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.review.api.fields import create_field_review_router
from app.review.application.get_field_review import (
    EvidenceRetrievalError,
    FieldReviewQuery,
)
from app.review.contracts.field_review import ExtractedFieldDraft


class Authorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_view(self, actor_id: str, processing_record_id: str) -> bool:
        return self._allowed


class Repository:
    def __init__(self, drafts: tuple[ExtractedFieldDraft, ...] | None) -> None:
        self._drafts = drafts
        self.requested_record_ids: list[str] = []

    async def get_for_review(
        self, processing_record_id: str
    ) -> tuple[ExtractedFieldDraft, ...] | None:
        self.requested_record_ids.append(processing_record_id)
        return self._drafts


class Resolver:
    def __init__(self, failure: Exception | None = None) -> None:
        self._failure = failure

    async def resolve(self, locator: str) -> str:
        if self._failure:
            raise self._failure
        return f"review-safe:{locator}"


def draft(locator: str | None = "source://page/1") -> ExtractedFieldDraft:
    return ExtractedFieldDraft(
        field_name="provider_name",
        value="Example Provider",
        confidence_state="high_confidence",
        evidence_locator=locator,
    )


@pytest.mark.asyncio
async def test_field_review_denies_access_before_loading_fields() -> None:
    repository = Repository((draft(),))
    query = FieldReviewQuery(Authorizer(False), repository, Resolver())

    outcome = await query.get(actor_id="staff-1", processing_record_id="record-1")

    assert outcome.status == "access_denied"
    assert repository.requested_record_ids == []


@pytest.mark.asyncio
async def test_field_review_returns_confidence_and_review_safe_evidence() -> None:
    query = FieldReviewQuery(Authorizer(True), Repository((draft(),)), Resolver())

    outcome = await query.get(actor_id="staff-1", processing_record_id="record-1")

    assert outcome.review is not None
    assert outcome.review.fields[0].confidence_state == "high_confidence"
    assert outcome.review.fields[0].evidence_state == "resolved"
    assert outcome.review.fields[0].source_evidence_locator == "review-safe:source://page/1"
    assert outcome.review.fields[0].approval_eligible is True


@pytest.mark.asyncio
async def test_field_review_marks_evidence_retrieval_failure_unresolved() -> None:
    query = FieldReviewQuery(
        Authorizer(True),
        Repository((draft(),)),
        Resolver(EvidenceRetrievalError("source unavailable")),
    )

    outcome = await query.get(actor_id="staff-1", processing_record_id="record-1")

    assert outcome.review is not None
    assert outcome.review.fields[0].evidence_state == "unresolved"
    assert outcome.review.fields[0].source_evidence_locator is None
    assert outcome.review.fields[0].approval_eligible is False


def test_field_review_route_hides_data_for_an_inaccessible_record() -> None:
    application = FastAPI()
    application.include_router(
        create_field_review_router(
            FieldReviewQuery(Authorizer(False), Repository((draft(),)), Resolver()),
            lambda: "staff-1",
        )
    )

    with TestClient(application) as client:
        response = client.get("/review/processing-records/record-1/fields")

    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied."}