# Task - TASK_002

## Requirement Reference
- **User Story:** us_030
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_030/us_030.md
- **Acceptance Criteria:**
  - AC-001: Extraction, SOD recall, citation support, POC quality, refusal, and conditional-field results are recorded against a versioned test set.
- **Edge Cases:**
  - A missing evaluation category blocks release promotion.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-005, AIR-006 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | AIR-005 requires durable versioned evaluation evidence and release-gate completeness. |

---

## Task Overview
Persist versioned AI evaluation runs and category-level results with complete-gate enforcement. Estimated effort: 6 hours.

## Dependent Tasks
- US_030 AI release evaluator must define required category contracts.

## Impacted Components
- New AI evaluation run, result, and release-gate persistence tables.

## Implementation Plan
- Store proposed model or prompt identity and test-set version for each run.
- Persist one result for every required evaluation category.
- Enforce uniqueness by run and category.
- Persist an incomplete release-gate state when required categories are absent.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_030/us_030.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/ai_gateway/adapters/postgres/migrations/030_create_evaluation_results.sql | Creates versioned evaluation and complete-gate persistence. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Persist the proposed model or prompt identity and versioned test set for each evaluation run. (AC-001)
- [ ] Persist every required category result against its evaluation run. (AC-001)
- [ ] Enforce one result per required category for each run. (AC-001)
- [ ] Persist a blocked release-gate state when any required category is missing. (edge case)
