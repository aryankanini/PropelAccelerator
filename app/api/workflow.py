from datetime import UTC, date, datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field


class UploadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str = Field(min_length=1, max_length=200)
    format: str = Field(pattern="^(Format 1|Format 2|Open-source format)$")


class FieldDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str = Field(min_length=1, max_length=2_000)


class SourceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=300)
    effective_date: date


class WorkflowStore:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}
        self.sources = [
            {"id": "source-f689", "name": "CMS guidance for F689", "effective_date": "2026-07-01", "status": "Approved"},
            {"id": "source-f686", "name": "Tag definition F686", "effective_date": "2026-06-15", "status": "Approved"},
        ]
        self._seed_record()

    def _seed_record(self) -> None:
        record_id = "riverside-2026"
        self.records[record_id] = {
            "id": record_id,
            "provider": "Riverside Nursing Center",
            "format": "Format 2",
            "fields": {"Provider name": "Riverside Nursing Center", "Provider number": "145672", "Survey date": "08/12/2026", "Tag": "F689"},
            "verified_fields": set(),
            "deficiencies": [
                {"id": "f689", "tag": "F689", "title": "Free of accidents hazards/supervision", "confidence": "High"},
                {"id": "f686", "tag": "F686", "title": "Treatment/services to prevent healing", "confidence": "Needs staff confirmation"},
            ],
            "poc": {"content": "The facility will complete immediate safety rounds, document findings, educate assigned staff, and audit compliance weekly.", "state": "pending"},
        }

    def get_record(self, record_id: str) -> dict[str, object]:
        record = self.records.get(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Processing record not found.")
        return record


def create_workflow_router(store: WorkflowStore) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["workflow"])

    @router.get("/queue")
    async def get_queue() -> dict[str, object]:
        records = []
        for record in store.records.values():
            verified_fields = record["verified_fields"]
            poc = record["poc"]
            if len(verified_fields) < len(record["fields"]):
                stage, action, destination = "Fields need verification", "Review fields", "extraction-review"
            elif poc["state"] != "approved":
                stage, action, destination = "POC approval blocked", "Review POC", "poc-review"
            else:
                continue
            records.append({"id": record["id"], "provider": record["provider"], "format": record["format"], "stage": stage, "action": action, "destination": destination})
        return {"records": records}

    @router.post("/records", status_code=201)
    async def create_record(request: UploadRequest) -> dict[str, str]:
        record_id = str(uuid4())
        store.records[record_id] = {
            "id": record_id,
            "provider": request.provider,
            "format": request.format,
            "fields": {"Provider name": request.provider, "Provider number": "Requires review", "Survey date": "Requires review", "Tag": "Requires review"},
            "verified_fields": set(),
            "deficiencies": [],
            "poc": {"content": "", "state": "blocked"},
        }
        return {"record_id": record_id}

    @router.get("/records/{record_id}")
    async def get_record(record_id: str) -> dict[str, object]:
        record = store.get_record(record_id)
        return {"id": record["id"], "provider": record["provider"], "format": record["format"]}

    @router.get("/records/{record_id}/fields")
    async def get_fields(record_id: str) -> dict[str, object]:
        record = store.get_record(record_id)
        verified_fields = record["verified_fields"]
        return {"fields": [{"name": name, "value": value, "verified": name in verified_fields} for name, value in record["fields"].items()]}

    @router.put("/records/{record_id}/fields/{field_name}")
    async def verify_field(record_id: str, field_name: str, request: FieldDecisionRequest) -> dict[str, object]:
        record = store.get_record(record_id)
        fields = record["fields"]
        if field_name not in fields:
            raise HTTPException(status_code=404, detail="Field not found.")
        fields[field_name] = request.value
        record["verified_fields"].add(field_name)
        return {"field_name": field_name, "verified": True}

    @router.get("/records/{record_id}/deficiencies")
    async def get_deficiencies(record_id: str) -> dict[str, object]:
        record = store.get_record(record_id)
        return {"deficiencies": record["deficiencies"]}

    @router.post("/records/{record_id}/poc")
    async def save_poc(record_id: str, request: FieldDecisionRequest) -> dict[str, str]:
        record = store.get_record(record_id)
        if not record["deficiencies"]:
            raise HTTPException(status_code=422, detail="Confirm a deficiency before drafting a POC.")
        record["poc"] = {"content": request.value, "state": "pending"}
        return {"state": "pending"}

    @router.get("/records/{record_id}/poc")
    async def get_poc(record_id: str) -> dict[str, object]:
        record = store.get_record(record_id)
        return {"content": record["poc"]["content"], "state": record["poc"]["state"], "sources": store.sources}

    @router.post("/records/{record_id}/poc/approve")
    async def approve_poc(record_id: str) -> dict[str, str]:
        record = store.get_record(record_id)
        if len(record["verified_fields"]) < len(record["fields"]) or not record["poc"]["content"]:
            raise HTTPException(status_code=422, detail="All fields and a POC draft must be reviewed before approval.")
        record["poc"]["state"] = "approved"
        return {"state": "approved", "approved_at": datetime.now(UTC).isoformat()}

    @router.get("/governance/sources")
    async def get_sources() -> dict[str, object]:
        return {"sources": store.sources}

    @router.post("/governance/sources", status_code=201)
    async def add_source(request: SourceRequest) -> dict[str, object]:
        source = {"id": str(uuid4()), "name": request.name, "effective_date": request.effective_date.isoformat(), "status": "Pending review"}
        store.sources.append(source)
        return source

    @router.get("/outcomes")
    async def get_outcomes() -> dict[str, object]:
        return {"metrics": [{"name": "Field accuracy", "value": "96%"}, {"name": "SOD recall", "value": "95%"}, {"name": "Time reduction", "value": "52%"}], "coverage": [{"format": "Format 1", "samples": 12, "baseline": "42 min", "approval_rate": "100%"}, {"format": "Format 2", "samples": 14, "baseline": "45 min", "approval_rate": "100%"}, {"format": "Open-source", "samples": 10, "baseline": "39 min", "approval_rate": "100%"}]}

    return router