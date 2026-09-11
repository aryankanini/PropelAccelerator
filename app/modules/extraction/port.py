from typing import Protocol


class ExtractionPort(Protocol):
    async def handle(self, command: object) -> object: ...