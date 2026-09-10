# Task - TASK_002

## Requirement Reference
- **User Story:** us_020
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: Return each reviewable extracted value with its confidence state and source-evidence locator.
- **Edge Cases:**
  - An evidence retrieval failure returns an unresolved state and no approval control.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-007, FR-008, and UC-002 require a constrained review projection. |

## Task Overview
Implement the authorized extracted-field review query and evidence-resolution state. Estimated effort: 5 hours.

## Dependent Tasks
- US_018 evidence locator persistence must be available.

## Impacted Components
- New field-review route, application query, and review projection contracts.

## Implementation Plan
- Authorize record access and load fields with confidence and evidence data.
- Resolve each locator to a review-safe source reference.
- Return unresolved state and no approval eligibility when evidence cannot be retrieved.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_020/us_020.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/review/api/fields.py | Defines the extracted-field review endpoint. |
| CREATE | app/review/application/get_field_review.py | Builds the authorized review projection. |
| CREATE | app/review/contracts/field_review.py | Defines fields, confidence, evidence, and eligibility response data. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Authorize access before returning extracted-field review data. (AC-001)
- [ ] Return each field value and its confidence state. (AC-001)
- [ ] Return a review-safe source-evidence locator for each field. (AC-001)
- [ ] Represent unavailable evidence as unresolved. (edge case)
- [ ] Set approval eligibility false for unresolved evidence. (edge case)