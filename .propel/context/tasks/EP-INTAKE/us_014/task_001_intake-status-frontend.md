# Task - TASK_001

## Requirement Reference
- **User Story:** us_014
- **Story Location:** .propel/context/tasks/EP-INTAKE/us_014/us_014.md
- **Acceptance Criteria:**
  - AC-001: Display detected format and processing state without showing an error record as approved.
- **Edge Cases:**
  - An inaccessible record returns an authorization outcome without revealing document metadata.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | PENDING |
| **Wireframe Type** | N/A |
| **Wireframe Path/URL** | N/A |
| **Screen Spec** | SCR-002 reference pending |
| **UXR Requirements** | N/A |
| **Design Tokens** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React with TypeScript | React 19.x / TypeScript 5.x | UC-001 requires staff-visible intake state. |

## Task Overview
BLOCKED: Implement the processing-status view for a returned upload identifier after SCR-002 is specified. Estimated effort: 4 hours.

## Dependent Tasks
- US_011 upload acknowledgement must be available.
- TASK_002 intake status backend must expose authorized status data.

## Impacted Components
- New intake-status screen and status API client.

## Implementation Plan
- Fetch the status by processing-record identifier.
- Render format, current state, and a distinct unresolved/error presentation.
- Map authorization outcomes without displaying protected metadata.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-INTAKE/us_014/us_014.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/frontend/src/features/intake/ProcessingStatus.tsx | Renders authorized intake status. |
| CREATE | app/frontend/src/features/intake/statusApi.ts | Retrieves and maps status outcomes. |

## External References
- [React useEffect](https://react.dev/reference/react/useEffect)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Request status using the processing-record identifier. (AC-001)
- [ ] Display the detected format and current processing state. (AC-001)
- [ ] Render error states without any approved representation. (AC-001)
- [ ] Render an authorization outcome without document metadata. (edge case)