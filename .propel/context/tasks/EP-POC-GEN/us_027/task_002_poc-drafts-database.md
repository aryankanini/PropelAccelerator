# Task - TASK_002

## Requirement Reference
- **User Story:** us_027
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_027/us_027.md
- **Acceptance Criteria:**
  - AC-001: The completed POC job persists exactly one draft linked to each deficiency and source-set version.
- **Edge Cases:**
  - A generation failure records the deficiency-specific error and leaves the deficiency available for manual drafting.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-003 requires exactly one traceable POC draft per deficiency. |

---

## Task Overview
Create POC draft and generation-exception persistence with deficiency-scoped uniqueness. Estimated effort: 6 hours.

## Dependent Tasks
- US_021 must establish deficiency records.
- US_026 must provide source-set metadata.

## Impacted Components
- New PlanOfCorrection uniqueness constraint and generation-error records.

## Implementation Plan
- Add a unique deficiency parent relationship for each active draft.
- Persist source-set version with the draft and generation outcome.
- Store recoverable generation errors by deficiency without changing manual-drafting eligibility.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_027/us_027.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/adapters/postgres/migrations/027_create_poc_drafts.sql | Creates deficiency-scoped POC drafts and exception records. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Enforce exactly one active draft per deficiency. (AC-001)
- [ ] Persist the source-set version with every draft. (AC-001)
- [ ] Record a generation error against the failed deficiency. (edge case)
- [ ] Preserve manual-drafting eligibility after a generation failure. (edge case)
