# Task - TASK_001

## Requirement Reference
- **User Story:** us_037
- **Story Location:** .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_037/us_037.md
- **Acceptance Criteria:**
  - AC-001: An authorized approval makes a complete pending source eligible for new POC retrieval and records the approver and timestamp.
- **Edge Cases:**
  - An unauthorized approval attempt changes no source state.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-018 and AIR-002 require controlled promotion of source material used for grounding. |

## Task Overview
Implement authorized CMS source approval and retrieval-eligibility transition. Estimated effort: 5 hours.

## Dependent Tasks
- US_036 must retain governed source metadata.

## Impacted Components
- New CMS source approval route, application command, and retrieval-eligibility policy.

## Implementation Plan
- Authorize governance users before loading the pending source.
- Confirm required source metadata is complete before approval.
- Record approver identity and approval timestamp while transitioning the source to retrieval eligible.
- Reject unauthorized attempts without mutating source state.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_037/us_037.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/api/cms_source_approvals.py | Defines the governance-only source approval endpoint. |
| CREATE | app/knowledge/application/approve_cms_source.py | Validates completeness and applies source approval. |
| CREATE | app/knowledge/contracts/cms_source_approval.py | Defines source approval command and result data. |

## External References
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Authorize governance users before approving a source. (AC-001)
- [ ] Require complete source metadata before approval. (AC-001)
- [ ] Record the approver and timestamp when the source becomes retrieval eligible. (AC-001)
- [ ] Leave source state unchanged for unauthorized approval attempts. (edge case)