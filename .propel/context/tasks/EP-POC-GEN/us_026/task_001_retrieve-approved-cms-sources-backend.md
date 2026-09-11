# Task - TASK_001

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
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-011, TR-005, and TR-007 require an application-owned retrieval boundary. |

---

## Task Overview
Implement the POC retrieval workflow that obtains approved CMS context or returns a non-approvable blocked outcome. Estimated effort: 7 hours.

## Dependent Tasks
- US_025 must publish finalized deficiency work.
- CMS knowledge maintenance must provide approved source records.

## Impacted Components
- New CMS context retrieval service and typed grounded-request outcome.

## Implementation Plan
- Accept confirmed deficiency and Tag identity from the POC worker.
- Query only source records selected by the approved-source repository contract.
- Attach immutable source identifiers and versions to the grounded request.
- Return an ungrounded blocked result when no approved source is available.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_026/us_026.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/knowledge/application/cms_context_retrieval.py | Retrieves approved context for a confirmed deficiency. |
| CREATE | app/poc/domain/grounded_request.py | Defines grounded and blocked request outcomes. |

## External References
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Accept a confirmed deficiency and Tag as retrieval input. (AC-001)
- [x] Select only approved CMS records through the knowledge repository. (AC-001)
- [x] Attach source identifiers and versions to the grounded request. (AC-001)
- [x] Return a blocked ungrounded result and no approvable draft when no source is approved. (edge case)
