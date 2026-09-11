from dataclasses import dataclass
from typing import Literal, Protocol


ApprovalStatus = Literal["approved", "rejected"]


@dataclass(frozen=True)
class PocApprovalState:
    poc_id: str
    status: ApprovalStatus
    reviewer_id: str


@dataclass(frozen=True)
class ContentRevision:
    revision_id: str
    poc_id: str
    content: str
    editor_id: str


class ApprovalStateRepository(Protocol):
    async def save(self, approval_state: PocApprovalState) -> None: ...


class AuditRevisionRepository(Protocol):
    async def append(self, revision: ContentRevision) -> None: ...