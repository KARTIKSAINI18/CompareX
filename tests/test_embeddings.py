from app.retrieval.embeddings import EmbeddingService


def test_embedding_generation():
    service = EmbeddingService()

    text = "A smartphone with a powerful processor and large battery."

    embedding = service.embed_text(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)