# Task - TASK_002

## Requirement Reference
- **User Story:** us_007
- **Story Location:** .propel/context/tasks/EP-DATA/us_007/us_007.md
- **Acceptance Criteria:**
  - AC-001: Record object identity, media type, and content hash for an accepted document upload.
- **Edge Cases:**
  - Persist a failed integrity state that prevents downstream processing after a hash mismatch.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-005 and DR-007 require durable document provenance linked to workflow state. |

---

## Task Overview
Add relational source-document provenance and integrity-state storage linked to a processing record. Estimated effort: 5 hours.

## Dependent Tasks
- US_006 workflow record schema must exist before adding the SourceDocument relationship.

## Impacted Components
- New SourceDocument table and processing-record integrity state fields.

## Implementation Plan
- Add SourceDocument with a required ProcessingRecord foreign key, object identity, media type, and content hash.
- Make the object identity immutable and unique within its storage namespace.
- Record extraction-library name and version for reproducible document handling.
- Store a controlled upload integrity state that can prevent processing after verification failure.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-DATA/us_007/us_007.md
`- .propel/context/docs/model.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/documents/adapters/postgres/migrations/002_create_source_documents.sql | Adds source-document provenance and integrity-state records. |

## External References
- [PostgreSQL 16 data types](https://www.postgresql.org/docs/16/datatype.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [x] Add SourceDocument with a required ProcessingRecord parent identifier. (AC-001)
- [x] Persist immutable object identity, media type, and content hash. (AC-001)
- [x] Record the approved extraction library name and version for each source document. (AC-001)
- [x] Enforce uniqueness for a stored object identity in its configured namespace. (AC-001)
- [x] Persist an integrity failure state that prevents downstream processing. (edge case)