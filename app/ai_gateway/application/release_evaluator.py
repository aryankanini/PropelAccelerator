from app.ai_gateway.domain.evaluation_contract import (
    REQUIRED_EVALUATION_CATEGORIES,
    EvaluationResult,
    ReleaseDecision,
)


class ReleaseEvaluator:
    def evaluate(
        self,
        *,
        test_set_version: str,
        candidate_identity: str,
        results: tuple[EvaluationResult, ...],
    ) -> ReleaseDecision:
        completed = {result.category for result in results}
        missing = tuple(
            category
            for category in REQUIRED_EVALUATION_CATEGORIES
            if category not in completed
        )
        return ReleaseDecision(
            status="blocked" if missing else "eligible",
            missing_categories=missing,
            test_set_version=test_set_version,
            candidate_identity=candidate_identity,
        )