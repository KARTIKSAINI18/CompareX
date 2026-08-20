import json
import re
from pathlib import Path


INPUT_FILE = (
    "data/processed/amazon/"
    "amazon_cell_phones_products.jsonl"
)

OUTPUT_FILE = (
    "data/processed/amazon/"
    "real_smartphones.jsonl"
)


# These normally indicate that the product itself
# is an accessory rather than a smartphone.
ACCESSORY_TERMS = {
    "dust plug",
    "charm",
    "wallet",
    "purse",
    "bag",
    "crossbody",
    "earphone cap",
    "jack cap",
    "phone purse",
    "phone bag",
    "anti-dust",
    "anti dust",
    "case",
    "cover",
    "holster",
    "pouch",
    "wallet case",
    "lanyard",
    "wristlet",
    "grip",
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
    "tripod",
    "selfie stick",
    "gimbal",
    "lens",
    "lens attachment",
    "fan",
    "cooling fan",
    "sim card",
    "sim eject",
    "eject pin",
    "stylus",
    "pen",
    "armband",
    "headset",
    "vr headset",
    "vr goggles",
    "replacement",
    "replacement part",
    "battery case",
    "dock",
    "skin",
    "sticker",
    "strap",
    "screen",
    "car mount",
}


# Strong indicators that the product itself is a phone.
PHONE_PRODUCT_PATTERNS = [
    r"\bunlocked\s+(android\s+)?cell\s+phone\b",
    r"\bunlocked\s+smartphone\b",
    r"\bandroid\s+smartphone\b",
    r"\bandroid\s+phone\b",
    r"\bcell\s+phone\b",
    r"\bmobile\s+phone\b",
    r"\bsmartphone\b",
]


def normalize(text):
    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text).lower(),
    ).strip()


def accessory_match(name):
    """
    Check whether the product title primarily describes
    an accessory.
    """
    name = normalize(name)

    matches = []

    for term in ACCESSORY_TERMS:
        if term in name:
            matches.append(term)

    return matches


def has_phone_product_signal(product):
    """
    Strong evidence that the item itself is a phone.
    """

    name = normalize(
        product.get("name", "")
    )

    description = normalize(
        product.get("description", "")
    )

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

    combined = (
        name
        + " "
        + description
        + " "
        + specification_text
    )

    # Strong explicit product wording.
    for pattern in PHONE_PRODUCT_PATTERNS:
        if re.search(pattern, name):
            return True

    # Phone specifications are very strong evidence.
    phone_spec_terms = [
        "ram",
        "storage",
        "internal memory",
        "battery",
        "display",
        "screen size",
        "processor",
        "cpu",
        "operating system",
        "camera",
    ]

    spec_matches = sum(
        term in specification_text
        for term in phone_spec_terms
    )

    if spec_matches >= 3:
        return True

    # Strong phone-model names.
    model_patterns = [
        r"\biphone\s+\d",
        r"\bgalaxy\s+(s|a|m|z|note|fold|flip)\d",
        r"\boneplus\s+\d",
        r"\bpixel\s+\d",
        r"\bredmi\s+(note\s+)?\d",
        r"\bmoto\s+[a-z0-9]+",
        r"\bmotorola\s+[a-z0-9]+",
        r"\bnokia\s+[a-z0-9]+",
        r"\btcl\s+\d",
        r"\bxiaomi\s+[a-z0-9]+",
        r"\boppo\s+[a-z0-9]+",
        r"\bvivo\s+[a-z0-9]+",
        r"\brealme\s+[a-z0-9]+",
        r"\bhuawei\s+[a-z0-9]+",
        r"\bhonor\s+[a-z0-9]+",
    ]

    for pattern in model_patterns:
        if re.search(pattern, name):
            # Model name alone is not enough.
            # Require at least one phone specification
            # or explicit phone term.
            if (
                "smartphone" in name
                or "cell phone" in name
                or "android phone" in name
                or spec_matches >= 2
            ):
                return True

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
    rejected_accessories = 0
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

            # First remove obvious accessories.
            accessory_matches = accessory_match(
                product.get("name", "")
            )

            if accessory_matches:
                rejected_accessories += 1
                continue

            # Then require strong evidence that the
            # product itself is a phone.
            if not has_phone_product_signal(product):
                rejected_no_phone_signal += 1
                continue

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
    print("REAL SMARTPHONE EXTRACTION")
    print("=" * 70)
    print()
    print(f"Input products          : {total:,}")
    print(f"Real smartphones        : {selected:,}")
    print(
        f"Accessories rejected   : "
        f"{rejected_accessories:,}"
    )
    print(
        f"No phone evidence      : "
        f"{rejected_no_phone_signal:,}"
    )
    print()
    print(f"Output:")
    print(output_path)
    print()
    print("Original datasets were NOT modified.")
    print("=" * 70)


if __name__ == "__main__":
    main()