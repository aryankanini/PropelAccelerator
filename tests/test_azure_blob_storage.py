import hashlib
from collections.abc import AsyncIterable
from dataclasses import dataclass

import pytest

from app.documents.adapters.azure_blob_storage import AzureBlobStorage


@dataclass
class FakeProperties:
    metadata: dict[str, str]


class FakeBlobClient:
    def __init__(self) -> None:
        self.content = b""
        self.metadata: dict[str, str] = {}
        self.overwrite: bool | None = None

    async def upload_blob(
        self,
        data: AsyncIterable[bytes],
        *,
        overwrite: bool,
    ) -> None:
        self.content = b"".join([chunk async for chunk in data])
        self.overwrite = overwrite

    async def set_blob_metadata(self, metadata: dict[str, str]) -> None:
        self.metadata = metadata

    async def get_blob_properties(self) -> FakeProperties:
        return FakeProperties(metadata=self.metadata)


class FakeContainerClient:
    def __init__(self) -> None:
        self.blobs: dict[str, FakeBlobClient] = {}

    def get_blob_client(self, blob: str) -> FakeBlobClient:
        return self.blobs.setdefault(blob, FakeBlobClient())


async def source_bytes() -> AsyncIterable[bytes]:
    yield b"survey"


@pytest.mark.asyncio
async def test_store_creates_non_overwritable_blob_with_hash_metadata() -> None:
    container = FakeContainerClient()
    storage = AzureBlobStorage("evidence", container)

    stored_object = await storage.store(
        source_bytes(),
        object_name="record-1/survey.pdf",
        media_type="application/pdf",
    )

    blob = container.blobs[stored_object.object_id]
    assert blob.overwrite is False
    assert stored_object.content_hash == hashlib.sha256(b"survey").hexdigest()
    assert await storage.content_hash_for(stored_object) == stored_object.content_hash