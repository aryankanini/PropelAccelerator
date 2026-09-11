import pytest

from app.knowledge.adapters.postgres.poc_source_version_repository import (
    PocSourceVersion,
    PocSourceVersionRepository,
)


class FakeConnection:
    def __init__(self) -> None:
        self.executed: list[tuple[str, tuple[object, ...]]] = []

    async def execute(self, query: str, *parameters: object) -> None:
        self.executed.append((query, parameters))

    async def fetch(self, query: str, *parameters: object) -> list[dict[str, object]]:
        return [
            {
                'source_id': 'source-1',
                'effective_version': '2026.1',
                'source_set_version': 'a' * 64,
            }
        ]


@pytest.mark.asyncio
async def test_source_versions_are_persisted_for_a_draft_and_retrieved_for_audit() -> None:
    connection = FakeConnection()
    repository = PocSourceVersionRepository(connection)
    source_version = PocSourceVersion('source-1', '2026.1', 'a' * 64)

    await repository.persist('poc-1', source_version)
    audit_sources = await repository.list_for_audit('poc-1')

    assert connection.executed[0][1] == ('poc-1', 'source-1', '2026.1', 'a' * 64)
    assert audit_sources == (source_version,)