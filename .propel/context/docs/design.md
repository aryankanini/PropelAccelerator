# Architecture Design

## Project Overview
CMS-2567 Compliance Assistant is an Azure-hosted solution for nursing-home compliance staff. A Python 3.12 modular monolith with a FastAPI API accepts three survey-form formats, coordinates open-source document extraction and CMS knowledge retrieval jobs, supports evidence-linked review, drafts deficiency-specific Plans of Correction, and records staff approval.

## Architecture Goals
- Goal 1: Reduce staff processing time while preserving mandatory human verification and approval.
- Goal 2: Keep transactional compliance records, source documents, evidence, and review history traceable and durable.
- Goal 3: Isolate AI uncertainty behind an application-owned gateway with grounded retrieval and structured outputs.
- Goal 4: Provide controlled asynchronous processing with observable retries, dead letters, and recoverable failures.
- Goal 5: Preserve clear module boundaries so the initial release can evolve without premature service distribution.

## Non-Functional Requirements
- NFR-001: [SOURCE:INPUT] System MUST return a synchronous upload acknowledgement and processing-record identifier within 2 seconds at the 95th percentile under 100 concurrent user sessions.
  Basis: The selected REST-plus-queue model requires responsive user actions; the numeric target is an architecture baseline to validate during pilot.
- NFR-002: [SOURCE:INPUT] System MUST complete 95% of standard CMS-2567 processing jobs within 10 minutes of queue acceptance, excluding time waiting for staff review.
  Basis: Background processing must provide a bounded operational experience while OCR and AI work run asynchronously.
- NFR-003: [SOURCE:INPUT] System MUST provide 99.9% monthly availability for interactive API and review operations, excluding scheduled maintenance announced at least 24 hours in advance.
  Basis: Compliance staff need dependable access to review work; the availability target is an initial production baseline.
- NFR-005: [SOURCE:INPUT] System MUST prevent an unverified field or unapproved POC from being represented as ready for use or submission.
  Basis: The upstream specification makes staff verification and approval mandatory before use or submission.
- NFR-006: [SOURCE:INPUT] System MUST make job state, retry count, and failure reason observable to authorized operators within 60 seconds of a state change.
  Basis: Durable asynchronous work requires operational visibility; the time target is an initial baseline.
- NFR-007: [SOURCE:INPUT] System MUST support at least 20 concurrent document-processing jobs without exceeding the processing completion target in NFR-002 for standard documents.
  Basis: Queue-based load leveling is selected for variable OCR and AI demand; capacity must be validated with representative samples.
- NFR-009: [SOURCE:INPUT] System MUST expose correlation identifiers across API requests, queue messages, database writes, storage objects, AI calls, and review decisions.
  Basis: Cross-component traceability is required to investigate compliance records and asynchronous failures.

## Data Requirements
- DR-001: [SOURCE:INPUT] System MUST persist a CMS-2567 processing record containing provider identity, provider number, survey date, detected format, and processing state.
  Basis: These fields and workflow states are defined in the upstream functional specification.
- DR-002: [SOURCE:INPUT] System MUST persist each deficiency as a distinct record linked to its SOD text, Tag, source evidence, and processing record.
  Basis: The upstream specification requires separate deficiency handling and source-linked evidence.
- DR-003: [SOURCE:INPUT] System MUST persist each POC as a distinct record linked to exactly one deficiency, its CMS source references, validation result, source-set version, approval state, and change history.
  Basis: The upstream specification requires one POC per deficiency, CMS grounding, validation, and traceability.
- DR-004: [SOURCE:INPUT] System MUST retain AI-generated and staff-edited content as attributable revisions without overwriting review history.
  Basis: AI-versus-staff change tracking and documented approval require retained review history.
- DR-005: [SOURCE:INPUT] System MUST store uploaded survey forms and source-evidence snapshots in object storage, with database references containing object identity, content hash, and media type.
  Basis: PostgreSQL plus object storage is the confirmed persistence choice for transactional records and source documents.
- DR-006: [SOURCE:INPUT] System MUST retain each approved CMS knowledge source obtained from open-source CMS data with its canonical reference, content hash, effective date or version, approval state, and indexing state.
  Basis: Authoritative CMS knowledge maintenance, open-source data provenance, and source-version traceability are explicit requirements.
- DR-007: [SOURCE:INPUT] System MUST record the approved open-source extraction library name and version used to process each uploaded survey form.
  Basis: Open-source extraction is the selected input-processing approach, and per-record library provenance supports reproducible extraction evaluation.
