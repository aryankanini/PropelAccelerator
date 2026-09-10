# Task - TASK_003

## Requirement Reference
- **User Story:** us_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Support observable duplicate delivery without producing duplicate compliance work.
  - AC-002: Dead-letter commands with their correlation identifier and failure reason after configured bounded retries.
- **Edge Cases:**
  - Route malformed commands to the dead-letter path without worker execution.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Service Bus | Current GA service APIs | TR-003 and TR-009 require at-least-once delivery, bounded retries, duplicate detection, and dead-letter routing. |

---

## Task Overview
Provision and configure the durable Service Bus command queue, duplicate-detection window, bounded delivery count, and dead-letter operational path. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 must establish the infrastructure-as-code and environment configuration boundary.
- TASK_001 must define the message contract and settlement outcomes.

## Impacted Components
- New Azure Service Bus namespace, processing queue, dead-letter monitoring configuration, and least-privilege identities.

## Implementation Plan
- Define the processing queue in infrastructure as code with duplicate detection enabled and a documented history window.
- Set an explicit max delivery count consistent with the worker's bounded retry policy.
- Enable the built-in dead-letter subqueue and route terminal application failures through explicit settlement metadata.
- Grant API send and worker receive/settle identities only the required Service Bus data roles.
- Configure alerts for dead-letter growth and max-delivery exhaustion without including message body content.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/
|  |- context/tasks/EP-TECH/us_003/us_003.md
|  `- context/docs/design.md
`- .github/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | infra/service-bus.bicep | Defines the namespace, processing queue, duplicate detection, and bounded delivery count. |
| CREATE | infra/monitoring/service-bus-alerts.bicep | Defines dead-letter and retry-exhaustion alerts. |
| CREATE | infra/roles/service-bus-roles.bicep | Assigns least-privilege sender and receiver roles to workload identities. |

## External References
- [Azure Service Bus dead-letter queues](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-dead-letter-queues)
- [Azure Service Bus duplicate detection](https://learn.microsoft.com/azure/service-bus-messaging/duplicate-detection)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Provision a queue with duplicate detection and a bounded max delivery count. (AC-001, AC-002)
- [ ] Configure the duplicate-detection window for stable processing command IDs. (AC-001)
- [ ] Retain the Service Bus dead-letter subqueue for invalid and exhausted commands. (AC-002, edge case)
- [ ] Restrict sender and receiver access using workload identities and least-privilege data roles. (AC-001, AC-002)
- [ ] Alert on dead-letter growth and max-delivery exhaustion without exposing message contents. (AC-002)