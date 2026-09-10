# Task - TASK_002

## Requirement Reference
- **User Story:** us_022
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_022/us_022.md
- **Acceptance Criteria:**
  - AC-001: Each candidate displays its Tag, SOD, evidence, and segmentation status.
- **Edge Cases:**
  - An empty inventory shows an incomplete state and no POC-generation action.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-009 and UC-003 require typed candidate and evidence retrieval. |

---

## Task Overview
Expose a typed inventory query that returns reviewable deficiency candidates or an explicit incomplete result. Estimated effort: 5 hours.

## Dependent Tasks
- US_021 must persist candidate deficiencies.

## Impacted Components
- New Deficiency query service, response models, and FastAPI inventory endpoint.

## Implementation Plan
- Query candidates by processing record through the Deficiency module.
- Return Tag, SOD, evidence references, and segmentation status in typed responses.
- Return an explicit incomplete response when no candidate exists and omit POC actions.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_022/us_022.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/application/inventory_query.py | Loads reviewable deficiency candidates. |
| CREATE | app/api/routes/deficiency_inventory.py | Provides typed inventory responses. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Return Tag, SOD, evidence references, and segmentation status for every candidate. (AC-001)
- [ ] Return an explicit incomplete inventory outcome when no candidates exist. (edge case)
- [ ] Exclude POC-generation actions from an incomplete inventory response. (edge case)
