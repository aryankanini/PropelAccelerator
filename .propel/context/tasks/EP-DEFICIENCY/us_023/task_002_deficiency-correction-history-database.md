# Task - TASK_002

## Requirement Reference
- **User Story:** us_023
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_023/us_023.md
- **Acceptance Criteria:**
  - AC-001: Updated records retain source links and a change record with actor and timestamp.
- **Edge Cases:**
  - A split without a source boundary is rejected and preserves the existing record.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-004 requires attributable revisions without overwriting review history. |

---

## Task Overview
Add immutable correction history and transactional safeguards for deficiency changes. Estimated effort: 6 hours.

## Dependent Tasks
- US_021 must establish deficiency storage.

## Impacted Components
- New deficiency correction history table and source-boundary constraints.

## Implementation Plan
- Create append-only correction records with actor, timestamp, operation, and source references.
- Associate replacement deficiencies to their source deficiency where applicable.
- Enforce required source-boundary data for split operations.
- Use one transaction for current state and correction history writes.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_023/us_023.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/adapters/postgres/migrations/023_add_correction_history.sql | Creates immutable correction history and source-boundary constraints. |

## External References
- [PostgreSQL 16 transactions](https://www.postgresql.org/docs/16/tutorial-transactions.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Persist the correction operation, actor, and timestamp without overwriting prior history. (AC-001)
- [ ] Persist retained source evidence and source-deficiency links for corrected records. (AC-001)
- [ ] Require a source boundary for split history records. (edge case)
- [ ] Roll back the correction transaction when split validation fails. (edge case)