- DR-008: [SOURCE:INPUT] System MUST support backward-compatible schema migrations with an explicit migration version and rollback or restore procedure.
  Basis: Transactional approval data requires controlled evolution without loss of traceability.
- DR-009: [SOURCE:INPUT] System MUST provide point-in-time database restore with a recovery point objective of 15 minutes and recovery time objective of 4 hours for production data.
  Basis: Managed PostgreSQL backups support restore operations; the targets are initial recovery baselines requiring operational validation.
- DR-010: [SOURCE:INPUT] System MUST make queue messages and processing commands idempotent using a stable processing-record and job-attempt identity.
  Basis: At-least-once queue delivery and retry handling can otherwise duplicate extraction, POC generation, or review records.

### Domain Entities
- ProcessingRecord: One uploaded CMS-2567 workflow; contains provider, survey metadata, detected format, state, and source-document references.
- SourceDocument: Immutable uploaded document metadata and object-storage location, including content hash and media type.
- ExtractedField: A field value, field type, confidence/status, source-evidence location, and current review state.
- Deficiency: One identified SOD, Tag, evidence set, segmentation status, and link to its POC.
- PlanOfCorrection: One deficiency-specific draft or approved POC, validation result, CMS references, source-set version, and approval state.
- ContentRevision: Versioned AI-generated or staff-edited field/POC content with author type, actor, timestamp, and change reason.
- CMSKnowledgeSource: Approved or pending regulation, guidance, or tag definition with version metadata and approval state.
- Job: Idempotent asynchronous command with type, processing-record identity, attempt count, state, error, and correlation identifier.

## AI Consideration

**Status:** Applicable

**Rationale:** Upstream requirements contain `[HYBRID]` classifications for OCR extraction, deficiency identification, CMS-grounded POC drafting, and human-reviewed output. The design therefore combines deterministic workflow gates with AI-assisted extraction and generation.

## AI Requirements
- AIR-001: [HYBRID] [SOURCE:INPUT] System MUST produce extraction and POC results in schema-validated structures that distinguish required fields, nullable conditional fields, confidence/status, evidence references, and refusal or failure states.
  Basis: The functional specification requires conditional fields, source-linked evidence, confidence flags, and separate POC records; application-owned schema validation constrains the selected LLM response.
- AIR-002: [HYBRID] [SOURCE:INPUT] System MUST retrieve approved CMS regulations, guidance, and tag definitions before generating a POC and MUST attach the retrieved source references to the draft.
  Basis: CMS knowledge retrieval and source-linked POC grounding are explicit requirements.
- AIR-003: [HYBRID] [SOURCE:INPUT] System MUST abstain from presenting an AI result as complete when source evidence is missing, confidence is below the approved threshold, or required POC elements are absent.
  Basis: The upstream specification requires low-confidence/incomplete flags and staff approval gates.
- AIR-004: [HYBRID] [SOURCE:INPUT] System MUST keep AI-generated content, prompts or prompt templates, retrieved source identifiers, model deployment identifier, and structured result associated with the processing job for staff review.
  Basis: AI-versus-staff change tracking and source-set versioning require traceable generated results.
- AIR-005: [HYBRID] [SOURCE:INPUT] System MUST evaluate extraction, SOD recall, citation support, POC quality, refusal behavior, and format-specific conditional-field handling against a versioned test set before model or prompt changes are released.
  Basis: The upstream success criteria require field accuracy, SOD recall, POC quality, and format-specific behavior; versioned evaluation prevents regressions.
- AIR-006: [DETERMINISTIC] [SOURCE:INPUT] System MUST prevent AI output from changing approval state without deterministic application rules and staff action.
  Basis: AI assists with drafts, while approval remains a staff workflow decision.

### AI Architecture Pattern
**Selected Pattern:** Grounded LLM with deterministic source context and review gates

**Rationale:**
- AIR-002 and AIR-004 require authoritative source context, citations, and source/version traceability; the application will use approved source records and deterministic lookup. No managed AI or search service is used for retrieval.
- AIR-001 and AIR-003 require strict response structures and explicit failure handling; application-owned schema validation constrains the selected LLM response.
- AIR-006 requires the application-owned gateway to keep model output advisory and make approval, validation, and state transitions deterministic.

