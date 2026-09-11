from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.knowledge.application.approve_cms_source import ApproveCmsSourceService
from app.knowledge.contracts.cms_source_approval import (
    CmsSourceApprovalCommand,
    CmsSourceApprovalResult,
)


def create_cms_source_approval_router(
    service: ApproveCmsSourceService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix='/governance', tags=['governance'])

    @router.post(
        '/cms-sources/{source_id}/approval', response_model=CmsSourceApprovalResult
    )
    async def approve_source(
        source_id: str,
        request: CmsSourceApprovalCommand,
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> CmsSourceApprovalResult:
        if source_id != request.source_id:
            raise HTTPException(status_code=422, detail='Source identifiers must match.')

        outcome = await service.approve(
            actor_id=actor_id, source_id=source_id, occurred_at=request.occurred_at
        )
        if outcome.status == 'access_denied':
            raise HTTPException(status_code=403, detail='Access denied.')
        if outcome.status == 'not_found':
            raise HTTPException(status_code=404, detail='CMS source not found.')
        if outcome.status == 'incomplete':
            raise HTTPException(status_code=422, detail='CMS source metadata is incomplete.')

        return CmsSourceApprovalResult(
            source_id=source_id,
            status='approved',
            approver_id=outcome.approver_id,
            approved_at=outcome.approved_at,
        )

    return router