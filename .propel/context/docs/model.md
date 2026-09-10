# Design Modelling

## UML Models Overview
This model documents the CMS-2567 Compliance Assistant from system boundary through deployment, data movement, persistence, grounded LLM context, and user workflow timing. The architectural views derive from the approved architecture design; the sequence views correspond to UC-001 through UC-007 and UC-009 in [spec.md](./spec.md). Use the architectural views first for structure, then the UC sequence diagrams for behavior and the AI sequence diagrams for model and source-context controls.

---

## Architectural Views

### Component Architecture Diagram
<!-- RENDER type="mermaid" src="./uml-models/component-architecture.png" -->

![Component Architecture Diagram](./uml-models/component-architecture.png)

```mermaid
flowchart LR
    UI[Review Frontend\nReact + TypeScript]
    API[API Boundary\nFastAPI REST]
    subgraph APP[CMS-2567 Modular Monolith]
        Intake[Intake and Format Recognition]
        Extract[Extraction and Evidence]
        Defect[Deficiency Management]
        Poc[POC Preparation]
        Review[Review and Approval]
        Knowledge[CMS Knowledge Governance]
        Gateway[Application-Owned AI Gateway]
    end
    Queue[(Azure Service Bus\nDurable Queue)]
    DB[(Azure PostgreSQL\nTransactional Store)]
    Blob[(Azure Blob Storage\nSource Documents)]
    Source[(Approved CMS\nSource Records)]
    LLM[Approved LLM Model]
    UI --> API
    API --> Intake
    API --> Review
    API --> Knowledge
    Intake --> Queue
    Queue --> Extract
    Queue --> Poc
    Extract --> Defect
    Defect --> Poc
    Poc --> Review
    Knowledge --> Source
    Gateway --> Source
    Gateway --> LLM
    Intake --> Blob
    Extract --> DB
    Defect --> DB
    Poc --> DB
    Review --> DB
    Knowledge --> DB
```

---

### Deployment Architecture Diagram
<!-- RENDER type="plantuml" src="./uml-models/deployment-architecture.png" -->

![Deployment Architecture Diagram](./uml-models/deployment-architecture.png)

```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle
actor "Compliance Staff" as User
cloud "Azure Subscription" as Azure {
  node "Virtual Network" as VNet {
    node "Container Apps Environment" as CAE {
      component "API Revision\nFastAPI" as API
      component "Worker Revision\nPython 3.12" as Worker
    }
        database "PostgreSQL Flexible Server" as DB
        storage "Blob Storage" as Blob
    queue "Service Bus\nQueue + DLQ" as Bus
    component "AI Gateway" as Gateway
  }
    component "Approved LLM\nModel Endpoint" as LLM
  component "Monitor + App Insights" as Monitor
}
User --> API : HTTPS / REST
API --> Worker : queue job
API --> DB : TLS
API --> Blob : HTTPS
API --> Bus : AMQP
Worker --> Bus : receive / settle
Worker --> DB : TLS
Worker --> Blob : HTTPS
Worker --> Gateway : typed port
Gateway --> LLM : structured inference
API --> Monitor : traces/logs
Worker --> Monitor : traces/logs
@enduml
```

#### Enhanced Deployment Details [CONDITIONAL: infrastructure specification available]
No infrastructure specification artifact is available. Deployment sizing, network address ranges, and service SKUs remain architecture assumptions to confirm during infrastructure planning.

| Component | Specification | Source |
|-----------|---------------|--------|
| Compute | Azure Container Apps with separately scalable API and worker revisions | NFR-002, NFR-007, TR-011 |
| Data | Azure PostgreSQL Flexible Server with point-in-time restore; Blob Storage for source files | DR-005, DR-009, TR-004 |
| Monitoring | Azure Monitor, Application Insights, Log Analytics, OpenTelemetry | NFR-006, NFR-009, TR-011 |

---

### Data Flow Diagram
<!-- RENDER type="plantuml" src="./uml-models/data-flow.png" -->

![Data Flow Diagram](./uml-models/data-flow.png)