## Architecture and Design Decisions
- Architecture style: Modular monolith with hexagonal boundaries inside one deployable application. Context: the initial release has one cohesive workflow and a small team, but domain volatility and traceability needs require separable modules. Decision: use Intake, Extraction, Deficiency, POC, Review, and Knowledge modules with public application ports. Benefit: low operational complexity now and a clear path to service extraction later. Trade-off: modules share a deployment lifecycle and require boundary tests.
- Pattern rationale: The modular monolith satisfies NFR-003, NFR-006, and DR-008 with fewer distributed failure modes than microservices. The application core remains framework-independent where practical, while adapters own FastAPI, PostgreSQL, Blob Storage, Service Bus, open-source extraction libraries, and the LLM integration. One authoritative writer owns each transactional dataset.
- API boundary: FastAPI exposes synchronous REST endpoints for upload acknowledgement, record status, evidence review, field edits, POC review, approval, knowledge maintenance, and review-history queries. API handlers validate input and delegate to module application services; they do not call storage or AI adapters directly.
- Asynchronous flow: REST stores the source-document reference and processing record, then publishes an idempotent job to Azure Service Bus. Workers execute open-source document extraction, field extraction, deficiency segmentation, CMS source lookup, POC drafting, and validation. The queue uses at-least-once delivery, exponential retry with bounded attempts, duplicate detection where supported, and a dead-letter queue for operator review.
- AI gateway: A single application-owned gateway enforces prompt templates, model selection, structured schemas, source-context requirements, token/time budgets, and refusal handling. Domain modules consume typed gateway ports and never call the LLM directly.
- Retrieval flow: CMS governance content is approved and stored with metadata in the application data stores. The gateway selects approved source records through deterministic lookup and includes their identifiers and versions in the LLM context. The POC draft stores those references. Source records are evidence, not approval.
- Data flow: Uploaded documents are stored in Blob Storage. PostgreSQL stores workflow state, normalized fields, deficiencies, POCs, revisions, approvals, and knowledge metadata. Large binary content does not enter transactional tables. The system writes a processing state transition before publishing the next job and uses job identity to make retries idempotent.
- Consistency: PostgreSQL is the authoritative writer for workflow, knowledge, and approval state. Blob Storage is authoritative for source-document bytes. Approval state changes use a database transaction that records the review decision and revision history.
- Failure modes: unreadable documents enter a non-approved error state; missing evidence blocks approval; unavailable CMS knowledge blocks grounded POC approval; transient Azure failures retry; exhausted jobs dead-letter; stale CMS source records surface maintenance status.
- Evolution: Keep module contracts and message schemas versioned additively. Extract a worker or service only when load, team ownership, or deployment independence justifies the operational cost. Preserve PostgreSQL ownership boundaries and migrate through expand-migrate-contract steps.

## Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React with TypeScript | React 19.x / TypeScript 5.x | Separate review UI supports NFR-001, NFR-005, and NFR-009. |
| Mobile | N/A | N/A | The approved scope is a desktop-oriented compliance workflow; no mobile requirement is stated. |
| Backend | Python with FastAPI and Pydantic | Python 3.12 / FastAPI 0.141.1 / Pydantic 2.x | Confirmed architecture choice; typed REST contracts support NFR-001 and TR-002. |
| Document extraction | Tesseract OCR and PyMuPDF | Tesseract 5.x / PyMuPDF 1.x | Open-source extraction supports the three input formats without adding an AI/ML cloud service; evaluated by AIR-005. |
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | Confirmed persistence choice; supports DR-001, DR-003, DR-008, and DR-009. |
| AI/ML | Application-owned gateway and one approved LLM model | LLM model/version TBD | The approved LLM is the sole AI service. Extraction uses open-source libraries and CMS grounding uses application-owned source records. |
| Testing | pytest, pytest-asyncio, HTTPX, contract and evaluation test suites | pytest 8.x / HTTPX 0.28.x | Tests typed API, async jobs, approval gates, and AI evaluation metrics for NFR-005 and AIR-005. |
| Infrastructure | Azure Container Apps, Azure Service Bus, Azure Blob Storage | Current GA service APIs | Managed Azure services support NFR-002, NFR-006, DR-005, and DR-010. |
| Deployment | Azure Container Apps with separate API and worker revisions | Current GA service APIs | Independent worker scaling supports NFR-002 and NFR-007 without splitting the domain monolith. |
| Monitoring | Azure Monitor, Application Insights, Log Analytics, OpenTelemetry | Current GA service APIs / OpenTelemetry 1.x | Correlation and operational visibility support NFR-006 and NFR-009. |
| Documentation | Markdown architecture source plus OpenAPI generated from FastAPI contracts | OpenAPI 3.1 | Shared contracts and traceability support NFR-009 and downstream implementation work. |

