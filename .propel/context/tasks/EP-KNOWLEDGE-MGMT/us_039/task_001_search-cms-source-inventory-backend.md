# Task - TASK_001

## Requirement Reference
- **User Story:** us_039
- **Story Location:** .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_039/us_039.md
- **Acceptance Criteria:**
  - AC-001: Source inventory results match reference, version, or approval-state filters and accurately identify authoritative sources.
- **Edge Cases:**
  - An empty query returns a bounded, paginated result set.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-018 requires a governed, bounded inventory query for source maintenance. |

## Task Overview
Implement an authorized, paginated CMS source inventory search. Estimated effort: 5 hours.

## Dependent Tasks
- US_036 must persist governed CMS source metadata.

## Impacted Components
- New source-inventory route, filtered query service, and paginated response contracts.

## Implementation Plan
- Authorize governance users before querying the inventory.
- Apply optional reference, version, and approval-state filters through a structured query contract.
- Limit and paginate unfiltered results with a stable ordering.
- Derive the authoritative label only from approved source state.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-KNOWLEDGE-MGMT/us_039/us_039.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/api/cms_source_inventory.py | Defines the authorized source-inventory search endpoint. |
| CREATE | app/knowledge/application/search_cms_sources.py | Applies typed filters, stable ordering, and pagination. |
| CREATE | app/knowledge/contracts/cms_source_inventory.py | Defines source filters and paginated metadata results. |

## External References
- [FastAPI query parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Authorize governance users before returning inventory data. (AC-001)
- [x] Filter sources by reference, version, and approval state. (AC-001)
- [x] Label only approved sources as authoritative. (AC-001)
- [x] Return empty searches as a bounded, paginated result set. (edge case)