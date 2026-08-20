from typing import Any


class ProductDocument:
    """Represents a chunk of product-related document knowledge."""

    def __init__(
        self,
        document_id: str,
        product_id: str | None,
        title: str,
        content: str,
        source: str,
        metadata: dict[str, Any] | None = None,
    ):
        self.document_id = document_id
        self.product_id = product_id
        self.title = title
        self.content = content
        self.source = source
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "product_id": self.product_id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "metadata": self.metadata,
        }