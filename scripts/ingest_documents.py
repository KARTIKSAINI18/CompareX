from pathlib import Path
import json
import sys

from app.database.mongodb import MongoDB


COLLECTION_NAME = "product_documents"


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python scripts/ingest_documents.py <embeddings_jsonl>"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    database = MongoDB()
    collection = database.get_collection(
        COLLECTION_NAME
    )

    total = 0
    inserted = 0
    updated = 0
    failed = 0

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            total += 1

            try:
                document = json.loads(line)

                chunk_id = document["chunk_id"]

                result = collection.replace_one(
                    {"chunk_id": chunk_id},
                    document,
                    upsert=True,
                )

                if result.upserted_id is not None:
                    inserted += 1
                else:
                    updated += 1

            except Exception as exc:
                failed += 1
                print(
                    f"Failed chunk {total}: {exc}"
                )

            if total % 50 == 0:
                print(
                    f"Processed: {total:,} | "
                    f"Inserted: {inserted:,} | "
                    f"Updated: {updated:,}"
                )

    print()
    print("=" * 70)
    print("DOCUMENT INGESTION COMPLETE")
    print("=" * 70)
    print(f"Records processed : {total:,}")
    print(f"Inserted           : {inserted:,}")
    print(f"Updated            : {updated:,}")
    print(f"Failed             : {failed:,}")
    print()
    print(f"MongoDB collection : {COLLECTION_NAME}")
    print("=" * 70)

    database.close()


if __name__ == "__main__":
    main()