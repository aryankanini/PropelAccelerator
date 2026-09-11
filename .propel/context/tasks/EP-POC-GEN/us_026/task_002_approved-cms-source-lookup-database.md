# Task - TASK_002

## Requirement Reference
- **User Story:** us_026
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_026/us_026.md
- **Acceptance Criteria:**
  - AC-001: The gateway retrieves only approved CMS records and attaches identifiers and versions to the request.
- **Edge Cases:**
  - No approved source returns a blocked, ungrounded outcome and does not approve a draft.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | AIR-002 and TR-007 require approved-source and version filtering. |

---

## Task Overview
Provide a deterministic PostgreSQL lookup of approved CMS sources with stable identifiers and versions. Estimated effort: 5 hours.

## Dependent Tasks
- CMS knowledge maintenance must establish CMSKnowledgeSource records.

## Impacted Components
- New approved-source index and repository query.

## Implementation Plan
- Index approved CMS sources by approval state, Tag applicability, and effective version.
- Select only currently approved records with stable canonical identifiers.
- Return an empty set rather than fallback or unapproved records.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_026/us_026.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/adapters/postgres/approved_source_repository.py | Queries approved CMS sources deterministically. |
| CREATE | app/knowledge/adapters/postgres/migrations/026_index_approved_sources.sql | Adds approved-source lookup indexes. |

## External References
- [PostgreSQL 16 indexes](https://www.postgresql.org/docs/16/indexes.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Index approved CMS records for Tag and effective-version lookup. (AC-001)
- [x] Return only approved source records with identifiers and versions. (AC-001)
- [x] Return no fallback rows when no approved source is available. (edge case)
