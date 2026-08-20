from app.rag.service import RAGService


def test_rag_service():
    service = RAGService()

    result = service.answer(
        "Which smartphone has the largest battery?",
        limit=2,
    )

    assert "query" in result
    assert "answer" in result
    assert "products" in result

    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
    assert len(result["products"]) > 0