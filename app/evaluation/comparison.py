from typing import Any


class ComparisonEvaluator:
    """Evaluator for deterministic product comparisons."""

    @staticmethod
    def evaluate(
        comparison: dict[str, Any],
        expected_winners: dict[str, str],
    ) -> dict[str, Any]:
        results = {}

        correct = 0
        total = len(expected_winners)

        for field, expected_winner in expected_winners.items():
            actual = comparison["top_level"].get(
                field,
                {},
            ).get("winner")

            is_correct = actual == expected_winner

            results[field] = {
                "expected": expected_winner,
                "actual": actual,
                "correct": is_correct,
            }

            if is_correct:
                correct += 1

        accuracy = (
            correct / total
            if total
            else 0.0
        )

        return {
            "correct": correct,
            "total": total,
            "accuracy": accuracy,
            "fields": results,
        }