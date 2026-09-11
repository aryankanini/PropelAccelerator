CREATE TABLE poc_validation_results (
    poc_draft_id UUID PRIMARY KEY REFERENCES poc_drafts(id) ON DELETE RESTRICT,
    quality_score NUMERIC(5, 4) NOT NULL CHECK (quality_score >= 0 AND quality_score <= 1),
    required_element_results JSONB NOT NULL,
    required_elements_complete BOOLEAN NOT NULL,
    approval_blocked BOOLEAN NOT NULL,
    evaluator_version TEXT NOT NULL,
    validated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (required_elements_complete OR approval_blocked)
);