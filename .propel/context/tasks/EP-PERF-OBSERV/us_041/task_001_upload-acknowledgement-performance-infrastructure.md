# Task - TASK_001

## Requirement Reference
- **User Story:** us_041
- **Story Location:** .propel/context/tasks/EP-PERF-OBSERV/us_041/us_041.md
- **Acceptance Criteria:**
  - AC-001: Under 100 concurrent user sessions with standard documents, the 95th percentile upload acknowledgement is at most 2 seconds.
- **Edge Cases:**
  - Background queue delay does not extend the synchronous acknowledgement.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Container Apps, Azure Service Bus, and Azure Monitor | Current GA service APIs | NFR-001 and NFR-007 require independent queueing and measured acknowledgement latency under concurrent load. |

---

## Task Overview
Provision a repeatable upload performance-test environment and Azure Monitor query that measures the API acknowledgement boundary independently of background queue processing. Estimated effort: 6 hours.

## Dependent Tasks
- US_011 intake endpoint implementation must be available before the performance scenario is executed.
- US_004 deployment workflow must establish the API revision and its Azure resources.

## Impacted Components
- New Azure Monitor workbook/query and load-test configuration for the deployed upload endpoint.

## Implementation Plan
- Define a representative standard-document upload scenario with 100 concurrent virtual users.
- Configure measurement from request receipt to synchronous processing-record acknowledgement only.
- Capture percentile latency in Azure Monitor using correlation-safe telemetry dimensions.
- Configure a pass/fail threshold for a 2-second 95th percentile acknowledgement.
- Report queue delay separately so asynchronous backlog cannot inflate acknowledgement latency.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-PERF-OBSERV/us_041/us_041.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | infra/monitoring/upload-acknowledgement-performance.bicep | Defines the latency query, threshold, and workbook resources for acknowledgement monitoring. |
| CREATE | infra/load-tests/upload-acknowledgement.yaml | Defines the 100-session standard-document upload performance scenario. |

## External References
- [Azure Load Testing test configuration](https://learn.microsoft.com/azure/load-testing/how-to-create-and-run-load-test)
- [Azure Monitor log queries](https://learn.microsoft.com/azure/azure-monitor/logs/log-query-overview)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Validate the infrastructure template against the target Azure subscription.
- [ ] Run the configured upload load test and inspect the acknowledgement percentile query.

## Implementation Checklist
- [x] Define a 100-concurrent-session upload scenario using standard documents. (AC-001)
- [x] Measure acknowledgement when the API returns the processing-record identifier. (AC-001)
- [x] Calculate and report the 95th percentile acknowledgement latency. (AC-001)
- [x] Set the performance threshold to at most 2 seconds at the 95th percentile. (AC-001)
- [x] Emit queue-delay telemetry separately from synchronous acknowledgement timing. (AC-001, edge case)