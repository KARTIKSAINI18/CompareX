import json
import heapq
from pathlib import Path


TARGET_PRODUCTS = 5000

# Words that strongly suggest an actual phone/device.
PHONE_KEYWORDS = {
    "smartphone",
    "cell phone",
    "mobile phone",
    "android phone",
    "iphone",
    "galaxy",
    "pixel",
    "oneplus",
    "motorola",
    "nokia",
    "xiaomi",
    "redmi",
    "oppo",
    "vivo",
    "realme",
    "google phone",
}

# Products containing these terms are usually accessories.
ACCESSORY_KEYWORDS = {
    "case",
    "cover",
    "screen protector",
    "screen guard",
    "tempered glass",
    "charger",
    "charging cable",
    "usb cable",
    "cable",
    "adapter",
    "mount",
    "holder",
    "stand",
    "wallet case",
    "bumper",
    "skin",
    "sticker",
    "replacement",
    "battery case",
    "car mount",
    "phone holder",
    "pouch",
    "sleeve",
}


def text_from_list(value):
    """Convert a list of text values into one string."""
    if not value:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, list):
        parts = []

        for item in value:
            if isinstance(item, str):
                item = item.strip()

                if item:
                    parts.append(item)

        return " ".join(parts)

    return str(value)


def flatten_details(details):
    """
    Convert Amazon's details dictionary into a simple
    specifications dictionary.
    """
    if not isinstance(details, dict):
        return {}

    specifications = {}

    for key, value in details.items():
        if isinstance(value, dict):
            # Example: Best Sellers Rank can itself be a dictionary.
            nested_values = []

            for nested_key, nested_value in value.items():
                nested_values.append(
                    f"{nested_key}: {nested_value}"
                )

            specifications[str(key)] = "; ".join(nested_values)

        elif isinstance(value, list):
            specifications[str(key)] = ", ".join(
                str(item) for item in value
            )

        elif value is not None:
            specifications[str(key)] = str(value)

    return specifications


def calculate_quality_score(record):
    """
    Score products so that useful, information-rich products
    are preferred over nearly empty records.

    This is NOT an ML model.
    It is only a deterministic data-cleaning rule.
    """
    title = str(record.get("title") or "").lower()

    features = text_from_list(record.get("features")).lower()
    description = text_from_list(record.get("description")).lower()

    details = record.get("details") or {}

    combined_text = (
        f"{title} {features} {description}"
    )

    score = 0

    # Strong preference for actual phones.
    for keyword in PHONE_KEYWORDS:
        if keyword in title:
            score += 15

    # Penalize obvious accessories.
    for keyword in ACCESSORY_KEYWORDS:
        if keyword in title:
            score -= 20

    # Product information completeness.
    if record.get("price") is not None:
        score += 5

    if record.get("average_rating") is not None:
        score += 3

    if record.get("rating_number") is not None:
        score += 3

    if features:
        score += min(len(record.get("features", [])) * 2, 10)

    if description:
        score += 5

    if details:
        score += min(len(details), 10)

    # Prefer products with reasonable review evidence.
    rating_number = record.get("rating_number")

    if isinstance(rating_number, (int, float)):
        if rating_number >= 100:
            score += 5
        elif rating_number >= 20:
            score += 3

    return score


