from pprint import pprint

from app.services.comparex_service import (
    CompareXService,
)


def main():
    service = CompareXService()

    queries = [
        "Which smartphone has the largest battery?",
        "Recommend a Samsung Android phone with good camera",
        "Show me smartphones with at least 5000mAh battery",
    ]

    try:
        for query in queries:
            print()
            print("=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            result = service.process(
                query=query,
                candidate_limit=30,
                final_limit=5,
            )

            print()
            print("INTENT:")
            pprint(result["intent"])

            print()
            print("REQUIREMENTS:")
            pprint(result["requirements"])

            if "comparison" in result:
                print()
                print("COMPARISON:")
                pprint(result["comparison"])

            if "recommendations" in result:
                print()
                print("RECOMMENDATIONS:")

                for index, product in enumerate(
                    result["recommendations"],
                    start=1,
                ):
                    print()
                    print(
                        f"{index}. "
                        f"{product.get('name')}"
                    )
                    print(
                        "   Recommendation score: "
                        f"{product.get('recommendation_score')}"
                    )

            if "products" in result:
                print()
                print("PRODUCTS:")

                for index, product in enumerate(
                    result["products"],
                    start=1,
                ):
                    print()
                    print(
                        f"{index}. "
                        f"{product.get('name')}"
                    )
                    print(
                        f"   Score: "
                        f"{product.get('score')}"
                    )

    finally:
        service.close()

    print()
    print("=" * 80)
    print("COMPAREX PIPELINE TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()