from app.database.repository import ProductRepository
from app.database.mongodb import MongoDB


def test_product_repository():
    database = MongoDB()
    repository = ProductRepository(database)

    product = {
        "product_id": "test_product",
        "name": "Test Product",
        "brand": "CompareX",
        "category": "Test",
        "description": "Test product for repository testing.",
        "specifications": {},
        "price": 100.0,
        "currency": "INR",
        "rating": 5.0,
        "review_count": 1,
        "source": "test",
        "searchable_text": "Test product",
        "embedding": [0.1] * 384,
    }

    repository.upsert_product(product)

    stored_product = repository.get_product("test_product")

    assert stored_product is not None
    assert stored_product["name"] == "Test Product"
    assert len(stored_product["embedding"]) == 384

    repository.collection.delete_one(
        {"product_id": "test_product"}
    )

    database.close()