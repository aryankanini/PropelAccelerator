# Task - TASK_001

## Requirement Reference
- **User Story:** us_036
- **Story Location:** .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_036/us_036.md
- **Acceptance Criteria:**
  - AC-001: A governed CMS source retains canonical reference, hash, effective version, approval state, and indexing state.
- **Edge Cases:**
  - A source without version metadata remains pending.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | PostgreSQL | Version TBD | DR-006 requires durable, versioned source governance metadata. |

## Task Overview
Implement durable CMS source records with version, approval, and indexing governance state. Estimated effort: 5 hours.

## Dependent Tasks
- US_006 must provide the source persistence foundation.

## Impacted Components
- New governed CMS source schema, constraints, and repository mapping.

## Implementation Plan
- Model canonical references, content hashes, effective versions, approval state, and indexing state.
- Enforce source identity and version constraints needed for governed updates.
- Default sources missing version metadata to pending approval and indexing-ineligible state.
- Preserve source metadata for later approval, conflict, and historical-version operations.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_036/us_036.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/infrastructure/migrations/create_cms_sources.sql | Creates governed CMS source storage and constraints. |
| CREATE | app/knowledge/infrastructure/cms_source_repository.py | Maps governed source records through the persistence boundary. |

## External References
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Migration tests pass
- [ ] Repository integration tests pass

## Implementation Checklist
- [ ] Persist canonical reference, content hash, effective version, approval state, and indexing state. (AC-001)
- [ ] Constrain source identity and governed version records. (AC-001)
- [ ] Default records without version metadata to pending. (edge case)
- [ ] Keep pending sources ineligible for indexing and grounding. (edge case)