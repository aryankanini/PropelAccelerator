CREATE TABLE cms_source_conflict_decisions (
    decision_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id UUID NOT NULL REFERENCES cms_knowledge_sources(canonical_id) ON DELETE RESTRICT,
    decision TEXT NOT NULL CHECK (decision IN ('approve', 'reject')),
    decided_by TEXT NOT NULL,
    decided_at TIMESTAMPTZ NOT NULL,
    UNIQUE (source_id, decision_id)
);

CREATE TABLE poc_source_set_versions (
    poc_draft_id UUID NOT NULL REFERENCES poc_drafts(id) ON DELETE RESTRICT,
    source_id UUID NOT NULL REFERENCES cms_knowledge_sources(canonical_id) ON DELETE RESTRICT,
    effective_version TEXT NOT NULL,
    source_set_version CHAR(64) NOT NULL,
    PRIMARY KEY (poc_draft_id, source_id, effective_version)
);

CREATE INDEX poc_source_set_versions_source_set_version_index
    ON poc_source_set_versions (source_set_version);