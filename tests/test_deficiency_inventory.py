from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.deficiency_inventory import create_deficiency_inventory_router
from app.deficiency.application.inventory_query import DeficiencyInventoryQuery
from app.deficiency.domain.segmentation_result import DeficiencyCandidate


class InventoryRepository:
    def __init__(self, candidates: tuple[DeficiencyCandidate, ...]) -> None:
        self._candidates = candidates

    async def list_for_record(
        self,
        processing_record_id: str,
    ) -> tuple[DeficiencyCandidate, ...]:
        return self._candidates


def test_inventory_returns_an_explicit_incomplete_state_without_poc_availability() -> None:
    application = FastAPI()
    application.include_router(
        create_deficiency_inventory_router(DeficiencyInventoryQuery(InventoryRepository(())))
    )

    with TestClient(application) as client:
        response = client.get("/deficiencies/processing-records/record-1")

    assert response.status_code == 200
    assert response.json() == {
        "processing_record_id": "record-1",
        "status": "incomplete",
        "candidates": [],
        "poc_generation_available": False,
    }


def test_inventory_returns_candidate_tag_sod_evidence_and_status() -> None:
    candidate = DeficiencyCandidate(
        deficiency_id="deficiency-1",
        processing_record_id="record-1",
        sod_text="Deficiency text.",
        tag="F600",
        evidence_references=("evidence-1",),
        segmentation_status="confirmed",
    )
    query = DeficiencyInventoryQuery(InventoryRepository((candidate,)))

    result = __import__("asyncio").run(query.get("record-1"))

    assert result.status == "complete"
    assert result.candidates[0].model_dump() == {
        "deficiency_id": "deficiency-1",
        "sod_text": "Deficiency text.",
        "tag": "F600",
        "evidence_references": ("evidence-1",),
        "segmentation_status": "confirmed",
    }