import pytest

from app.processing.adapters.postgres.idempotent_job_repository import (
    IdempotentJobRepository,
)


class FakeConnection:
    def __init__(self, created: bool) -> None:
        self._created = created
        self.calls = 0

    async def fetchrow(self, query: str, *parameters: object) -> dict[str, object]:
        self.calls += 1
        return {
            "correlation_id": "original-correlation",
            "state": "complete",
            "retry_count": 1,
            "failure_reason": None,
            "created": self._created,
        }


@pytest.mark.asyncio
async def test_persist_or_return_classifies_conflicted_identity_as_duplicate() -> None:
    connection = FakeConnection(created=False)
    repository = IdempotentJobRepository(connection)

    result = await repository.persist_or_return(
        processing_record_id="record-1",
        attempt_id="attempt-1",
        correlation_id="new-correlation",
        state="pending",
        retry_count=0,
        failure_reason=None,
    )

    assert result.disposition == "duplicate"
    assert result.correlation_id == "original-correlation"
    assert connection.calls == 1