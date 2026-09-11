from dataclasses import dataclass

from app.poc.domain.grounded_request import GroundedPocRequest, GroundedRequestOutcome


@dataclass(frozen=True)
class ModelInferenceRequest:
    deficiency_id: str
    tag: str
    deficiency_text: str
    source_set_version: str
    sources: tuple[tuple[str, str, str], ...]


class GroundedRequestGuard:
    def create(self, request: GroundedPocRequest) -> GroundedRequestOutcome | ModelInferenceRequest:
        if not request.sources or any(
            not source.approved or not source.source_id or not source.version
            for source in request.sources
        ):
            return GroundedRequestOutcome(status="blocked", reason="no_approved_sources")

        return ModelInferenceRequest(
            deficiency_id=request.deficiency.deficiency_id,
            tag=request.deficiency.tag,
            deficiency_text=request.deficiency.sod_text,
            source_set_version=request.source_set_version,
            sources=tuple(
                (source.source_id, source.version, source.content)
                for source in request.sources
            ),
        )