CREATE TABLE processing_records (
    id UUID PRIMARY KEY,
    provider_name TEXT NOT NULL,
    provider_number TEXT NOT NULL,
    survey_date DATE NOT NULL,
    detected_format TEXT NOT NULL,
    processing_state TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE extracted_fields (
    id UUID PRIMARY KEY,
    processing_record_id UUID NOT NULL REFERENCES processing_records(id) ON DELETE RESTRICT,
    field_name TEXT NOT NULL,
    extracted_value TEXT NOT NULL
);

CREATE TABLE deficiencies (
    id UUID PRIMARY KEY,
    processing_record_id UUID NOT NULL REFERENCES processing_records(id) ON DELETE RESTRICT,
    extracted_field_id UUID NOT NULL REFERENCES extracted_fields(id) ON DELETE RESTRICT,
    sod_text TEXT NOT NULL,
    tag TEXT NOT NULL,
    source_evidence TEXT NOT NULL
);

CREATE TABLE plans_of_correction (
    id UUID PRIMARY KEY,
    deficiency_id UUID NOT NULL REFERENCES deficiencies(id) ON DELETE RESTRICT,
    content TEXT NOT NULL,
    validation_result TEXT NOT NULL,
    source_set_version TEXT NOT NULL,
    approval_state TEXT NOT NULL
);

CREATE TABLE content_revisions (
    id UUID PRIMARY KEY,
    extracted_field_id UUID REFERENCES extracted_fields(id) ON DELETE RESTRICT,
    poc_id UUID REFERENCES plans_of_correction(id) ON DELETE RESTRICT,
    content TEXT NOT NULL,
    editor_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK ((extracted_field_id IS NOT NULL) <> (poc_id IS NOT NULL))
);