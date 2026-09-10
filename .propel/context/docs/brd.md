# CMS-2567 Compliance Assistant

## Description
An AI-assisted CMS-2567 processing solution for nursing-home compliance staff. It accepts supported CMS Survey Form formats, identifies the format, extracts required survey and deficiency information with source-linked evidence, and drafts a separate CMS-aligned Plan of Correction for each deficiency. Every extracted result and POC requires staff verification and documented approval before use or submission.

## Problems & Solutions

### Problem 1: Manual deficiency review delays response
**Who is affected:** Nursing-home compliance staff
**Impact:** Staff spend substantial time reviewing survey forms, locating each SOD, and organizing deficiencies before corrective-action work can begin. This slows response preparation.
**How this product solves it:** The product identifies the survey format, extracts provider and survey details, segments each deficiency, and links extracted values to source evidence for rapid staff verification.

### Problem 2: POC drafting is inconsistent and difficult to validate
**Who is affected:** Compliance staff and nursing-home leadership responsible for corrective actions
**Impact:** Manually drafted POCs may vary in completeness, clarity, and alignment with CMS expectations, requiring extensive revision and increasing compliance risk.
**How this product solves it:** The product drafts a separate CMS-aligned POC for each deficiency, while requiring documented compliance-staff verification and approval before the POC can be used or submitted.

### Problem 3: Compliance validation and traceability are difficult
**Who is affected:** Compliance staff and nursing-home leadership
**Impact:** Missing evidence, incomplete POCs, or unclear links between deficiencies and corrective actions can make review difficult and increase compliance risk.
**How this product solves it:** The product links each deficiency and POC to source evidence, validates required POC elements, flags low-confidence or incomplete content, and maintains a review record of staff verification and approval.

## Key Features
- Upload and process CMS Survey Forms in all three supported formats.
- Identify the uploaded form format before extraction.
- Extract Provider Name, Provider Number, Survey Date, Tag, and SOD from all supported formats.
- Extract Plan of Correction and Completion Date only from Format 2; leave both fields blank for Format 1 and the open-source format.
- Link every extracted field and deficiency to its source evidence.
- Identify and separate each deficiency for individual handling.
- Draft a separate CMS-aligned POC for every deficiency.
- Ground POC generation in authoritative CMS regulations, guidance, and tag definitions, with a process to maintain that knowledge.
- Validate required POC elements and flag incomplete or low-confidence content.
- Require staff verification and documented approval for every extracted field and POC.
- Show AI-generated content separately from staff edits and preserve the review history.

## Success Criteria
- Average staff processing time per CMS-2567 is reduced by at least 50% during a representative pilot.
- 100% of extracted fields and POCs have documented compliance-staff verification and approval before use or submission.
- Field-level extraction accuracy is at least 95% on the validated test set across all three supported formats.
- Format 2 Plan of Correction and Completion Date extraction meets the agreed accuracy threshold; those fields remain blank for Format 1 and the open-source format.
- Deficiency/SOD recall is at least 95% across the validated test set.
- Every identified deficiency has a distinct POC draft linked to its source SOD evidence.
- Generated POCs meet an agreed minimum CMS-compliance and quality score based on expert review.
- Required POC elements and missing or low-confidence content are flagged before approval.
- AI-generated text and staff edits are distinguishable in the review history.

## Scope
**In:** Upload and processing of the three specified CMS Survey Form formats; format identification; OCR extraction of common fields; conditional extraction of POC and Completion Date for Format 2; SOD identification and source evidence linking; CMS-grounded POC drafting for each deficiency; retrieval and maintenance of authoritative CMS regulations, guidance, and tag definitions; required-element and confidence validation; AI-versus-staff change tracking; staff verification and documented approval; review history.

**Out:** Automatic submission of POCs to CMS; replacing compliance-staff judgment or approval; unsupported survey-form formats beyond the three defined formats; determination of whether a provider is legally compliant; execution or monitoring of the nursing home’s corrective actions; broader clinical, resident-care, or general document-processing workflows outside CMS-2567 handling.

## Assumptions & Open Questions

| # | Item | Risk / Impact | Owner |
|---|------|---------------|-------|
| 1 | The three defined survey-form formats can be reliably identified from uploaded documents. | Misclassification could cause POC or Completion Date fields to be extracted incorrectly. | Product owner and compliance subject-matter expert |
| 2 | A validated test set covering all three formats and representative SODs is available. | Accuracy and the 50% time-reduction target cannot be measured credibly. | Product owner and pilot nursing homes |
| 3 | The minimum acceptable CMS-compliance/quality score for POCs will be defined by expert reviewers. | POCs may pass extraction checks but fail practical compliance review. | Compliance subject-matter expert / facility compliance leadership |
| 4 | CMS regulations, guidance, and tag definitions have authoritative sources and an approved maintenance process. CMS nursing-home survey guidance states that surveyors use federal requirements and interpretive guidelines when assessing compliance. | Outdated or conflicting guidance could produce noncompliant drafts. | Compliance governance owner |
| 5 | Every output must remain blocked from use or submission until a designated staff member approves it. | Accidental reliance on unreviewed AI content could create regulatory and operational exposure. | Compliance leadership |
| 6 | The initial release will support CMS-2567 processing only and will not determine legal compliance or execute corrective actions. | Scope expansion could delay validation and obscure product accountability. | Product owner |
| 7 | Pilot facilities will provide representative historical CMS-2567 samples and staff time measurements. | Without real-world samples and baseline timings, the 95% accuracy and 50% time-reduction targets cannot be validated reliably. | Product owner and pilot nursing homes |
