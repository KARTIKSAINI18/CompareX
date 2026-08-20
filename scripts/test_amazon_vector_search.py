from app.retrieval.vector_search import VectorSearchService


def main():
    service = VectorSearchService()

    queries = [
        "smartphone with a large battery",
        "affordable Android smartphone",
        "smartphone with a good camera",
        "Samsung smartphone with good performance",
    ]

    for query in queries:
        print()
        print("=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = service.search(
            query=query,
            limit=5,
        )

        if not results:
            print("No results found.")
            continue

        for index, product in enumerate(
            results,
            start=1,
        ):
            print()
            print(
                f"{index}. {product.get('name')}"
            )
            print(
                f"   Product ID : "
                f"{product.get('product_id')}"
            )
            print(
                f"   Brand      : "
                f"{product.get('brand')}"
            )
            print(
                f"   Price      : "
                f"{product.get('price')}"
            )
            print(
                f"   Rating     : "
                f"{product.get('rating')}"
            )
            print(
                f"   Score      : "
                f"{product.get('score')}"
            )

    print()
    print("=" * 80)
    print("VECTOR SEARCH TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()