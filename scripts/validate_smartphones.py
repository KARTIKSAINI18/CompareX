import json
from pathlib import Path
from collections import Counter


INPUT_FILE = (
    "data/processed/amazon/"
    "smartphones.jsonl"
)


def main():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / INPUT_FILE

    if not input_path.exists():
        raise FileNotFoundError(
            f"File not found:\n{input_path}"
        )

    total = 0

    fields = Counter()
    brands = Counter()
    categories = Counter()

    missing_price = 0
    missing_rating = 0
    missing_description = 0
    missing_specs = 0

    samples = []

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            product = json.loads(line)

            total += 1

            # Count fields
            for field in product:
                fields[field] += 1

            # Brand distribution
            brand = product.get("brand")

            if brand:
                brands[brand] += 1

            # Category distribution
            category = product.get("category")

            if category:
                categories[category] += 1

            # Missing important fields
            if product.get("price") is None:
                missing_price += 1

            if product.get("rating") is None:
                missing_rating += 1

            if not product.get("description"):
                missing_description += 1

            if not product.get("specifications"):
                missing_specs += 1

            # Keep first 10 examples
            if len(samples) < 10:
                samples.append(product)

    print()
    print("=" * 70)
    print("SMARTPHONE DATASET VALIDATION")
    print("=" * 70)

    print()
    print(f"Total smartphone records : {total:,}")

    print()
    print("-" * 70)
    print("FIELD COVERAGE")
    print("-" * 70)

    for field, count in fields.most_common():
        percentage = (count / total) * 100
        print(
            f"{field:25} : "
            f"{count:5} / {total} "
            f"({percentage:6.2f}%)"
        )

    print()
    print("-" * 70)
    print("MISSING IMPORTANT DATA")
    print("-" * 70)

    print(
        f"Missing price        : "
        f"{missing_price:,}"
    )

    print(
        f"Missing rating       : "
        f"{missing_rating:,}"
    )

    print(
        f"Missing description  : "
        f"{missing_description:,}"
    )

    print(
        f"Missing specifications : "
        f"{missing_specs:,}"
    )

    print()
    print("-" * 70)
    print("TOP BRANDS")
    print("-" * 70)

    for brand, count in brands.most_common(20):
        print(
            f"{str(brand):30} : {count}"
        )

    print()
    print("-" * 70)
    print("TOP CATEGORIES")
    print("-" * 70)

    for category, count in categories.most_common(20):
        print(
            f"{str(category):50} : {count}"
        )

    print()
    print("-" * 70)
    print("SAMPLE PRODUCTS")
    print("-" * 70)

    for index, product in enumerate(
        samples,
        start=1,
    ):
        print()
        print(f"[{index}]")
        print(
            f"Product ID : "
            f"{product.get('product_id')}"
        )
        print(
            f"Brand      : "
            f"{product.get('brand')}"
        )
        print(
            f"Name       : "
            f"{product.get('name')}"
        )
        print(
            f"Price      : "
            f"{product.get('price')}"
        )
        print(
            f"Rating     : "
            f"{product.get('rating')}"
        )
        print(
            f"Category   : "
            f"{product.get('category')}"
        )

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()