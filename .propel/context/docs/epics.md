---
applyTo: "**/epics.md"
---

# CMS-2567 Compliance Assistant - Epic Decomposition

## Executive Summary

This document decomposes the CMS-2567 Compliance Assistant specification into 9 prioritized, capacity-bounded epics organized by business value and dependency. The epics span infrastructure bootstrap, data persistence, document intake, AI-assisted field extraction, deficiency identification, POC generation with CMS grounding, staff review/approval workflow, knowledge governance, and production reliability.

**Green-field project detected.** EP-TECH provides infrastructure bootstrap; all feature epics depend on foundational layers in priority order.

---

## Epic Planning Inventory

| EP-ID | Epic Title | Requirement Count | Dependencies | Est. Person-Days |
|-------|------------|-------------------|--------------|------------------|
| EP-TECH | Infrastructure & Deployment Bootstrap | 8 | None | 35 |
| EP-DATA | Data Foundation & Persistence | 10 | EP-TECH | 44 |
| EP-INTAKE | Document Upload & Format Recognition | 3 | EP-TECH, EP-DATA | 9 |
| EP-EXTRACT | Extract Fields & Link Evidence | 7 | EP-INTAKE | 32 |
| EP-DEFICIENCY | Identify & Organize Deficiencies | 1 | EP-EXTRACT | 5 |
| EP-POC-GEN | Generate CMS-Grounded POC Drafts | 8 | EP-DEFICIENCY | 57 |
| EP-REVIEW-APPROVAL | Field Verification & POC Approval Workflow | 6 | EP-POC-GEN | 30 |
| EP-KNOWLEDGE-MGMT | CMS Knowledge Maintenance & Governance | 2 | EP-TECH | 5 |
| EP-PERF-OBSERV | Performance, Observability & Reliability | 7 | EP-TECH | 60 |

---

## Epic Descriptions

### EP-TECH: Infrastructure & Deployment Bootstrap

**Business Value**: Foundation enabler for all feature development and production deployment. Establishes the Azure Container Apps environment, deployment pipelines, local development setup, and operational monitoring baseline.

**Description**: Set up the core infrastructure for the CMS-2567 Compliance Assistant. This epic covers containerized Python 3.12 application scaffolding with FastAPI, Azure Container Apps deployment, Azure Service Bus queue setup for async job processing, PostgreSQL Flexible Server provisioning, Azure Blob Storage configuration, and CI/CD pipeline for automated testing and deployment. Includes local development environment setup (Docker Compose or dev container), environment variable management, structured logging, and correlation ID propagation across components.

**UI Impact**: No

**Screen References**: N/A

**Key Deliverables**:
- FastAPI project scaffold with project structure, module boundaries, and adapter layers
- Azure Container Apps environment configuration (API revision, worker revision)
- Azure Service Bus queue and dead-letter queue setup with idempotency configuration
- PostgreSQL Flexible Server provisioning with network access controls
- Azure Blob Storage container provisioning and lifecycle policies
- GitHub Actions CI/CD pipeline for build, test, and deployment
- Local development environment (Docker Compose or devcontainer.json)
- Structured logging setup with correlation IDs across all components
- Application health checks and startup/readiness probes
- Environment configuration management (dev, staging, production)

**Dependent EPICs**: None

**Mapped Requirement IDs**: Infrastructure-derived from NFR-003 (availability infra), NFR-006 (observability infra), DR-008 (migration infrastructure), DR-009 (backup infrastructure)

**UI Impact**: No

---

### EP-DATA: Data Foundation & Persistence

**Business Value**: Establishes the transactional data model and persistence layer required for all compliance workflows. Provides durable storage for processing records, extracted fields, deficiencies, POCs, review history, and approved CMS knowledge sources.

