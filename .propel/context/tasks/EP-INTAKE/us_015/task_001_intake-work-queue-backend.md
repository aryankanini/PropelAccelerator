# Task - TASK_001

## Requirement Reference
- **User Story:** us_015
- **Story Location:** .propel/context/tasks/EP-INTAKE/us_015/us_015.md
- **Acceptance Criteria:**
  - AC-001: Persist and publish extraction work containing processing-record and correlation identifiers.
- **Edge Cases:**
  - A publication failure leaves the record retryable rather than showing extraction started.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | TR-003, DR-010, and NFR-009 require reliable application-owned scheduling. |

## Task Overview
Implement the transactional intake-to-extraction scheduling service. Estimated effort: 7 hours.

## Dependent Tasks
- US_009 idempotent job-attempt persistence must be available.
- US_012 successful classification must be available.

## Impacted Components
- New extraction command factory, intake scheduling service, and retryable state transition.

## Implementation Plan
- Create a stable extraction command from a classified record.
- Persist job identity, processing-record identity, correlation identifier, and pending state before publication.
- Publish through a queue port and transition failures to a retryable state.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-INTAKE/us_015/us_015.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/intake/application/schedule_extraction.py | Persists and publishes extraction commands. |
| CREATE | app/intake/contracts/extraction_command.py | Defines the correlated extraction command contract. |
| CREATE | app/intake/domain/scheduling_state.py | Defines pending, published, and retryable scheduling states. |

## External References
- [Azure Service Bus Python SDK](https://learn.microsoft.com/python/api/overview/azure/servicebus-readme)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Create an extraction command only for a successfully classified record. (AC-001)
- [x] Include stable processing-record and correlation identifiers in the command. (AC-001)
- [x] Persist the job and pending state before queue publication. (AC-001)
- [x] Publish the command through the application queue port. (AC-001)
- [x] Move a publication failure to a retryable state. (edge case)
- [x] Prevent a failed publication from indicating extraction has started. (edge case)