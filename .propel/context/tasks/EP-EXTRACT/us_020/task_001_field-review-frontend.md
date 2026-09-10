# Task - TASK_001

## Requirement Reference
- **User Story:** us_020
- **Story Location:** .propel/context/tasks/EP-EXTRACT/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: Display each extracted value with confidence state and source-evidence locator.
- **Edge Cases:**
  - Evidence retrieval failure displays an unresolved state and no approval control.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | PENDING |
| **Wireframe Type** | N/A |
| **Wireframe Path/URL** | N/A |
| **Screen Spec** | SCR-003 and SCR-004 references pending |
| **UXR Requirements** | N/A |
| **Design Tokens** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React with TypeScript | React 19.x / TypeScript 5.x | FR-007, FR-008, and UC-002 require evidence-linked review display. |

## Task Overview
BLOCKED: Implement the staff field-review view with confidence and evidence states after SCR-003 and SCR-004 are specified. Estimated effort: 6 hours.

## Dependent Tasks
- US_018 evidence locator persistence must be available.
- TASK_002 field review backend must expose review-safe field data.

## Impacted Components
- New extracted-field review screen and API client.

## Implementation Plan
- Fetch reviewable field projections for a processing record.
- Display field values, confidence status, and evidence locator controls.
- Hide approval controls while evidence is unresolved or unavailable.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-EXTRACT/us_020/us_020.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/frontend/src/features/review/FieldReview.tsx | Renders extracted fields and evidence states. |
| CREATE | app/frontend/src/features/review/fieldReviewApi.ts | Retrieves review-safe field projections. |

## External References
- [React useEffect](https://react.dev/reference/react/useEffect)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Load the extracted-field review projection for the selected record. (AC-001)
- [ ] Display each field value with its confidence state. (AC-001)
- [ ] Provide a control that opens the field source-evidence locator. (AC-001)
- [ ] Display an unresolved state when evidence retrieval fails. (edge case)
- [ ] Do not render an approval control for unresolved evidence. (edge case)