# Task - TASK_002

## Requirement Reference
- **User Story:** us_028
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_028/us_028.md
- **Acceptance Criteria:**
  - AC-001: Validation records required-element results and quality score before review.
- **Edge Cases:**
  - A missing required element blocks approval and identifies the missing element.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001, AIR-003 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-003 requires retained validation results and approval state. |

---

## Task Overview
Persist POC rubric outcomes and approval-blocking state for each draft. Estimated effort: 4 hours.

## Dependent Tasks
- US_027 must establish POC draft storage.

## Impacted Components
- New POC validation result table and approval-block constraint.

## Implementation Plan
- Store quality score, element results, evaluator version, and validation timestamp.
- Relate the result to exactly one POC draft.
- Enforce blocked review state when required elements are missing.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_028/us_028.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/adapters/postgres/migrations/028_add_poc_validation.sql | Stores rubric outcomes and approval-block state. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Persist required-element results and quality score for each POC draft. (AC-001)
- [ ] Persist validation before the draft enters review. (AC-001)
- [ ] Constrain missing required elements to an approval-blocking state. (edge case)
