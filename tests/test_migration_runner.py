import pytest

from app.database.migrations.config import Migration, MigrationRunner, ordered_migrations


class FakeDatabase:
    def __init__(self, failure: Exception | None = None) -> None:
        self._failure = failure
        self.statements: list[str] = []
        self.committed = False
        self.rolled_back = False

    async def execute(self, statement: str, *parameters: object) -> None:
        if self._failure and statement == "CREATE TABLE workflow_records ();":
            raise self._failure
        self.statements.append(statement)

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


@pytest.mark.asyncio
async def test_apply_records_migration_version_in_the_same_transaction() -> None:
    database = FakeDatabase()
    runner = MigrationRunner(database)

    await runner.apply(Migration("001", "CREATE TABLE workflow_records ();", "rollback"))

    assert database.committed is True
    assert database.rolled_back is False
    assert database.statements[-1].startswith("INSERT INTO schema_migration_history")


@pytest.mark.asyncio
async def test_apply_rolls_back_without_recording_a_failed_migration() -> None:
    database = FakeDatabase(RuntimeError("database unavailable"))
    runner = MigrationRunner(database)

    with pytest.raises(RuntimeError, match="database unavailable"):
        await runner.apply(Migration("001", "CREATE TABLE workflow_records ();", "restore"))

    assert database.rolled_back is True
    assert not any("INSERT INTO schema_migration_history" in item for item in database.statements)


def test_ordered_migrations_sorts_versions_lexically() -> None:
    migrations = ordered_migrations((Migration("002", "", ""), Migration("001", "", "")))

    assert [migration.version for migration in migrations] == ["001", "002"]