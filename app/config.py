import os

from pydantic import BaseModel, ConfigDict


class ConfigurationError(ValueError):
    """Raised when required runtime configuration is absent."""


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    environment: str
    service_bus_namespace: str | None = None

    @classmethod
    def from_environment(cls) -> "AppSettings":
        environment = os.getenv("CMS2567_ENVIRONMENT")
        if not environment:
            raise ConfigurationError("Missing required configuration: CMS2567_ENVIRONMENT")

        return cls(
            environment=environment,
            service_bus_namespace=os.getenv("CMS2567_SERVICE_BUS_NAMESPACE"),
        )