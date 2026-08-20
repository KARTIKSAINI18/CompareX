from pathlib import Path
import json
import sys

from app.retrieval.embeddings import EmbeddingService


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python scripts/embed_document.py <chunks_jsonl>"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    embedding_service = EmbeddingService()

    output_dir = Path(
        "data/processed/documents/embeddings"
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{input_path.stem}_embeddings.jsonl"
    )

    total = 0

    with (
        input_path.open("r", encoding="utf-8") as input_file,
        output_path.open("w", encoding="utf-8") as output_file,
    ):
        for line in input_file:
            line = line.strip()

            if not line:
                continue

            chunk = json.loads(line)

            embedding = embedding_service.embed_text(
                chunk["text"]
            )

            chunk["embedding"] = embedding

            output_file.write(
                json.dumps(
                    chunk,
                    ensure_ascii=False,
                )
                + "\n"
            )

            total += 1

            if total % 50 == 0:
                print(
                    f"Embedded: {total:,}"
                )

    print()
    print("=" * 70)
    print("DOCUMENT EMBEDDING COMPLETE")
    print("=" * 70)
    print(f"Chunks embedded : {total:,}")
    print("Embedding model : all-MiniLM-L6-v2")
    print("Embedding size  : 384")
    print("Normalization   : enabled")
    print()
    print("Output:")
    print(output_path)
    print("=" * 70)


if __name__ == "__main__":
    main()