**Description**: Design and implement the PostgreSQL schema for CMS-2567 processing records, source documents, extracted fields, deficiencies, Plans of Correction, content revisions, and CMS knowledge sources. Implement domain entities, repository patterns, database migrations with rollback capability, and backup/recovery procedures (15-minute RPO, 4-hour RTO). Add object storage integration for source-document persistence with content-hash verification. Implement change-data capture or event-sourcing patterns to support review-history traceability and AI-vs-staff attribution. Include schema versioning and forward/backward compatibility migration strategies.

**UI Impact**: No

**Screen References**: N/A

**Key Deliverables**:
- PostgreSQL schema for ProcessingRecord, SourceDocument, ExtractedField, Deficiency, PlanOfCorrection, ContentRevision, CMSKnowledgeSource, and Job entities
- Domain entity models and repository interfaces with repository implementations
- Database migration framework with versioning and rollback procedures
- Idempotent job command handling with duplicate detection
- Change-data capture or revision-history tracking for content attribution
- Blob Storage integration with content-hash and media-type metadata
- Point-in-time restore backup configuration (15-min RPO, 4-hour RTO)
- Schema migration and evolution documentation
- Database connection pooling and transaction management
- Data access layer with dependency injection for repository implementations

**Dependent EPICs**: EP-TECH

**Mapped Requirement IDs**: DR-001, DR-002, DR-003, DR-004, DR-005, DR-006, DR-007, DR-008, DR-009, DR-010

---

### EP-INTAKE: Document Upload & Format Recognition

**Business Value**: Enables compliance staff to initiate processing by uploading survey forms. Detects format and prepares the document for extraction-specific workflows.

**Description**: Implement REST endpoint for document upload. Store the source document in Blob Storage and create a ProcessingRecord in PostgreSQL. Detect the document format (Format 1, Format 2, or open-source format) using format-specific markers, headers, or content parsing. Route unreadable or unsupported documents to an error state without creating an approved record. Implement idempotent upload handling with duplicate detection. Add request validation, authentication/authorization checks, and correlation ID propagation. Provide synchronous upload acknowledgement with processing-record identifier within 2 seconds at 95th percentile under typical load.

**UI Impact**: Yes

**Screen References**: SCR-001 (Document Upload), SCR-002 (Processing Status)

**Key Deliverables**:
- REST endpoint POST /upload for document submission
- Document format detection logic (Format 1, Format 2, open-source format)
- ProcessingRecord creation with format and initial state
- Blob Storage upload and reference tracking
- Error handling for unreadable/unsupported formats
- Idempotent upload with duplicate detection
- Request validation and authentication/authorization
- Synchronous response within 2 seconds (95th percentile)
- Correlation ID assignment and propagation
- API documentation and error codes

**Dependent EPICs**: EP-TECH, EP-DATA

**Mapped Requirement IDs**: FR-001, FR-002, FR-003

---

### EP-EXTRACT: Extract Fields & Link Evidence

**Business Value**: Automatically extracts key survey fields and links them to their source locations, reducing manual data entry and improving traceability.

**Description**: Implement asynchronous extraction job triggered by ProcessingRecord creation. Use deterministic extraction rules for common fields (Provider Name, Provider Number, Survey Date, Tag, SOD) across all formats. Apply format-specific rules for conditional fields (Plan of Correction and Completion Date for Format 2 only; empty for Format 1 and open-source format). Link each extracted value to its source evidence (page, coordinates, or text snippet). Mark low-confidence values and missing evidence for staff review. Implement schema-validated extraction with structured output that distinguishes required, conditional, and optional fields. Use Azure Service Bus for job queueing with exponential retry and dead-letter handling. Publish extraction-complete events for downstream deficiency identification.

**UI Impact**: Yes

**Screen References**: SCR-003 (Field Review), SCR-004 (Evidence Viewer)

