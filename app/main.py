from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import AppSettings
from app.modules.deficiency.port import DeficiencyPort
from app.modules.extraction.port import ExtractionPort
from app.modules.intake.port import IntakePort
from app.modules.knowledge.port import GovernancePort, KnowledgePort
from app.modules.poc.port import PocPort
from app.modules.review.port import ReviewPort


class HealthResponse(BaseModel):
    status: Literal["ok"]


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

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    return application


app = create_app()