# Task - TASK_001

## Requirement Reference
- **User Story:** us_032
- **Story Location:** .propel/context/tasks/EP-REVIEW-APPROVAL/us_032/us_032.md
- **Acceptance Criteria:**
  - AC-001: Field history displays AI or staff attribution, reviewer, timestamp, content change, and approval status.
- **Edge Cases:**
  - A request without review permission does not expose content or reviewer identity.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-016 and FR-017 require a permission-scoped audit projection. |

## Task Overview
Implement an authorized field-review history query with attributable revision details. Estimated effort: 5 hours.

## Dependent Tasks
- US_031 must record field review decisions.

## Impacted Components
- New field-history route, application query, and immutable history response contracts.

## Implementation Plan
- Authorize review access before querying revision history.
- Load AI and staff revisions in review chronology.
- Project attribution, reviewer, timestamp, content delta, and approval status into the response.
- Deny unauthorized requests before any history content or reviewer identity is resolved.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-REVIEW-APPROVAL/us_032/us_032.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/review/api/field_history.py | Defines the authorized field-history endpoint. |
| CREATE | app/review/application/get_field_history.py | Produces the permission-scoped revision history projection. |
| CREATE | app/review/contracts/field_history.py | Defines attributable revision and approval-status response data. |

## External References
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Authorize review access before loading history. (edge case)
- [x] Return AI or staff attribution for every revision. (AC-001)
- [x] Return reviewer, timestamp, content change, and approval status. (AC-001)
- [x] Do not expose history content or reviewer identity to unauthorized callers. (edge case)