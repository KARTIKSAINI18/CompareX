import json
from collections import Counter
from pathlib import Path


EXPECTED_PRODUCTS = 5000


def main():
    project_root = Path(__file__).resolve().parents[1]

    file_path = (
        project_root
        / "data"
        / "processed"
        / "amazon"
        / "amazon_cell_phones_products.jsonl"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found:\n{file_path}"
        )

    products = []

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                product = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}"
                ) from exc

            products.append(product)

    print("=" * 70)
    print("CompareX - Amazon Dataset Validation")
    print("=" * 70)
    print()

    print(f"Products loaded: {len(products):,}")
    print()

    # ---------------------------------------------------------
    # 1. Product count
    # ---------------------------------------------------------

    assert len(products) == EXPECTED_PRODUCTS, (
        f"Expected {EXPECTED_PRODUCTS} products, "
        f"found {len(products)}"
    )

    print("✓ Product count: PASS")

    # ---------------------------------------------------------
    # 2. Required fields
    # ---------------------------------------------------------

    required_fields = {
        "product_id",
        "name",
        "brand",
        "category",
        "currency",
        "description",
        "price",
        "rating",
        "review_count",
        "specifications",
        "searchable_text",
        "source",
    }

    missing_fields = Counter()

    for product in products:
        for field in required_fields:
            if field not in product:
                missing_fields[field] += 1

    if missing_fields:
        print()
        print("Missing fields:")

        for field, count in missing_fields.items():
            print(f"  {field}: {count}")

        raise AssertionError(
            "Some required fields are missing."
        )

    print("✓ Required fields: PASS")

    # ---------------------------------------------------------
    # 3. Product ID uniqueness
    # ---------------------------------------------------------

    product_ids = [
        product["product_id"]
        for product in products
    ]

    unique_product_ids = set(product_ids)

    duplicate_count = (
        len(product_ids) - len(unique_product_ids)
    )

    print(
        f"✓ Unique product IDs: "
        f"{len(unique_product_ids):,}"
    )

    if duplicate_count:
        print(
            f"WARNING: {duplicate_count:,} duplicate IDs"
        )
    else:
        print("✓ Duplicate product IDs: NONE")

    # ---------------------------------------------------------
    # 4. Source check
    # ---------------------------------------------------------

    sources = Counter(
        product["source"]
        for product in products
    )

    print()
    print("Sources:")

    for source, count in sources.items():
        print(f"  {source}: {count:,}")

    assert sources.get(
        "amazon_reviews_2023", 0
    ) == len(products)

    print("✓ Source validation: PASS")

    # ---------------------------------------------------------
    # 5. Category distribution
    # ---------------------------------------------------------

    categories = Counter(
        product["category"]
        for product in products
    )

    print()
    print("Top categories:")

    for category, count in categories.most_common(15):
        print(f"  {category}: {count:,}")

    # ---------------------------------------------------------
    # 6. Price coverage
    # ---------------------------------------------------------

    products_with_price = [
        product
        for product in products
        if product["price"] is not None
    ]

    price_percentage = (
        len(products_with_price)
        / len(products)
        * 100
    )

    print()
    print(
        f"Products with price: "
        f"{len(products_with_price):,} "
        f"({price_percentage:.2f}%)"
    )

    # ---------------------------------------------------------
    # 7. Rating coverage
    # ---------------------------------------------------------

    products_with_rating = [
        product
        for product in products
        if product["rating"] is not None
    ]

    rating_percentage = (
        len(products_with_rating)
        / len(products)
        * 100
    )

    print(
        f"Products with rating: "
        f"{len(products_with_rating):,} "
        f"({rating_percentage:.2f}%)"
    )

    # ---------------------------------------------------------
    # 8. Searchable text coverage
    # ---------------------------------------------------------

    products_with_search_text = [
        product
        for product in products
        if product["searchable_text"].strip()
    ]

    search_percentage = (
        len(products_with_search_text)
        / len(products)
        * 100
    )

    print(
        f"Products with searchable text: "
        f"{len(products_with_search_text):,} "
        f"({search_percentage:.2f}%)"
    )

    assert len(products_with_search_text) == len(products)

    print("✓ Searchable text: PASS")

    # ---------------------------------------------------------
    # 9. Specification coverage
    # ---------------------------------------------------------

    products_with_specs = [
        product
        for product in products
        if product["specifications"]
    ]

    specs_percentage = (
        len(products_with_specs)
        / len(products)
        * 100
    )

    print(
        f"Products with specifications: "
        f"{len(products_with_specs):,} "
        f"({specs_percentage:.2f}%)"
    )

    # ---------------------------------------------------------
    # 10. Show representative products
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("REPRESENTATIVE PRODUCTS")
    print("=" * 70)

    for index, product in enumerate(
        products[:5],
        start=1,
    ):
        print()
        print(f"PRODUCT {index}")
        print(f"ID:       {product['product_id']}")
        print(f"Name:     {product['name']}")
        print(f"Brand:    {product['brand']}")
        print(f"Category: {product['category']}")
        print(f"Price:    {product['price']}")
        print(f"Rating:   {product['rating']}")
        print(
            f"Reviews:  {product['review_count']}"
        )
        print(
            f"Features: "
            f"{len(product.get('features', []))}"
        )
        print(
            f"Specs:    "
            f"{len(product['specifications'])}"
        )
        print(
            "Search text preview:"
        )
        print(
            product["searchable_text"][:300]
        )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    print("Dataset is ready for embedding.")