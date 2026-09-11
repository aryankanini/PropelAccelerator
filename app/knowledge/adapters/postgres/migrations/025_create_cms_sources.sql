CREATE TABLE cms_knowledge_sources (
    canonical_id UUID PRIMARY KEY,
    canonical_reference TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'),
    effective_version TEXT,
    applicable_tag TEXT NOT NULL,
    content TEXT NOT NULL,
    approval_state TEXT NOT NULL DEFAULT 'pending'
        CHECK (approval_state IN ('pending', 'approved', 'conflict', 'retired')),
    indexing_state TEXT NOT NULL DEFAULT 'ineligible'
        CHECK (indexing_state IN ('ineligible', 'indexed')),
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (canonical_reference, effective_version),
    CHECK (
        effective_version IS NOT NULL
        OR (approval_state = 'pending' AND indexing_state = 'ineligible')
    ),
    CHECK (
        approval_state <> 'approved'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND indexing_state = 'indexed')
    )
);