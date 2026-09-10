# Task - TASK_001

## Requirement Reference
- **User Story:** us_019
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_019/us_019.md
- **Acceptance Criteria:**
  - AC-001: Mark fields incomplete or low-confidence for missing, ambiguous, or below-threshold evidence and never represent them as complete.
- **Edge Cases:**
  - Reject malformed AI responses into a failure state without partial unvalidated fields.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001, AIR-003 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | app/ai_gateway/prompts/extraction/ |
| **Guardrails Config** | app/ai_gateway/contracts/extraction_result.py |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI Gateway | Application-owned gateway and Pydantic | Pydantic 2.x | AIR-001 and AIR-003 require strict response validation and abstention handling. |

## Task Overview
Implement schema and confidence guardrails for AI-assisted extraction results. Estimated effort: 7 hours.

## Dependent Tasks
- US_016 extraction worker must supply structured result candidates.

## Impacted Components
- New strict result schema, confidence policy, and extraction failure mapper.

## Implementation Plan
- Define a closed Pydantic extraction-result contract.
- Evaluate evidence availability, ambiguity, and approved confidence thresholds.
- Persist only wholly validated results or a bounded failure state.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_019/us_019.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/ai_gateway/contracts/extraction_result.py | Defines strict AI extraction response models. |
| CREATE | app/ai_gateway/application/validate_extraction_result.py | Applies evidence and confidence guardrails. |
| CREATE | app/extraction/domain/extraction_failure.py | Maps rejected results to durable failure state. |

## External References
- [Pydantic extra data](https://docs.pydantic.dev/latest/concepts/models/#extra-data)
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Define a strict extraction response model that forbids unexpected properties. (AC-001)
- [ ] Require evidence references with explicit confidence and status values. (AC-001)
- [ ] Mark absent evidence as incomplete rather than complete. (AC-001)
- [ ] Mark ambiguous or below-threshold results low-confidence. (AC-001)
- [ ] Reject malformed responses before any extracted fields are persisted. (edge case)
- [ ] Record a durable failure state for rejected AI responses. (edge case)