**Key Deliverables**:
- Asynchronous extraction job handler (Service Bus consumer)
- Format-specific extraction rules (Format 1, Format 2, open-source)
- Conditional field handling with format-based logic
- Source-evidence linking (page references, text snippets, coordinates)
- Low-confidence flagging and incomplete-content marking
- Schema-validated extraction with structured output
- Service Bus job publishing with correlation IDs
- Extraction state transitions and error handling
- Evidence storage and retrieval (Blob Storage references)
- Deficiency extraction as part of POC context (e.g., SOD text)

**Dependent EPICs**: EP-INTAKE

**Mapped Requirement IDs**: FR-004, FR-005, FR-006, FR-007, FR-008, AIR-001, AIR-003

---

### EP-DEFICIENCY: Identify & Organize Deficiencies

**Business Value**: Structures identified deficiencies (SODs) as distinct planning units for corrective-action drafting, enabling targeted POC generation per deficiency.

**Description**: Implement deficiency segmentation logic that groups extracted SOD text by deficiency boundary. Assign each deficiency a unique identifier and link it to its Tag, source evidence, and processing record. Implement deficiency confirmation/correction workflow where staff can merge, split, or manually create deficiency records. Mark deficiencies with ambiguous boundaries for staff attention. Provide a deficiency inventory view for staff to confirm segmentation before POC generation. Handle edge cases where no deficiency can be identified (mark record as incomplete and block POC generation). Emit deficiency-finalized events to trigger POC generation.

**UI Impact**: Yes

**Screen References**: SCR-005 (Deficiency Review), SCR-006 (Deficiency Segmentation)

**Key Deliverables**:
- Deficiency entity creation and linking to ExtractedField records
- Deficiency segmentation logic with boundary detection
- Staff deficiency confirmation/correction UI
- Merge/split/manual-create deficiency operations
- Deficiency inventory view with source evidence
- Flagging of ambiguous boundaries
- No-deficiency error state handling
- Deficiency-finalized event publishing
- Change tracking for deficiency edits

**Dependent EPICs**: EP-EXTRACT

**Mapped Requirement IDs**: FR-009

---

### EP-POC-GEN: Generate CMS-Grounded POC Drafts

**Business Value**: Automatically generates deficiency-specific Plans of Correction grounded in authoritative CMS regulations and guidance, accelerating POC drafting while ensuring compliance support.

**Description**: Implement POC generation pipeline with CMS knowledge retrieval (Retrieval-Augmented Generation). For each confirmed deficiency, retrieve approved CMS regulations, guidance, and tag definitions from the application's knowledge source store. Call the LLM through the application-owned AI gateway with structured prompt template, CMS context, deficiency details, and schema constraints. Generate one separate POC draft per deficiency with required elements (regulatory citation, root-cause analysis, specific action, timeline, responsible party). Validate each draft against the required-element rubric and compute a quality score. Record the source-set version and effective date used for grounding. Mark drafts with missing elements or insufficient CMS support for staff escalation. Implement versioned evaluation test set to validate extraction, SOD recall, citation accuracy, and POC quality before model/prompt changes are released.

**UI Impact**: Yes

**Screen References**: SCR-007 (POC Review), SCR-008 (CMS Source References)

**Key Deliverables**:
- POC generation service with Service Bus job handler
- CMS knowledge retrieval from approved source store (RAG)
- LLM gateway integration with structured prompt templates
- Schema-validated POC response with required-element distinction
- Quality-score computation against rubric
- Source-set version and effective-date recording
- Missing-element flagging and escalation marking
- Versioned evaluation test set (extraction, recall, citation, quality)
- Model and prompt versioning
- Refusal handling when CMS sources unavailable or evidence missing
- POC-generation event publishing

**Dependent EPICs**: EP-DEFICIENCY

**Mapped Requirement IDs**: FR-010, FR-011, FR-012, FR-013, FR-019, AIR-002, AIR-005, AIR-006

---

### EP-REVIEW-APPROVAL: Field Verification & POC Approval Workflow

**Business Value**: Enforces mandatory staff review and approval for all extracted content and POCs before use or submission, ensuring accountability and compliance.

