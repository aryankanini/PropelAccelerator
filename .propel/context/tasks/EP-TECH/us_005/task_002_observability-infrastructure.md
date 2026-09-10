# Task - TASK_002

## Requirement Reference
- **User Story:** us_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Acceptance Criteria:**
  - AC-001: Invoke readiness probes for deployed API and worker revisions.
  - AC-002: Export correlated structured logs and OpenTelemetry-compatible traces for workflow diagnosis.
- **Edge Cases:**
  - Ensure a timed-out dependency readiness check results in a not-ready probe response without credentials.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Monitor, Application Insights, Log Analytics, and OpenTelemetry | Current GA service APIs / OpenTelemetry 1.x | NFR-006, NFR-009, TR-011, and TR-012 require managed health and correlation visibility. |

---

## Task Overview
Configure Container Apps readiness probes and Azure telemetry resources so API and worker deployments expose usable, correlated diagnostic signals without disclosing sensitive data. Estimated effort: 6 hours.

## Dependent Tasks
- TASK_001 readiness and correlation backend implementation must be available before probe and exporter configuration.
- US_004 deployment workflow must establish the Container Apps deployment definitions.

## Impacted Components
- New Azure Monitor workspace, Application Insights resource, Container Apps probe configuration, diagnostic settings, and operational alerts.

## Implementation Plan
- Configure API and worker Container Apps with readiness probes that use the application readiness endpoint or equivalent worker readiness mechanism.
- Set probe timing and failure thresholds that respect the application dependency timeout and avoid marking a revision ready prematurely.
- Create Application Insights and Log Analytics destinations for OpenTelemetry-compatible traces and structured logs.
- Configure diagnostic settings and retention consistent with authorized operator troubleshooting.
- Add alerts for unavailable revisions, sustained not-ready state, and telemetry export failures without recording credentials or request payloads.

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
| CREATE | infra/observability.bicep | Defines Log Analytics, Application Insights, and diagnostic settings. |
| CREATE | infra/container-app-probes.bicep | Defines API and worker readiness probes and thresholds. |
| CREATE | infra/monitoring/health-alerts.bicep | Defines alerts for readiness and telemetry export failures. |

## External References
- [Azure Container Apps health probes](https://learn.microsoft.com/azure/container-apps/health-probes)
- [Azure Monitor OpenTelemetry overview](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-overview)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Configure readiness probes for API and worker revisions with explicit timing and failure thresholds. (AC-001)
- [ ] Keep revisions unavailable when the application reports a required dependency or configuration failure. (AC-001, edge case)
- [ ] Provision telemetry destinations for structured logs and OpenTelemetry-compatible traces. (AC-002)
- [ ] Enable diagnostics that retain correlation identifiers while excluding credentials and message payloads. (AC-002)
- [ ] Alert authorized operators on sustained not-ready revisions and telemetry export failures. (AC-001, AC-002)