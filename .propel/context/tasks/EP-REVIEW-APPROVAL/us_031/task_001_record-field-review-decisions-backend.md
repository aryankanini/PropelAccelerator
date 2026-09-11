# Task - TASK_001

## Requirement Reference
- **User Story:** us_031
- **Story Location:** .propel/context/tasks/EP-REVIEW-APPROVAL/us_031/us_031.md
- **Acceptance Criteria:**
  - AC-001: A field review decision, reviewer, timestamp, and resulting review state are persisted.
- **Edge Cases:**
  - Missing evidence keeps the field unresolved and blocks approval.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-014, FR-016, and FR-017 require authorized, attributable field review decisions. |

## Task Overview
Implement the authorized field-review decision command and deterministic review-state transition. Estimated effort: 6 hours.

## Dependent Tasks
- US_020 must provide the evidence-aware field-review projection.

## Impacted Components
- New field-review command route, application service, and decision contracts.

## Implementation Plan
- Authorize the reviewer before loading the field and its source evidence.
- Reject accept or correction decisions when evidence is unavailable.
- Persist the decision with reviewer identity, timestamp, and resulting review state through the repository boundary.
- Return the persisted review state without exposing unauthorized evidence.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-REVIEW-APPROVAL/us_031/us_031.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/review/api/field_decisions.py | Defines the authorized field-review decision endpoint. |
| CREATE | app/review/application/record_field_decision.py | Validates evidence and applies the review-state transition. |
| CREATE | app/review/contracts/field_decision.py | Defines accept and correction command and result data. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Authorize the reviewer before reading or changing a field. (AC-001)
- [x] Require source evidence before accepting or correcting the field. (edge case)
- [x] Persist the decision, reviewer identity, timestamp, and resulting review state. (AC-001)
- [x] Keep fields without evidence unresolved and ineligible for approval. (edge case)