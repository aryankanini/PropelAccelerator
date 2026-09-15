# SCR-001 Processing Queue Figma Specification

## Overview

| Field | Value |
|---|---|
| Screen | SCR-001 Processing Queue |
| Version | 1.0 |
| Source | `context/wireframes/Lo-Fi/wireframe-SCR-001-processing-queue.html` |
| Primary user | Compliance review staff |
| Objective | Direct staff to records requiring verification or plan approval. |

## Direction And Foundations

**Direction:** Utilitarian.

The screen is a compact operational worklist. It prioritizes scan speed, explicit queue state, and an obvious next action rather than decorative treatment. It must not resemble a marketing dashboard or card-heavy analytics experience.

| Token group | Values |
|---|---|
| Typography | Georgia headings and body; Arial controls and labels; 16px body; 48px desktop H1. |
| Spacing | 4, 8, 12, 16, 20, 24, 32, 40, 64. |
| Radius | 4px controls; 8px queue panel. |
| Elevation | One restrained raised panel shadow. |
| Color roles | Ink for text; white raised surface; cool-gray canvas and borders; teal primary action; amber verification warning; red approval blocker. |
| Motion | 150ms ease transitions; skeleton shimmer only; no motion when reduced-motion is enabled. |

## Screen Inventory

| Frame | Size | Required content |
|---|---:|---|
| ProcessingQueue/Default | 1440x1024 | Header, primary navigation, page heading, start-record action, records table with two review rows. |
| ProcessingQueue/Loading | 1440x1024 | Same header and panel geometry, queue summary, three skeleton rows. |
| ProcessingQueue/Empty | 1440x1024 | Same header and panel geometry, no-records statement, start-record action. |
| ProcessingQueue/Error | 1440x1024 | Same header and panel geometry, unavailable statement, retry action. |
| ProcessingQueue/Default-Mobile | 390x844 | Stacked heading/action, horizontally scrollable table, full-width action. |
| ProcessingQueue/Default-Tablet | 768x1024 | Full navigation and queue panel with responsive spacing. |

## Components

| Figma component | Variants | Usage |
|---|---|---|
| C/Navigation/Header | Desktop, Mobile; Default, Focus | Brand and primary navigation. Current page is visible and programmatically identified. |
| C/Actions/Button | Primary; Medium; Default, Hover, Focus, Active, Disabled, Loading | Start new record and retry. Minimum 44px height. |
| C/Actions/Link | Default, Hover, Focus, Active | Review links in the action column. |
| C/Content/Status | Verification, Blocked | Text-plus-color status; amber for verification and red for approval blocker. |
| C/Content/Table | Default, Loading, Empty, Error | Four columns: provider, format, stage, action. |

## Layout And Responsive Behavior

- Use auto layout on all frames and components. The page container fills its parent up to 1200px; the queue panel fills the container.
- Desktop uses a 12-column grid with 32px outer gutters. Header is 76px tall. The heading and start-record action share one row.
- At 768px, reduce gutters to 24px while retaining the full navigation.
- At 390px, stack heading and primary action. Keep navigation horizontally scrollable and retain the table as a horizontally scrollable semantic table.
- Do not truncate provider names without exposing the full name to assistive technology.

## Interaction Flows

| Trigger | Outcome | Destination or state |
|---|---|---|
| Start new record | Opens CMS survey upload workflow. | SCR-002 Upload Survey Form |
| Review fields | Opens extraction verification workflow. | SCR-003 Extraction Review |
| Review POC | Opens plan approval workflow. | SCR-006 POC Review Approval |
| Queue request pending | Preserves table geometry with skeleton rows. | ProcessingQueue/Loading |
| Queue has no records | Shows recovery action. | ProcessingQueue/Empty |
| Queue request fails | Shows retry action; retry returns to loading then default. | ProcessingQueue/Error |

## Accessibility And Handoff

- Use header, navigation, main, section, heading, button, link, and table semantics. Include a skip link before repeated navigation.
- The tab sequence is skip link, brand, navigation, start-record action, review links, then retry when present.
- Use a visible 3px focus outline with offset on every interactive control.
- Associate table headers using `scope="col"`. Announce queue count changes through a polite live region and failures through an alert.
- Do not use color as the only status indicator; status text states both verification and approval-blocked conditions.
- Export naming: `CMS2567__Web__ProcessingQueue__Default__v1.jpg`, plus Loading, Empty, Error, and Mobile variants.