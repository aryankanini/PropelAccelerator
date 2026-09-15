# Information Architecture - CMS-2567 Processing

## 1. Wireframe Specification

**Fidelity Level**: Low
**Screen Type**: Web
**Viewport**: 1440 x 900

## 2. System Overview

CMS-2567 Processing is a review-controlled workspace for compliance staff to upload a survey form, verify extracted data with evidence, organize deficiencies, prepare CMS-grounded POCs, and approve outputs before use. It also supports governance-source maintenance and pilot-outcome review.

| SCR-ID | Screen Name | Derived From | Type | Priority | Has Modal/Overlay | Fidelity Dir |
|---|---|---|---|---|---|---|
| SCR-001 | Processing Queue | UC-001, UC-005, UC-006 | Screen | P0 | No | Lo-Fi |
| SCR-002 | Upload Survey Form | UC-001 | Screen | P0 | Yes | Lo-Fi |
| SCR-003 | Extraction Review | UC-002, UC-005 | Screen | P0 | No | Lo-Fi |
| SCR-004 | Deficiency Segmentation | UC-003 | Screen | P0 | No | Lo-Fi |
| SCR-005 | POC Draft Workspace | UC-004 | Screen | P0 | No | Lo-Fi |
| SCR-006 | POC Review and Approval | UC-006 | Screen | P0 | No | Lo-Fi |
| SCR-007 | Approved Export | UC-006, FR-024 | Screen | P1 | No | Lo-Fi |
| SCR-008 | Knowledge Governance | UC-007 | Screen | P1 | No | Lo-Fi |
| SCR-009 | Pilot Outcomes | UC-009 | Screen | P2 | No | Lo-Fi |
| SCR-010 | Upload Error | UC-001 | Modal | P0 | Yes | Lo-Fi |

## 3. Wireframe References

### Generated Wireframes

**Figma Wireframes** (if applicable): N/A for low-fidelity HTML output.

**HTML/Image Wireframes**:

| Screen/Feature | File Path | Description | Fidelity | Date Created |
|---|---|---|---|---|
| Processing Queue | [Lo-Fi/wireframe-SCR-001-processing-queue.html](Lo-Fi/wireframe-SCR-001-processing-queue.html) | Staff worklist | Low | 2026-09-11 |
| Upload Survey Form | [Lo-Fi/wireframe-SCR-002-upload-survey-form.html](Lo-Fi/wireframe-SCR-002-upload-survey-form.html) | Format-aware intake | Low | 2026-09-11 |
| Extraction Review | [Lo-Fi/wireframe-SCR-003-extraction-review.html](Lo-Fi/wireframe-SCR-003-extraction-review.html) | Field review and evidence | Low | 2026-09-11 |
| Deficiency Segmentation | [Lo-Fi/wireframe-SCR-004-deficiency-segmentation.html](Lo-Fi/wireframe-SCR-004-deficiency-segmentation.html) | Confirm discrete SODs | Low | 2026-09-11 |
| POC Draft Workspace | [Lo-Fi/wireframe-SCR-005-poc-draft-workspace.html](Lo-Fi/wireframe-SCR-005-poc-draft-workspace.html) | Grounded POC drafting | Low | 2026-09-11 |
| POC Review and Approval | [Lo-Fi/wireframe-SCR-006-poc-review-approval.html](Lo-Fi/wireframe-SCR-006-poc-review-approval.html) | Staff approval control | Low | 2026-09-11 |
| Approved Export | [Lo-Fi/wireframe-SCR-007-approved-export.html](Lo-Fi/wireframe-SCR-007-approved-export.html) | Use-ready approved output | Low | 2026-09-11 |
| Knowledge Governance | [Lo-Fi/wireframe-SCR-008-knowledge-governance.html](Lo-Fi/wireframe-SCR-008-knowledge-governance.html) | Source-set management | Low | 2026-09-11 |
| Pilot Outcomes | [Lo-Fi/wireframe-SCR-009-pilot-outcomes.html](Lo-Fi/wireframe-SCR-009-pilot-outcomes.html) | Pilot measures | Low | 2026-09-11 |
| Upload Error | [Lo-Fi/wireframe-SCR-010-upload-error.html](Lo-Fi/wireframe-SCR-010-upload-error.html) | Controlled intake exception | Low | 2026-09-11 |

