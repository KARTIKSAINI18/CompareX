from app.services.requirement_extractor import (
    RequirementExtractor,
)


def main():
    extractor = RequirementExtractor()

    queries = [
        "Samsung Android phone under 30000 with at least 8GB RAM",
        "iPhone under 70000 with good camera",
        "phone with at least 5000mAh battery",
        "affordable Android smartphone with good performance",
        "Samsung phone under 25000 with 8GB RAM and 256GB storage",
    ]

    for query in queries:
        result = extractor.extract(query)

        print()
        print("=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        print(result.model_dump())


if __name__ == "__main__":
    main()