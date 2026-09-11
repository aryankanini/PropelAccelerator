import hashlib
from collections.abc import AsyncIterable, AsyncIterator
from typing import Protocol

from app.documents.ports.object_storage import StoredObject


class BlobProperties(Protocol):
    metadata: dict[str, str]


class BlobClient(Protocol):
    async def upload_blob(
        self,
        data: AsyncIterable[bytes],
        *,
        overwrite: bool,
    ) -> None: ...

    async def set_blob_metadata(self, metadata: dict[str, str]) -> None: ...

    async def get_blob_properties(self) -> BlobProperties: ...


class BlobContainerClient(Protocol):
    def get_blob_client(self, blob: str) -> BlobClient: ...


class ContentHasher(Protocol):
    def update(self, data: bytes) -> None: ...


class AzureBlobStorage:
    """Stores content at a non-overwritable blob identity within one container."""

    def __init__(self, namespace: str, container_client: BlobContainerClient) -> None:
        self._namespace = namespace
        self._container_client = container_client

    async def store(
        self,
        source: AsyncIterable[bytes],
        *,
        object_name: str,
        media_type: str,
    ) -> StoredObject:
        content_hasher = hashlib.sha256()
        blob_client = self._container_client.get_blob_client(object_name)
        await blob_client.upload_blob(
            self._hash_stream(source, content_hasher),
            overwrite=False,
        )
        content_hash = content_hasher.hexdigest()
        await blob_client.set_blob_metadata({"content_hash": content_hash})
        return StoredObject(
            namespace=self._namespace,
            object_id=object_name,
            media_type=media_type,
            content_hash=content_hash,
        )

    async def content_hash_for(self, stored_object: StoredObject) -> str:
        blob_client = self._container_client.get_blob_client(stored_object.object_id)
        properties = await blob_client.get_blob_properties()
        return properties.metadata.get("content_hash", "")

    async def _hash_stream(
        self,
        source: AsyncIterable[bytes],
        content_hasher: ContentHasher,
    ) -> AsyncIterator[bytes]:
        async for chunk in source:
            content_hasher.update(chunk)
            yield chunk