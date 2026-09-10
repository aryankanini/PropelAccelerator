# Task - TASK_001

## Requirement Reference
- **User Story:** us_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Acceptance Criteria:**
  - AC-001: Build API and worker images and run automated tests before deployment promotion.
  - AC-002: Start the API, worker, and local dependencies with one documented command.
- **Edge Cases:**
  - Fail deployment configuration validation for an absent required secret without printing its name or value.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| DevOps | Azure Container Apps with separate API and worker revisions | Current GA service APIs | NFR-003, DR-008, and TR-012 require repeatable promotion and separately scalable deployments. |

---

## Task Overview
Create a reproducible local environment and delivery pipeline that builds separate API and worker images, runs the canonical tests, validates required deployment secrets safely, and blocks promotion on failure. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 must package the API and worker application boundaries.

## Impacted Components
- New container build definitions, local dependency composition, CI workflow, deployment manifest, and environment-variable contract.

## Implementation Plan
- Define separate API and worker container build targets from the shared Python application source.
- Create one local composition command that starts the API, worker, PostgreSQL, Azurite, and Service Bus emulator or documented development equivalent.
- Add CI stages to build both images and run the configured test command before any deploy stage.
- Require each deployment environment to validate required secret references without echoing keys or values.
- Gate promotion on the successful build and test stages and publish only immutable image references.
- Document local configuration variable names and the single startup command without recording secret values.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .env
|- .github/
`- .propel/
   `- context/tasks/EP-TECH/us_004/us_004.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | Dockerfile | Builds selectable API and worker container targets. |
| CREATE | compose.yaml | Starts API, worker, and required local dependencies with one command. |
| CREATE | .github/workflows/ci.yml | Builds both images, runs tests, and gates promotion. |
| CREATE | infra/container-apps.bicep | Defines API and worker deployment revisions from immutable image references. |
| CREATE | .env.example | Documents local configuration variable names without values. |
| CREATE | README.md | Documents the one-command local startup workflow. |

## External References
- [Azure Container Apps CI/CD](https://learn.microsoft.com/azure/container-apps/github-actions)
- [Docker Compose reference](https://docs.docker.com/compose/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Build independent API and worker container images from the shared application source. (AC-001)
- [ ] Run the configured automated test command as a required CI stage. (AC-001)
- [ ] Prevent deployment promotion whenever image build or tests fail. (AC-001)
- [ ] Start API, worker, and local dependencies with the documented compose command. (AC-002)
- [ ] Validate required deployment secret references without logging secret names or values. (edge case)
- [ ] Deploy API and worker as separately scalable Container Apps revisions using immutable image references. (AC-001)