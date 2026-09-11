# PostgreSQL Point-in-Time Restore Runbook

## Preconditions

- Confirm the incident timestamp, target recovery point, and affected database.
- Obtain incident approval before changing production traffic.
- Use a separate restore target; do not overwrite the source server.

## Restore Procedure

1. In Azure Portal or CLI, restore the PostgreSQL Flexible Server to the latest valid point at or before the incident timestamp.
2. Restrict the restored server to the migration role and read-only verification access.
3. Verify `schema_migration_history`, row counts for workflow tables, and source-document hashes against the recovery target.
4. Smoke-test compatible application reads against the restored server.
5. Record the recovery point, validation results, and cutover decision in the incident record.
6. Redirect traffic only after the application owner approves the verified restore.

## Recovery Objectives

- Recovery point objective: 15 minutes.
- Recovery time objective: 4 hours.

Validate both objectives during a production-like restore exercise at least annually and after material schema or backup-policy changes.