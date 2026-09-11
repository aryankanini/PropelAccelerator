from typing import Any, Literal, Protocol

from app.processing.ports.idempotent_job_repository import JobOutcome


class DatabaseConnectionError(ConnectionError):
    """A transient database connectivity failure that callers may retry."""


class PostgresConnection(Protocol):
    async def fetchrow(
        self,
        query: str,
        *parameters: object,
    ) -> dict[str, Any]: ...


class IdempotentJobRepository:
    _CREATE_OR_RETURN = """
        INSERT INTO job_attempts (
            processing_record_id,
            attempt_id,
            correlation_id,
            state,
            retry_count,
            failure_reason
        ) VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (processing_record_id, attempt_id) DO UPDATE
        SET attempt_id = EXCLUDED.attempt_id
        RETURNING correlation_id, state, retry_count, failure_reason, (xmax = 0) AS created;
    """

    def __init__(self, connection: PostgresConnection) -> None:
        self._connection = connection

    async def persist_or_return(
        self,
        *,
        processing_record_id: str,
        attempt_id: str,
        correlation_id: str,
        state: str,
        retry_count: int,
        failure_reason: str | None,
    ) -> JobOutcome:
        try:
            row = await self._connection.fetchrow(
                self._CREATE_OR_RETURN,
                processing_record_id,
                attempt_id,
                correlation_id,
                state,
                retry_count,
                failure_reason,
            )
        except DatabaseConnectionError:
            return JobOutcome(
                correlation_id=correlation_id,
                state="pending",
                retry_count=retry_count,
                failure_reason=None,
                disposition="connection_failed",
            )

        return JobOutcome(
            correlation_id=row["correlation_id"],
            state=row["state"],
            retry_count=row["retry_count"],
            failure_reason=row["failure_reason"],
            disposition="created" if row["created"] else "duplicate",
        )