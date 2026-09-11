CREATE TABLE ai_evaluation_runs (
    id UUID PRIMARY KEY,
    test_set_version TEXT NOT NULL,
    candidate_identity TEXT NOT NULL,
    release_gate_state TEXT NOT NULL DEFAULT 'blocked'
        CHECK (release_gate_state IN ('blocked', 'eligible')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ai_evaluation_results (
    evaluation_run_id UUID NOT NULL REFERENCES ai_evaluation_runs(id) ON DELETE RESTRICT,
    category TEXT NOT NULL CHECK (category IN (
        'extraction', 'sod_recall', 'citation_support', 'poc_quality', 'refusal',
        'conditional_fields'
    )),
    score NUMERIC(5, 4) NOT NULL CHECK (score >= 0 AND score <= 1),
    PRIMARY KEY (evaluation_run_id, category)
);