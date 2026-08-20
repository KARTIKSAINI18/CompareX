from app.models.requirements import ProductRequirements
from app.services.product_matcher import ProductMatcher
from app.services.comparison_engine import ComparisonEngine


def main():
    query = "smartphone with a large battery"

    requirements = ProductRequirements(
        preferences=["large battery"]
    )

    matcher = ProductMatcher()
    comparator = ComparisonEngine()

    print()
    print("=" * 80)
    print("COMPAREX STRUCTURED COMPARISON TEST")
    print("=" * 80)

    candidates = matcher.match(
        query=query,
        requirements=requirements,
        candidate_limit=30,
    )

    print()
    print(
        f"Candidates retrieved: {len(candidates)}"
    )

    result = comparator.compare(
        products=candidates,
        field="battery",
        direction="max",
    )

    print()
    print("=" * 80)
    print("BATTERY COMPARISON")
    print("=" * 80)

    for product in result["products"]:
        print()
        print(
            f"{product['name']}"
        )
        print(
            f"   Battery: {product['value']} mAh"
        )

    print()
    print("=" * 80)
    print("WINNER")
    print("=" * 80)

    winner = result["winner"]

    if winner:
        print()
        print(
            f"Product : {winner['name']}"
        )
        print(
            f"Battery : {winner['value']} mAh"
        )

    print()
    print("=" * 80)
    print("COMPARISON TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()