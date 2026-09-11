from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


class MigrationDatabase(Protocol):
    async def execute(self, statement: str, *parameters: object) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


@dataclass(frozen=True)
class Migration:
    version: str
    sql: str
    restore_procedure: str


class MigrationRunner:
    _CREATE_HISTORY = """
        CREATE TABLE IF NOT EXISTS schema_migration_history (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    _RECORD_VERSION = "INSERT INTO schema_migration_history (version) VALUES ($1);"

    def __init__(self, database: MigrationDatabase) -> None:
        self._database = database

    async def apply(self, migration: Migration) -> None:
        try:
            await self._database.execute(self._CREATE_HISTORY)
            await self._database.execute(migration.sql)
            await self._database.execute(self._RECORD_VERSION, migration.version)
            await self._database.commit()
        except Exception:
            await self._database.rollback()
            raise


def ordered_migrations(migrations: Sequence[Migration]) -> tuple[Migration, ...]:
    return tuple(sorted(migrations, key=lambda migration: migration.version))