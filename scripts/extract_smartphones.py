import json
import re
from pathlib import Path


INPUT_FILE = (
    "data/processed/amazon/"
    "amazon_cell_phones_products.jsonl"
)

OUTPUT_FILE = (
    "data/processed/amazon/"
    "smartphones.jsonl"
)


# Words strongly associated with phone accessories.
ACCESSORY_TERMS = {
    "case",
    "cover",
    "holster",
    "pouch",
    "wallet",
    "charm",
    "stylus",
    "screen protector",
    "screen protection",
    "charger",
    "charging cable",
    "cable",
    "adapter",
    "mount",
    "holder",
    "stand",
    "tripod",
    "lens",
    "lens attachment",
    "sim card",
    "sim eject",
    "eject pin",
    "dust plug",
    "replacement part",
    "battery case",
    "phone bag",
    "belt clip",
}


# Terms that strongly suggest an actual phone.
PHONE_TERMS = {
    "smartphone",
    "cell phone",
    "mobile phone",
}


# Common smartphone model families.
PHONE_MODEL_PATTERNS = [
    r"\biphone\s+\d",
    r"\biphone\s+\w+\s+\d",
    r"\bgalaxy\s+(s|a|m|z|note|fold|flip)\d",
    r"\boneplus\s+\d",
    r"\bpixel\s+\d",
    r"\bredmi\s+(note\s+)?\d",
    r"\bmi\s+\d",
    r"\bxiaomi\s+\d",
    r"\bmoto\s+[a-z0-9]+",
    r"\bmotorola\s+[a-z0-9]+",
    r"\bnothing\s+phone",
    r"\brog\s+phone",
    r"\bhuawei\s+[a-z]",
    r"\bhonor\s+[a-z0-9]",
    r"\boppo\s+[a-z]",
    r"\bvivo\s+[a-z]",
    r"\brealme\s+[a-z0-9]",
]


def normalize(text):
    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text).lower(),
    ).strip()


def looks_like_accessory(product):
    text = normalize(
        product.get("name", "")
        + " "
        + product.get("description", "")
        + " "
        + " ".join(product.get("features", []))
    )

    matches = [
        term
        for term in ACCESSORY_TERMS
        if term in text
    ]

    return matches


def has_phone_signal(product):
    name = normalize(product.get("name", ""))
    description = normalize(
        product.get("description", "")
    )

    searchable = normalize(
        product.get("searchable_text", "")
    )

    combined = (
        name
        + " "
        + description
        + " "
        + searchable
    )

    # Strong generic signal.
    if any(term in name for term in PHONE_TERMS):
        return True

    # Model-name signal.
    for pattern in PHONE_MODEL_PATTERNS:
        if re.search(pattern, name):
            return True

    # Specifications can contain strong phone indicators.
    specifications = product.get(
        "specifications",
        {},
    )

    specification_text = normalize(
        " ".join(
            f"{key} {value}"
            for key, value in specifications.items()
        )
    )

    if (
        "operating system" in specification_text
        or "android" in specification_text
        or "ios" in specification_text
    ):
        return True

    # Avoid using searchable_text alone as a strong
    # signal because accessory descriptions mention
    # compatible phone models.
    return False


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
    selected = 0
    rejected_accessory = 0
    rejected_no_phone_signal = 0

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

            product_id = product.get(
                "product_id"
            )

            if not product_id:
                continue

            if product_id in seen_ids:
                continue

            seen_ids.add(product_id)

            accessory_matches = looks_like_accessory(
                product
            )

            if accessory_matches:
                rejected_accessory += 1
                continue

            if not has_phone_signal(product):
                rejected_no_phone_signal += 1
                continue

            # Add a stable dataset label.
            product["product_type"] = "smartphone"

            destination.write(
                json.dumps(
                    product,
                    ensure_ascii=False,
                )
                + "\n"
            )

            selected += 1

    print()
    print("=" * 70)
    print("SMARTPHONE EXTRACTION COMPLETE")
    print("=" * 70)
    print()
    print(f"Input products              : {total:,}")
    print(f"Smartphones selected        : {selected:,}")
    print(
        f"Accessories rejected       : "
        f"{rejected_accessory:,}"
    )
    print(
        f"No phone signal rejected   : "
        f"{rejected_no_phone_signal:,}"
    )
    print()
    print(f"Output file:")
    print(output_path)
    print()
    print("Original dataset was NOT modified.")
    print("=" * 70)


if __name__ == "__main__":
    main()