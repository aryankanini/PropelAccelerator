import hashlib
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Literal, Protocol

from app.documents.ports.object_storage import ObjectStoragePort, StoredObject


class DocumentProvenanceRepository(Protocol):
    async def save_verified(
        self,
        stored_object: StoredObject,
        *,
        processing_record_id: str,
        extraction_library: str,
        extraction_library_version: str,
    ) -> None: ...

    async def mark_integrity_failed(self, processing_record_id: str) -> None: ...


class ContentHasher(Protocol):
    def update(self, data: bytes) -> None: ...


@dataclass(frozen=True)
class UploadResult:
    status: Literal["accepted", "failed"]
    can_process_downstream: bool
    stored_object: StoredObject | None = None
    error_code: str | None = None


class DocumentProvenanceService:
    def __init__(
        self,
        storage: ObjectStoragePort,
        repository: DocumentProvenanceRepository,
    ) -> None:
        self._storage = storage
        self._repository = repository

    async def store_verified_document(
        self,
        source: AsyncIterable[bytes],
        *,
        processing_record_id: str,
        object_name: str,
        media_type: str,
        extraction_library: str,
        extraction_library_version: str,
        expected_content_hash: str | None = None,
    ) -> UploadResult:
        content_hasher = hashlib.sha256()
        stored_object = await self._storage.store(
            self._hash_stream(source, content_hasher),
            object_name=object_name,
            media_type=media_type,
        )
        computed_hash = content_hasher.hexdigest()
        stored_hash = await self._storage.content_hash_for(stored_object)

        if (
            stored_object.content_hash != computed_hash
            or stored_hash != computed_hash
            or (
                expected_content_hash is not None
                and expected_content_hash != computed_hash
            )
        ):
            await self._repository.mark_integrity_failed(processing_record_id)
            return UploadResult(
                status="failed",
                can_process_downstream=False,
                error_code="content_hash_mismatch",
            )

        await self._repository.save_verified(
            stored_object,
            processing_record_id=processing_record_id,
            extraction_library=extraction_library,
            extraction_library_version=extraction_library_version,
        )
        return UploadResult(
            status="accepted",
            can_process_downstream=True,
            stored_object=stored_object,
        )

    async def _hash_stream(
        self,
        source: AsyncIterable[bytes],
        content_hasher: ContentHasher,
    ) -> AsyncIterator[bytes]:
        async for chunk in source:
            content_hasher.update(chunk)
            yield chunk