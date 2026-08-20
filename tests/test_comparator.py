from app.comparison.comparator import ProductComparator


def test_product_comparator():
    galaxy = {
        "name": "Galaxy S24",
        "price": 64999,
        "rating": 4.5,
        "review_count": 1250,
        "specifications": {
            "RAM": "8GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Battery": "4000mAh",
        },
    }

    oneplus = {
        "name": "OnePlus 12",
        "price": 59999,
        "rating": 4.4,
        "review_count": 980,
        "specifications": {
            "RAM": "12GB",
            "Storage": "256GB",
            "Processor": "Snapdragon 8 Gen 3",
            "Battery": "5400mAh",
        },
    }

    result = ProductComparator.compare(
        galaxy,
        oneplus,
    )

    assert result["product_a"] == "Galaxy S24"
    assert result["product_b"] == "OnePlus 12"

    assert result["top_level"]["price"]["winner"] == "OnePlus 12"

    assert (
        result["specifications"]["Storage"]["same"]
        is True
    )

    assert (
        result["specifications"]["Battery"]["same"]
        is False
    )