## AI Component Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Model Provider | One approved LLM model selected through the gateway | Structured field extraction and deficiency-specific POC drafting. |
| Source Context | PostgreSQL-approved CMS source records | Deterministic lookup of authoritative regulations, guidance, and tag definitions without a cloud search service. |
| AI Gateway | Application-owned FastAPI module with typed ports and policy enforcement | Centralize prompt, model, source-context, schema, timeout, and retry controls. |
| Guardrails | Pydantic/JSON Schema validation, deterministic field rules, source citation checks, approval state machine | Prevent malformed, ungrounded, incomplete, or unapproved AI output from becoming usable. |

## Alternative Technology Options
- Microservices were not selected for the initial release because independent deployment would add distributed tracing, data ownership, and operational overhead before scale or team autonomy requires it.
- Django REST Framework was not selected because FastAPI better matches the confirmed Python document-processing and typed asynchronous API direction; an integrated administration surface is not an initial business requirement.
- Azure Cosmos DB was not selected because PostgreSQL better expresses approval state, revisions, and relational ownership constraints.
- Fully synchronous processing was not selected because OCR and AI latency would hold user requests open and weaken NFR-001.
- Managed cloud AI/search services are not used for the initial release. The approved LLM is the sole AI service, while open-source libraries perform document extraction and application-owned PostgreSQL records supply source context.
- [CONDITIONAL: $AI_SIGNAL=true] A provider-neutral multi-model platform was not selected as the primary strategy because it would add portability complexity before a second model is required; the application-owned gateway still keeps the domain independent of direct model calls.

## Technology Decision
| Metric (from NFR/DR/AIR) | Candidate 1 | Candidate 2 | Rationale |
|--------------------------|-------------|-------------|-----------|
| NFR-001 typed API delivery | FastAPI/Python 3.12: High | Django/DRF/Python 3.12: Medium | FastAPI’s typed contracts and async support fit the responsive API boundary. |
| NFR-003 managed availability | Azure Container Apps: High | Azure App Service: High | Container Apps provides a natural API/worker deployment shape while retaining managed operations. |
| DR-001/DR-003 transactional integrity | Azure PostgreSQL: High | Azure Cosmos DB: Medium | Relational transactions fit workflow and approval ownership. |
| DR-005 source-document storage | Azure Blob Storage: High | PostgreSQL large objects: Low | Blob Storage is designed for large unstructured documents and distributed access. |
| AIR-002 approved CMS context | PostgreSQL source lookup: High | Managed search service: Low | Application-owned source records satisfy citation and version traceability without an additional managed service. |

### AI Technology Decision: Model Provider
| Metric (from AIR/NFR) | Approved LLM model | Self-hosted extraction-only stack | Rationale |
|-----------------------|--------------|-------------------------------|-----------|
| AIR-001 structured outputs | High | Low | The selected LLM is constrained by application-owned JSON Schema validation; extraction libraries do not generate POCs. |
| NFR-004 data boundary | High | High | The gateway applies approved data-boundary controls to the selected LLM integration. |
| AIR-005 evaluation operations | High | High | Versioned application evaluation covers the LLM and open-source extraction libraries independently. |

### AI Technology Decision: Source Context
| Metric (from AIR/DR) | PostgreSQL-approved source records | Cloud search service | Rationale |
|----------------------|-----------------|-----------------------------|-----------|
| AIR-002 approved CMS context | High | Medium | Application-owned lookup preserves source identity, effective date, and approval metadata. |
| DR-006 source metadata | High | Medium | PostgreSQL remains the authoritative store for source identity, effective date, and approval metadata. |
| NFR-006 operations | High | Medium | Removing a separate search service reduces operational dependencies. |

### AI Technology Decision: AI Gateway
| Metric (from AIR/NFR) | Application-owned gateway | Direct provider calls from modules | Rationale |
|-----------------------|--------------------------|----------------------------------|-----------|
| AIR-004 traceability | High | Low | One gateway can consistently record model, prompt, source, schema, and job identifiers. |
| AIR-006 deterministic controls | High | Low | Central policy enforcement keeps LLM output advisory and approval state deterministic. |
| NFR-009 correlation | High | Medium | The gateway carries correlation context across retrieval and inference calls. |

### AI Technology Decision: Guardrails
| Metric (from AIR/NFR) | Schema plus deterministic gates | Prompt-only instructions | Rationale |
|-----------------------|-------------------------------|---------------------------|-----------|
| AIR-001 output shape | High | Low | Pydantic/JSON Schema validation rejects malformed responses. |
| AIR-003 abstention | High | Low | Evidence, confidence, and required-element checks can block incomplete output. |
| NFR-005 approval safety | High | Low | The state machine prevents unapproved content from becoming usable. |

