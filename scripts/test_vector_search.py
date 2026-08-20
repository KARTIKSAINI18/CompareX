from app.database.mongodb import MongoDB
from app.retrieval.vector_search import VectorSearchService


def main():
    database = MongoDB()

    service = VectorSearchService(
        database=database
    )

    query = "smartphone with a large battery"

    results = service.search(
        query,
        limit=3,
    )

    print(f"\nQuery: {query}\n")
    print("Results:")

    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['name']} "
            f"({result['brand']}) "
            f"- score={result['score']:.4f}"
        )

    database.close()


if __name__ == "__main__":
    main()