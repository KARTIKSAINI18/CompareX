from app.database.mongodb import MongoDB
from app.services.comparex_service import CompareXService


def test_get_product():
    database = MongoDB()

    service = CompareXService(
        database=database
    )

    product = service.get_product(
        "phone_001"
    )

    assert product is not None
    assert product["product_id"] == "phone_001"

    service.close()


def test_compare_products():
    database = MongoDB()

    service = CompareXService(
        database=database
    )

    result = service.compare(
        "phone_001",
        "phone_002",
    )

    assert result["product_a"] is not None
    assert result["product_b"] is not None
    assert "top_level" in result
    assert "specifications" in result

    service.close()


def test_search_products():
    database = MongoDB()

    service = CompareXService(
        database=database
    )

    results = service.search(
        "smartphone with a large battery",
        limit=2,
    )

    assert len(results) > 0
    assert len(results) <= 2

    service.close()