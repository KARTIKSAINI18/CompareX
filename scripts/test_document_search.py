from app.retrieval.document_search import DocumentSearchService


def main():
    service = DocumentSearchService()

    queries = [
        "How do I charge the phone?",
        "What are the camera features?",
        "What battery information is provided?",
    ]

    for query in queries:
        print()
        print("=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        results = service.search(
            query=query,
            limit=3,
        )

        for index, result in enumerate(
            results,
            start=1,
        ):
            print()
            print(
                f"{index}. "
                f"Score: {result.get('score')}"
            )
            print(
                f"   Page: "
                f"{result.get('page')}"
            )
            print(
                f"   Source: "
                f"{result.get('source')}"
            )
            print(
                f"   Text: "
                f"{result.get('text', '')[:500]}"
            )

    service.database.close()

    print()
    print("=" * 70)
    print("DOCUMENT SEARCH TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()