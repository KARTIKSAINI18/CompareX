from typing import Any

from app.database.mongodb import MongoDB
from app.retrieval.embeddings import EmbeddingService


class DocumentSearchService:
    """Semantic search over product documentation."""

    def __init__(
        self,
        database: MongoDB | None = None,
        embedding_service: EmbeddingService | None = None,
    ):
        self.database = database or MongoDB()

        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.collection = self.database.get_collection(
            "product_documents"
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Find relevant document chunks."""

        query_embedding = (
            self.embedding_service.embed_text(query)
        )

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": max(limit * 10, 50),
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "chunk_id": 1,
                    "document_id": 1,
                    "source": 1,
                    "page": 1,
                    "chunk_index": 1,
                    "text": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    },
                }
            },
        ]

        return list(
            self.collection.aggregate(pipeline)
        )