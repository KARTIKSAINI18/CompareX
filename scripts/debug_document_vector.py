from app.database.mongodb import MongoDB
from app.retrieval.embeddings import EmbeddingService


def main():
    database = MongoDB()
    collection = database.get_collection(
        "product_documents"
    )

    embedding_service = EmbeddingService()

    query = "What battery information is provided?"

    query_vector = embedding_service.embed_text(query)

    print("=" * 70)
    print("DOCUMENT VECTOR DEBUG")
    print("=" * 70)

    print(f"Query vector length: {len(query_vector)}")

    sample = collection.find_one(
        {"embedding": {"$exists": True}}
    )

    print(
        f"Stored vector length: "
        f"{len(sample['embedding']) if sample else 0}"
    )

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 5,
            }
        },
        {
            "$project": {
                "_id": 0,
                "chunk_id": 1,
                "page": 1,
                "text": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                },
            }
        },
    ]

    results = list(
        collection.aggregate(pipeline)
    )

    print(f"Results: {len(results)}")

    for index, result in enumerate(
        results,
        start=1,
    ):
        print()
        print(f"{index}. Score: {result.get('score')}")
        print(f"Page: {result.get('page')}")
        print(
            f"Text: "
            f"{result.get('text', '')[:500]}"
        )

    database.close()


if __name__ == "__main__":
    main()