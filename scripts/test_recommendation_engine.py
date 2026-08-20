from app.models.requirements import ProductRequirements
from app.services.product_matcher import ProductMatcher
from app.services.recommendation_engine import (
    RecommendationEngine,
)


def main():
    query = (
        "Samsung Android phone with "
        "large battery and good camera"
    )

    requirements = ProductRequirements(
        brand="samsung",
        platform="android",
        camera_preference="good",
        preferences=[
            "large battery"
        ],
    )

    matcher = ProductMatcher()
    engine = RecommendationEngine()

    print()
    print("=" * 80)
    print("COMPAREX RECOMMENDATION TEST")
    print("=" * 80)

    print()
    print("QUERY:")
    print(query)

    print()
    print("REQUIREMENTS:")
    print(requirements.model_dump())

    candidates = matcher.match(
        query=query,
        requirements=requirements,
        candidate_limit=30,
    )

    print()
    print(
        f"Matching candidates: "
        f"{len(candidates)}"
    )

    ranked = engine.rank(
        candidates,
        requirements,
    )

    print()
    print("=" * 80)
    print("RANKED RECOMMENDATIONS")
    print("=" * 80)

    for index, product in enumerate(
        ranked[:10],
        start=1,
    ):
        print()
        print(
            f"{index}. {product.get('name')}"
        )
        print(
            f"   Brand               : "
            f"{product.get('brand')}"
        )
        print(
            f"   Price               : "
            f"{product.get('price')}"
        )
        print(
            f"   Rating              : "
            f"{product.get('rating')}"
        )
        print(
            f"   Vector score        : "
            f"{product.get('score')}"
        )
        print(
            f"   Recommendation score: "
            f"{product.get('recommendation_score')}"
        )

    print()
    print("=" * 80)
    print("RECOMMENDATION TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()