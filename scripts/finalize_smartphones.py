import json
from pathlib import Path


INPUT_FILE = (
    "data/processed/amazon/"
    "real_smartphones.jsonl"
)

OUTPUT_FILE = (
    "data/processed/amazon/"
    "comparex_smartphones.jsonl"
)


def clean_text(value):
    if value is None:
        return ""

    return " ".join(
        str(value).split()
    ).strip()


def clean_list(value):
    if not value:
        return []

    if isinstance(value, str):
        value = [value]

    return [
        clean_text(item)
        for item in value
        if clean_text(item)
    ]


def clean_specifications(value):
    if not isinstance(value, dict):
        return {}

    cleaned = {}

    for key, item in value.items():
        key = clean_text(key)
        item = clean_text(item)

        if key and item:
            cleaned[key] = item

    return cleaned


def build_searchable_text(product):
    parts = []

    if product.get("name"):
        parts.append(
            f"Product: {product['name']}"
        )

    if product.get("brand"):
        parts.append(
            f"Brand: {product['brand']}"
        )

    if product.get("category"):
        parts.append(
            f"Category: {product['category']}"
        )

    if product.get("description"):
        parts.append(
            f"Description: {product['description']}"
        )

    features = product.get("features", [])

    if features:
        parts.append(
            "Features: "
            + " | ".join(features)
        )

    specifications = product.get(
        "specifications",
        {},
    )

    if specifications:
        parts.append(
            "Specifications: "
            + " | ".join(
                f"{key}: {value}"
                for key, value
                in specifications.items()
            )
        )

    if product.get("price") is not None:
        parts.append(
            f"Price: {product['price']} USD"
        )

    if product.get("rating") is not None:
        parts.append(
            f"Rating: {product['rating']}"
        )

    if product.get("review_count") is not None:
        parts.append(
            f"Review count: "
            f"{product['review_count']}"
        )

    return "\n".join(parts)


def main():
    project_root = Path(__file__).resolve().parents[1]

    input_path = project_root / INPUT_FILE
    output_path = project_root / OUTPUT_FILE

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{input_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = 0
    final_count = 0
    skipped = 0

    seen_ids = set()

    with (
        input_path.open(
            "r",
            encoding="utf-8",
        ) as source,
        output_path.open(
            "w",
            encoding="utf-8",
        ) as destination,
    ):

        for line in source:
            line = line.strip()

            if not line:
                continue

            total += 1

            product = json.loads(line)

            product_id = clean_text(
                product.get("product_id")
            )

            name = clean_text(
                product.get("name")
            )

            if not product_id or not name:
                skipped += 1
                continue

            if product_id in seen_ids:
                skipped += 1
                continue

            seen_ids.add(product_id)

            specifications = (
                clean_specifications(
                    product.get(
                        "specifications",
                        {},
                    )
                )
            )

            features = clean_list(
                product.get("features", [])
            )

            normalized = {
                "product_id": product_id,
                "name": name,
                "brand": clean_text(
                    product.get("brand")
                ) or None,
                "category": clean_text(
                    product.get("category")
                ) or "Cell Phones & Accessories",
                "currency": "USD",
                "price": product.get("price"),
                "rating": product.get("rating"),
                "review_count": product.get(
                    "review_count",
                    0,
                ),
                "description": clean_text(
                    product.get("description")
                ) or None,
                "features": features,
                "specifications": specifications,
                "searchable_text": "",
                "source": "amazon_reviews_2023",
                "product_type": "smartphone",
            }

            normalized["searchable_text"] = (
                build_searchable_text(
                    normalized
                )
            )

            destination.write(
                json.dumps(
                    normalized,
                    ensure_ascii=False,
                )
                + "\n"
            )

            final_count += 1

    print()
    print("=" * 70)
    print("COMPAREX SMARTPHONE DATASET FINALIZED")
    print("=" * 70)
    print()
    print(f"Input candidates : {total:,}")
    print(f"Final products   : {final_count:,}")
    print(f"Skipped          : {skipped:,}")
    print()
    print(f"Output:")
    print(output_path)
    print()
    print("Dataset is now ready for embedding.")
    print("=" * 70)


if __name__ == "__main__":
    main()