# Task - TASK_001

## Requirement Reference
- **User Story:** us_008
- **Story Location:** .propel/context/tasks/EP-DATA/us_008/us_008.md
- **Acceptance Criteria:**
  - AC-001: Record migration version and preserve compatible reads during expand-migrate-contract evolution.
- **Edge Cases:**
  - Stop a failed migration before recording its version and identify the required rollback or restore procedure.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-008, DR-009, and TR-013 require recoverable, versioned schema evolution. |

---

## Task Overview
Establish a versioned PostgreSQL migration baseline and documented restore-aware failure handling for additive schema changes. Estimated effort: 8 hours.

## Dependent Tasks
- US_002 production PostgreSQL service must be available for restore validation.

## Impacted Components
- New migration runner configuration, migration history table, migration conventions, and restore procedure.

## Implementation Plan
- Select and configure one migration runner with an authoritative migration history table.
- Require each migration to be recorded only after its transactional application succeeds.
- Define expand-migrate-contract stages that preserve application reads throughout compatibility windows.
- Require every migration to declare rollback eligibility or the restore procedure it needs.
- Document point-in-time restore steps and the $15$-minute RPO and $4$-hour RTO validation targets.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-DATA/us_008/us_008.md
`- .propel/context/docs/design.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/database/migrations/config.py | Configures the versioned PostgreSQL migration runner. |
| CREATE | app/database/migrations/README.md | Defines expand-migrate-contract, rollback, and restore requirements. |
| CREATE | infra/postgres-restore-runbook.md | Documents point-in-time restore procedure and verification targets. |

## External References
- [PostgreSQL 16 transactions](https://www.postgresql.org/docs/16/tutorial-transactions.html)
- [Azure Database for PostgreSQL backup and restore](https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-backup-restore)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Configure one authoritative migration history mechanism. (AC-001)
- [ ] Record a migration version only after successful transactional application. (AC-001, edge case)
- [ ] Define additive expand stages that preserve existing application reads. (AC-001)
- [ ] Define migrate and contract stages with explicit compatibility windows. (AC-001)
- [ ] Require a rollback or point-in-time restore procedure for every migration. (edge case)
- [ ] Document and validate recovery objectives for production data restoration. (AC-001)