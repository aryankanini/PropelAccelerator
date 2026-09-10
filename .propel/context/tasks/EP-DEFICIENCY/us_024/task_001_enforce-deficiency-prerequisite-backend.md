# Task - TASK_001

## Requirement Reference
- **User Story:** us_024
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_024/us_024.md
- **Acceptance Criteria:**
  - AC-001: A record with no confirmed deficiency remains incomplete and no POC job is published.
- **Edge Cases:**
  - Removing a confirmed deficiency by correction invalidates pending POC work.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-009 and UC-003 require deterministic POC eligibility checks. |

---

## Task Overview
Implement the deterministic pre-publication gate that allows POC work only for records with confirmed deficiencies. Estimated effort: 5 hours.

## Dependent Tasks
- US_023 must provide final correction state.

## Impacted Components
- New POC eligibility policy and pending-work invalidation application service.

## Implementation Plan
- Derive eligibility from current confirmed deficiency state.
- Mark records incomplete and return a blocked outcome when none is confirmed.
- Prevent queue publication on blocked outcomes.
- Invalidate pending POC work after a correction removes the last confirmation.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_024/us_024.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/application/deficiency_eligibility.py | Enforces confirmed-deficiency prerequisite and invalidation. |

## External References
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Allow POC eligibility only when at least one deficiency is confirmed. (AC-001)
- [ ] Return an incomplete blocked outcome for a record with no confirmed deficiency. (AC-001)
- [ ] Prevent POC job publication for a blocked outcome. (AC-001)
- [ ] Invalidate pending POC work when correction removes the final confirmed deficiency. (edge case)
