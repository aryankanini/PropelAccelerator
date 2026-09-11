from enum import StrEnum


class SchedulingState(StrEnum):
    PENDING = "pending"
    PUBLISHED = "published"
    RETRYABLE = "retryable"