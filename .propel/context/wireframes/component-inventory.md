# Component Inventory - CMS-2567 Processing

## Component Specification

**Fidelity Level**: Low
**Screen Type**: Web
**Viewport**: 1440 x 900

## Component Summary

| Component Name | Type | Screens Used | Priority | Implementation Status |
|---|---|---|---|---|
| Header and navigation | Layout/Navigation | SCR-001 to SCR-009 | High | Wireframed |
| Review form | Interactive | SCR-002, SCR-003, SCR-005, SCR-006, SCR-008 | High | Wireframed |
| Evidence panel | Content | SCR-003 to SCR-006 | High | Wireframed |
| Data table | Content | SCR-001, SCR-008, SCR-009 | Medium | Wireframed |
| Status and error feedback | Feedback | SCR-002, SCR-003, SCR-005 to SCR-007, SCR-010 | High | Wireframed |

## Detailed Component Specifications

### Layout Components

#### Header and Content Grid

- **Type**: Layout.
- **Used In Screens**: SCR-001 to SCR-009.
- **Wireframe References**: [Processing Queue](Lo-Fi/wireframe-SCR-001-processing-queue.html), [Extraction Review](Lo-Fi/wireframe-SCR-003-extraction-review.html).
- **Description**: Bounded page header and one- or two-column task surface.
- **Variants**: Queue, record review, administration.
- **Interactive States**: Navigation link default, hover, focus, active.
- **Responsive Behavior**: Desktop uses multi-column panels; tablet and mobile stack panels.
- **Implementation Notes**: Preserve landmark order and content maximum width.

### Navigation Components

#### Primary and Record Navigation

- **Type**: Navigation.
- **Used In Screens**: SCR-001 to SCR-009.
- **Wireframe References**: [Upload](Lo-Fi/wireframe-SCR-002-upload-survey-form.html), [POC Review](Lo-Fi/wireframe-SCR-006-poc-review-approval.html).
- **Description**: Primary navigation moves between operating areas; record navigation moves through the review path.
- **Variants**: Primary, record-stage, back link, active route.
- **Interactive States**: Default, hover, focus, active, disabled when a prerequisite is unmet.
- **Responsive Behavior**: Links stack below 768px.
- **Implementation Notes**: Use meaningful link text and `aria-current` for the active route.

### Content Components

#### Evidence and Review Card

- **Type**: Content.
- **Used In Screens**: SCR-003 to SCR-006.
- **Wireframe References**: [Extraction Review](Lo-Fi/wireframe-SCR-003-extraction-review.html), [POC Draft Workspace](Lo-Fi/wireframe-SCR-005-poc-draft-workspace.html).
- **Description**: Displays extraction data, source location, confidence, validation, or CMS grounding.
- **Variants**: Field evidence, deficiency, POC checks, grounding source.
- **Interactive States**: Default, loading while evidence is retrieved, empty when evidence is absent.
- **Responsive Behavior**: Secondary evidence panel stacks after primary review content.
- **Implementation Notes**: Preserve source location and AI-versus-staff provenance.

#### Data Table

- **Type**: Content.
- **Used In Screens**: SCR-001, SCR-008, SCR-009.
- **Wireframe References**: [Processing Queue](Lo-Fi/wireframe-SCR-001-processing-queue.html), [Pilot Outcomes](Lo-Fi/wireframe-SCR-009-pilot-outcomes.html).
- **Description**: Shows records, source versions, and pilot results.
- **Variants**: Queue, governance source list, outcome metrics.
- **Interactive States**: Default, loading, empty, selected row where future bulk actions are required.
- **Responsive Behavior**: Horizontally scrollable at narrow widths.
- **Implementation Notes**: Use semantic table headers; align numeric values right in production.

### Interactive Components

#### Form Controls and Workflow Actions

- **Type**: Interactive.
- **Used In Screens**: SCR-002, SCR-003, SCR-005, SCR-006, SCR-008.
- **Wireframe References**: [Upload](Lo-Fi/wireframe-SCR-002-upload-survey-form.html), [POC Review](Lo-Fi/wireframe-SCR-006-poc-review-approval.html).
- **Description**: File selection, field inputs, textareas, and actions that advance a documented flow.
- **Variants**: Primary action, secondary action, required input, disabled approval.
- **Interactive States**: Default, hover, active, focus, disabled, loading, error.
- **Responsive Behavior**: Full-width controls; 44px minimum target size.
- **Implementation Notes**: Associate labels and errors with inputs; only enable approval after requirements pass.

