from typing import Protocol


class KnowledgePort(Protocol):
    async def handle(self, command: object) -> object: ...


class GovernancePort(Protocol):
    async def handle(self, command: object) -> object: ...