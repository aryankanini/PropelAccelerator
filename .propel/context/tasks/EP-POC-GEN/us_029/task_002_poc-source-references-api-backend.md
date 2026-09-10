# Task - TASK_002

## Requirement Reference
- **User Story:** us_029
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_029/us_029.md
- **Acceptance Criteria:**
  - AC-001: The interface displays source references and source-set version used for the POC draft.
- **Edge Cases:**
  - A missing citation is displayed as a blocking validation flag, not as CMS support.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-013, FR-019, and UC-004 require a typed POC review query. |

---

## Task Overview
Expose POC source references, source-set version, and citation-blocking state through a typed review query. Estimated effort: 5 hours.

## Dependent Tasks
- US_027 must persist POC drafts and source-set versions.
- US_028 must persist validation outcomes.

## Impacted Components
- New POC review query service and FastAPI response models.

## Implementation Plan
- Load the POC's source references and version by draft identity.
- Return citation metadata separately from validation flags.
- Mark missing citations as blocking and never represent them as supporting CMS evidence.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_029/us_029.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/application/source_reference_query.py | Loads POC source references and blocking citation status. |
| CREATE | app/api/routes/poc_review.py | Exposes typed POC source-review responses. |

## External References
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Return every persisted source reference and source-set version for the requested POC draft. (AC-001)
- [ ] Keep citation metadata separate from validation status in the response. (AC-001)
- [ ] Return a blocking validation flag for a missing citation. (edge case)
- [ ] Never label a missing citation as CMS support. (edge case)
