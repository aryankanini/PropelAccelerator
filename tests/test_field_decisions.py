from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.review.api.field_decisions import create_field_decision_router
from app.review.application.record_field_decision import (
    FieldDecisionService,
    RecordedFieldDecision,
    ReviewableField,
)


class Authorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_review(self, actor_id: str, processing_record_id: str) -> bool:
        return self._allowed


class Repository:
    def __init__(self, field: ReviewableField | None) -> None:
        self._field = field
        self.requested_fields: list[tuple[str, str]] = []
        self.decisions: list[RecordedFieldDecision] = []

    async def get_field(
        self, processing_record_id: str, field_name: str
    ) -> ReviewableField | None:
        self.requested_fields.append((processing_record_id, field_name))
        return self._field

    async def record(self, decision: RecordedFieldDecision) -> None:
        self.decisions.append(decision)


def reviewed_at() -> datetime:
    return datetime(2026, 9, 11, 9, 30, tzinfo=UTC)


@pytest.mark.asyncio
async def test_field_decision_denies_access_before_loading_the_field() -> None:
    repository = Repository(ReviewableField("provider_name", True))
    service = FieldDecisionService(Authorizer(False), repository)

    outcome = await service.record(
        actor_id="staff-1",
        processing_record_id="record-1",
        field_name="provider_name",
        decision="accepted",
        corrected_value=None,
        occurred_at=reviewed_at(),
    )

    assert outcome.status == "access_denied"
    assert repository.requested_fields == []


@pytest.mark.asyncio
async def test_field_decision_keeps_missing_evidence_unresolved() -> None:
    repository = Repository(ReviewableField("provider_name", False))
    service = FieldDecisionService(Authorizer(True), repository)

    outcome = await service.record(
        actor_id="staff-1",
        processing_record_id="record-1",
        field_name="provider_name",
        decision="accepted",
        corrected_value=None,
        occurred_at=reviewed_at(),
    )

    assert outcome.status == "missing_evidence"
    assert repository.decisions == []


@pytest.mark.asyncio
async def test_field_decision_records_reviewer_timestamp_and_verified_state() -> None:
    repository = Repository(ReviewableField("provider_name", True))
    service = FieldDecisionService(Authorizer(True), repository)

    outcome = await service.record(
        actor_id="staff-1",
        processing_record_id="record-1",
        field_name="provider_name",
        decision="corrected",
        corrected_value="Updated Provider",
        occurred_at=reviewed_at(),
    )

    assert outcome.status == "recorded"
    assert repository.decisions == [
        RecordedFieldDecision(
            processing_record_id="record-1",
            field_name="provider_name",
            decision="corrected",
            corrected_value="Updated Provider",
            reviewer_id="staff-1",
            reviewed_at=reviewed_at(),
            review_state="verified",
        )
    ]


def test_field_decision_route_returns_an_evidence_error() -> None:
    application = FastAPI()
    application.include_router(
        create_field_decision_router(
            FieldDecisionService(
                Authorizer(True),
                Repository(ReviewableField("provider_name", False)),
            ),
            lambda: "staff-1",
        )
    )

    with TestClient(application) as client:
        response = client.post(
            "/review/processing-records/record-1/fields/provider_name/decisions",
            json={"decision": "accepted", "occurred_at": reviewed_at().isoformat()},
        )

    assert response.status_code == 422