**Description**: Implement review and approval workflow for extracted fields and generated POCs. Staff open field details with source evidence in a split-view interface and accept or edit each value. For each change, record whether content was AI-generated or staff-edited, reviewer identity, timestamp, and change reason. Staff review POCs alongside deficiency details, SOD text, and supporting CMS references. Mark fields and POCs as approved only after all required elements pass validation and reviewer signs off. Prevent unapproved records from being exported or submitted. Implement bulk approval for batches of related records. Track review history with full change audit for compliance traceability. Emit approval-state-changed events to trigger export/submission readiness.

**UI Impact**: Yes

**Screen References**: SCR-003 (Field Review), SCR-007 (POC Review), SCR-009 (Approval Summary)

**Key Deliverables**:
- Review and approval endpoints (REST)
- Field-level review interface with source-evidence viewer
- AI-vs-staff change attribution and tracking
- Reviewer identity and timestamp recording
- POC review interface with CMS reference display
- Approval state transitions (pending → approved/rejected)
- Bulk approval for related records
- Review history audit log
- Prevention of unapproved export/submission
- Rejection handling with required correction paths
- Approval summary and export-readiness reporting

**Dependent EPICs**: EP-POC-GEN

**Mapped Requirement IDs**: FR-014, FR-015, FR-016, FR-017, FR-024, AIR-004

---

### EP-KNOWLEDGE-MGMT: CMS Knowledge Maintenance & Governance

**Business Value**: Allows compliance governance staff to keep the authoritative CMS source set current and accurate, ensuring POC drafts remain grounded in valid, up-to-date regulatory guidance.

**Description**: Implement administrative interface for compliance governance staff to add, update, retire, or approve CMS source records (regulations, guidance, tag definitions). Each source record includes canonical reference, content hash, effective date or version, approval state, and indexing state. Implement conflict detection when sources overlap or contradict; mark conflicting sources as pending until governance resolves the conflict. Prevent unapproved sources from being used for POC grounding. Record source-maintenance history with decision, approver identity, and timestamp. Implement search and filter on source content and metadata. Add validation to ensure all new sources have effective dates and version identifiers before approval. Existing approved POCs retain the source-set version used at generation time; source updates do not retroactively change POCs.

**UI Impact**: Yes

**Screen References**: SCR-010 (Knowledge Source Management), SCR-011 (Source Conflict Resolution)

**Key Deliverables**:
- Administrative UI for source management (add, update, retire, approve)
- CMSKnowledgeSource entity management
- Source approval workflow with governance controls
- Conflict detection and escalation
- Source search and filter interface
- Effective-date and version validation
- Source-maintenance audit log
- Approval state transitions (pending → approved/retired)
- Version pinning on generated POCs
- Prevention of unapproved sources from grounding
- Bulk source import and versioning

**Dependent EPICs**: EP-TECH

**Mapped Requirement IDs**: FR-018, (DR-006 data layer)

---

### EP-PERF-OBSERV: Performance, Observability & Reliability

**Business Value**: Ensures production-grade performance, monitoring, and reliability required for compliance staff to depend on the system during daily workflows.

**Description**: Implement performance optimizations for upload acknowledgement (2-second 95th percentile response), asynchronous job completion (95% within 10 minutes), and concurrent job handling (20+ concurrent documents). Add comprehensive observability through structured logging, metrics, and distributed tracing with correlation IDs. Implement job-state visibility for operators (state, retry count, failure reason observable within 60 seconds). Add health checks and readiness probes for Container Apps revision deployment. Implement SLA monitoring for 99.9% monthly availability. Add load testing harness to validate concurrent-job capacity. Configure queue retry policies (exponential backoff, bounded attempts) and dead-letter handling. Add circuit-breaker and bulkhead patterns for LLM and storage dependencies. Implement graceful degradation when external dependencies become unavailable.

