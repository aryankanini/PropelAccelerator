import pytest
from fastapi.testclient import TestClient

from app.config import AppSettings, ConfigurationError
from app.main import create_app
from app.modules.deficiency.port import DeficiencyPort
from app.modules.extraction.port import ExtractionPort
from app.modules.intake.port import IntakePort
from app.modules.knowledge.port import GovernancePort, KnowledgePort
from app.modules.poc.port import PocPort
from app.modules.review.port import ReviewPort


def test_create_app_with_valid_settings_exposes_typed_health_response() -> None:
    application = create_app(lambda: AppSettings(environment="test"))

    with TestClient(application) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert application.state.dependencies.enabled_adapters == frozenset()
        assert set(application.state.dependencies.module_ports) == {
            "intake",
            "extraction",
            "deficiency",
            "poc",
            "review",
            "knowledge",
            "governance",
        }


def test_create_app_with_missing_required_configuration_fails_before_requests() -> None:
    application = create_app(lambda: AppSettings.from_environment())

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.delenv("CMS2567_ENVIRONMENT", raising=False)

        with pytest.raises(ConfigurationError, match="CMS2567_ENVIRONMENT") as error:
            with TestClient(application):
                pass

    assert "CMS2567_ENVIRONMENT" in str(error.value)
    assert "=" not in str(error.value)


def test_compose_dependencies_enables_optional_service_bus_only_when_configured() -> None:
    application = create_app(
        lambda: AppSettings(environment="test", service_bus_namespace="namespace")
    )

    with TestClient(application):
        assert application.state.dependencies.enabled_adapters == frozenset({"service_bus"})


def test_module_ports_are_framework_independent_protocols() -> None:
    ports = (
        IntakePort,
        ExtractionPort,
        DeficiencyPort,
        PocPort,
        ReviewPort,
        KnowledgePort,
        GovernancePort,
    )

    assert len(ports) == 7