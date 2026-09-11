from typing import Protocol

from app.intake.domain.format_classifier import ClassificationResult, FormatClassifier


class ClassificationRecordRepository(Protocol):
    async def set_classification(
        self,
        *,
        processing_record_id: str,
        detected_format: str | None,
        processing_state: str,
    ) -> None: ...


class UploadClassificationService:
    def __init__(
        self,
        classifier: FormatClassifier,
        repository: ClassificationRecordRepository,
    ) -> None:
        self._classifier = classifier
        self._repository = repository

    async def classify(self, *, processing_record_id: str, content: str) -> ClassificationResult:
        result = self._classifier.classify(content)
        await self._repository.set_classification(
            processing_record_id=processing_record_id,
            detected_format=result.detected_format,
            processing_state=result.processing_state,
        )
        return result