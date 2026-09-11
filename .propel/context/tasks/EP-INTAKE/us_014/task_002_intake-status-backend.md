# Task - TASK_002

## Requirement Reference
- **User Story:** us_014
- **Story Location:** .propel/context/tasks/EP-INTAKE/us_014/us_014.md
- **Acceptance Criteria:**
  - AC-001: Return the detected format and current processing state for an accessible processing record.
- **Edge Cases:**
  - Return an authorization outcome for inaccessible records without revealing document metadata.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-002, FR-003, and UC-001 require an authorized status contract. |

## Task Overview
Implement the authorized processing-status query and response contract. Estimated effort: 4 hours.

## Dependent Tasks
- US_011 processing-record persistence must be available.
- US_012 classification state must be available.

## Impacted Components
- New intake status route, application query, and response model.

## Implementation Plan
- Authorize access before loading a record response.
- Return a constrained status projection containing only permitted fields.
- Ensure non-approved states cannot be serialized as approved.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-INTAKE/us_014/us_014.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/intake/api/status.py | Defines the processing-status endpoint. |
| CREATE | app/intake/application/get_processing_status.py | Authorizes and retrieves the status projection. |
| CREATE | app/intake/contracts/status.py | Defines the permitted status response fields. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Define a typed status response with detected format and processing state. (AC-001)
- [x] Authorize access before loading the processing-record projection. (edge case)
- [x] Return an authorization outcome without document metadata when access is denied. (edge case)
- [x] Return the current detected format and processing state for an accessible record. (AC-001)
- [x] Prevent error-state records from being represented as approved. (AC-001)