from app.database.mongodb import MongoDB
from app.retrieval.vector_search import VectorSearchService


def test_vector_search():
    database = MongoDB()

    service = VectorSearchService(
        database=database
    )

    results = service.search(
        "smartphone with a large battery",
        limit=2,
    )

    assert len(results) > 0
    assert len(results) <= 2

    for result in results:
        assert "product_id" in result
        assert "name" in result
        assert "score" in result

    database.close()