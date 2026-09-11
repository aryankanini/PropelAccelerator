# Task - TASK_001

## Requirement Reference
- **User Story:** us_042
- **Story Location:** .propel/context/tasks/EP-PERF-OBSERV/us_042/us_042.md
- **Acceptance Criteria:**
  - AC-001: At least 95% of representative standard-document jobs complete within 10 minutes of queue acceptance.
- **Edge Cases:**
  - Staff review time is excluded from processing-duration measurement.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Container Apps, Azure Service Bus, and Azure Monitor | Current GA service APIs | NFR-002 and NFR-007 require scalable worker processing and measured completion duration from queue acceptance. |

---

## Task Overview
Configure a processing performance scenario and telemetry query that measures queue-accepted jobs through completed processing, excluding the human review phase. Estimated effort: 6 hours.

## Dependent Tasks
- US_003 durable worker delivery must be available before completion-duration measurement.
- US_004 deployment workflow must establish separately scalable worker revisions.

## Impacted Components
- New worker performance-test configuration and Azure Monitor completion-duration query.

## Implementation Plan
- Define representative standard-document processing input for the worker load scenario.
- Capture the queue-acceptance timestamp and terminal processing-completion timestamp.
- Exclude staff-review transitions from the completion-duration calculation.
- Calculate the percentage of accepted jobs completed within ten minutes.
- Configure a threshold that requires at least 95% of measured jobs to meet the target.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-PERF-OBSERV/us_042/us_042.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | infra/monitoring/processing-completion-performance.bicep | Defines completion-duration queries, threshold, and workbook resources. |
| CREATE | infra/load-tests/processing-completion.yaml | Defines representative document processing performance inputs and success criteria. |

## External References
- [Azure Container Apps scaling](https://learn.microsoft.com/azure/container-apps/scale-app)
- [Azure Monitor log queries](https://learn.microsoft.com/azure/azure-monitor/logs/log-query-overview)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Validate the infrastructure template against the target Azure subscription.
- [ ] Run the processing scenario and verify the completion-duration query excludes review time.

## Implementation Checklist
- [x] Define representative standard-document processing load inputs. (AC-001)
- [x] Record the queue-acceptance timestamp for every measured job. (AC-001)
- [x] Calculate completion duration through terminal processing completion. (AC-001)
- [x] Exclude staff-review time from the processing-duration calculation. (AC-001, edge case)
- [x] Require at least 95% of accepted jobs to complete within 10 minutes. (AC-001)