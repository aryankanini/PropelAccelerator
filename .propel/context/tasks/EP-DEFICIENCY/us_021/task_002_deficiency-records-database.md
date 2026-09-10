# Task - TASK_002

## Requirement Reference
- **User Story:** us_021
- **Story Location:** .propel/context/tasks/EP-DEFICIENCY/us_021/us_021.md
- **Acceptance Criteria:**
  - AC-001: Each detected SOD boundary creates a distinct deficiency linked to its SOD, Tag, evidence, and processing record.
- **Edge Cases:**
  - Ambiguous boundaries are flagged for correction rather than finalized.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Database | Azure Database for PostgreSQL Flexible Server | PostgreSQL 16 | DR-002 requires distinct, traceable deficiency records with enforceable parent links. |

---

## Task Overview
Create PostgreSQL storage for distinct deficiency candidates, their source associations, and segmentation status. Estimated effort: 6 hours.

## Dependent Tasks
- US_006 must establish workflow-record parent tables.

## Impacted Components
- New Deficiency table constraints and evidence-link persistence schema.

## Implementation Plan
- Add deficiency columns for SOD text, Tag, segmentation status, and processing-record identity.
- Store evidence references in a normalized child relation or constrained reference field.
- Enforce one valid processing-record parent for every deficiency.
- Persist correction-required status independently from confirmed status.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/docs/design.md
`- .propel/context/tasks/EP-DEFICIENCY/us_021/us_021.md
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/deficiency/adapters/postgres/migrations/021_create_deficiencies.sql | Creates deficiency and evidence-link storage with integrity constraints. |

## External References
- [PostgreSQL 16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Create one persistent deficiency record per detected boundary. (AC-001)
- [ ] Persist the source SOD text, Tag, and processing-record foreign key for each deficiency. (AC-001)
- [ ] Persist each deficiency evidence association without duplicating the parent record. (AC-001)
- [ ] Constrain segmentation status to distinguish confirmed and correction-required candidates. (AC-001, edge case)
