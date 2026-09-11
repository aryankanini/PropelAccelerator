ALTER TABLE processing_records
    ADD COLUMN poc_eligibility_state TEXT NOT NULL DEFAULT 'incomplete',
    ADD CONSTRAINT processing_records_poc_eligibility_state_check
        CHECK (poc_eligibility_state IN ('incomplete', 'eligible'));

CREATE TABLE job_attempts (
    processing_record_id UUID NOT NULL REFERENCES processing_records(id) ON DELETE RESTRICT,
    attempt_id UUID NOT NULL,
    correlation_id TEXT NOT NULL,
    state TEXT NOT NULL,
    retry_count INTEGER NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
    failure_reason TEXT,
    PRIMARY KEY (processing_record_id, attempt_id)
);

CREATE TABLE poc_job_deficiency_basis (
    processing_record_id UUID NOT NULL,
    attempt_id UUID NOT NULL,
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    state TEXT NOT NULL DEFAULT 'pending'
        CHECK (state IN ('pending', 'invalidated', 'published')),
    PRIMARY KEY (processing_record_id, attempt_id),
    FOREIGN KEY (processing_record_id, attempt_id)
        REFERENCES job_attempts(processing_record_id, attempt_id) ON DELETE RESTRICT
);

CREATE INDEX poc_job_deficiency_basis_deficiency_id_index
    ON poc_job_deficiency_basis (deficiency_id)
    WHERE state = 'pending';