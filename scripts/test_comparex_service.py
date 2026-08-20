from app.database.mongodb import MongoDB
from app.services.comparex_service import CompareXService


def main():
    database = MongoDB()

    service = CompareXService(
        database=database
    )

    try:
        print("\n" + "=" * 70)
        print("COMPAREX APPLICATION SERVICE")
        print("=" * 70)

        # --------------------------------------------------
        # 1. Semantic Search
        # --------------------------------------------------

        print("\n[1] SEMANTIC SEARCH")
        print("-" * 70)

        search_results = service.search(
            "smartphone with a large battery",
            limit=3,
        )

        for result in search_results:
            print(
                f"- {result['name']} "
                f"({result['brand']}) "
                f"score={result['score']:.4f}"
            )

        # --------------------------------------------------
        # 2. Product Comparison
        # --------------------------------------------------

        print("\n[2] PRODUCT COMPARISON")
        print("-" * 70)

        comparison = service.compare(
            "phone_001",
            "phone_002",
        )

        print(
            f"{comparison['product_a']} "
            f"vs "
            f"{comparison['product_b']}"
        )

        for field, result in comparison[
            "top_level"
        ].items():
            print(
                f"{field}: "
                f"{result['product_a']} vs "
                f"{result['product_b']} "
                f"→ {result['winner']}"
            )

        # --------------------------------------------------
        # 3. RAG Question
        # --------------------------------------------------

        print("\n[3] RAG QUESTION")
        print("-" * 70)

        answer = service.ask(
            "Which smartphone has the largest battery?",
            limit=3,
        )

        print(answer["answer"])

    finally:
        service.close()


if __name__ == "__main__":
    main()