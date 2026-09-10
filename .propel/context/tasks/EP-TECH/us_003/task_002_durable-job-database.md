# Task - TASK_002

## Requirement Reference
- **User Story:** us_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Persist one logical processing outcome per stable processing-record and job-attempt identity.
  - AC-002: Retain correlation identifier and failure reason for exhausted retries.
- **Edge Cases:**
  - Persist a validation failure reason for a malformed command without creating processing side effects.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-010 requires authoritative idempotency state; TR-004 assigns transactional ownership to PostgreSQL. |

---

## Task Overview
Create the authoritative job persistence schema that makes processing identities unique, retains retry and duplicate observations, and supports operator diagnosis of terminal outcomes. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 database migration and application persistence conventions must be established first.

## Impacted Components
- New Job and JobDeliveryObservation relational records and an additive PostgreSQL migration.

## Implementation Plan
- Create a Job table keyed by an immutable job ID with processing-record ID, job-attempt ID, state, attempt count, correlation ID, and sanitized error fields.
- Enforce a unique constraint on processing-record ID plus job-attempt ID to make duplicate delivery concurrency-safe.
- Create a delivery-observation table linked to Job for received timestamps and duplicate indicators.
- Add indexes supporting lookup by idempotency key, correlation ID, and active/terminal state.
- Use an expand migration compatible with the project migration and restore requirements.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-TECH/us_003/us_003.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/processing/adapters/postgres/migrations/001_create_jobs.sql | Creates job and delivery-observation tables, constraints, and indexes. |
| CREATE | app/processing/adapters/postgres/job_repository.py | Implements atomic Job persistence and duplicate outcome lookup. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)
- [PostgreSQL 16 indexes](https://www.postgresql.org/docs/16/indexes.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Create the job persistence model with processing identity, retry state, correlation ID, and terminal failure fields. (AC-001, AC-002)
- [ ] Add a unique processing-record and job-attempt constraint for atomic idempotency enforcement. (AC-001)
- [ ] Store one delivery observation per receipt and mark duplicate observations. (AC-001)
- [ ] Add targeted indexes for idempotency, correlation, and operator state lookup. (AC-001, AC-002)
- [ ] Apply the schema as an additive, reviewed migration with no destructive data operation. (AC-001, AC-002)