from app.evaluation.comparison import ComparisonEvaluator
from app.evaluation.retrieval import RetrievalEvaluator


def test_retrieval_evaluator():
    results = [
        {"product_id": "phone_002"},
        {"product_id": "phone_001"},
    ]

    evaluation = RetrievalEvaluator.evaluate(
        results=results,
        expected_product_ids={"phone_002"},
    )

    assert evaluation["retrieved_count"] == 2
    assert evaluation["relevant_retrieved"] == 1
    assert evaluation["precision"] == 0.5
    assert evaluation["recall"] == 1.0


def test_comparison_evaluator():
    comparison = {
        "top_level": {
            "price": {
                "product_a": 64999,
                "product_b": 59999,
                "winner": "OnePlus 12",
            },
            "rating": {
                "product_a": 4.5,
                "product_b": 4.4,
                "winner": "Galaxy S24",
            },
        }
    }

    evaluation = ComparisonEvaluator.evaluate(
        comparison=comparison,
        expected_winners={
            "price": "OnePlus 12",
            "rating": "Galaxy S24",
        },
    )

    assert evaluation["correct"] == 2
    assert evaluation["total"] == 2
    assert evaluation["accuracy"] == 1.0