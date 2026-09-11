import hashlib
from collections.abc import AsyncIterable

import pytest

from app.documents.application.document_provenance import DocumentProvenanceService
from app.documents.ports.object_storage import StoredObject


class InMemoryStorage:
    def __init__(self, returned_hash: str | None = None) -> None:
        self._returned_hash = returned_hash
        self._stored_object: StoredObject | None = None

    async def store(
        self,
        source: AsyncIterable[bytes],
        *,
        object_name: str,
        media_type: str,
    ) -> StoredObject:
        content = b"".join([chunk async for chunk in source])
        content_hash = self._returned_hash or hashlib.sha256(content).hexdigest()
        self._stored_object = StoredObject(
            namespace="evidence",
            object_id=object_name,
            media_type=media_type,
            content_hash=content_hash,
        )
        return self._stored_object

    async def content_hash_for(self, stored_object: StoredObject) -> str:
        return stored_object.content_hash


class InMemoryProvenanceRepository:
    def __init__(self) -> None:
        self.saved: list[StoredObject] = []
        self.failed_processing_records: list[str] = []

    async def save_verified(
        self,
        stored_object: StoredObject,
        *,
        processing_record_id: str,
        extraction_library: str,
        extraction_library_version: str,
    ) -> None:
        self.saved.append(stored_object)

    async def mark_integrity_failed(self, processing_record_id: str) -> None:
        self.failed_processing_records.append(processing_record_id)


async def source_bytes() -> AsyncIterable[bytes]:
    yield b"CMS-"
    yield b"2567"


@pytest.mark.asyncio
async def test_store_verified_document_persists_only_matching_hashes() -> None:
    storage = InMemoryStorage()
    repository = InMemoryProvenanceRepository()
    service = DocumentProvenanceService(storage, repository)

    result = await service.store_verified_document(
        source_bytes(),
        processing_record_id="record-1",
        object_name="survey.pdf",
        media_type="application/pdf",
        extraction_library="pymupdf",
        extraction_library_version="1.24.0",
    )

    assert result.status == "accepted"
    assert result.can_process_downstream is True
    assert result.stored_object is not None
    assert len(repository.saved) == 1


@pytest.mark.asyncio
async def test_store_verified_document_blocks_mismatched_hash_without_persistence() -> None:
    storage = InMemoryStorage(returned_hash="incorrect")
    repository = InMemoryProvenanceRepository()
    service = DocumentProvenanceService(storage, repository)

    result = await service.store_verified_document(
        source_bytes(),
        processing_record_id="record-1",
        object_name="survey.pdf",
        media_type="application/pdf",
        extraction_library="pymupdf",
        extraction_library_version="1.24.0",
    )

    assert result.status == "failed"
    assert result.can_process_downstream is False
    assert result.error_code == "content_hash_mismatch"
    assert repository.saved == []
    assert repository.failed_processing_records == ["record-1"]