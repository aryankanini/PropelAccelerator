# PostgreSQL Migration Rules

Apply migrations through `MigrationRunner`, which creates and records each
version in `schema_migration_history` in the same transaction as its SQL. A
failed migration is rolled back and is never recorded as applied.

Every migration must state one of these recovery paths before review:

- A transactional rollback procedure for additive or reversible changes.
- A point-in-time restore procedure for irreversible changes, using
  [the PostgreSQL restore runbook](../../../../infra/postgres-restore-runbook.md).

Use expand-migrate-contract releases:

1. **Expand:** add backward-compatible tables, indexes, or nullable columns.
2. **Migrate:** backfill in observable, restartable batches while old reads remain valid.
3. **Switch:** deploy readers and writers that understand both representations.
4. **Contract:** remove the retired representation only after the compatibility window and restore verification pass.