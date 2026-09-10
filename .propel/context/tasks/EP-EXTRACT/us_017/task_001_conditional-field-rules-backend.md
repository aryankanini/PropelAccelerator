# Task - TASK_001

## Requirement Reference
- **User Story:** us_017
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_017/us_017.md
- **Acceptance Criteria:**
  - AC-001: Persist POC and Completion Date only for Format 2; persist both empty for Format 1 and open-source format.
- **Edge Cases:**
  - An unknown format prevents conditional extraction and enters a non-approved error state.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-005, FR-006, and UC-002 require deterministic format-specific persistence. |

## Task Overview
Implement format-conditioned extraction and persistence of POC and Completion Date fields. Estimated effort: 5 hours.

## Dependent Tasks
- US_016 common extracted fields must be available.

## Impacted Components
- New conditional-field policy and extraction-worker extension.

## Implementation Plan
- Use the processing record's detected format as the sole rule input.
- Extract conditional values only for Format 2.
- Store explicit empty values for formats that do not supply those fields and fail unknown formats safely.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_017/us_017.md
`- .propel/context/docs/spec.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/extraction/domain/conditional_field_policy.py | Applies the detected-format rules. |
| MODIFY | app/extraction/application/extract_common_fields.py | Applies conditional-field policy before persistence. |

## External References
- [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Read the persisted detected format before conditional extraction. (AC-001)
- [ ] Extract POC and Completion Date drafts for Format 2 only. (AC-001)
- [ ] Persist both conditional fields as empty for Format 1. (AC-001)
- [ ] Persist both conditional fields as empty for open-source format. (AC-001)
- [ ] Move unknown formats to a non-approved error state. (edge case)
- [ ] Prevent conditional extraction after an unknown-format outcome. (edge case)