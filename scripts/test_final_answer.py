from app.services.comparex_service import (
    CompareXService,
)


def main():
    service = CompareXService()

    queries = [
        "Which smartphone has the largest battery?",
        "Recommend a Samsung Android phone with a good camera",
    ]

    try:
        for query in queries:
            print()
            print("=" * 80)
            print("USER QUERY")
            print("=" * 80)
            print(query)

            result = service.answer_query(
                query=query,
                candidate_limit=30,
                final_limit=5,
            )

            print()
            print("=" * 80)
            print("COMPAREX ANSWER")
            print("=" * 80)

            print(result["answer"])

            print()
            print("=" * 80)
            print("STRUCTURED RESULT")
            print("=" * 80)

            print(
                "Intent:",
                result["intent"],
            )

            print(
                "Requirements:",
                result["requirements"],
            )

            if "comparison" in result:
                print()
                print(
                    "Verified comparison:"
                )

                comparison = result[
                    "comparison"
                ]

                print(
                    "Winner:",
                    comparison.get(
                        "winner"
                    ),
                )

    finally:
        service.close()

    print()
    print("=" * 80)
    print("FINAL ANSWER TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()