```plantuml
@startuml
left to right direction
actor "Compliance Staff" as Staff
rectangle "Review Frontend" as UI
rectangle "FastAPI API" as API
queue "Service Bus Queue" as Queue
rectangle "Open-Source OCR and Extraction Worker" as OCR
rectangle "Deficiency Worker" as Defect
rectangle "POC and Validation Worker" as POC
rectangle "AI Gateway" as Gateway
cloud "Approved LLM Model" as Model
database "Approved CMS Source Records" as Source
storage "Blob Storage" as Blob
database "PostgreSQL" as DB
Staff --> UI : upload / review / approve
UI --> API : REST request
API --> Blob : source document
API --> DB : processing record
API ..> Queue : processing command
Queue ..> OCR : at-least-once job
OCR --> Blob : read document
OCR --> DB : fields + evidence
OCR ..> Defect : deficiency command
Defect --> DB : deficiency records
Defect ..> POC : POC command
POC --> Gateway : typed AI request
Gateway --> Source : deterministic lookup
Gateway --> Model : structured generation
Model --> Gateway : schema result
Gateway --> POC : result + citations
POC --> DB : POC + validation
DB --> API : review state
API --> UI : evidence + status
@enduml
```

---

### Logical Data Model (ERD)
<!-- RENDER type="mermaid" src="./uml-models/logical-data-model.png" -->

![Logical Data Model](./uml-models/logical-data-model.png)

```mermaid
erDiagram
    PROCESSING_RECORD ||--|| SOURCE_DOCUMENT : has
    PROCESSING_RECORD ||--o{ EXTRACTED_FIELD : contains
    PROCESSING_RECORD ||--o{ DEFICIENCY : identifies
    DEFICIENCY ||--|| PLAN_OF_CORRECTION : receives
    PLAN_OF_CORRECTION ||--o{ CONTENT_REVISION : has
    EXTRACTED_FIELD ||--o{ CONTENT_REVISION : has
    PLAN_OF_CORRECTION ||--o{ KNOWLEDGE_CITATION : uses
    CMS_KNOWLEDGE_SOURCE ||--o{ KNOWLEDGE_CITATION : supports
    PROCESSING_RECORD ||--o{ JOB : schedules
    PROCESSING_RECORD {
        uuid processing_record_id PK
        string detected_format
        string workflow_state
        date survey_date
    }
    SOURCE_DOCUMENT {
        uuid source_document_id PK
        uuid processing_record_id FK
        string blob_uri
        string content_hash
    }
    EXTRACTED_FIELD {
        uuid field_id PK
        uuid processing_record_id FK
        string field_type
        string value
        string confidence_state
        string evidence_locator
        string approval_state
    }
    DEFICIENCY {
        uuid deficiency_id PK
        uuid processing_record_id FK
        string tag
        string sod_text
        string segmentation_state
    }
    PLAN_OF_CORRECTION {
        uuid poc_id PK
        uuid deficiency_id FK
        string approval_state
        string validation_state
        string source_set_version
    }
    CONTENT_REVISION {
        uuid revision_id PK
        string author_type
        uuid actor_id
        datetime created_at
        string content_hash
    }
    CMS_KNOWLEDGE_SOURCE {
        uuid source_id PK
        string canonical_reference
        string effective_version
        string approval_state
        string index_state
    }
    KNOWLEDGE_CITATION {
        uuid citation_id PK
        uuid poc_id FK
        uuid source_id FK
        string locator
    }
    JOB {
        uuid job_id PK
        uuid processing_record_id FK
        string job_type
        int attempt_count
        string state
    }
```

---

### AI Architecture Diagrams [CONDITIONAL: $AI_SIGNAL = true]

#### Grounded LLM Context Pipeline Diagram [CONDITIONAL: grounded LLM pattern identified]
<!-- RENDER type="plantuml" src="./uml-models/rag-pipeline.png" -->

![RAG Pipeline Diagram](./uml-models/rag-pipeline.png)

```plantuml
@startuml
left to right direction
actor "Compliance Governance Staff" as Gov
storage "Approved CMS Source\nBlob/Object Store" as SourceFiles
component "Knowledge Ingestion\nNormalize + Validate" as Ingest
database "Approved CMS Source Records" as Source
actor "Compliance Staff" as Staff
component "Application-Owned\nAI Gateway" as Gateway
component "Retrieval Policy\nVersion Filters" as Policy
cloud "Approved LLM Model" as Model
component "Schema + Citation\nGuardrails" as Guard
Gov --> SourceFiles : approve source
SourceFiles --> Ingest : ingest approved content
Ingest --> Source : save metadata and version
Staff --> Gateway : request POC draft
Gateway --> Policy : apply filters
Policy --> Source : deterministic lookup
Source --> Policy : approved source records
Policy --> Gateway : sources + versions
Gateway --> Model : grounded structured prompt
Model --> Gateway : structured draft
Gateway --> Guard : validate schema + citations
Guard --> Gateway : draft or abstain
Gateway --> Staff : draft + citations + flags
@enduml
```