### Component Inventory

**Reference**: See [Component Inventory](component-inventory.md) for component specifications, states, responsive behavior, reuse, and implementation priority.

## 4. User Personas & Flows

### Persona 1: Compliance Staff

- **Role**: Reviews survey forms and approves controlled POC outputs.
- **Goals**: Resolve extraction flags, verify evidence, approve each POC before use.
- **Key Screens**: SCR-001 through SCR-007.
- **Primary Flow**: Processing Queue -> Upload Survey Form -> Extraction Review -> Deficiency Segmentation -> POC Draft Workspace -> POC Review and Approval -> Approved Export.
- **Wireframe References**: SCR-001 through SCR-007.
- **Decision Points**: Document support, field verification, deficiency boundaries, POC approval.

### User Flow Diagrams

- **Primary Flow**: FL-001 Intake and POC approval; see [Navigation Map](navigation-map.md).
- **Secondary Flow**: FL-002 Knowledge governance and FL-003 Pilot measurement; see [Navigation Map](navigation-map.md).

## 5. Screen Hierarchy

### Level 1: Processing Workspace

- **SCR-001 Processing Queue** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-001-processing-queue.html)
  - Description: Worklist and workflow entry point.
  - User Entry Point: Yes.
  - Key Components: Header, primary navigation, record table, action links.

- **SCR-002 Upload Survey Form** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-002-upload-survey-form.html)
  - Description: Starts a controlled processing record.
  - Parent Screen: SCR-001.
  - Key Components: Upload form, error link, record-control notice.

- **SCR-003 Extraction Review** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-003-extraction-review.html)
- **SCR-004 Deficiency Segmentation** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-004-deficiency-segmentation.html)
- **SCR-005 POC Draft Workspace** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-005-poc-draft-workspace.html)
- **SCR-006 POC Review and Approval** (P0 - Critical) - [Wireframe](Lo-Fi/wireframe-SCR-006-poc-review-approval.html)
- **SCR-007 Approved Export** (P1 - High Priority) - [Wireframe](Lo-Fi/wireframe-SCR-007-approved-export.html)

### Level 2: Governance and Measurement

- **SCR-008 Knowledge Governance** (P1 - High Priority) - [Wireframe](Lo-Fi/wireframe-SCR-008-knowledge-governance.html)
- **SCR-009 Pilot Outcomes** (P2 - Medium Priority) - [Wireframe](Lo-Fi/wireframe-SCR-009-pilot-outcomes.html)

### Screen Priority Legend

- **P0**: Critical path screens.
- **P1**: High-priority screens.
- **P2**: Medium-priority screens.
- **P3**: Low-priority screens.

### Modal/Dialog/Overlay Inventory

| Modal/Dialog Name | Type | Trigger Context | Parent Screen | Wireframe Reference | Priority |
|---|---|---|---|---|---|
| Upload Error | Modal | Unsupported or unreadable survey form | SCR-002 | [SCR-010](Lo-Fi/wireframe-SCR-010-upload-error.html) | P0 |

**Modal Behavior Notes**: The error state offers retry and queue return; production implementation must return focus to the triggering upload control when dismissed.

## 6. Navigation Architecture

```text
Processing Queue (SCR-001)
+-- Upload Survey Form (SCR-002)
|   +-- Upload Error (SCR-010)
|   +-- Extraction Review (SCR-003)
|       +-- Deficiency Segmentation (SCR-004)
|           +-- POC Draft Workspace (SCR-005)
|               +-- POC Review and Approval (SCR-006)
|                   +-- Approved Export (SCR-007)
+-- Knowledge Governance (SCR-008)
+-- Pilot Outcomes (SCR-009)
```

### Navigation Patterns

- **Primary Navigation**: Persistent links between queue, upload, governance, and pilot outcomes.
- **Secondary Navigation**: Record-stage links move backward or forward through review stages.
- **Mobile Navigation**: Collapses to a stacked single-column link group.

