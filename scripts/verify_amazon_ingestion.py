from app.database.mongodb import MongoDB


def main():
    database = MongoDB()
    collection = database.get_collection('products')

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

    amazon_products = collection.count_documents({
        "source": "amazon_reviews_2023"
    })

    smartphones = collection.count_documents({
        "product_type": "smartphone"
    })

    print()
    print("=" * 70)
    print("COMPAREX - AMAZON MONGODB VERIFICATION")
    print("=" * 70)

    print()
    print(f"Total documents          : {total:,}")
    print(f"Amazon documents         : {amazon_products:,}")
    print(f"Smartphone documents     : {smartphones:,}")
    print(f"Documents with embedding : {with_embedding:,}")
    print(
        f"384-dim embeddings      : "
        f"{correct_embedding_size:,}"
    )

    print()

    # Show a few actual products.
    print("-" * 70)
    print("SAMPLE PRODUCTS")
    print("-" * 70)

    samples = collection.find(
        {
            "source": "amazon_reviews_2023",
            "product_type": "smartphone",
        },
        {
            "_id": 0,
            "product_id": 1,
            "name": 1,
            "brand": 1,
            "price": 1,
            "rating": 1,
        },
    ).limit(5)

    for index, product in enumerate(
        samples,
        start=1,
    ):
        print()
        print(f"{index}. {product.get('name')}")
        print(
            f"   ID: {product.get('product_id')}"
        )
        print(
            f"   Brand: {product.get('brand')}"
        )
        print(
            f"   Price: {product.get('price')}"
        )
        print(
            f"   Rating: {product.get('rating')}"
        )

    print()
    print("=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()