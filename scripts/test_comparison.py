from app.database.mongodb import MongoDB
from app.database.repository import ProductRepository
from app.comparison.comparator import ProductComparator


def main():
    database = MongoDB()
    repository = ProductRepository(database)

    galaxy = repository.get_product("phone_001")
    oneplus = repository.get_product("phone_002")

    if galaxy is None or oneplus is None:
        raise RuntimeError(
            "Required products were not found in MongoDB."
        )

    result = ProductComparator.compare(
        galaxy,
        oneplus,
    )

    print("\n" + "=" * 60)
    print("COMPAREX PRODUCT COMPARISON")
    print("=" * 60)

    print(
        f"\n{result['product_a']} "
        f"vs "
        f"{result['product_b']}"
    )

    print("\nTOP-LEVEL COMPARISON")
    print("-" * 60)

    for field, comparison in result["top_level"].items():
        print(
            f"{field}: "
            f"{comparison['product_a']} vs "
            f"{comparison['product_b']} "
            f"→ winner: {comparison['winner']}"
        )

    print("\nSPECIFICATIONS")
    print("-" * 60)

    for field, comparison in result["specifications"].items():
        print(
            f"{field}: "
            f"{comparison['product_a']} vs "
            f"{comparison['product_b']}"
        )

    database.close()


if __name__ == "__main__":
    main()