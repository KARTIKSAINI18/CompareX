from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    """Generate vector embeddings for CompareX documents."""

    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_product(self, product) -> list[float]:
        return self.embed_text(product.to_searchable_text())