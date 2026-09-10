# Task - TASK_001

## Requirement Reference
- **User Story:** us_028
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_028/us_028.md
- **Acceptance Criteria:**
  - AC-001: Validation records required-element results and quality score before review.
- **Edge Cases:**
  - A missing required element blocks approval and identifies the missing element.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001, AIR-003 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-012 and AIR-003 require deterministic validation before review. |

---

## Task Overview
Implement the deterministic rubric validator and approval gate for generated POC drafts. Estimated effort: 6 hours.

## Dependent Tasks
- US_027 must persist generated POC drafts.

## Impacted Components
- New POC rubric validation service and blocked-review outcome.

## Implementation Plan
- Evaluate required elements against the approved rubric.
- Calculate and return a quality score with element-level results.
- Mark a draft blocked before review when required elements are missing.
- Keep approval transitions outside AI-generated output.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_028/us_028.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/poc/application/rubric_validator.py | Evaluates required POC elements and quality score. |

## External References
- [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Evaluate each draft against approved required POC elements. (AC-001)
- [ ] Produce a quality score and element-level validation result before review. (AC-001)
- [ ] Block the approval path when a required element is absent. (edge case)
- [ ] Identify every missing required element in the blocked result. (edge case)
