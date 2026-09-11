from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PocElementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    content: str = Field(min_length=1)
    evidence_source_ids: tuple[str, ...] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class PocResponseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["completed", "refused"]
    elements: tuple[PocElementResponse, ...] = ()
    refusal_reason: str | None = None
    missing_elements: tuple[str, ...] = ()

    @model_validator(mode="after")
    def require_content_or_refusal_reason(self) -> "PocResponseSchema":
        if self.status == "completed" and not self.elements:
            raise ValueError("Completed POC responses must include at least one element.")
        if self.status == "refused" and not self.refusal_reason:
            raise ValueError("Refused POC responses must include a refusal reason.")
        return self