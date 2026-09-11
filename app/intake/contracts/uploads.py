from dataclasses import dataclass


@dataclass(frozen=True)
class UploadAcknowledgement:
    processing_record_id: str