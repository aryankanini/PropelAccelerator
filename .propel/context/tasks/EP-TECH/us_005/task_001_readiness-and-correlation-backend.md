# Task - TASK_001

## Requirement Reference
- **User Story:** us_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Acceptance Criteria:**
  - AC-001: Report ready only after required dependencies and configuration checks succeed.
  - AC-002: Preserve one correlation identifier in structured logs and OpenTelemetry-compatible traces across workflow operations.
- **Edge Cases:**
  - Report not ready within the configured dependency timeout without exposing credentials.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | NFR-006, NFR-009, and TR-011 require health and correlation from the application boundary. |

---

## Task Overview
Implement bounded readiness evaluation and correlation-context propagation in the shared API and worker application boundary. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 common application startup boundary must be available.
- US_003 message contracts must carry correlation ID before worker correlation propagation is connected.

## Impacted Components
- New readiness service, FastAPI health route and middleware, correlation context utility, and worker context adapter.

## Implementation Plan
- Define a readiness port for required configuration and dependency probes with per-probe timeouts.
- Execute readiness checks during application lifespan and expose a minimal readiness result that contains no configuration values or credentials.
- Return not-ready when a required probe fails or times out; distinguish readiness from liveness.
- Establish correlation ID from a trusted request header or generate one at the API boundary.
- Include correlation ID in queue message application properties and restore it before worker operations.
- Add correlation, processing-record, job, and source-document identifiers as structured log fields and trace attributes.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-TECH/us_005/us_005.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/platform/health/readiness.py | Defines bounded readiness checks and sanitized result states. |
| CREATE | app/platform/observability/correlation.py | Defines correlation context and structured identifier fields. |
| CREATE | app/api/health.py | Exposes the readiness route. |
| CREATE | app/api/middleware/correlation.py | Establishes request correlation context. |
| CREATE | app/processing/adapters/correlation_context.py | Transfers correlation context into and out of queue messages. |

## External References
- [FastAPI lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [FastAPI middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Define required configuration and dependency readiness checks with bounded timeouts. (AC-001)
- [ ] Return ready only after all required checks succeed during application startup. (AC-001)
- [ ] Return a sanitized not-ready response when a dependency fails or times out. (AC-001, edge case)
- [ ] Establish and preserve a correlation ID at the API request boundary. (AC-002)
- [ ] Include correlation ID in application-owned queue message properties and restore it in the worker. (AC-002)
- [ ] Attach correlation, processing-record, job, and source-document identifiers to structured logs and trace spans. (AC-002)