from app.database.mongodb import MongoDB
from app.retrieval.vector_search import VectorSearchService


def evaluate_retrieval(
    vector_search: VectorSearchService,
):
    query = "smartphone with a large battery"

    results = vector_search.search(
        query=query,
        limit=3,
    )

    print()
    print("=" * 60)
    print("RETRIEVAL EVALUATION")
    print("=" * 60)

    print(f"Query: {query}")
    print(f"Retrieved: {len(results)}")

    battery_relevant = 0

    for result in results:
        text = (
            f"{result.get('name', '')} "
            f"{result.get('description', '')} "
            f"{result.get('specifications', '')}"
        ).lower()

        if (
            "battery" in text
            or "mah" in text
        ):
            battery_relevant += 1

    print(
        f"Battery-relevant: "
        f"{battery_relevant}"
    )

    print("\nRetrieved products:")

    for result in results:
        print(
            f"- {result['product_id']}: "
            f"{result['name']} "
            f"(score={result['score']:.4f})"
        )

    if results and battery_relevant > 0:
        print("\nStatus: PASS")
    else:
        print("\nStatus: FAIL")


def main():
    database = MongoDB()

    vector_search = VectorSearchService(
        database=database
    )

    evaluate_retrieval(
        vector_search
    )

    database.close()


if __name__ == "__main__":
    main()