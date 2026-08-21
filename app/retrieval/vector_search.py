from typing import Any

from app.database.mongodb import MongoDB
from app.retrieval.embeddings import EmbeddingService


class VectorSearchService:
    """Semantic search over CompareX products."""

    COLLECTION_NAME = "products"
    INDEX_NAME = "comparex_vector_index"

    def __init__(
        self,
        database: MongoDB | None = None,
        embedding_service: EmbeddingService | None = None,
    ):
        self.database = database or MongoDB()
        self.collection = self.database.get_collection(
            self.COLLECTION_NAME
        )
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        query_embedding = self.embedding_service.embed_text(query)

        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.INDEX_NAME,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": max(limit * 20, 100),
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "product_id": 1,
                    "name": 1,
                    "brand": 1,
                    "category": 1,
                    "description": 1,
                    "specifications": 1,
                    "price": 1,
                    "currency": 1,
                    "rating": 1,
                    "review_count": 1,
                    "source": 1,
                    "product_type": 1,
                    "searchable_text": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    },
                }
            },
        ]

        return list(
            self.collection.aggregate(pipeline)
        )