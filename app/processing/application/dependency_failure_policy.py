from dataclasses import dataclass
from typing import Literal


MAX_RETRY_ATTEMPTS = 3
BASE_RETRY_DELAY_SECONDS = 1


class TransientStorageFailure(Exception):
    """Raised when Blob Storage is temporarily unavailable."""


class TransientLlmFailure(Exception):
    """Raised when an approved LLM provider is temporarily unavailable."""


@dataclass(frozen=True)
class DependencyFailureOutcome:
    category: Literal['storage', 'llm', 'unknown']
    disposition: Literal['retry', 'dead_letter', 'failed']
    retry_count: int
    retry_delay_seconds: int | None
    reason: str


class DependencyFailurePolicy:
    def evaluate(self, error: Exception, retry_count: int) -> DependencyFailureOutcome:
        category = self._classify(error)
        if category == 'unknown':
            return DependencyFailureOutcome(
                category=category,
                disposition='failed',
                retry_count=retry_count,
                retry_delay_seconds=None,
                reason='dependency_failure',
            )

        next_retry_count = retry_count + 1
        if next_retry_count > MAX_RETRY_ATTEMPTS:
            return DependencyFailureOutcome(
                category=category,
                disposition='dead_letter',
                retry_count=retry_count,
                retry_delay_seconds=None,
                reason=f'transient_{category}_retry_exhausted',
            )

        return DependencyFailureOutcome(
            category=category,
            disposition='retry',
            retry_count=next_retry_count,
            retry_delay_seconds=BASE_RETRY_DELAY_SECONDS * (2 ** retry_count),
            reason=f'transient_{category}_failure',
        )

    @staticmethod
    def _classify(error: Exception) -> Literal['storage', 'llm', 'unknown']:
        if isinstance(error, TransientStorageFailure):
            return 'storage'
        if isinstance(error, TransientLlmFailure):
            return 'llm'
        return 'unknown'