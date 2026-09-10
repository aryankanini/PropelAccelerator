# Task - TASK_001

## Requirement Reference
- **User Story:** us_012
- **Story Location:** .propel/context/tasks/EP-INTAKE/us_012/us_012.md
- **Acceptance Criteria:**
  - AC-001: Store exactly one supported format before extraction is queued.
- **Edge Cases:**
  - Conflicting format markers create an error state and do not queue extraction.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-002 and UC-001 require deterministic intake classification. |

## Task Overview
Implement deterministic form-marker classification and its processing-record state transition. Estimated effort: 6 hours.

## Dependent Tasks
- US_011 accepted upload persistence must be available.

## Impacted Components
- New intake classifier and processing-record state transition service.

## Implementation Plan
- Define supported marker rules for Format 1, Format 2, and open-source format.
- Require one unambiguous result before setting detected format.
- Store a non-approved error state and prevent queue scheduling for conflicts.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-INTAKE/us_012/us_012.md
`- .propel/context/docs/spec.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/intake/domain/format_classifier.py | Classifies supported survey-form markers. |
| CREATE | app/intake/application/classify_upload.py | Applies classification to a persisted processing record. |

## External References
- [Pydantic model validation](https://docs.pydantic.dev/latest/concepts/models/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Define the three supported deterministic format outcomes. (AC-001)
- [ ] Evaluate uploaded content markers before extraction is scheduled. (AC-001)
- [ ] Persist exactly one detected format on a successful classification. (AC-001)
- [ ] Reject ambiguous marker matches into a non-approved error state. (edge case)
- [ ] Prevent extraction scheduling when classification is unsuccessful. (edge case)