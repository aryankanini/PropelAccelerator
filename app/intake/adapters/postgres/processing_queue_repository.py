from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from app.intake.application.get_processing_queue import ProcessingQueueItem


class PostgresConnection(Protocol):
    async def fetch(self, query: str, *parameters: object) -> Sequence[Mapping[str, Any]]: ...


class PostgresProcessingQueueRepository:
    _LIST_REQUIRING_REVIEW = """
        SELECT
            processing_record.id AS processing_record_id,
            processing_record.provider_name AS provider,
            processing_record.detected_format,
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM extracted_fields AS field
                    WHERE field.processing_record_id = processing_record.id
                      AND field.review_state <> 'verified'
                ) THEN 'verification'
                ELSE 'blocked'
            END AS stage_key
        FROM processing_records AS processing_record
        WHERE EXISTS (
            SELECT 1
            FROM extracted_fields AS field
            WHERE field.processing_record_id = processing_record.id
              AND field.review_state <> 'verified'
        ) OR EXISTS (
            SELECT 1
            FROM deficiencies AS deficiency
            JOIN poc_drafts AS poc_draft ON poc_draft.deficiency_id = deficiency.id
            WHERE deficiency.processing_record_id = processing_record.id
              AND poc_draft.superseded_at IS NULL
              AND poc_draft.review_state <> 'approved'
        )
        ORDER BY processing_record.created_at ASC;
    """
    _FORMAT_LABELS = {
        "format_1": "Format 1",
        "format_2": "Format 2",
        "open_source": "Open-source format",
    }

    def __init__(self, connection: PostgresConnection) -> None:
        self._connection = connection

    async def list_requiring_review(self) -> tuple[ProcessingQueueItem, ...]:
        rows = await self._connection.fetch(self._LIST_REQUIRING_REVIEW)
        return tuple(self._to_item(row) for row in rows)

    @classmethod
    def _to_item(cls, row: Mapping[str, Any]) -> ProcessingQueueItem:
        stage_key = str(row["stage_key"])
        if stage_key == "verification":
            return ProcessingQueueItem(
                processing_record_id=str(row["processing_record_id"]),
                provider=str(row["provider"]),
                format=cls._format_label(str(row["detected_format"])),
                stage="Fields need verification",
                stage_key="verification",
                action="Review fields",
                review_url=(
                    "/wireframes/wireframe-SCR-003-extraction-review.html"
                ),
            )

        return ProcessingQueueItem(
            processing_record_id=str(row["processing_record_id"]),
            provider=str(row["provider"]),
            format=cls._format_label(str(row["detected_format"])),
            stage="POC approval blocked",
            stage_key="blocked",
            action="Review POC",
            review_url="/wireframes/wireframe-SCR-006-poc-review-approval.html",
        )

    @classmethod
    def _format_label(cls, detected_format: str) -> str:
        return cls._FORMAT_LABELS.get(detected_format, detected_format)