# Task - TASK_003

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
| AI/ML | Application-owned gateway and one approved LLM model | LLM model/version TBD | AIR-001 and AIR-003 require strict structured output and abstention. |

---

## Task Overview
Define and enforce the AI gateway POC response schema used by deterministic rubric validation. Estimated effort: 5 hours.

## Dependent Tasks
- US_026 must establish grounded requests.

## Impacted Components
- New POC structured-output schema and gateway refusal mapping.

## Implementation Plan
- Define required POC element, confidence, evidence, and refusal fields.
- Reject unknown properties and malformed structured responses.
- Translate missing elements or refusal to a validation-ready blocked outcome.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_028/us_028.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/ai_gateway/domain/poc_response_schema.py | Defines strict POC structured output validation. |

## External References
- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Require structured required-element, evidence, and confidence fields. (AC-001)
- [ ] Reject malformed or additional response properties before review. (AC-001)
- [ ] Map a missing required element to a blocked validation outcome. (edge case)
- [ ] Preserve the missing-element identity in the refusal or validation result. (edge case)
