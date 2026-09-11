from collections.abc import AsyncIterable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StoredObject:
    namespace: str
    object_id: str
    media_type: str
    content_hash: str


class ObjectStoragePort(Protocol):
    async def store(
        self,
        source: AsyncIterable[bytes],
        *,
        object_name: str,
        media_type: str,
    ) -> StoredObject: ...

    async def content_hash_for(self, stored_object: StoredObject) -> str: ...