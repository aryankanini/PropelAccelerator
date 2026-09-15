import pytest

from app.intake.application.get_processing_queue import (
    ProcessingQueueItem,
    ProcessingQueueQuery,
)
from app.intake.adapters.postgres.processing_queue_repository import (
    PostgresProcessingQueueRepository,
)


class QueueRepository:
    async def list_requiring_review(self) -> tuple[ProcessingQueueItem, ...]:
        return (
            ProcessingQueueItem(
                processing_record_id="record-1",
                provider="Riverside Nursing Center",
                format="Format 2",
                stage="Fields need verification",
                stage_key="verification",
                action="Review fields",
                review_url="/wireframes/wireframe-SCR-003-extraction-review.html",
            ),
        )


class PostgresConnection:
    def __init__(self) -> None:
        self.queries: list[str] = []

    async def fetch(self, query: str) -> list[dict[str, str]]:
        self.queries.append(query)
        return [
            {
                "processing_record_id": "record-1",
                "provider": "Riverside Nursing Center",
                "detected_format": "format_2",
                "stage_key": "verification",
            },
            {
                "processing_record_id": "record-2",
                "provider": "Oak Meadows Care",
                "detected_format": "format_1",
                "stage_key": "blocked",
            },
        ]


@pytest.mark.asyncio
async def test_processing_queue_returns_records_supplied_by_repository() -> None:
    items = await ProcessingQueueQuery(QueueRepository()).get()

    assert items == (
        ProcessingQueueItem(
            processing_record_id="record-1",
            provider="Riverside Nursing Center",
            format="Format 2",
            stage="Fields need verification",
            stage_key="verification",
            action="Review fields",
            review_url="/wireframes/wireframe-SCR-003-extraction-review.html",
        ),
    )


@pytest.mark.asyncio
async def test_postgres_processing_queue_repository_maps_review_stages() -> None:
    connection = PostgresConnection()

    items = await PostgresProcessingQueueRepository(connection).list_requiring_review()

    assert "extracted_fields" in connection.queries[0]
    assert "poc_drafts" in connection.queries[0]
    assert [(item.format, item.stage_key, item.action) for item in items] == [
        ("Format 2", "verification", "Review fields"),
        ("Format 1", "blocked", "Review POC"),
    ]