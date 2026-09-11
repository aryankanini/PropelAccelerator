from typing import Protocol


class IntakePort(Protocol):
    async def handle(self, command: object) -> object: ...