# Task - TASK_001

## Requirement Reference
- **User Story:** us_021
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_021/us_021.md
- **Acceptance Criteria:**
  - AC-001: Each detected SOD boundary creates a distinct deficiency linked to its SOD, Tag, evidence, and processing record.
- **Edge Cases:**
  - Ambiguous boundaries are flagged for correction rather than finalized.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-009, DR-002, and UC-003 require typed deficiency segmentation and review-ready outcomes. |

---

## Task Overview
Implement the Deficiency module application service that converts extracted SOD content into distinct, evidence-linked candidate deficiencies. Estimated effort: 7 hours.

## Dependent Tasks
- US_018 must provide extracted SOD content and source evidence.
- US_006 must provide ProcessingRecord and Deficiency persistence.

## Impacted Components
- New Deficiency module segmentation service, typed candidate result, and repository port.

## Implementation Plan
- Define typed inputs for extracted SOD text, Tag, evidence references, and processing-record identity.
- Detect candidate boundaries and produce one candidate for each defensible segment.
- Return ambiguous boundaries as correction-required outcomes without finalizing them.
- Delegate persistence through the Deficiency repository port and retain correlation context.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/docs/design.md
`- .propel/context/tasks/EP-DEFICIENCY/us_021/us_021.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/application/segmentation_service.py | Creates distinct candidate deficiencies from extracted SOD content. |
| CREATE | app/deficiency/domain/segmentation_result.py | Defines typed confirmed-candidate and correction-required outcomes. |
| CREATE | app/deficiency/ports/deficiency_repository.py | Defines persistence operations for candidate deficiencies. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Accept extracted SOD, Tag, evidence references, and processing-record identity as typed segmentation input. (AC-001)
- [x] Produce a distinct candidate for every detected SOD boundary. (AC-001)
- [x] Carry the source SOD, Tag, evidence, and processing-record link on every candidate. (AC-001)
- [x] Return an ambiguous boundary as correction-required without finalizing its candidate. (edge case)
