# Task - TASK_001

## Requirement Reference
- **User Story:** us_044
- **Story Location:** .propel/context/tasks/EP-PERF-OBSERV/us_044/us_044.md
- **Acceptance Criteria:**
  - AC-001: A worker uses bounded retries for transient storage or LLM dependency failures and records a recoverable failure without approving content.
- **Edge Cases:**
  - An exhausted retry routes the job to the dead-letter queue.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | NFR-002, NFR-006, and TR-009 require typed worker failure classification and bounded recovery. |

---

## Task Overview
Extend worker dependency handling so transient Blob Storage and approved-LLM failures use bounded exponential retries, preserve recoverable job state, and never advance unapproved content. Estimated effort: 7 hours.

## Dependent Tasks
- US_003 durable worker delivery must provide idempotency, retryable result handling, and dead-letter settlement.
- US_019 extraction result guardrails must prevent failed or incomplete work from becoming approved content.

## Impacted Components
- New worker dependency-failure policy and updates to the processing job service and Service Bus worker adapter.

## Implementation Plan
- Define typed dependency-failure categories for transient storage and LLM failures.
- Apply a bounded exponential-backoff policy only to retryable categories.
- Persist a recoverable failure state and sanitized reason for each retryable outcome.
- Preserve the existing approval state whenever dependency processing fails.
- Return terminal settlement instructions after retry exhaustion so the Service Bus adapter dead-letters the job.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-PERF-OBSERV/us_044/us_044.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/processing/application/dependency_failure_policy.py | Defines retryable dependency categories, retry bounds, and failure-state transitions. |
| MODIFY | app/processing/application/job_service.py | Applies dependency-failure policy while preserving approval state. |
| MODIFY | app/processing/adapters/service_bus_worker.py | Maps exhausted retryable outcomes to Service Bus dead-letter settlement. |

## External References
- [FastAPI 0.141.1 error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Azure Service Bus dead-letter queues](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-dead-letter-queues)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass.
- [ ] Integration tests verify retry bounds, recovery records, approval preservation, and dead-letter settlement.

## Implementation Checklist
- [ ] Classify transient storage and LLM dependency failures as retryable worker outcomes. (AC-001)
- [ ] Apply bounded exponential retries only to retryable dependency failures. (AC-001)
- [ ] Record a recoverable job failure with a sanitized reason for each retryable outcome. (AC-001)
- [ ] Preserve the current unapproved content state when dependency processing fails. (AC-001)
- [ ] Dead-letter the job after its bounded retry attempts are exhausted. (AC-001, edge case)