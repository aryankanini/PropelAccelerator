from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.knowledge.application.search_cms_sources import SearchCmsSourcesService
from app.knowledge.contracts.cms_source_inventory import (
    CmsSourceInventoryFilter,
    CmsSourceInventoryPage,
)


def create_cms_source_inventory_router(
    service: SearchCmsSourcesService,
    actor_id_dependency: Callable[[], str],
) -> APIRouter:
    router = APIRouter(prefix='/governance', tags=['governance'])

    @router.get('/cms-sources', response_model=CmsSourceInventoryPage)
    async def search_sources(
        filters: Annotated[CmsSourceInventoryFilter, Depends()],
        actor_id: Annotated[str, Depends(actor_id_dependency)],
    ) -> CmsSourceInventoryPage:
        page = await service.search(actor_id=actor_id, filters=filters)
        if page is None:
            raise HTTPException(status_code=403, detail='Access denied.')
        return page

    return router