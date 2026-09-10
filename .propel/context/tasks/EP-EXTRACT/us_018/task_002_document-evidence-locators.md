# Task - TASK_002

## Requirement Reference
- **User Story:** us_018
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: Supply a page, coordinate, or text-snippet locator for every extracted field or SOD.
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
| Document extraction | Tesseract OCR and PyMuPDF | Tesseract 5.x / PyMuPDF 1.x | FR-007 requires locators based on document extraction output. |

## Task Overview
Implement source-evidence locator generation from page text and coordinate extraction results. Estimated effort: 5 hours.

## Dependent Tasks
- US_016 document content extraction must be available.

## Impacted Components
- New source-evidence locator builder.

## Implementation Plan
- Prefer page and coordinate locators when geometric data is available.
- Fall back to a bounded text-snippet locator when coordinates are unavailable.
- Return an explicit unavailable result when source evidence cannot be located.

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
| CREATE | app/extraction/domain/evidence_locator.py | Builds typed page, coordinate, and text-snippet locators. |
| CREATE | app/extraction/adapters/pymupdf_evidence.py | Derives locator data from PyMuPDF page results. |

## External References
- [PyMuPDF text search](https://pymupdf.readthedocs.io/en/latest/page.html#Page.search_for)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Generate page and coordinate locators when extraction geometry is available. (AC-001)
- [ ] Generate a bounded text-snippet locator when geometry is unavailable. (AC-001)
- [ ] Associate a locator with each extracted field and SOD candidate. (AC-001)
- [ ] Return an unavailable evidence result when no source location can be derived. (edge case)
- [ ] Supply the unavailable result to the backend approval guard. (edge case)