**UI Impact**: Partial (Operator Dashboard)

**Screen References**: SCR-012 (Operator Dashboard), monitoring/alerting via Azure Monitor/Application Insights

**Key Deliverables**:
- Response-time optimization for upload endpoint (2s @ 95th %ile)
- Async job completion optimization (95% within 10 min)
- Concurrent job capacity testing (20+ documents)
- Structured logging with correlation IDs
- Distributed tracing (OpenTelemetry or Application Insights)
- Metrics collection (request latency, queue depth, job state, errors)
- Health check endpoints and readiness probes
- Operator dashboard for job-state visibility (state, retry, errors)
- SLA monitoring (99.9% availability)
- Load testing harness and capacity reporting
- Queue retry policies and dead-letter handling
- Circuit-breaker and bulkhead implementations
- Graceful degradation and fallback strategies
- Azure Monitor alerting rules and runbooks

**Dependent EPICs**: EP-TECH

**Mapped Requirement IDs**: NFR-001, NFR-002, NFR-003, NFR-005, NFR-006, NFR-007, NFR-009

---

## Dependency Map

```
EP-TECH
  ├── EP-DATA
  ├── EP-INTAKE
  ├── EP-KNOWLEDGE-MGMT
  └── EP-PERF-OBSERV

EP-INTAKE
  └── EP-EXTRACT

EP-EXTRACT
  └── EP-DEFICIENCY

EP-DEFICIENCY
  └── EP-POC-GEN

EP-POC-GEN
  └── EP-REVIEW-APPROVAL
```

**Parallelization Opportunities**:
- EP-DATA, EP-INTAKE, EP-KNOWLEDGE-MGMT, and EP-PERF-OBSERV can begin in parallel once EP-TECH is complete.
- EP-EXTRACT can begin when EP-INTAKE completes.
- EP-DEFICIENCY follows EP-EXTRACT.
- EP-POC-GEN follows EP-DEFICIENCY.
- EP-REVIEW-APPROVAL follows EP-POC-GEN.

---

## Quality Gate Checklist

- [x] Project type detected: Green-field
- [x] EP-TECH tagged [SOURCE:RULE] as foundational infrastructure epic
- [x] Requirement coverage: All 62 requirements (FR, UC, NFR, DR, AIR) mapped to epics or noted as implemented
- [x] Epic effort cap: All epics ≤ 60 person-days
- [x] No orphaned requirements
- [x] No duplicate requirement mappings
- [x] No cross-feature epic dependencies (only foundational and sequential)
- [x] Dependency graph enables parallel development (3+ independent epics can execute simultaneously)
- [x] Decomposition limited to logical workflow sequence (no XL requirements routed to backlog refinement)
- [x] Template compliance: All sections populated with real data
- [x] Migration mode N/A (no migration plan present)

---

## Already Implemented (No Epic)

None. This is a green-field project with no existing codebase.

---

## Backlog Refinement Required

None. All requirements are traceable and sized.

---

## Notes

- **Green-field Infrastructure**: EP-TECH provides the foundational container, queue, database, and storage infrastructure required by all feature epics.
- **AI-Assisted Workflows**: EP-EXTRACT (AIR-001, AIR-003), EP-POC-GEN (AIR-002, AIR-005, AIR-006), and EP-REVIEW-APPROVAL (AIR-004) implement AI integration with deterministic approval gates.
- **Regulatory Compliance Focus**: EP-KNOWLEDGE-MGMT and EP-POC-GEN ensure POC drafts remain grounded in authoritative CMS sources; EP-REVIEW-APPROVAL ensures staff approval before use.
- **Traceability & Audit**: DR-004 (content revision tracking) and FR-017 (review history) provide full audit trail for compliance reporting.
- **Pilot Validation**: UC-009 (pilot measurement) will validate success criteria (50% time reduction, 95% extraction accuracy, 95% SOD recall, POC quality threshold).

