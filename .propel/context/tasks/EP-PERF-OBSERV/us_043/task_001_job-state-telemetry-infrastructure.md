# Task - TASK_001

## Requirement Reference
- **User Story:** us_043
- **Story Location:** .propel/context/tasks/EP-PERF-OBSERV/us_043/us_043.md
- **Acceptance Criteria:**
  - AC-001: Authorized operators can view state, retry count, and failure reason within 60 seconds of a job state change.
- **Edge Cases:**
  - Telemetry failure does not expose restricted document content.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Monitor, Application Insights, Log Analytics, and OpenTelemetry | Current GA service APIs / OpenTelemetry 1.x | NFR-006, NFR-009, and TR-011 require correlated, sanitized operational telemetry. |

---

## Task Overview
Provision operational telemetry queries and alerts that expose state changes, retry counts, and sanitized failure reasons to authorized operators within the required observation window. Estimated effort: 6 hours.

## Dependent Tasks
- US_005 correlated telemetry implementation must be available before telemetry routing is configured.
- US_004 deployment workflow must establish Azure Monitor and Application Insights resources.

## Impacted Components
- New Log Analytics query, Azure Monitor workbook, diagnostic settings, and stale-telemetry alert.

## Implementation Plan
- Route worker state-change telemetry to Application Insights and Log Analytics.
- Configure queries that display job state, retry count, failure reason, and correlation identifiers.
- Restrict operational views and alert delivery to authorized operator channels.
- Configure a 60-second freshness window for state-change visibility.
- Exclude document bodies, storage URLs, credentials, and other restricted content from telemetry fields.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-PERF-OBSERV/us_043/us_043.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | infra/monitoring/job-state-telemetry.bicep | Defines telemetry diagnostic settings, workbook query, and freshness alert resources. |

## External References
- [Azure Monitor OpenTelemetry overview](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-overview)
- [Azure Monitor log queries](https://learn.microsoft.com/azure/azure-monitor/logs/log-query-overview)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Validate the infrastructure template against the target Azure subscription.
- [ ] Emit a state transition and verify the operator query shows the required fields within 60 seconds.

## Implementation Checklist
- [ ] Route worker state-change telemetry to the centralized monitoring resources. (AC-001)
- [ ] Create an authorized-operator query for state, retry count, and sanitized failure reason. (AC-001)
- [ ] Include correlation identifiers needed to associate a telemetry record with its job. (AC-001)
- [ ] Configure a 60-second freshness threshold for state-change visibility. (AC-001)
- [ ] Exclude restricted document content and credentials from configured telemetry fields. (AC-001, edge case)