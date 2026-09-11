CREATE TABLE deficiency_corrections (
    id UUID PRIMARY KEY,
    processing_record_id UUID NOT NULL REFERENCES processing_records(id) ON DELETE RESTRICT,
    operation TEXT NOT NULL CHECK (operation IN ('merge', 'split', 'create')),
    actor_id TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    correlation_id TEXT NOT NULL,
    source_boundary TEXT,
    CHECK (operation <> 'split' OR source_boundary IS NOT NULL)
);

CREATE TABLE deficiency_correction_sources (
    correction_id UUID NOT NULL REFERENCES deficiency_corrections(id) ON DELETE RESTRICT,
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    PRIMARY KEY (correction_id, deficiency_id)
);

CREATE FUNCTION reject_deficiency_correction_changes()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Deficiency correction history is immutable';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER deficiency_corrections_immutable
BEFORE UPDATE OR DELETE ON deficiency_corrections
FOR EACH ROW EXECUTE FUNCTION reject_deficiency_correction_changes();