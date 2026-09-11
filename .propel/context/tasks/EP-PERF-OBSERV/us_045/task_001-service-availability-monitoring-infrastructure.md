# Task - TASK_001

## Requirement Reference
- **User Story:** us_045
- **Story Location:** .propel/context/tasks/EP-PERF-OBSERV/us_045/us_045.md
- **Acceptance Criteria:**
  - AC-001: Monitoring emits an actionable alert when health or availability thresholds are breached and reports monthly API availability against the 99.9% target.
- **Edge Cases:**
  - Scheduled maintenance announced at least 24 hours ahead is excluded from the availability calculation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Container Apps, Azure Monitor, Application Insights, and Log Analytics | Current GA service APIs | NFR-003 and NFR-006 require managed health checks, actionable alerts, and monthly availability reporting. |

---

## Task Overview
Configure API and worker health monitoring, actionable availability-risk alerts, and a monthly API availability report that applies the approved maintenance exclusion. Estimated effort: 6 hours.

## Dependent Tasks
- US_005 health and correlation telemetry must be available before availability signals are configured.
- US_004 deployment workflow must establish the API and worker revisions being monitored.

## Impacted Components
- New Azure Monitor availability query, alert rules, action group, and monthly availability workbook.

## Implementation Plan
- Configure health and availability signals for deployed API and worker revisions.
- Define alerts for breached health and availability thresholds with operator action context.
- Calculate monthly API availability against the 99.9% objective.
- Record announced maintenance windows with announcement timestamps.
- Exclude only maintenance announced at least 24 hours before the window from the availability calculation.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-PERF-OBSERV/us_045/us_045.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | infra/monitoring/service-availability.bicep | Defines health signals, alert rules, action group, and monthly availability workbook resources. |

## External References
- [Azure Monitor availability tests](https://learn.microsoft.com/azure/azure-monitor/app/availability-overview)
- [Azure Monitor alert rules](https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-create-metric-alert-rule)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Validate the infrastructure template against the target Azure subscription.
- [ ] Simulate a threshold breach and verify alert payload and monthly availability calculation.

## Implementation Checklist
- [x] Configure API and worker health signals for deployed revisions. (AC-001)
- [x] Create actionable alerts for breached health or availability thresholds. (AC-001)
- [x] Calculate monthly API availability against the 99.9% target. (AC-001)
- [x] Publish the availability result through the operational monitoring view. (AC-001)
- [x] Exclude only maintenance announced at least 24 hours ahead from the calculation. (AC-001, edge case)