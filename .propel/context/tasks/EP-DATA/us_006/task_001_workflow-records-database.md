# Task - TASK_001

## Requirement Reference
- **User Story:** us_006
- **Story Location:** .propel/context/tasks/EP-DATA/us_006/us_006.md
- **Acceptance Criteria:**
  - AC-001: Persist fields, deficiencies, POCs, and revisions with valid parent identifiers and referential integrity.
- **Edge Cases:**
  - Reject deletion of a processing record when retained audit data exists.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-001 through DR-004 and TR-004 require authoritative relational workflow state. |

---

## Task Overview
Create the normalized, traceable PostgreSQL schema for compliance workflow records and enforce parent-child integrity. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 application module boundary must establish the owning domain modules.

## Impacted Components
- New ProcessingRecord, ExtractedField, Deficiency, PlanOfCorrection, and ContentRevision tables and constraints.

## Implementation Plan
- Create the processing-record table with provider identity, survey metadata, format, and workflow state.
- Create child tables using non-null foreign keys matching the approved logical data model.
- Model POC ownership by one deficiency and revision ownership by an extracted field or POC using enforced relationships.
- Preserve review history with immutable revision rows rather than overwriting content.
- Restrict processing-record deletion when dependent audit history exists.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-DATA/us_006/us_006.md
`- .propel/context/docs/model.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/workflow/adapters/postgres/migrations/001_create_workflow_records.sql | Creates workflow tables, foreign keys, and deletion protections. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Create ProcessingRecord with the required workflow identity and state fields. (AC-001)
- [ ] Create ExtractedField and Deficiency tables with required ProcessingRecord foreign keys. (AC-001)
- [ ] Create PlanOfCorrection with exactly one Deficiency parent. (AC-001)
- [ ] Create ContentRevision records that retain attributable revision history. (AC-001)
- [ ] Enforce non-null parent relationships and foreign-key integrity for all workflow children. (AC-001)
- [ ] Reject deletion of a processing record with retained audit data. (edge case)