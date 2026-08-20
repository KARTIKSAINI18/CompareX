import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INPUT_FILE = (
    "data/processed/amazon/"
    "comparex_smartphones.jsonl"
)

OUTPUT_FILE = (
    "data/processed/amazon/"
    "comparex_smartphones_embeddings.jsonl"
)

BATCH_SIZE = 32


def main():
    project_root = Path(__file__).resolve().parents[1]

    input_path = project_root / INPUT_FILE
    output_path = project_root / OUTPUT_FILE

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{input_path}"
        )

    print("=" * 70)
    print("CompareX - Smartphone Embedding Generation")
    print("=" * 70)
    print()
    print(f"Model: {MODEL_NAME}")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print()

    # Load the same model we already tested.
    model = SentenceTransformer(MODEL_NAME)

    # ---------------------------------------------------------
    # Read products
    # ---------------------------------------------------------

    products = []

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            products.append(
                json.loads(line)
            )

    print(
        f"Products loaded: {len(products):,}"
    )

    if not products:
        raise RuntimeError(
            "No products found."
        )

    # ---------------------------------------------------------
    # Generate embeddings in batches
    # ---------------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = len(products)

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as output:

        for start in range(
            0,
            total,
            BATCH_SIZE,
        ):
            end = min(
                start + BATCH_SIZE,
                total,
            )

            batch = products[start:end]

            texts = [
                product["searchable_text"]
                for product in batch
            ]

            embeddings = model.encode(
                texts,
                batch_size=BATCH_SIZE,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            for product, embedding in zip(
                batch,
                embeddings,
            ):
                document = {
                    **product,
                    "embedding": embedding.tolist(),
                }

                output.write(
                    json.dumps(
                        document,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

            processed = end

            print(
                f"Embedded: "
                f"{processed:,}/{total:,}"
            )

    print()
    print("=" * 70)
    print("EMBEDDING GENERATION COMPLETE")
    print("=" * 70)
    print()
    print(
        f"Products embedded: {total:,}"
    )
    print(
        "Embedding dimension: 384"
    )
    print(
        "Normalization: enabled"
    )
    print()
    print(f"Output:")
    print(output_path)
    print()
    print("Ready for MongoDB ingestion.")
    print("=" * 70)


if __name__ == "__main__":
    main()