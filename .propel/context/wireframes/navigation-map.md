# Navigation Map - CMS-2567 Processing

## Flow Index

| Flow ID | Source Use Case | Sequence | Completion Condition |
|---|---|---|---|
| FL-001 | UC-001 to UC-006 | SCR-001 -> SCR-002 -> SCR-003 -> SCR-004 -> SCR-005 -> SCR-006 -> SCR-007 | Staff-approved POC is available for controlled use |
| FL-002 | UC-001 exception | SCR-002 -> SCR-010 -> SCR-002 or SCR-001 | No record is approved for unreadable or unsupported input |
| FL-003 | UC-007 | SCR-008 -> SCR-008 | Source is saved pending review and cannot ground POCs until approved |
| FL-004 | UC-009 | SCR-009 -> SCR-002 or SCR-001 | Pilot measures and representative coverage are visible |

## Screen-to-Screen Links

| Source Screen | Element | Action | Target Screen | Flow |
|---|---|---|---|---|
| SCR-001 | Start new record | Click | SCR-002 | FL-001 |
| SCR-001 | Review fields | Click | SCR-003 | FL-001 |
| SCR-002 | Classify and extract | Submit | SCR-003 | FL-001 |
| SCR-002 | View unreadable document state | Click | SCR-010 | FL-002 |
| SCR-003 | Verify fields and review deficiencies | Submit | SCR-004 | FL-001 |
| SCR-003 | Processing queue | Click | SCR-001 | FL-001 |
| SCR-004 | Confirm deficiencies and generate POC drafts | Click | SCR-005 | FL-001 |
| SCR-004 | Extraction review | Click | SCR-003 | FL-001 |
| SCR-005 | Save draft and begin POC review | Submit | SCR-006 | FL-001 |
| SCR-005 | Deficiencies | Click | SCR-004 | FL-001 |
| SCR-006 | Approve POC for controlled export | Submit | SCR-007 | FL-001 |
| SCR-006 | Return for correction | Click | SCR-005 | FL-001 |
| SCR-007 | Return to processing queue | Click | SCR-001 | FL-001 |
| SCR-008 | Save as pending review | Submit | SCR-008 status | FL-003 |
| SCR-009 | Upload form or processing queue | Click | SCR-002 or SCR-001 | FL-004 |
| SCR-010 | Choose another document | Click | SCR-002 | FL-002 |
| SCR-010 | Return to processing queue | Click | SCR-001 | FL-002 |

## Dead Ends and Exceptions

- SCR-007 is a documented completion state with a return link to SCR-001; it provides no submission action.
- SCR-008 persists a visible pending-review response on the same screen; sources are intentionally unavailable for POC grounding until approved.
- SCR-010 is the controlled exception state; it confirms that no approved record was created and supplies recovery paths.
- All other screens have at least one explicit outbound link or form action.