from app.rag.service import RAGService


def main():
    service = RAGService()

    query = "Which smartphone has the largest battery?"

    result = service.answer(
        query=query,
        limit=3,
    )

    print("\n" + "=" * 60)
    print("QUERY")
    print("=" * 60)
    print(query)

    print("\n" + "=" * 60)
    print("RETRIEVED PRODUCTS")
    print("=" * 60)

    for product in result["products"]:
        print(
            f"- {product['name']} "
            f"({product['brand']}) "
            f"score={product['score']:.4f}"
        )

    print("\n" + "=" * 60)
    print("RAG ANSWER")
    print("=" * 60)
    print(result["answer"])


if __name__ == "__main__":
    main()