## 7. Interaction Patterns

### Pattern 1: Controlled POC Approval

- **Trigger**: Staff submits the reviewed POC.
- **Flow**: Draft workspace -> POC review -> approved export.
- **Screens Involved**: SCR-005, SCR-006, SCR-007.
- **Feedback**: Approved output identifies reviewer and source-set version.
- **Components Used**: Textarea, validation notice, approval action, status panel.

### Pattern 2: Upload Validation

- **Trigger**: Staff selects and submits a survey form.
- **Flow**: Upload form -> extraction review, or Upload Error for invalid input.
- **Screens Involved**: SCR-002, SCR-003, SCR-010.
- **Feedback**: Required file validation and explicit no-record-created error state.
- **Components Used**: File input, action link, modal dialog.

## 8. Error Handling

### Error Scenario 1: Unsupported or Unreadable Document

- **Trigger**: The file cannot be read or classified into a supported format.
- **Error Screen/State**: [SCR-010 Upload Error](Lo-Fi/wireframe-SCR-010-upload-error.html).
- **User Action**: Choose another document or return to the queue.
- **Recovery Flow**: SCR-010 -> SCR-002 or SCR-001.

### Error Scenario 2: Missing Evidence or POC Element

- **Trigger**: A required field lacks evidence or POC validation finds a missing element.
- **Error Screen/State**: Flagged state in SCR-003 or SCR-005.
- **User Action**: Review evidence or return the POC for correction.
- **Recovery Flow**: SCR-003 -> SCR-004, or SCR-006 -> SCR-005.

## 9. Responsive Strategy

| Breakpoint | Width | Layout Changes | Navigation Changes | Component Adaptations |
|---|---|---|---|---|
| Mobile | 375px | Single column and stacked panels | Stacked navigation links | Tables scroll horizontally; controls remain 44px minimum |
| Tablet | 768px | Two columns collapse when needed | Compact link group | Evidence and forms stack |
| Desktop | 1440px | Multi-column review panels | Expanded navigation | Tables and evidence side-by-side |

### Responsive Wireframe Variants

- Mobile variants: Not generated; responsive behavior is documented in each HTML screen.
- Tablet variants: Not generated; responsive behavior is documented in each HTML screen.
- Desktop variants: All ten Lo-Fi HTML wireframes.

## 10. Accessibility

### WCAG Compliance

- **Target Level**: AA in production implementation.
- **Color Contrast**: Black text and controls on white or light-gray lo-fi surfaces.
- **Keyboard Navigation**: Semantic links, controls, skip links, and visible focus outlines.
- **Screen Reader Support**: Landmarks, associated form labels, status regions, table headers, and dialog semantics.

### Accessibility Considerations by Screen

| Screen | Key Accessibility Features | Wireframe Notes |
|---|---|---|
| SCR-002 | Required file input and live status | Supports controlled upload feedback |
| SCR-003 | Labels, source placeholder description | Keeps evidence understandable |
| SCR-006 | Required textarea and approval notice | Keeps approval criteria visible |
| SCR-010 | Dialog labels and clear recovery links | Production version needs focus return |

### Focus Order

- Each screen follows header navigation, main heading, primary content, then secondary panels in reading order.

## 11. Content Strategy

### Content Hierarchy

- **H1**: Identifies the current operational task.
- **H2**: Groups record content, evidence, checks, and metrics.
- **Body Text**: Uses concise compliance workflow language.
- **Placeholder Content**: Represents evidence and survey text only in low-fidelity screens.

### Content Types by Screen

| Screen | Content Types | Wireframe Reference |
|---|---|---|
| SCR-003 | Fields, evidence, flags | [Extraction Review](Lo-Fi/wireframe-SCR-003-extraction-review.html) |
| SCR-005 | POC text, validation, source references | [POC Draft Workspace](Lo-Fi/wireframe-SCR-005-poc-draft-workspace.html) |
| SCR-009 | Metrics and sample coverage table | [Pilot Outcomes](Lo-Fi/wireframe-SCR-009-pilot-outcomes.html) |