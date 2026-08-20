from app.rag.context_builder import ContextBuilder


def test_context_builder():
    products = [
        {
            "product_id": "phone_001",
            "name": "Galaxy S24",
            "brand": "Samsung",
            "category": "Smartphone",
            "price": 64999,
            "currency": "INR",
            "rating": 4.5,
            "review_count": 1250,
            "description": "Compact flagship smartphone.",
            "specifications": {
                "RAM": "8GB",
                "Storage": "256GB",
                "Battery": "4000mAh",
            },
        }
    ]

    context = ContextBuilder.build(products)

    assert "Galaxy S24" in context
    assert "Samsung" in context
    assert "4000mAh" in context
    assert "embedding" not in context.lower()