### Feedback Components

#### Status Notice and Error Dialog

- **Type**: Feedback.
- **Used In Screens**: SCR-002, SCR-003, SCR-005 to SCR-007, SCR-010.
- **Wireframe References**: [Approved Export](Lo-Fi/wireframe-SCR-007-approved-export.html), [Upload Error](Lo-Fi/wireframe-SCR-010-upload-error.html).
- **Description**: Communicates validation results, approval state, and controlled exceptions.
- **Variants**: Low confidence, missing requirement, approved, unsupported upload.
- **Interactive States**: Default, focus for recovery links, loading for asynchronous validation.
- **Responsive Behavior**: Dialog becomes full-width within the mobile content area.
- **Implementation Notes**: Use status live regions and modal focus management in production.

## Component Relationships

```text
Header
+-- Primary Navigation
Review Workspace
+-- Form Controls
+-- Evidence and Review Card
+-- Status Notice
+-- Workflow Action
```

## Component States Matrix

| Component | Default | Hover | Active | Focus | Disabled | Error | Loading | Empty |
|---|---|---|---|---|---|---|---|---|
| Navigation link | x | x | x | x | x | - | - | - |
| Workflow action | x | x | x | x | x | x | x | - |
| Input and textarea | x | x | x | x | x | x | - | x |
| Evidence card | x | - | - | - | - | x | x | x |
| Error dialog | x | - | - | x | - | x | - | - |

## Reusability Analysis

| Component | Reuse Count | Screens | Recommendation |
|---|---|---|---|
| Header and navigation | 9 | SCR-001 to SCR-009 | Create shared component |
| Workflow action | 8 | SCR-001 to SCR-008 | Create shared component |
| Status notice | 6 | SCR-002 to SCR-007 | Create shared component |
| Evidence and review card | 4 | SCR-003 to SCR-006 | Create variant |

## Responsive Breakpoints Summary

| Breakpoint | Width | Components Affected | Key Adaptations |
|---|---|---|---|
| Mobile | 375px | Navigation, forms, tables, dialogs | Stack content; scroll tables; retain 44px targets |
| Tablet | 768px | Evidence and review panels | Collapse two columns as needed |
| Desktop | 1440px | All components | Use multi-column review workspace |

## Implementation Priority Matrix

### High Priority (Core Components)

- [ ] Header and navigation - Used across operational screens.
- [ ] Review form and workflow action - Controls approvals and flow progression.

### Medium Priority (Feature Components)

- [ ] Evidence and review card - Supports traceable review.
- [ ] Data table - Supports queue, governance, and pilot analysis.

### Low Priority (Enhancement Components)

- [ ] Bulk selection toolbar - Not required in initial wireframes.

## Framework-Specific Notes

**Detected Framework**: Static HTML/CSS wireframe output; no UI framework dependency detected.
**Component Library**: Custom semantic HTML primitives.

### Framework Patterns Applied

- Semantic landmarks and native controls provide the accessible wireframe baseline.
- CSS media queries express responsive structure without a framework dependency.

### Component Library Mappings

| Wireframe Component | Framework Component | Customization Required |
|---|---|---|
| Workflow action | Native button or link | Approval gating and status feedback |
| Input field | Native input | Validation and evidence association |
| Data table | Native table | Sorting and filtering when implemented |

## Accessibility Considerations

| Component | ARIA Attributes | Keyboard Navigation | Screen Reader Notes |
|---|---|---|---|
| Navigation | `aria-label`, `aria-current` | Tab and Enter | Announces current route |
| Form control | `required`, `aria-required` | Tab and Enter | Label announces purpose |
| Status notice | `role=status`, `aria-live` | No extra tab stop | Announces feedback |
| Error dialog | `role=dialog`, labelled and described | Tab, Escape in production | Announces exception and recovery |

## Design System Integration

**Design System Reference**: Not available; this is a grayscale low-fidelity output.

### Components Matching Design System

- [x] Native form controls - Intentionally neutral lo-fi primitives.
- [x] Basic navigation - Intentionally neutral lo-fi primitives.

### New Components to Add to Design System

- [ ] Review evidence panel - Requires high-fidelity design-system definition.
- [ ] Approval status notice - Requires high-fidelity feedback semantics.