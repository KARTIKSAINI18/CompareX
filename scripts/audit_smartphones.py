import json
from pathlib import Path


INPUT_FILE = (
    "data/processed/amazon/"
    "comparex_smartphones.jsonl"
)


ACCESSORY_TERMS = {
    "case",
    "cover",
    "holster",
    "pouch",
    "wallet",
    "wallet case",
    "charm",
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
    "dust plug",
    "stylus",
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
    "car mount",
}


def main():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / INPUT_FILE

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    total = 0
    suspicious = []

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

            name = str(
                product.get("name", "")
            ).lower()

            matches = [
                term
                for term in ACCESSORY_TERMS
                if term in name
            ]

            if matches:
                suspicious.append(
                    {
                        "product_id": product.get(
                            "product_id"
                        ),
                        "name": product.get("name"),
                        "matches": matches,
                    }
                )

    print()
    print("=" * 70)
    print("COMPAREX SMARTPHONE DATASET AUDIT")
    print("=" * 70)
    print()
    print(f"Total products checked: {total:,}")
    print(
        f"Accessory-like products found: "
        f"{len(suspicious):,}"
    )

    print()
    print("-" * 70)
    print("FIRST 30 SUSPICIOUS PRODUCTS")
    print("-" * 70)

    for index, product in enumerate(
        suspicious[:30],
        start=1,
    ):
        print()
        print(f"{index}. {product['name']}")
        print(
            f"   ID: {product['product_id']}"
        )
        print(
            f"   Matched terms: "
            f"{', '.join(product['matches'])}"
        )

    print()
    print("=" * 70)
    print("AUDIT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()