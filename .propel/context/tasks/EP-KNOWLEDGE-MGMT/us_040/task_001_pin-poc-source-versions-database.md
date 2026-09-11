# Task - TASK_001

## Requirement Reference
- **User Story:** us_040
- **Story Location:** .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_040/us_040.md
- **Acceptance Criteria:**
  - AC-001: A generated POC retains the source-set version used at generation when source maintenance changes later.
- **Edge Cases:**
  - A retired source remains retrievable for historical audit only.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | PostgreSQL | Version TBD | FR-019 and DR-006 require immutable historical source provenance for approved POCs. |

## Task Overview
Implement immutable POC-to-source-set version persistence and historical retrieval rules. Estimated effort: 5 hours.

## Dependent Tasks
- US_037 must approve versioned CMS sources.

## Impacted Components
- New POC source-set version schema, historical audit query, and retrieval constraint.

## Implementation Plan
- Persist the exact source-set version reference with each generated POC.
- Prevent later source maintenance from overwriting recorded POC provenance.
- Retain retired source versions for audit retrieval.
- Exclude retired source versions from new grounding selections.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_040/us_040.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/infrastructure/migrations/create_poc_source_versions.sql | Creates immutable POC source-set version records. |
| CREATE | app/knowledge/infrastructure/poc_source_version_repository.py | Loads source provenance for audit without allowing replacement. |

## External References
- [PostgreSQL foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Migration tests pass
- [ ] Repository integration tests pass

## Implementation Checklist
- [x] Persist the source-set version used for every generated POC. (AC-001)
- [x] Prevent source maintenance from replacing persisted POC provenance. (AC-001)
- [x] Allow retired source versions to be retrieved for historical audit. (edge case)
- [x] Exclude retired source versions from new grounding selections. (edge case)