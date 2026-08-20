import json
from pathlib import Path

from app.retrieval.embeddings import EmbeddingService
from app.schemas.product import Product


def test_product_embedding():
    data_path = Path("data/raw/products.json")

    with data_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    product = Product.model_validate(data[0])

    service = EmbeddingService()

    searchable_text = product.to_searchable_text()
    embedding = service.embed_product(product)

    assert searchable_text
    assert "Galaxy S24" in searchable_text
    assert len(embedding) == 384