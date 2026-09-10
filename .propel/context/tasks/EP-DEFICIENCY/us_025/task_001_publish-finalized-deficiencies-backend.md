# Task - TASK_001

## Requirement Reference
- **User Story:** us_025
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_025/us_025.md
- **Acceptance Criteria:**
  - AC-001: One idempotent POC-generation command is published per confirmed deficiency.
- **Edge Cases:**
  - Repeated finalization does not publish duplicate logical POC work.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | FR-009, DR-010, and TR-003 require idempotent finalization commands. |

---

## Task Overview
Publish exactly one durable POC-generation command for each confirmed deficiency at finalization. Estimated effort: 7 hours.

## Dependent Tasks
- US_024 must establish POC eligibility.
- US_009 must provide idempotent job persistence.

## Impacted Components
- New finalization service and Service Bus publishing adapter port.

## Implementation Plan
- Validate that every selected deficiency is confirmed and eligible.
- Generate a stable command identity from the deficiency and finalization context.
- Create-or-return the job before publishing its command.
- Publish only newly created logical work and retain correlation identifiers.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
`- .propel/context/tasks/EP-DEFICIENCY/us_025/us_025.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/application/finalization_service.py | Creates idempotent POC-generation commands for confirmed deficiencies. |
| CREATE | app/processing/ports/poc_command_publisher.py | Defines durable POC command publication. |

## External References
- [Azure Service Bus duplicate detection](https://learn.microsoft.com/azure/service-bus-messaging/duplicate-detection)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Publish one POC-generation command for every confirmed deficiency. (AC-001)
- [ ] Use a stable deficiency-scoped identity for each command. (AC-001)
- [ ] Persist or retrieve the idempotent job outcome before publication. (AC-001)
- [ ] Return the prior outcome without duplicate publication on repeated finalization. (edge case)
