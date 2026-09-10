# Task - TASK_001

## Requirement Reference
- **User Story:** us_011
- **Story Location:** .propel/context/tasks/EP-INTAKE/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: Accept a readable supported form and acknowledge it with a processing-record identifier within the stated response target.
- **Edge Cases:**
  - Reject an empty upload before a document or processing record is stored.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | PENDING |
| **Wireframe Type** | N/A |
| **Wireframe Path/URL** | N/A |
| **Screen Spec** | SCR-001 reference pending |
| **UXR Requirements** | N/A |
| **Design Tokens** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React with TypeScript | React 19.x / TypeScript 5.x | NFR-001 requires a responsive upload interaction. |

## Task Overview
BLOCKED: Implement the staff-facing survey-upload form and acknowledgement state after SCR-001 is specified. Estimated effort: 5 hours.

## Dependent Tasks
- US_007 immutable document storage must be available.
- TASK_002 survey upload backend must expose the upload contract.

## Impacted Components
- New intake upload screen and API client.

## Implementation Plan
- Build a multipart upload form with selected-file and pending states.
- Submit the file to the intake endpoint without manually setting the multipart content type.
- Display the returned processing-record identifier and sanitized validation errors.

## Current Project State
```text
HealthcareAccelerator/
|- package.json
|- .propel/context/tasks/EP-INTAKE/us_011/us_011.md
`- .propel/context/docs/design.md
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | app/frontend/src/features/intake/SurveyUploadForm.tsx | Provides the survey file upload interaction. |
| CREATE | app/frontend/src/features/intake/intakeApi.ts | Sends multipart uploads and maps acknowledgement responses. |

## External References
- [React 19 forms](https://react.dev/reference/react-dom/components/form)

## Build Commands
- [Refer to applicable technology stack build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)

## Implementation Checklist
- [ ] Provide a file input and submit control for CMS Survey Forms. (AC-001)
- [ ] Disable duplicate submission while an upload acknowledgement is pending. (AC-001)
- [ ] Send the selected file as multipart form data to the intake API. (AC-001)
- [ ] Display the processing-record identifier returned for an accepted upload. (AC-001)
- [ ] Present the empty-file rejection as a sanitized validation outcome. (edge case)