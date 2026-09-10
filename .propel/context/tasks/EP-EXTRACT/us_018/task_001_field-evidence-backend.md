# Task - TASK_001

## Requirement Reference
- **User Story:** us_018
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: Persist a page, coordinate, or text-snippet locator for every extracted field or SOD.
- **Edge Cases:**
  - An unavailable locator flags the field incomplete and blocks approval.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | app/extraction/prompts/common_fields/ |
| **Guardrails Config** | app/extraction/contracts/evidence.py |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-007 and AIR-001 require traceable field evidence. |

## Task Overview
Implement evidence-locator construction and persistence for extracted fields and SODs. Estimated effort: 6 hours.

## Dependent Tasks
- US_007 evidence storage must be available.
- US_016 common field extraction must be available.

## Impacted Components
- New evidence locator contract, locator builder, and extracted-field persistence extension.

## Implementation Plan
- Derive a page, coordinate, or source text locator from extraction output.
- Validate that each persisted draft has a retrievable locator.
- Mark locator failures incomplete so approval remains blocked.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_018/us_018.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/extraction/contracts/evidence.py | Defines evidence-locator validation contracts. |
| MODIFY | app/extraction/adapters/postgres/extracted_fields.py | Persists evidence locators and incomplete state. |

## External References
- [PyMuPDF text search](https://pymupdf.readthedocs.io/en/latest/page.html#Page.search_for)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Build a page, coordinate, or text-snippet locator for each field and SOD. (AC-001)
- [ ] Validate locator data before persisting extracted content. (AC-001)
- [ ] Persist the locator with each extracted field and SOD draft. (AC-001)
- [ ] Mark a draft incomplete when no locator can be created. (edge case)
- [ ] Surface the incomplete state to the approval boundary. (edge case)