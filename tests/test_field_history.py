from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.review.api.field_history import create_field_history_router
from app.review.application.get_field_history import FieldHistoryQuery, FieldRevision


class Authorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_view(self, actor_id: str, processing_record_id: str) -> bool:
        return self._allowed


class Repository:
    def __init__(self, revisions: tuple[FieldRevision, ...] | None) -> None:
        self._revisions = revisions
        self.requests: list[tuple[str, str]] = []

    async def list_revisions(
        self, processing_record_id: str, field_name: str
    ) -> tuple[FieldRevision, ...] | None:
        self.requests.append((processing_record_id, field_name))
        return self._revisions


def revision() -> FieldRevision:
    return FieldRevision(
        revision_id="revision-1",
        attribution="staff",
        reviewer_id="staff-1",
        reviewed_at=datetime(2026, 9, 11, 9, 30, tzinfo=UTC),
        content_change="Example Provider -> Updated Provider",
        approval_status="approved",
    )


@pytest.mark.asyncio
async def test_field_history_denies_access_before_loading_revisions() -> None:
    repository = Repository((revision(),))
    outcome = await FieldHistoryQuery(Authorizer(False), repository).get(
        actor_id="staff-1",
        processing_record_id="record-1",
        field_name="provider_name",
    )

    assert outcome.status == "access_denied"
    assert repository.requests == []


@pytest.mark.asyncio
async def test_field_history_returns_attributable_revision_details() -> None:
    outcome = await FieldHistoryQuery(Authorizer(True), Repository((revision(),))).get(
        actor_id="staff-1",
        processing_record_id="record-1",
        field_name="provider_name",
    )

    assert outcome.history is not None
    assert outcome.history.revisions[0].attribution == "staff"
    assert outcome.history.revisions[0].reviewer_id == "staff-1"
    assert outcome.history.revisions[0].approval_status == "approved"


def test_field_history_route_hides_reviewer_identity_when_access_is_denied() -> None:
    application = FastAPI()
    application.include_router(
        create_field_history_router(FieldHistoryQuery(Authorizer(False), Repository((revision(),))), lambda: "staff-1")
    )

    with TestClient(application) as client:
        response = client.get(
            "/review/processing-records/record-1/fields/provider_name/history"
        )

    assert response.status_code == 403
    assert "staff-1" not in response.text