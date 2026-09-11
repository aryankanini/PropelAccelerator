# Task - TASK_003

## Requirement Reference
- **User Story:** us_026
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_026/us_026.md
- **Acceptance Criteria:**
  - AC-001: The gateway retrieves only approved CMS records and attaches identifiers and versions to the request.
- **Edge Cases:**
  - No approved source returns a blocked, ungrounded outcome and does not approve a draft.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Application-owned gateway and one approved LLM model | LLM model/version TBD | AIR-002 and TR-005 require source context before inference. |

---

## Task Overview
Enforce grounded-request construction in the application-owned AI gateway. Estimated effort: 5 hours.

## Dependent Tasks
- US_026 approved-source retrieval must provide deterministic source context.

## Impacted Components
- New AI gateway source-context guard and structured request contract.

## Implementation Plan
- Require approved source identifiers and versions before creating an inference request.
- Include source context in the request supplied to the approved model.
- Refuse inference when the source set is empty or unapproved.
- Keep draft approval state outside the gateway.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_026/us_026.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/ai_gateway/application/grounded_request_guard.py | Requires approved source context before model invocation. |

## External References
- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Require approved source identifiers and versions in every model request. (AC-001)
- [x] Attach the approved source context to the model request. (AC-001)
- [x] Refuse an empty or unapproved source set with a blocked ungrounded outcome. (edge case)
- [x] Keep draft approval state under deterministic application control. (edge case)
