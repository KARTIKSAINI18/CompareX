from app.database.mongodb import MongoDB


COLLECTION_NAME = "product_documents"


def main():
    database = MongoDB()
    collection = database.get_collection(
        COLLECTION_NAME
    )

    total = collection.count_documents({})

    with_embedding = collection.count_documents({
        "embedding": {"$exists": True}
    })

    correct_embedding_size = collection.count_documents({
        "embedding": {
            "$exists": True,
            "$size": 384,
        }
    })

    print()
    print("=" * 70)
    print("COMPAREX - DOCUMENT INGESTION VERIFICATION")
    print("=" * 70)

    print()
    print(f"Total documents          : {total:,}")
    print(f"Documents with embedding : {with_embedding:,}")
    print(
        f"384-dim embeddings      : "
        f"{correct_embedding_size:,}"
    )

    print()
    print("-" * 70)
    print("SAMPLE DOCUMENT CHUNKS")
    print("-" * 70)

    samples = collection.find(
        {},
        {
            "_id": 0,
            "chunk_id": 1,
            "document_id": 1,
            "source": 1,
            "page": 1,
            "chunk_index": 1,
            "text": 1,
        },
    ).limit(3)

    for index, document in enumerate(
        samples,
        start=1,
    ):
        print()
        print(f"{index}. {document.get('chunk_id')}")
        print(
            f"   Document : "
            f"{document.get('document_id')}"
        )
        print(
            f"   Source   : "
            f"{document.get('source')}"
        )
        print(
            f"   Page     : "
            f"{document.get('page')}"
        )
        print(
            f"   Chunk    : "
            f"{document.get('chunk_index')}"
        )

        text = document.get("text", "")

        print(
            f"   Text     : "
            f"{text[:250]}..."
        )

    print()
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)

    database.close()


if __name__ == "__main__":
    main()