from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.workflow import WorkflowStore, create_workflow_router


def test_workflow_api_requires_field_review_before_poc_approval() -> None:
    application = FastAPI()
    application.include_router(create_workflow_router(WorkflowStore()))

    with TestClient(application) as client:
        queue = client.get("/api/queue")
        record_id = queue.json()["records"][0]["id"]
        blocked = client.post(f"/api/records/{record_id}/poc/approve")
        fields = client.get(f"/api/records/{record_id}/fields").json()["fields"]
        for field in fields:
            response = client.put(
                f"/api/records/{record_id}/fields/{field['name']}",
                json={"value": field["value"]},
            )
            assert response.status_code == 200
        approved = client.post(f"/api/records/{record_id}/poc/approve")

    assert queue.status_code == 200
    assert blocked.status_code == 422
    assert approved.status_code == 200
    assert approved.json()["state"] == "approved"


def test_workflow_api_creates_pending_record_and_pending_source() -> None:
    application = FastAPI()
    application.include_router(create_workflow_router(WorkflowStore()))

    with TestClient(application) as client:
        record = client.post(
            "/api/records",
            json={"provider": "Oak Meadows Care", "format": "Format 1"},
        )
        source = client.post(
            "/api/governance/sources",
            json={"name": "CMS guidance for F600", "effective_date": "2026-09-15"},
        )

    assert record.status_code == 201
    assert source.status_code == 201
    assert source.json()["status"] == "Pending review"