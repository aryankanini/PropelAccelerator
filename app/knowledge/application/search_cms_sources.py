from typing import Protocol

from app.knowledge.contracts.cms_source_inventory import (
    CmsSourceInventoryFilter,
    CmsSourceInventoryItem,
    CmsSourceInventoryPage,
)


class CmsSourceInventoryAuthorizer(Protocol):
    async def can_view_sources(self, actor_id: str) -> bool: ...


class CmsSourceInventoryRepository(Protocol):
    async def search(self, filters: CmsSourceInventoryFilter) -> tuple[CmsSourceInventoryItem, ...]: ...


class SearchCmsSourcesService:
    def __init__(
        self,
        authorizer: CmsSourceInventoryAuthorizer,
        repository: CmsSourceInventoryRepository,
    ) -> None:
        self._authorizer = authorizer
        self._repository = repository

    async def search(
        self, *, actor_id: str, filters: CmsSourceInventoryFilter
    ) -> CmsSourceInventoryPage | None:
        if not await self._authorizer.can_view_sources(actor_id):
            return None
        return CmsSourceInventoryPage(
            items=await self._repository.search(filters),
            limit=filters.limit,
            offset=filters.offset,
        )