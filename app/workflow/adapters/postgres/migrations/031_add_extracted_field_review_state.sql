ALTER TABLE extracted_fields
    ADD COLUMN confidence_state TEXT NOT NULL DEFAULT 'high_confidence',
    ADD COLUMN evidence_locator TEXT,
    ADD COLUMN review_state TEXT NOT NULL DEFAULT 'pending',
    ADD COLUMN reviewer_id TEXT,
    ADD COLUMN reviewed_at TIMESTAMPTZ,
    ADD CONSTRAINT extracted_fields_confidence_state_check
        CHECK (confidence_state IN ('high_confidence', 'low_confidence', 'incomplete')),
    ADD CONSTRAINT extracted_fields_review_state_check
        CHECK (review_state IN ('pending', 'verified'));

CREATE INDEX extracted_fields_processing_record_review_state_index
    ON extracted_fields (processing_record_id, review_state);