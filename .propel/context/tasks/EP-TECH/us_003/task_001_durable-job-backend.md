# Task - TASK_001

## Requirement Reference
- **User Story:** us_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Record one logical processing outcome for duplicate deliveries of a stable processing-record and job-attempt identity.
  - AC-002: Dead-letter a command with correlation identifier and failure reason after bounded retries.
- **Edge Cases:**
  - Reject malformed commands before execution and provide a validation failure reason for dead-letter handling.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | DR-010 and TR-003 require typed, idempotent asynchronous commands. |

---

## Task Overview
Implement typed processing-command contracts and worker orchestration that validates messages, uses a stable idempotency key, records duplicate delivery, and classifies retryable failures. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 application worker ports must be available before connecting the worker adapter.
- TASK_002 durable-job database persistence must be completed before worker outcome recording.

## Impacted Components
- New Processing Job application port, command schema, idempotency service, and worker message handler.

## Implementation Plan
- Define an additive, versioned processing-command schema containing processing-record ID, job-attempt ID, correlation ID, and attempt count.
- Validate the command before invoking domain processing; classify malformed payloads as non-retryable validation failures.
- Derive one stable idempotency key from the processing-record and job-attempt IDs.
- Coordinate outcome lookup and persistence through the job repository port so duplicate deliveries return the recorded logical outcome without re-execution.
- Record duplicate-delivery observations and structured failure classifications on the job outcome.
- Expose retryable versus terminal worker results to the Service Bus adapter without logging command payloads or credentials.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-TECH/us_003/us_003.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/processing/application/commands.py | Defines validated, versioned processing-command models. |
| CREATE | app/processing/application/job_service.py | Coordinates idempotency, execution, duplicate observation, and failure classification. |
| CREATE | app/processing/ports/job_repository.py | Defines the persistence boundary for job outcomes and delivery observations. |
| CREATE | app/processing/adapters/service_bus_worker.py | Receives commands and maps application results to message settlement actions. |

## External References
- [FastAPI 0.141.1 middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Define and validate the stable processing command identity before execution. (AC-001)
- [ ] Ensure the worker invokes domain processing only after schema validation succeeds. (AC-001, edge case)
- [ ] Return the recorded outcome instead of re-executing a duplicate identity. (AC-001)
- [ ] Persist a duplicate-delivery observation for an already completed identity. (AC-001)
- [ ] Classify transient failures for bounded retry and terminal failures for dead-lettering. (AC-002)
- [ ] Preserve correlation ID and a sanitized failure reason in the terminal result. (AC-002)