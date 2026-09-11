import pytest

from app.knowledge.adapters.postgres.cms_source_repository import (
    CmsSourceRecord,
    CmsSourceRepository,
)


class FakeConnection:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    async def execute(self, query: str, *parameters: object) -> None:
        self.calls.append((query, parameters))


@pytest.mark.asyncio
async def test_save_keeps_a_source_without_version_pending_and_indexing_ineligible() -> None:
    connection = FakeConnection()
    source = CmsSourceRecord(
        canonical_id='source-1',
        canonical_reference='cms:F600',
        content_hash='a' * 64,
        effective_version=None,
        applicable_tag='F600',
        content='CMS guidance',
        approval_state='pending',
        indexing_state='ineligible',
    )

    await CmsSourceRepository(connection).save(source)

    assert len(connection.calls) == 1
    assert connection.calls[0][1][-2:] == ('pending', 'ineligible')