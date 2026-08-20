from typing import Any

from app.database.mongodb import MongoDB


class ProductRepository:
    """Database operations for CompareX products."""

    COLLECTION_NAME = "products"

    def __init__(self, database: MongoDB | None = None):
        self.database = database or MongoDB()
        self.collection = self.database.get_collection(self.COLLECTION_NAME)

    def upsert_product(self, product: dict) -> None:
        """
        Insert or update a product using product_id as the
        stable MongoDB identifier.
        """
        self.collection.update_one(
            {"product_id": product["product_id"]},
            {"$set": product},
            upsert=True,
        )

    def upsert_products(
        self,
        product_documents: list[dict[str, Any]],
    ) -> None:
        """Insert or update multiple products."""

        for product_document in product_documents:
            self.upsert_product(product_document)

    def get_product(self, product_id: str) -> dict[str, Any] | None:
        """Retrieve one product by product ID."""

        return self.collection.find_one(
            {"product_id": product_id}
        )

    def count_products(self) -> int:
        """Return the number of stored products."""

        return self.collection.count_documents({})