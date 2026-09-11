ALTER TABLE deficiencies
    ADD COLUMN segmentation_status TEXT NOT NULL DEFAULT 'correction_required',
    ADD CONSTRAINT deficiencies_segmentation_status_check
        CHECK (segmentation_status IN ('confirmed', 'correction_required'));

CREATE TABLE deficiency_evidence_links (
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    evidence_reference TEXT NOT NULL,
    PRIMARY KEY (deficiency_id, evidence_reference)
);

CREATE INDEX deficiency_evidence_links_deficiency_id_index
    ON deficiency_evidence_links (deficiency_id);