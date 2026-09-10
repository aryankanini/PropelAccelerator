# Task - TASK_001

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
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-010, FR-019, and UC-004 require deficiency-scoped worker orchestration. |

---

## Task Overview
Implement POC job orchestration that creates one deficiency-scoped draft outcome and retains recoverable failures. Estimated effort: 7 hours.

## Dependent Tasks
- US_026 must provide approved source context.

## Impacted Components
- New POC worker application service and deficiency-specific error outcome.

## Implementation Plan
- Process each confirmed deficiency as a separate idempotent work item.
- Submit the grounded request through the AI gateway port.
- Persist the returned draft with its source-set version through the POC repository.
- Capture failure against the specific deficiency and preserve manual drafting availability.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_027/us_027.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/application/generation_worker.py | Coordinates one POC generation outcome per deficiency. |
| CREATE | app/poc/domain/generation_outcome.py | Defines persisted and recoverable failure outcomes. |

## External References
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Process each confirmed deficiency as an independent POC job input. (AC-001)
- [ ] Request a grounded draft only with approved source context. (AC-001)
- [ ] Persist the returned draft with its deficiency and source-set version. (AC-001)
- [ ] Record an error against only the failed deficiency and leave it available for manual drafting. (edge case)
