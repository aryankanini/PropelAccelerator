# Task - TASK_001

## Requirement Reference
- **User Story:** us_030
- **Story Location:** .propel/context/tasks/EP-POC-GEN/us_030/us_030.md
- **Acceptance Criteria:**
  - AC-001: Extraction, SOD recall, citation support, POC quality, refusal, and conditional-field results are recorded against a versioned test set.
- **Edge Cases:**
  - A missing evaluation category blocks release promotion.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-005, AIR-006 |
| **AI Pattern** | Grounded LLM with deterministic source context and review gates |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | N/A |
| **Model Provider** | One approved LLM model; version TBD |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Application-owned gateway and one approved LLM model | LLM model/version TBD | AIR-005 and AIR-006 require versioned evaluation and deterministic release gating. |

---

## Task Overview
Implement versioned AI evaluation that requires complete category coverage before release promotion. Estimated effort: 8 hours.

## Dependent Tasks
- US_028 must establish the approved POC validation rubric.

## Impacted Components
- New AI evaluation runner, category result contract, and deterministic release gate.

## Implementation Plan
- Define a versioned test-set manifest and candidate prompt/model identity.
- Run and collect extraction, SOD recall, citation support, POC quality, refusal, and conditional-field evaluations.
- Verify every required category produced a result before computing release eligibility.
- Return a deterministic blocked decision for incomplete results without modifying approval state.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-POC-GEN/us_030/us_030.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/ai_gateway/application/release_evaluator.py | Runs versioned evaluation categories and release gate. |
| CREATE | app/ai_gateway/domain/evaluation_contract.py | Defines required category and release-decision structures. |

## External References
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Version the evaluated test set and proposed model or prompt identity. (AC-001)
- [ ] Record extraction, SOD recall, citation support, POC quality, refusal, and conditional-field results. (AC-001)
- [ ] Compute release eligibility only after all required category results exist. (AC-001)
- [ ] Block release promotion when any evaluation category is missing. (edge case)
- [ ] Keep approval-state transitions under deterministic application rules. (AC-001)
