# Task - TASK_002

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Acceptance Criteria:**
  - AC-002: Validate typed API startup
- **Edge Cases:**
  - Missing optional adapter configuration disables only that adapter and does not silently route workflow work.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| DevOps | Python configuration and FastAPI lifespan | Python 3.12, FastAPI 0.141.1 | TR-002 requires fail-fast typed API startup and NFR-003 requires reliable availability. |

---

## Task Overview
Implement typed environment configuration validation that fails before the API accepts requests and never exposes secret values.

## Dependent Tasks
- TASK_001 - Establishes the FastAPI composition root used for lifespan validation.

## Impacted Components
- CREATE: `app/config.py` typed runtime configuration model.
- MODIFY: `app/main.py` lifespan startup validation.

## Implementation Plan
1. Define required and optional configuration values in a typed model.
2. Validate required values at application startup through FastAPI lifespan.
3. Produce sanitized errors that identify missing keys only.
4. Explicitly disable adapters whose optional configuration is absent.
5. Inject validated configuration into the composition root.

## Current Project State
```
HealthcareAccelerator/
└── package.json
```

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | app/config.py | Provides typed required and optional runtime configuration. |
| MODIFY | app/main.py | Validates configuration in the FastAPI lifespan before serving requests. |

## External References
- https://fastapi.tiangolo.com/advanced/events/
- https://fastapi.tiangolo.com/advanced/testing-events/

## Build Commands
- Refer to the applicable Python build commands in `.propel/build/`.

## Implementation Validation Strategy
- [x] Unit tests verify missing required configuration produces sanitized validation errors.
- [x] Integration tests verify the FastAPI lifespan rejects invalid configuration before requests are accepted.

## Implementation Checklist
- [x] Define typed required and optional settings for AC-002.
- [x] Validate required settings during the FastAPI lifespan for AC-002.
- [x] Return the missing key name without a secret value for AC-002.
- [x] Disable, rather than silently substitute, an adapter with missing optional settings.
- [x] Pass only validated settings to the application composition root.