#### AI Sequence Diagram — UC-002 [CONDITIONAL: $AI_SIGNAL = true, repeat per AI-enabled UC]
<!-- RENDER type="mermaid" src="./uml-models/ai-seq-uc-002.png" -->

![AI Sequence Diagram](./uml-models/ai-seq-uc-002.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Worker as Extraction Worker
    participant Gateway as AI Gateway
    participant Model as Approved LLM Model
    participant DB as PostgreSQL
    Staff->>API: Start extraction review
    API->>Worker: Queue extraction job
    Worker->>Gateway: Submit form content and format
    Gateway->>Model: Request structured field extraction
    Model-->>Gateway: Schema-constrained fields
    Gateway->>Gateway: Validate schema and confidence
    Gateway-->>Worker: Fields, flags, evidence candidates
    Worker->>DB: Persist draft and review state
    DB-->>API: Draft status
    API-->>Staff: Fields and confidence flags
    alt Missing or ambiguous evidence
        Gateway-->>Worker: Abstain or flag field
        Worker-->>API: Manual review required
    end
```

#### AI Sequence Diagram — UC-003 [CONDITIONAL: $AI_SIGNAL = true, repeat per AI-enabled UC]
<!-- RENDER type="mermaid" src="./uml-models/ai-seq-uc-003.png" -->

![AI Sequence Diagram](./uml-models/ai-seq-uc-003.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Worker as Deficiency Worker
    participant Gateway as AI Gateway
    participant Model as Approved LLM Model
    participant DB as PostgreSQL
    Staff->>API: Request deficiency identification
    API->>Worker: Queue deficiency job
    Worker->>Gateway: Submit SOD text and evidence
    Gateway->>Model: Identify deficiency boundaries
    Model-->>Gateway: Structured deficiency candidates
    Gateway->>Gateway: Validate evidence references
    Gateway-->>Worker: Candidates and confidence flags
    Worker->>DB: Persist distinct deficiency records
    DB-->>API: Deficiency review state
    API-->>Staff: Candidates with source evidence
    alt Ambiguous boundaries
        Gateway-->>Worker: Low-confidence segmentation
        Worker-->>API: Request staff correction
    end
```

#### AI Sequence Diagram — UC-004 [CONDITIONAL: $AI_SIGNAL = true, repeat per AI-enabled UC]
<!-- RENDER type="mermaid" src="./uml-models/ai-seq-uc-004.png" -->

![AI Sequence Diagram](./uml-models/ai-seq-uc-004.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Worker as POC Worker
    participant Source as Approved CMS Sources
    participant Gateway as AI Gateway
    participant Model as Approved LLM Model
    participant DB as PostgreSQL
    Staff->>API: Request POC drafts
    API->>Worker: Queue POC job
    Worker->>Gateway: Submit deficiency and tag
    Gateway->>Source: Deterministic lookup with source filters
    Source-->>Gateway: Approved CMS sources
    Gateway->>Model: Grounded structured POC request
    Model-->>Gateway: POC draft and citations
    Gateway->>Gateway: Validate schema and citation support
    Gateway-->>Worker: Draft, sources, quality flags
    Worker->>DB: Persist POC and source-set version
    DB-->>API: POC review state
    API-->>Staff: POC draft and citations
    alt No authoritative source
        Source-->>Gateway: No approved source
        Gateway-->>Worker: Ungrounded draft blocked
        Worker-->>API: Manual compliance review required
    end
```

#### AI Sequence Diagram — UC-006 [CONDITIONAL: $AI_SIGNAL = true, repeat per AI-enabled UC]
<!-- RENDER type="mermaid" src="./uml-models/ai-seq-uc-006.png" -->

![AI Sequence Diagram](./uml-models/ai-seq-uc-006.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Review as Review Module
    participant Gateway as AI Gateway
    participant DB as PostgreSQL
    Staff->>API: Open POC review
    API->>Review: Load POC, evidence, citations
    Review->>DB: Read draft and revisions
    DB-->>Review: AI and staff content history
    Review->>Gateway: Validate current draft if edited
    Gateway-->>Review: Schema, citation, and confidence results
    Review-->>API: Review model with differences
    API-->>Staff: Show AI text and staff edits
    Staff->>API: Approve or reject POC
    API->>Review: Apply deterministic approval rule
    Review->>DB: Transactionally persist decision and review history
    DB-->>API: Approval state
    API-->>Staff: Approved or blocked result
    alt Required element missing
        Review-->>API: Block approval and list missing elements
        API-->>Staff: Correction required
    end
```

---

## Use Case Sequence Diagrams

### UC-001: Upload and Classify CMS Survey Form
**Source:** [spec.md#uc-001-upload-and-classify-cms-survey-form-sourceinput](./spec.md#uc-001-upload-and-classify-cms-survey-form-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-001.png" -->

![UC-001 Sequence Diagram](./uml-models/seq-uc-001.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant UI as Review Frontend
    participant API as FastAPI API
    participant Intake as Intake Module
    participant Blob as Blob Storage
    participant DB as PostgreSQL
    Staff->>UI: Select CMS Survey Form
    UI->>API: POST upload
    API->>Intake: Validate upload request
    Intake->>Blob: Store source document
    Intake->>DB: Create processing record
    Intake-->>API: Format and record identifier
    API-->>UI: Upload acknowledgement
    UI-->>Staff: Show processing status
    alt Unsupported or unreadable document
        Intake-->>API: Error state
        API-->>UI: No approved record created
    end
```

### UC-002: Extract Survey Fields and Link Evidence
**Source:** [spec.md#uc-002-extract-survey-fields-and-link-evidence-sourceinput](./spec.md#uc-002-extract-survey-fields-and-link-evidence-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-002.png" -->

![UC-002 Sequence Diagram](./uml-models/seq-uc-002.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Queue as Service Bus
    participant Worker as Extraction Worker
    participant Blob as Blob Storage
    participant DB as PostgreSQL
    Staff->>API: Request extraction status
    API->>Queue: Enqueue extraction job
    Queue-->>Worker: Deliver job
    Worker->>Blob: Read source document
    Worker->>Worker: Apply format-specific extraction
    Worker->>DB: Save fields, SOD, evidence, flags
    DB-->>API: Draft review state
    API-->>Staff: Show fields and evidence
    alt Format 1 or open-source format
        Worker->>DB: Save blank POC and Completion Date
    end
    opt Missing evidence or ambiguity
        Worker->>DB: Save low-confidence flag
        API-->>Staff: Request correction
    end
```

### UC-003: Identify and Organize Deficiencies
**Source:** [spec.md#uc-003-identify-and-organize-deficiencies-sourceinput](./spec.md#uc-003-identify-and-organize-deficiencies-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-003.png" -->

![UC-003 Sequence Diagram](./uml-models/seq-uc-003.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Defect as Deficiency Module
    participant DB as PostgreSQL
    Staff->>API: Open SOD review
    API->>Defect: Load SOD and evidence
    Defect->>DB: Read extracted SOD
    DB-->>Defect: SOD text and Tag
    Defect->>Defect: Segment deficiency candidates
    Defect-->>API: Distinct deficiency records
    API-->>Staff: Show candidates with evidence
    Staff->>API: Confirm or correct segmentation
    API->>DB: Persist segmentation decision
    alt Ambiguous boundary
        Defect-->>API: Flag for staff correction
        API-->>Staff: Show source region for correction
    end
    opt No deficiency identified
        API->>DB: Mark record incomplete
        API-->>Staff: Block POC generation
    end
```

### UC-004: Generate CMS-Grounded POC Drafts
**Source:** [spec.md#uc-004-generate-cms-grounded-poc-drafts-sourceinput](./spec.md#uc-004-generate-cms-grounded-poc-drafts-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-004.png" -->

![UC-004 Sequence Diagram](./uml-models/seq-uc-004.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Queue as Service Bus
    participant Worker as POC Worker
    participant Gateway as AI Gateway
    participant Source as Approved CMS Sources
    participant Model as Approved LLM Model
    participant DB as PostgreSQL
    Staff->>API: Request POC drafts
    API->>Queue: Enqueue POC job
    Queue-->>Worker: Deliver job
    Worker->>Gateway: Submit deficiency and Tag
    Gateway->>Source: Deterministic lookup of approved CMS sources
    Source-->>Gateway: Approved sources and versions
    Gateway->>Model: Request structured grounded POC
    Model-->>Gateway: Draft and citations
    Gateway->>Gateway: Validate schema and required elements
    Gateway->>DB: Save draft and source-set version
    DB-->>API: POC review state
    API-->>Staff: Show POC and supporting sources
    alt No approved source or failed validation
        Gateway-->>Worker: Blocked draft with reason
        Worker->>DB: Save exception state
        API-->>Staff: Manual review required
    end
```

### UC-005: Review and Edit Extracted Content
**Source:** [spec.md#uc-005-review-and-edit-extracted-content-sourceinput](./spec.md#uc-005-review-and-edit-extracted-content-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-005.png" -->

![UC-005 Sequence Diagram](./uml-models/seq-uc-005.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant UI as Review Frontend
    participant API as FastAPI API
    participant Review as Review Module
    participant DB as PostgreSQL
    Staff->>UI: Open extracted field
    UI->>API: GET field and evidence
    API->>Review: Load review context
    Review->>DB: Read field, evidence, history
    DB-->>Review: Current value and source locator
    Review-->>API: Review context
    API-->>UI: Field and evidence
    UI-->>Staff: Display source-linked value
    Staff->>UI: Accept or edit value
    UI->>API: Submit decision
    Review->>DB: Save revision and review decision
    DB-->>API: Updated review state
    API-->>UI: Verified or unresolved
    opt Missing evidence
        Review-->>API: Keep field unresolved
        API-->>UI: Approval blocked
    end
```

### UC-006: Review, Edit, and Approve POCs
**Source:** [spec.md#uc-006-review-edit-and-approve-pocs-sourceinput](./spec.md#uc-006-review-edit-and-approve-pocs-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-006.png" -->

![UC-006 Sequence Diagram](./uml-models/seq-uc-006.png)

```mermaid
sequenceDiagram
    participant Staff as Compliance Staff
    participant UI as Review Frontend
    participant API as FastAPI API
    participant Review as Review Module
    participant DB as PostgreSQL
    Staff->>UI: Open POC review
    UI->>API: GET POC, SOD, sources, history
    API->>Review: Load review context
    Review->>DB: Read draft and revisions
    DB-->>Review: Review data
    Review-->>API: AI/staff differences and flags
    API-->>UI: Reviewable POC
    Staff->>UI: Edit or approve POC
    UI->>API: Submit decision
    API->>Review: Apply deterministic approval gate
    Review->>DB: Save revision and review decision
    alt Required elements missing
        Review-->>API: Block approval
        API-->>UI: List missing elements
    else Approved
        Review->>DB: Commit approved state
        API-->>UI: Approved for authorized use
    end
```

### UC-007: Maintain CMS Knowledge Sources and POC Rubric
**Source:** [spec.md#uc-007-maintain-cms-knowledge-sources-and-poc-rubric-sourceinput](./spec.md#uc-007-maintain-cms-knowledge-sources-and-poc-rubric-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-007.png" -->

![UC-007 Sequence Diagram](./uml-models/seq-007.png)

```mermaid
sequenceDiagram
    participant Gov as Compliance Governance Staff
    participant API as FastAPI API
    participant Knowledge as Knowledge Module
    participant Store as Source Storage
    participant Source as Approved CMS Sources
    participant DB as PostgreSQL
    Gov->>API: Add or update CMS source
    API->>Knowledge: Validate governance permission
    Knowledge->>Store: Store source content
    Knowledge->>DB: Save source metadata and version
    Knowledge->>Source: Save approved source record
    Source-->>Knowledge: Source status
    Knowledge->>DB: Save indexing state
    API-->>Gov: Source status
    Gov->>API: Update POC rubric
    API->>DB: Save rubric version
    API-->>Gov: Governance confirmation
    alt Missing version or conflicting source
        Knowledge->>DB: Save pending state
        API-->>Gov: Resolution required
    end
```

### UC-009: Supply Pilot Evidence and Measure Outcomes
**Source:** [spec.md#uc-009-supply-pilot-evidence-and-measure-outcomes-sourceinput](./spec.md#uc-009-supply-pilot-evidence-and-measure-outcomes-sourceinput)

<!-- RENDER type="mermaid" src="./uml-models/seq-uc-009.png" -->

![UC-009 Sequence Diagram](./uml-models/seq-uc-009.png)

```mermaid
sequenceDiagram
    participant Coordinator as Pilot Facility Coordinator
    participant Staff as Compliance Staff
    participant API as FastAPI API
    participant Pilot as Pilot Measurement Module
    participant DB as PostgreSQL
    Coordinator->>API: Provide representative samples
    API->>Pilot: Validate sample coverage
    Pilot->>DB: Record governed sample metadata
    Staff->>API: Record baseline processing time
    API->>DB: Save baseline measurement
    Staff->>API: Review pilot outputs
    API->>Pilot: Calculate accuracy, recall, quality, time
    Pilot->>DB: Save evaluation results
    DB-->>API: Pilot report
    API-->>Staff: Show release-readiness results
    alt Missing format coverage or timing baseline
        Pilot->>DB: Mark evaluation incomplete
        API-->>Staff: Validation result unavailable
    end
```
