from app.models.requirements import ProductRequirements
from app.services.product_matcher import ProductMatcher


def main():
    matcher = ProductMatcher()

    tests = [
        (
            "Samsung Android phone with at least 8GB RAM",
            ProductRequirements(
                brand="samsung",
                platform="android",
                min_ram_gb=8,
            ),
        ),
        (
            "phone with at least 5000mAh battery",
            ProductRequirements(
                min_battery_mah=5000,
            ),
        ),
        (
            "smartphone rated at least 4 stars",
            ProductRequirements(
                min_rating=4,
            ),
        ),
    ]

    for query, requirements in tests:
        print()
        print("=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        print()
        print("REQUIREMENTS:")
        print(requirements.model_dump())

        results = matcher.match(
            query=query,
            requirements=requirements,
            candidate_limit=30,
        )

        print()
        print(
            f"MATCHING PRODUCTS: {len(results)}"
        )

        for index, product in enumerate(
            results[:10],
            start=1,
        ):
            print()
            print(
                f"{index}. {product.get('name')}"
            )
            print(
                f"   Brand  : {product.get('brand')}"
            )
            print(
                f"   Price  : {product.get('price')}"
            )
            print(
                f"   Rating : {product.get('rating')}"
            )
            print(
                f"   Score  : {product.get('score')}"
            )

    print()
    print("=" * 80)
    print("PRODUCT MATCHER TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()