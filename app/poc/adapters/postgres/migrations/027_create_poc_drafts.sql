CREATE TABLE poc_drafts (
    id UUID PRIMARY KEY,
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    source_set_version CHAR(64) NOT NULL,
    content TEXT NOT NULL,
    review_state TEXT NOT NULL DEFAULT 'pending'
        CHECK (review_state IN ('pending', 'blocked', 'approved')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    superseded_at TIMESTAMPTZ,
    UNIQUE (deficiency_id, source_set_version)
);

CREATE UNIQUE INDEX poc_drafts_one_active_per_deficiency_index
    ON poc_drafts (deficiency_id)
    WHERE superseded_at IS NULL;

CREATE TABLE poc_generation_errors (
    id UUID PRIMARY KEY,
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    error_message TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);