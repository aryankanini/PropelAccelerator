# Task - TASK_001

## Requirement Reference
- **User Story:** us_023
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_023/us_023.md
- **Acceptance Criteria:**
  - AC-001: Updated records retain source links and a change record with actor and timestamp.
- **Edge Cases:**
  - A split without a source boundary is rejected and preserves the existing record.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-009, DR-004, and UC-003 require controlled correction commands. |

---

## Task Overview
Implement authorized merge, split, and create correction commands that preserve evidence links and revision attribution. Estimated effort: 8 hours.

## Dependent Tasks
- US_022 must expose reviewable candidate records.

## Impacted Components
- New correction command service, permission boundary, and revision command models.

## Implementation Plan
- Validate review permission and correction command shape.
- Apply merge, split, and create operations through a transactional application service.
- Reject split commands lacking a valid source boundary before mutation.
- Pass actor, timestamp, source links, and correlation context to persistence.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_023/us_023.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/application/correction_service.py | Authorizes and applies segmentation corrections. |
| CREATE | app/api/routes/deficiency_corrections.py | Validates correction requests and returns typed outcomes. |

## External References
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Require review permission for every merge, split, and create correction command. (AC-001)
- [ ] Preserve inherited SOD, Tag, and evidence links on corrected records. (AC-001)
- [ ] Send actor and timestamp attribution with each accepted correction. (AC-001)
- [ ] Reject a split without a valid source boundary before changing records. (edge case)
