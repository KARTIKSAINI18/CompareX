import json
from pathlib import Path

from app.database.repository import ProductRepository


INPUT_FILE = (
    "data/processed/amazon/"
    "comparex_smartphones_embeddings.jsonl"
)


def main():
    project_root = Path(__file__).resolve().parents[1]

    input_path = project_root / INPUT_FILE

    if not input_path.exists():
        raise FileNotFoundError(
            f"Embedding file not found:\n{input_path}"
        )

    repository = ProductRepository()

    total = 0
    inserted_or_updated = 0
    failed = 0

    print()
    print("=" * 70)
    print("CompareX - Amazon Product Ingestion")
    print("=" * 70)
    print()
    print(f"Input: {input_path}")
    print()

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1,
        ):
            line = line.strip()

            if not line:
                continue

            total += 1

            try:
                product = json.loads(line)

                if not product.get("product_id"):
                    failed += 1
                    print(
                        f"Skipping line {line_number}: "
                        "missing product_id"
                    )
                    continue

                embedding = product.get("embedding")

                if not embedding:
                    failed += 1
                    print(
                        f"Skipping line {line_number}: "
                        "missing embedding"
                    )
                    continue

                if len(embedding) != 384:
                    failed += 1
                    print(
                        f"Skipping line {line_number}: "
                        f"expected 384 dimensions, "
                        f"got {len(embedding)}"
                    )
                    continue

                repository.upsert_product(product)

                inserted_or_updated += 1

                if inserted_or_updated % 100 == 0:
                    print(
                        f"Ingested: "
                        f"{inserted_or_updated:,}/"
                        f"{total:,}"
                    )

            except Exception as exc:
                failed += 1

                print(
                    f"Failed line {line_number}: "
                    f"{type(exc).__name__}: {exc}"
                )

    print()
    print("=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)
    print()
    print(f"Records read        : {total:,}")
    print(
        f"Inserted / updated  : "
        f"{inserted_or_updated:,}"
    )
    print(f"Failed              : {failed:,}")
    print()
    print(
        "Products are now stored in MongoDB Atlas."
    )
    print("=" * 70)


if __name__ == "__main__":
    main()