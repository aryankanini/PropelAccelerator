from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ContentInspectionResult:
    is_supported: bool


class ContentInspector:
    """Checks media signatures without opening or executing uploaded content."""

    def __init__(self, supported_signatures: Mapping[str, bytes]) -> None:
        self._supported_signatures = supported_signatures

    def inspect(self, content: bytes, declared_media_type: str) -> ContentInspectionResult:
        signature = self._supported_signatures.get(declared_media_type)
        return ContentInspectionResult(
            is_supported=bool(content) and signature is not None and content.startswith(signature)
        )