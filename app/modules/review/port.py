from typing import Protocol


class ReviewPort(Protocol):
    async def handle(self, command: object) -> object: ...