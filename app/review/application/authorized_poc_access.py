from dataclasses import dataclass
from typing import Literal, Protocol


class AuthorizedPocAccessAuthorizer(Protocol):
    async def can_use(self, actor_id: str, poc_id: str) -> bool: ...


@dataclass(frozen=True)
class StoredPoc:
    poc_id: str
    content: str
    approval_state: Literal["pending", "rejected", "approved"]


class AuthorizedPocRepository(Protocol):
    async def get(self, poc_id: str) -> StoredPoc | None: ...


@dataclass(frozen=True)
class AuthorizedPocOutcome:
    status: Literal["available", "access_denied", "not_found", "unavailable"]
    poc: StoredPoc | None = None


class AuthorizedPocAccess:
    def __init__(
        self,
        authorizer: AuthorizedPocAccessAuthorizer,
        repository: AuthorizedPocRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def get(self, *, actor_id: str, poc_id: str) -> AuthorizedPocOutcome:
        if not await self._authorizer.can_use(actor_id, poc_id):
            return AuthorizedPocOutcome(status="access_denied")

        poc = await self._repository.get(poc_id)
        if poc is None:
            return AuthorizedPocOutcome(status="not_found")
        if poc.approval_state != "approved":
            return AuthorizedPocOutcome(status="unavailable")

        return AuthorizedPocOutcome(status="available", poc=poc)