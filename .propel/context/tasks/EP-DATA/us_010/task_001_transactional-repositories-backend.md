# Task - TASK_001

## Requirement Reference

- **User Story:** us_010
- **Story Location:** .propel/context/tasks/EP-DATA/us_010/us_010.md
- **Acceptance Criteria:**
  - AC-001: Commit approval state and audit revision together or store neither change.
- **Edge Cases:**
  - Return a recoverable database connection error without reporting a review decision as approved.

---

## Applicable Technology Stack

| Layer   | Technology | Version     | Justification                                                                                         |
| ------- | ---------- | ----------- | ----------------------------------------------------------------------------------------------------- |
| Backend | Python     | Python 3.12 | DR-003 and DR-004 require application-owned transaction boundaries around review state and revisions. |

---

## Task Overview

Define typed repository and unit-of-work ports so the review service commits approval state and immutable audit revisions atomically. Estimated effort: 7 hours.

## Dependent Tasks

- US_006 workflow record schema must provide approval and revision records.

## Impacted Components

- New repository protocols, unit-of-work port, review persistence service, and recoverable persistence error.

## Implementation Plan

- Define typed repositories for POC approval state and content revision persistence.
- Define a unit-of-work port with explicit transaction commit and rollback semantics.
- Make the review application service persist the decision and immutable audit revision through one unit of work.
- Roll back both pending changes when validation or persistence fails.
- Translate database connectivity failures to a recoverable result that never represents approval as successful.

## Current Project State

```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-DATA/us_010/us_010.md
`- .propel/context/docs/design.md
```

## Expected Changes

| Action | File Path                                    | Description                                                           |
| ------ | -------------------------------------------- | --------------------------------------------------------------------- |
| CREATE | app/review/ports/repositories.py             | Defines typed approval-state and audit-revision repository protocols. |
| CREATE | app/platform/ports/unit_of_work.py           | Defines transaction commit and rollback contract.                     |
| CREATE | app/review/application/review_persistence.py | Coordinates atomic review decision and audit revision persistence.    |

## External References

- [Python 3.12 typing protocols](https://docs.python.org/3.12/library/typing.html#typing.Protocol)
- [PostgreSQL 16 transactions](https://www.postgresql.org/docs/16/tutorial-transactions.html)

## Build Commands

- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist

- [X] Define typed repositories for approval state and immutable audit revisions. (AC-001)
- [X] Define a unit-of-work transaction boundary for related review writes. (AC-001)
- [X] Persist approval state and audit revision before one explicit commit. (AC-001)
- [X] Roll back all pending review changes when either write fails. (AC-001)
- [X] Return a recoverable connection failure without an approved outcome. (edge case)
