from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionCommand:
    job_id: str
    processing_record_id: str
    correlation_id: str