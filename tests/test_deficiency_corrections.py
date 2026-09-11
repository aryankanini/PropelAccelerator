from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.deficiency_corrections import create_deficiency_correction_router
from app.deficiency.application.correction_service import (
    CorrectionCommand,
    DeficiencyCorrectionService,
)


class Authorizer:
    def __init__(self, allowed: bool) -> None:
        self._allowed = allowed

    async def can_review(self, actor_id: str) -> bool:
        return self._allowed


class RecordingCorrectionRepository:
    def __init__(self) -> None:
        self.commands: list[CorrectionCommand] = []

    async def apply_correction(self, command: CorrectionCommand) -> None:
        self.commands.append(command)


@pytest.mark.asyncio
async def test_split_without_source_boundary_is_rejected_before_mutation() -> None:
    repository = RecordingCorrectionRepository()
    service = DeficiencyCorrectionService(Authorizer(True), repository)

    outcome = await service.correct(
        CorrectionCommand(
            processing_record_id="record-1",
            operation="split",
            source_deficiency_ids=("deficiency-1",),
            source_boundary=None,
            actor_id="reviewer-1",
            occurred_at=datetime.now(UTC),
            correlation_id="correlation-1",
        )
    )

    assert outcome.status == "invalid_split"
    assert repository.commands == []


def test_correction_route_preserves_actor_timestamp_and_correlation_context() -> None:
    repository = RecordingCorrectionRepository()
    application = FastAPI()
    application.include_router(
        create_deficiency_correction_router(
            DeficiencyCorrectionService(Authorizer(True), repository),
            lambda: "reviewer-1",
        )
    )

    with TestClient(application) as client:
        response = client.post(
            "/deficiencies/processing-records/record-1/corrections",
            json={
                "operation": "create",
                "occurred_at": "2026-09-11T10:00:00Z",
                "correlation_id": "correlation-1",
            },
        )

    assert response.status_code == 200
    assert repository.commands[0].actor_id == "reviewer-1"
    assert repository.commands[0].correlation_id == "correlation-1"