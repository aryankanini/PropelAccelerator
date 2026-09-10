# Task - TASK_001

## Requirement Reference
- **User Story:** us_016
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Persist Provider Name, Provider Number, Survey Date, Tag, and SOD drafts for review.
- **Edge Cases:**
  - Missing required source text creates an incomplete field rather than an inferred value.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | app/extraction/prompts/common_fields/ |
| **Guardrails Config** | app/extraction/contracts/common_fields.py |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-004 and AIR-001 require typed, reviewable extraction results. |

## Task Overview
Implement the worker flow that extracts common survey content and persists reviewable drafts. Estimated effort: 8 hours.

## Dependent Tasks
- US_015 queued extraction work must be available.

## Impacted Components
- New extraction worker, common-field contract, and extracted-field repository adapter.

## Implementation Plan
- Load the stored source document for the queued command.
- Extract text and page structure with the approved libraries.
- Persist only validated common field drafts, marking absent source text incomplete.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_016/us_016.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/extraction/application/extract_common_fields.py | Coordinates common-field extraction jobs. |
| CREATE | app/extraction/contracts/common_fields.py | Defines validated common-field draft contracts. |
| CREATE | app/extraction/adapters/postgres/extracted_fields.py | Persists field drafts for review. |

## External References
- [PyMuPDF text extraction](https://pymupdf.readthedocs.io/en/latest/recipes-text.html)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Consume a classified extraction command and load its source document. (AC-001)
- [ ] Extract Provider Name, Provider Number, Survey Date, Tag, and SOD candidates. (AC-001)
- [ ] Validate extracted drafts against the application-owned contract. (AC-001)
- [ ] Persist validated common field drafts for review. (AC-001)
- [ ] Mark required fields incomplete when their source text is missing. (edge case)
- [ ] Do not infer a value when required source text is unavailable. (edge case)