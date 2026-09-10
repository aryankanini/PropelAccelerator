# Task - TASK_001

## Requirement Reference
- **User Story:** US_002
- **Story Location:** `.propel/context/tasks/EP-TECH/us_002/us_002.md`
- **Acceptance Criteria:**
  - AC-001: Provision a Container Apps environment, PostgreSQL Flexible Server, Blob Storage, and Service Bus with PostgreSQL public access disabled or restricted by approved network policy.
  - AC-002: Version the source-document storage lifecycle policy with deployment configuration and evaluate it before promotion.
- **Edge Cases:**
  - A partial deployment failure must not report the environment as ready and must identify the failed resource for operator retry.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Infrastructure | Azure Container Apps, Azure Database for PostgreSQL Flexible Server, Azure Blob Storage, Azure Service Bus, Azure Monitor | Current GA service APIs | NFR-003, DR-005, DR-009, and TR-004 require isolated, durable, observable Azure runtime services. |

---

## Task Overview
Create a declarative Azure runtime foundation for the compliance application. The deployment must provision the approved compute, data, messaging, and object-storage services in a controlled network boundary, apply a versioned Blob lifecycle policy, and return an unambiguous readiness result for operators.

## Dependent Tasks
- US_001 must establish the application deployment boundary before this infrastructure task begins.

## Impacted Components
- New `infra/` deployment configuration for the application runtime boundary.
- New Azure resource modules for network, runtime services, monitoring, lifecycle policy, and deployment-result handling.
- No existing application source is modified; the repository currently contains no infrastructure implementation.

## Implementation Plan
1. Establish a parameterized Bicep entry point with environment naming, region, tags, and approved network-policy inputs.
2. Create the virtual network, delegated PostgreSQL subnet, private DNS integration, and required private-access path before database provisioning.
3. Provision the Container Apps environment with Log Analytics integration and private-network configuration consistent with the approved policy.
4. Provision PostgreSQL Flexible Server on PostgreSQL 16 with public network access disabled, private DNS, backups, and restore settings aligned to DR-009.
5. Provision a hardened Storage account and source-document container, then attach the checked-in lifecycle management policy.
6. Provision the Service Bus namespace and required processing queue configuration with secure transport and diagnostic settings.
7. Add deployment orchestration that evaluates the lifecycle policy, waits for resource provisioning outcomes, and reports `ready` only when all resources succeed; on failure, return the Azure failed-resource detail for targeted retry.

## Current Project State
```text
HealthcareAccelerator/
├── .github/
├── .propel/
│   └── context/
│       └── tasks/
│           └── EP-TECH/
│               └── us_002/
│                   ├── us_002.md
│                   └── task_001_provision_azure_runtime_services.md
├── node_modules/
├── package-lock.json
└── package.json
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | `infra/main.bicep` | Composes the network, runtime, monitoring, and lifecycle modules and exposes non-secret deployment outputs. |
| CREATE | `infra/modules/network.bicep` | Defines the virtual network, PostgreSQL delegation, private DNS, and private-access resources required by the approved network policy. |
| CREATE | `infra/modules/runtime-services.bicep` | Defines the Container Apps environment, PostgreSQL Flexible Server, Storage account and container, and Service Bus namespace and queue. |
| CREATE | `infra/modules/monitoring.bicep` | Defines Log Analytics and Azure Monitor diagnostic settings for runtime resource health and failure investigation. |
| CREATE | `infra/policies/source-document-lifecycle.json` | Versions lifecycle-management rules for the source-document container so policy can be evaluated before promotion. |
| CREATE | `infra/parameters/production.bicepparam` | Supplies production-safe, non-secret deployment parameters and approved network-policy values. |
| CREATE | `infra/deploy.ps1` | Validates the lifecycle-policy input, executes the deployment, and emits ready or failed-resource status without exposing secrets. |

## External References
- https://learn.microsoft.com/azure/templates/microsoft.app/2024-03-01/managedenvironments
- https://learn.microsoft.com/azure/templates/microsoft.dbforpostgresql/2024-08-01/flexibleservers
- https://learn.microsoft.com/azure/templates/microsoft.storage/2023-05-01/storageaccounts
- https://learn.microsoft.com/azure/templates/microsoft.servicebus/2024-01-01/namespaces
- https://learn.microsoft.com/azure/templates/microsoft.insights/2021-05-01-preview/diagnosticsettings

## Build Commands
- N/A. The repository has no canonical `.propel/build/` command definition; the deployment command will be established with the infrastructure implementation.

## Implementation Validation Strategy
- [ ] Validate the Bicep entry point and production parameter file before deployment.
- [ ] Run an integration deployment in an approved non-production subscription and verify each required Azure resource reaches a successful provisioning state.
- [ ] Verify PostgreSQL rejects public-network access and is reachable only through the approved private-network path.
- [ ] Evaluate the checked-in lifecycle policy against the source-document container before promotion.
- [ ] Induce or inspect a failed deployment result to verify no ready status is emitted and the failed resource is identified.

## Implementation Checklist
- [ ] Create a parameterized Bicep entry point and environment parameters that provision the approved resource group scope and tags. (AC-001)
- [ ] Define private network resources, delegated PostgreSQL subnet, and private DNS integration before dependent runtime resources. (AC-001)
- [ ] Define the Container Apps environment with Log Analytics integration and network settings approved for the deployment boundary. (AC-001)
- [ ] Define PostgreSQL Flexible Server using PostgreSQL 16, private connectivity, backups, and disabled public network access. (AC-001)
- [ ] Define a Blob Storage account and source-document container with secure public-access and transport settings. (AC-001)
- [ ] Check in and attach the source-document lifecycle management policy so promotion validation can evaluate its versioned rules. (AC-002)
- [ ] Define the Service Bus namespace and processing queue with diagnostic settings for operational visibility. (AC-001)
- [ ] Implement deployment-result handling that reports ready only after every resource succeeds and identifies the failed resource on partial failure. (AC-001)