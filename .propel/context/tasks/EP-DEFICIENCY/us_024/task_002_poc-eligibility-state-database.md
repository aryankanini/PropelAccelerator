# Task - TASK_002

## Requirement Reference
- **User Story:** us_024
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_024/us_024.md
- **Acceptance Criteria:**
  - AC-001: A record with no confirmed deficiency remains incomplete and no POC job is published.
- **Edge Cases:**
  - Removing a confirmed deficiency by correction invalidates pending POC work.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-003 and DR-004 require durable, auditable POC eligibility state. |

---

## Task Overview
Persist POC eligibility and invalidation state without erasing correction or job history. Estimated effort: 4 hours.

## Dependent Tasks
- US_023 must establish correction history.

## Impacted Components
- New processing-record eligibility state and job invalidation references.

## Implementation Plan
- Add constrained incomplete, eligible, and invalidated eligibility states.
- Relate pending POC jobs to the confirmed-deficiency basis used at publication time.
- Mark affected pending jobs invalidated when their basis is removed.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_024/us_024.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/adapters/postgres/migrations/024_add_poc_eligibility.sql | Adds eligibility and pending-job invalidation state. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Persist incomplete eligibility when no confirmed deficiency exists. (AC-001)
- [ ] Record the confirmed-deficiency basis for each pending POC job. (AC-001)
- [ ] Mark pending POC work invalidated when its confirmed-deficiency basis is removed. (edge case)
