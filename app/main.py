from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import MappingProxyType
from pathlib import Path
from typing import Literal, Mapping

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.api.workflow import WorkflowStore, create_workflow_router
from app.config import AppSettings
from app.modules.deficiency.port import DeficiencyPort
from app.modules.extraction.port import ExtractionPort
from app.modules.intake.port import IntakePort
from app.modules.knowledge.port import GovernancePort, KnowledgePort
from app.modules.poc.port import PocPort
from app.modules.review.port import ReviewPort


class HealthResponse(BaseModel):
    status: Literal["ok"]


class ProcessingQueueRecord(BaseModel):
    provider: str
    format: str
    stage: str
    stage_key: Literal["verification", "blocked"]
    action: str
    review_url: str


class ProcessingQueueResponse(BaseModel):
    records: tuple[ProcessingQueueRecord, ...]


FRONTEND_PAGE = Path(__file__).parent / "frontend" / "processing-queue.html"
WORKFLOW_FRONTEND_PAGE = Path(__file__).parent / "frontend" / "workflow.html"
WIREFRAME_DIRECTORY = (
    Path(__file__).parent.parent / ".propel" / "context" / "wireframes" / "Lo-Fi"
)
PROCESSING_QUEUE_RECORDS = (
    ProcessingQueueRecord(
        provider="Riverside Nursing Center",
        format="Format 2",
        stage="Fields need verification",
        stage_key="verification",
        action="Review fields",
        review_url="/wireframes/wireframe-SCR-003-extraction-review.html",
    ),
    ProcessingQueueRecord(
        provider="Oak Meadows Care",
        format="Format 1",
        stage="POC approval blocked",
        stage_key="blocked",
        action="Review POC",
        review_url="/wireframes/wireframe-SCR-006-poc-review-approval.html",
    ),
)


MODULE_PORTS: Mapping[str, type[object]] = MappingProxyType(
    {
        "intake": IntakePort,
        "extraction": ExtractionPort,
        "deficiency": DeficiencyPort,
        "poc": PocPort,
        "review": ReviewPort,
        "knowledge": KnowledgePort,
        "governance": GovernancePort,
    }
)


@dataclass(frozen=True)
class ApplicationDependencies:
    settings: AppSettings
    enabled_adapters: frozenset[str]
    module_ports: Mapping[str, type[object]]


SettingsLoader = Callable[[], AppSettings]


def compose_dependencies(settings: AppSettings) -> ApplicationDependencies:
    enabled_adapters = frozenset(
        {"service_bus"} if settings.service_bus_namespace else set()
    )
    return ApplicationDependencies(
        settings=settings,
        enabled_adapters=enabled_adapters,
        module_ports=MODULE_PORTS,
    )


def create_app(settings_loader: SettingsLoader = AppSettings.from_environment) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        settings = settings_loader()
        application.state.dependencies = compose_dependencies(settings)
        yield

    application = FastAPI(title="CMS-2567 Compliance Assistant", lifespan=lifespan)
    application.include_router(create_workflow_router(WorkflowStore()))
    application.mount(
        "/wireframes",
        StaticFiles(directory=WIREFRAME_DIRECTORY),
        name="wireframes",
    )

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @application.get("/processing-queue", response_model=ProcessingQueueResponse)
    async def get_processing_queue() -> ProcessingQueueResponse:
        return ProcessingQueueResponse(records=PROCESSING_QUEUE_RECORDS)

    @application.get("/", include_in_schema=False)
    @application.get("/{screen}", include_in_schema=False)
    async def get_workflow_page(screen: str = "queue") -> FileResponse:
        if screen not in {
            "queue", "upload", "extraction-review", "deficiencies", "poc-draft",
            "poc-review", "export", "governance", "outcomes", "upload-error",
        }:
            return FileResponse(FRONTEND_PAGE)
        return FileResponse(WORKFLOW_FRONTEND_PAGE)

    return application


app = create_app()