## Technical Requirements
- TR-001: [SOURCE:INPUT] System MUST implement the initial solution as a modular monolith with separate Intake, Extraction, Deficiency, POC, Review, Knowledge, and Governance module boundaries.
  Basis: The architecture style was explicitly selected for the initial release and is justified by NFR-003, NFR-006, and DR-008.
- TR-002: [SOURCE:INPUT] System MUST implement the application boundary in Python 3.12 using FastAPI and typed request/response models.
  Basis: Python 3.12 and FastAPI were explicitly selected; the choice supports NFR-001 and NFR-009.
- TR-003: [SOURCE:INPUT] System MUST use synchronous REST endpoints for user actions and Azure Service Bus for durable asynchronous OCR, retrieval, POC-generation, and validation jobs.
  Basis: The integration style was explicitly selected and supports NFR-001, NFR-002, NFR-006, and DR-010.
- TR-004: [SOURCE:INPUT] System MUST use Azure Database for PostgreSQL as the authoritative transactional store and Azure Blob Storage for uploaded source documents and evidence snapshots.
  Basis: PostgreSQL plus object storage was explicitly selected and supports DR-001, DR-003, and DR-005.
- TR-005: [SOURCE:INPUT] System MUST route the approved LLM model and CMS source-context operations through an application-owned AI gateway.
  Basis: The AI integration is limited to one LLM model, while source grounding remains application-owned; this supports AIR-001, AIR-002, AIR-004, and AIR-006.
- TR-006: [SOURCE:INPUT] System MUST use strict application-owned structured-output schemas with all required properties and reject additional properties for LLM extraction and POC response contracts.
  Basis: Structured outputs are required by AIR-001 and deterministic validation must remain under application control.
- TR-007: [SOURCE:INPUT] System MUST use approved PostgreSQL CMS source records and deterministic lookup to provide grounded context and citations for POC generation.
  Basis: AIR-002 and DR-006 require authoritative source identity, effective version, approval state, and citation traceability without a cloud search service.
- TR-008: [SOURCE:INPUT] System MUST use an approved open-source document-extraction library for OCR and form-content extraction, with library version recorded for each processing job.
  Basis: The updated architecture requires open-source extraction and versioned evaluation of extraction behavior.
- TR-009: [SOURCE:INPUT] System MUST implement at-least-once job handling with stable idempotency keys, exponential backoff, bounded retries, dead-letter routing, and operator replay controls.
  Basis: Service Bus provides durable queues, dead-lettering, and duplicate-detection capabilities; these controls implement NFR-006 and DR-010 and make asynchronous work recoverable.
- TR-011: [SOURCE:INPUT] System MUST emit OpenTelemetry-compatible traces and structured logs containing processing-record, job, source-document, and correlation identifiers.
  Basis: NFR-006 and NFR-009 require diagnosable processing and review workflows.
- TR-012: [SOURCE:INPUT] System MUST deploy the API and worker processes as separately scalable revisions of the modular monolith.
  Basis: The selected modular monolith and queue-based integration require worker scaling without introducing independent domain services; this supports NFR-002 and NFR-007.
- TR-013: [SOURCE:INPUT] System MUST execute database schema changes through reviewed expand-migrate-contract migrations and verify restore procedures before production release.
  Basis: DR-008 and DR-009 require backward-compatible evolution and recoverability.

## Technical Constraints & Assumptions
- Azure is the confirmed deployment target; final region selection depends on facility data residency, service availability, and organizational policy.
- The initial release is a modular monolith, not a distributed set of domain services; API and worker processes may scale independently while sharing the application codebase.
- Python 3.12, FastAPI, PostgreSQL, Azure Blob Storage, Azure Service Bus, one approved LLM model, and an approved open-source extraction library are the confirmed technology direction.
- No existing codebase was available for compatibility analysis; architecture choices are therefore constraint-driven rather than carried forward from incumbent implementation patterns.
- Specific production throughput, availability, recovery, and latency thresholds are initial architecture baselines and require confirmation through representative pilot measurements.
- The selected LLM model, quota, and supported structured-output limits must be validated during environment setup; model output never bypasses deterministic validation or human approval.
- CMS source ingestion requires a compliance governance owner, source approval process, effective-date/version policy, and reindexing process.
- The design uses at-least-once asynchronous processing; idempotency and dead-letter replay are mandatory, while exactly-once end-to-end processing is not assumed.
- The separate frontend is included in the technology direction, but visual design, accessibility details, and frontend component architecture require a downstream UX/design workflow.
