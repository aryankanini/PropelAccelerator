from fastapi import APIRouter

from app.deficiency.application.inventory_query import DeficiencyInventoryQuery
from app.deficiency.contracts.inventory import DeficiencyInventoryResponse


def create_deficiency_inventory_router(
    query: DeficiencyInventoryQuery,
) -> APIRouter:
    router = APIRouter(prefix="/deficiencies", tags=["deficiencies"])

    @router.get(
        "/processing-records/{processing_record_id}",
        response_model=DeficiencyInventoryResponse,
    )
    async def get_inventory(
        processing_record_id: str,
    ) -> DeficiencyInventoryResponse:
        return await query.get(processing_record_id)

    return router