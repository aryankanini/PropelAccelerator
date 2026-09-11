from typing import Protocol


class DeficiencyPort(Protocol):
    async def handle(self, command: object) -> object: ...