ALTER TABLE processing_records
    ADD COLUMN integrity_state TEXT NOT NULL DEFAULT 'verified',
    ADD CONSTRAINT processing_records_integrity_state_check
        CHECK (integrity_state IN ('verified', 'failed')),
    ADD CONSTRAINT processing_records_failed_integrity_check
        CHECK (integrity_state <> 'failed' OR processing_state = 'failed');

CREATE TABLE source_documents (
    id UUID PRIMARY KEY,
    processing_record_id UUID NOT NULL REFERENCES processing_records(id) ON DELETE RESTRICT,
    storage_namespace TEXT NOT NULL,
    object_identity TEXT NOT NULL,
    media_type TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'),
    extraction_library TEXT NOT NULL,
    extraction_library_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (storage_namespace, object_identity)
);

CREATE FUNCTION reject_source_document_provenance_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.storage_namespace <> OLD.storage_namespace
       OR NEW.object_identity <> OLD.object_identity
       OR NEW.media_type <> OLD.media_type
       OR NEW.content_hash <> OLD.content_hash THEN
        RAISE EXCEPTION 'Source document provenance is immutable';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER source_documents_provenance_immutable
BEFORE UPDATE ON source_documents
FOR EACH ROW EXECUTE FUNCTION reject_source_document_provenance_changes();