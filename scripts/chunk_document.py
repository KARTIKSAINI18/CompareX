from pathlib import Path
import json
import sys


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    text = " ".join(text.split())

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python scripts/chunk_document.py <json_path>"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        document = json.load(file)

    document_id = document["document_id"]

    chunks = []

    for page in document.get("pages", []):
        page_number = page["page"]
        page_text = page["text"]

        page_chunks = chunk_text(page_text)

        for index, text in enumerate(
            page_chunks,
            start=1,
        ):
            chunks.append(
                {
                    "chunk_id": (
                        f"{document_id}"
                        f"_page_{page_number}"
                        f"_chunk_{index}"
                    ),
                    "document_id": document_id,
                    "source": document["filename"],
                    "page": page_number,
                    "chunk_index": index,
                    "text": text,
                }
            )

    output_dir = Path(
        "data/processed/documents/chunks"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{document_id}_chunks.jsonl"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for chunk in chunks:
            file.write(
                json.dumps(
                    chunk,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print()
    print("=" * 70)
    print("DOCUMENT CHUNKING COMPLETE")
    print("=" * 70)
    print(f"Document        : {document_id}")
    print(f"Chunks created  : {len(chunks):,}")
    print(f"Chunk size      : {CHUNK_SIZE}")
    print(f"Chunk overlap   : {CHUNK_OVERLAP}")
    print()
    print(f"Output:")
    print(output_path)
    print("=" * 70)


if __name__ == "__main__":
    main()