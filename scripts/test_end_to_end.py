from app.services.comparex_service import CompareXService


def main():
    service = CompareXService()

    queries = [
        "Recommend a Samsung phone under 30000 with good camera",
        "Which smartphone has the largest battery?",
        "Compare Samsung and OnePlus phones",
        "What does the Samsung S24 manual say about battery usage?",
        "Recommend a Samsung smartphone and tell me about its battery.",
    ]

    print()
    print("=" * 80)
    print("COMPAREX END-TO-END EVALUATION")
    print("=" * 80)

    for index, query in enumerate(queries, start=1):

        print()
        print("=" * 80)
        print(f"TEST {index}")
        print("=" * 80)
        print(f"QUERY: {query}")

        try:
            result = service.answer_query(query)

            print()
            print("INTENT:")
            print(result.get("intent"))

            print()
            print("ANSWER:")
            print("-" * 80)
            print(result.get("answer"))

            products = result.get("products", [])
            documents = result.get("documents", [])

            print()
            print(f"PRODUCTS RETRIEVED : {len(products)}")
            print(f"DOCUMENTS RETRIEVED: {len(documents)}")

            print()
            print("STATUS: PASS")

        except Exception as exc:

            print()
            print("STATUS: FAIL")
            print(f"ERROR: {exc}")

    service.close()

    print()
    print("=" * 80)
    print("END-TO-END EVALUATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()