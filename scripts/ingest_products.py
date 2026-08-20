import json
from pathlib import Path

from app.database.repository import ProductRepository
from app.retrieval.embeddings import EmbeddingService
from app.schemas.product import Product


DATA_PATH = Path("data/raw/products.json")


def load_products() -> list[Product]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        raw_products = json.load(file)

    return [
        Product.model_validate(product)
        for product in raw_products
    ]


def build_product_document(
    product: Product,
    embedding_service: EmbeddingService,
) -> dict:
    searchable_text = product.to_searchable_text()

    embedding = embedding_service.embed_text(searchable_text)

    return {
        "product_id": product.product_id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "description": product.description,
        "specifications": product.specifications,
        "price": product.price,
        "currency": product.currency,
        "rating": product.rating,
        "review_count": product.review_count,
        "source": product.source,
        "searchable_text": searchable_text,
        "embedding": embedding,
    }


def main():
    products = load_products()

    embedding_service = EmbeddingService()
    repository = ProductRepository()

    documents = [
        build_product_document(product, embedding_service)
        for product in products
    ]

    repository.upsert_products(documents)

    print(f"Successfully ingested {len(documents)} products.")
    print(f"Products in MongoDB: {repository.count_products()}")


if __name__ == "__main__":
    main()