# Task - TASK_001

## Requirement Reference
- **User Story:** us_038
- **Story Location:** .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_038/us_038.md
- **Acceptance Criteria:**
  - AC-001: A submitted source that overlaps an approved source remains pending and unavailable for grounding.
- **Edge Cases:**
  - A resolved conflict retains the prior decision history.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-018 requires deterministic exclusion of contradictory source guidance. |

## Task Overview
Implement conflict detection and governed holding for overlapping CMS source submissions. Estimated effort: 6 hours.

## Dependent Tasks
- US_036 must persist governed CMS source records.

## Impacted Components
- New source-conflict evaluator, resolution command, and decision-history contracts.

## Implementation Plan
- Compare a submitted source against approved source scope and version metadata.
- Mark overlapping submissions as pending conflict and retrieval ineligible.
- Record each conflict decision as append-only resolution history.
- Allow later resolution to change eligibility while retaining the previous decision history.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_038/us_038.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/application/detect_source_conflicts.py | Detects overlap with approved source records. |
| CREATE | app/knowledge/application/resolve_source_conflict.py | Applies governed resolution while retaining history. |
| CREATE | app/knowledge/contracts/source_conflict.py | Defines conflict state and decision-history data. |

## External References
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Evaluate submitted sources against overlapping approved sources. (AC-001)
- [x] Keep detected conflicts pending and unavailable for grounding. (AC-001)
- [x] Record conflict decisions in append-only history. (edge case)
- [x] Retain prior decisions after a conflict is resolved. (edge case)