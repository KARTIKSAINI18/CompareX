from app.rag.service import RAGService


def main():
    rag = RAGService()

    queries = [
        "What does the manual say about charging?",
        "What camera features are mentioned in the documentation?",
        "What battery information is provided in the manual?",
    ]

    for query in queries:
        print()
        print("=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        result = rag.answer(
            query=query,
            limit=3,
        )

        print()
        print("ANSWER")
        print("-" * 70)
        print(result["answer"])

        print()
        print(
            f"Products retrieved : "
            f"{len(result['products'])}"
        )

        print(
            f"Documents retrieved: "
            f"{len(result['documents'])}"
        )

    print()
    print("=" * 70)
    print("DOCUMENT RAG TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()