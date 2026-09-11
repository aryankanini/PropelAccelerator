from typing import Protocol


class PocPort(Protocol):
    async def handle(self, command: object) -> object: ...