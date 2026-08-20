from typing import Any


class RetrievalEvaluator:
    """Lightweight evaluator for semantic retrieval."""

    @staticmethod
    def evaluate(
        results: list[dict[str, Any]],
        expected_product_ids: set[str],
    ) -> dict[str, Any]:
        retrieved_ids = {
            result.get("product_id")
            for result in results
        }

        retrieved_ids.discard(None)

        relevant_retrieved = (
            retrieved_ids & expected_product_ids
        )

        precision = (
            len(relevant_retrieved) / len(retrieved_ids)
            if retrieved_ids
            else 0.0
        )

        recall = (
            len(relevant_retrieved) / len(expected_product_ids)
            if expected_product_ids
            else 0.0
        )

        return {
            "retrieved_count": len(retrieved_ids),
            "relevant_retrieved": len(relevant_retrieved),
            "precision": precision,
            "recall": recall,
        }