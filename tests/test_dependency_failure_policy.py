from app.processing.application.dependency_failure_policy import (
    DependencyFailurePolicy,
    MAX_RETRY_ATTEMPTS,
    TransientLlmFailure,
    TransientStorageFailure,
)


def test_transient_storage_failure_uses_bounded_exponential_retries() -> None:
    policy = DependencyFailurePolicy()

    first_attempt = policy.evaluate(TransientStorageFailure('storage host unavailable'), 0)
    exhausted_attempt = policy.evaluate(
        TransientStorageFailure('storage host unavailable'), MAX_RETRY_ATTEMPTS
    )

    assert first_attempt.disposition == 'retry'
    assert first_attempt.retry_count == 1
    assert first_attempt.retry_delay_seconds == 1
    assert first_attempt.reason == 'transient_storage_failure'
    assert exhausted_attempt.disposition == 'dead_letter'
    assert 'unavailable' not in exhausted_attempt.reason


def test_only_transient_llm_and_storage_errors_are_retryable() -> None:
    policy = DependencyFailurePolicy()

    llm_outcome = policy.evaluate(TransientLlmFailure('provider response'), 1)
    unknown_outcome = policy.evaluate(ValueError('unsafe internal detail'), 0)

    assert llm_outcome.disposition == 'retry'
    assert llm_outcome.retry_delay_seconds == 2
    assert unknown_outcome.disposition == 'failed'
    assert unknown_outcome.reason == 'dependency_failure'