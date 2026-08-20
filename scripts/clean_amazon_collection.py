from app.database.mongodb import MongoDB


COLLECTION_NAME = "products"


def main():
    database = MongoDB()
    collection = database.get_collection(
        COLLECTION_NAME
    )

    print()
    print("=" * 70)
    print("COMPAREX - CLEAN OLD AMAZON PRODUCTS")
    print("=" * 70)
    print()

    before = collection.count_documents({
        "source": "amazon_reviews_2023",
        "product_type": "smartphone",
    })

    print(
        f"Amazon smartphone documents before cleanup: "
        f"{before:,}"
    )

    result = collection.delete_many({
        "source": "amazon_reviews_2023",
        "product_type": "smartphone",
    })

    print(
        f"Deleted: {result.deleted_count:,}"
    )

    after = collection.count_documents({
        "source": "amazon_reviews_2023",
        "product_type": "smartphone",
    })

    print(
        f"Amazon smartphone documents after cleanup: "
        f"{after:,}"
    )

    print()
    print("=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()