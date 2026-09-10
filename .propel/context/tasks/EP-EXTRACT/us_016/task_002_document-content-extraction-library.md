# Task - TASK_002

## Requirement Reference
- **User Story:** us_016
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Supply Provider Name, Provider Number, Survey Date, Tag, and SOD source candidates for reviewable drafts.
- **Edge Cases:**
  - Missing required source text creates an incomplete field rather than an inferred value.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Document extraction | Tesseract OCR and PyMuPDF | Tesseract 5.x / PyMuPDF 1.x | TR-008 requires approved open-source form-content extraction. |

## Task Overview
Implement the document reader that exposes source-backed common field candidates to the extraction worker. Estimated effort: 6 hours.

## Dependent Tasks
- US_015 queued extraction work and source-document references must be available.

## Impacted Components
- New PyMuPDF document reader and OCR fallback adapter.

## Implementation Plan
- Open only the uploaded document bytes from the source-document port.
- Extract text, page positions, and OCR content using approved open-source libraries.
- Return source-backed candidates or a missing-source result without inferring data.

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
| CREATE | app/extraction/adapters/pymupdf_document_reader.py | Reads source document text and page structure. |
| CREATE | app/extraction/adapters/tesseract_ocr.py | Supplies OCR text for required source regions. |
| CREATE | app/extraction/contracts/document_content.py | Defines source-backed extraction candidates. |

## External References
- [PyMuPDF text extraction](https://pymupdf.readthedocs.io/en/latest/recipes-text.html)
- [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Read content from the stored source document through the document port. (AC-001)
- [ ] Extract page text and positions with PyMuPDF. (AC-001)
- [ ] Use Tesseract only for source regions requiring OCR. (AC-001)
- [ ] Return candidates for Provider Name, Provider Number, Survey Date, Tag, and SOD. (AC-001)
- [ ] Return a missing-source result when required text cannot be located. (edge case)
- [ ] Do not synthesize a value for a missing source region. (edge case)