def normalize_product(record):
    """
    Convert one Amazon metadata record into the CompareX
    product representation.
    """
    parent_asin = record.get("parent_asin")

    if not parent_asin:
        return None

    title = str(record.get("title") or "").strip()

    if not title:
        return None

    description = text_from_list(
        record.get("description")
    )

    features = record.get("features") or []

    if not isinstance(features, list):
        features = [str(features)]

    features = [
        str(item).strip()
        for item in features
        if str(item).strip()
    ]

    specifications = flatten_details(
        record.get("details")
    )

    categories = record.get("categories") or []

    if not isinstance(categories, list):
        categories = [str(categories)]

    categories = [
        str(category).strip()
        for category in categories
        if str(category).strip()
    ]

    main_category = (
        record.get("main_category")
        or (
            categories[0]
            if categories
            else "Cell Phones & Accessories"
        )
    )

    store = str(
        record.get("store") or ""
    ).strip()

    # Prefer an explicit Brand field when Amazon provides one.
    brand = specifications.get("Brand")

    if not brand:
        brand = store or None

    # Build a rich searchable representation.
    searchable_parts = [
        f"Product: {title}",
        f"Brand: {brand}" if brand else "",
        f"Category: {main_category}",
        f"Description: {description}" if description else "",
    ]

    if features:
        searchable_parts.append(
            "Features: " + " | ".join(features)
        )

    if specifications:
        specification_text = " | ".join(
            f"{key}: {value}"
            for key, value in specifications.items()
        )

        searchable_parts.append(
            f"Specifications: {specification_text}"
        )

    if record.get("price") is not None:
        searchable_parts.append(
            f"Price: {record['price']} USD"
        )

    if record.get("average_rating") is not None:
        searchable_parts.append(
            f"Rating: {record['average_rating']}"
        )

    searchable_text = "\n".join(
        part for part in searchable_parts if part
    )

    return {
        "product_id": parent_asin,
        "brand": brand,
        "category": main_category,
        "currency": "USD",
        "description": description,
        "name": title,
        "price": record.get("price"),
        "rating": record.get("average_rating"),
        "review_count": record.get("rating_number", 0),
        "specifications": specifications,
        "searchable_text": searchable_text,
        "source": "amazon_reviews_2023",
        "amazon_categories": categories,
        "features": features,
    }


def main():
    project_root = Path(__file__).resolve().parents[1]

    raw_dir = (
        project_root
        / "data"
        / "raw"
        / "amazon"
    )

    processed_dir = (
        project_root
        / "data"
        / "processed"
        / "amazon"
    )

    processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    input_files = list(
        raw_dir.glob("*.jsonl")
    )

    if not input_files:
        raise FileNotFoundError(
            f"No JSONL file found in {raw_dir}"
        )

    if len(input_files) > 1:
        raise RuntimeError(
            "Multiple JSONL files found. "
            "Keep only the Cell Phones metadata file "
            "in data/raw/amazon."
        )

    input_file = input_files[0]

    output_file = (
        processed_dir
        / "amazon_cell_phones_products.jsonl"
    )

    print("=" * 70)
    print("CompareX - Amazon Product Preparation")
    print("=" * 70)
    print(f"Input : {input_file}")
    print(f"Output: {output_file}")
    print(f"Target: {TARGET_PRODUCTS} products")
    print()

    # Heap stores:
    #
    # (quality_score, counter, product)
    #
    # We only keep the best TARGET_PRODUCTS records in memory.
    best_products = []

    seen_parent_asins = set()

    records_read = 0
    valid_records = 0
    duplicate_records = 0
    rejected_records = 0

    with input_file.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            records_read += 1

            try:
                record = json.loads(line)

            except json.JSONDecodeError:
                rejected_records += 1
                continue

            parent_asin = record.get("parent_asin")

            if not parent_asin:
                rejected_records += 1
                continue

            if parent_asin in seen_parent_asins:
                duplicate_records += 1
                continue

            seen_parent_asins.add(parent_asin)

            product = normalize_product(record)

            if product is None:
                rejected_records += 1
                continue

            valid_records += 1

            score = calculate_quality_score(record)

            # Use records_read as a deterministic tie-breaker.
            item = (
                score,
                records_read,
                product,
            )

            if len(best_products) < TARGET_PRODUCTS:
                heapq.heappush(
                    best_products,
                    item,
                )

            elif item[:2] > best_products[0][:2]:
                heapq.heapreplace(
                    best_products,
                    item,
                )

            # Progress every 100,000 records.
            if records_read % 100000 == 0:
                print(
                    f"Processed: {records_read:,} | "
                    f"Valid: {valid_records:,} | "
                    f"Selected: {len(best_products):,}"
                )

    # Highest quality first.
    best_products.sort(
        key=lambda item: (
            item[0],
            item[1],
        ),
        reverse=True,
    )

    products = [
        item[2]
        for item in best_products
    ]

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for product in products:
            file.write(
                json.dumps(
                    product,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print()
    print("=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Records read       : {records_read:,}")
    print(f"Valid records      : {valid_records:,}")
    print(f"Duplicates skipped : {duplicate_records:,}")
    print(f"Rejected records   : {rejected_records:,}")
    print(f"Products selected  : {len(products):,}")
    print(f"Output file        : {output_file}")
    print()
    print("The raw Amazon dataset was NOT modified.")


if __name__ == "__main__":
    main()