# Task - TASK_001

## Requirement Reference
- **User Story:** us_009
- **Story Location:** .propel/context/tasks/EP-DATA/us_009/us_009.md
- **Acceptance Criteria:**
  - AC-001: Return the existing outcome when the same job identity is persisted twice without creating another command record.
- **Edge Cases:**
  - Concurrent attempts create one job and return one recoverable duplicate response.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-010 and NFR-006 require concurrency-safe, observable idempotent job persistence. |

---

## Task Overview
Implement the atomic PostgreSQL repository operation that persists or returns one durable job attempt by stable identity. Estimated effort: 6 hours.

## Dependent Tasks
- US_003 durable message identity and foundational job schema task must define the shared identity constraint.

## Impacted Components
- New Job repository operation for atomic create-or-return outcome behavior.

## Implementation Plan
- Accept the stable processing-record and attempt identity as the sole repository idempotency key.
- Use a single database operation that creates a job or returns the existing outcome on unique-constraint conflict.
- Classify uniqueness conflicts as recoverable duplicates, not worker errors.
- Return the persisted correlation ID, state, retry count, and failure metadata to the caller.
- Avoid read-then-insert logic that can race under concurrent delivery.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-DATA/us_009/us_009.md
`- .propel/context/tasks/EP-TECH/us_003/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/processing/adapters/postgres/idempotent_job_repository.py | Implements atomic create-or-return job-attempt persistence. |

## External References
- [PostgreSQL 16 INSERT](https://www.postgresql.org/docs/16/sql-insert.html)
- [PostgreSQL 16 transaction isolation](https://www.postgresql.org/docs/16/transaction-iso.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Use processing-record and attempt IDs as the stable idempotency key. (AC-001)
- [x] Create the job through an atomic create-or-return operation. (AC-001)
- [x] Return the original job outcome for a repeated command identity. (AC-001)
- [x] Classify a unique-key conflict as a recoverable duplicate response. (AC-001, edge case)
- [x] Preserve a single job record under concurrent attempts. (edge case)