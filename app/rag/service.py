from typing import Any

from app.rag.context_builder import ContextBuilder
from app.rag.prompt import build_prompt
from app.retrieval.vector_search import VectorSearchService
from app.retrieval.document_search import DocumentSearchService
from app.llm.client import LLMClient


class RAGService:
    """Retrieval-Augmented Generation service for CompareX."""

    def __init__(
        self,
        vector_search: VectorSearchService | None = None,
        document_search: DocumentSearchService | None = None,
        llm: LLMClient | None = None,
    ):
        self.vector_search = (
            vector_search
            or VectorSearchService()
        )

        self.document_search = (
            document_search
            or DocumentSearchService()
        )

        self.llm = llm or LLMClient()


    def retrieve_documents(
        self,
        query: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant product-document chunks."""

        return self.document_search.search(
            query=query,
            limit=limit,
        )

    def answer(
        self,
        query: str,
        limit: int = 3,
    ) -> dict[str, Any]:
        """Retrieve products and documents, then generate an answer."""

        products = self.vector_search.search(
            query=query,
            limit=limit,
        )

        documents = self.document_search.search(
            query=query,
            limit=limit,
        )

        product_context = ContextBuilder.build(
            products
        )

        document_context = self.build_document_context(
            documents
        )

        context = (
            product_context
            + "\n\n"
            + document_context
        )

        answer = self.answer_from_context(
            query=query,
            context=context,
        )

        return {
            "query": query,
            "answer": answer,
            "products": products,
            "documents": documents,
        }

    def answer_from_context(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate an answer from already verified
        CompareX context.

        No additional retrieval is performed.
        """

        prompt = build_prompt(
            query=query,
            context=context,
        )

        return self.llm.generate(prompt)

    @staticmethod
    def build_document_context(
        documents: list[dict[str, Any]],
    ) -> str:
        if not documents:
            return "DOCUMENT CONTEXT:\nNo relevant documents found."

        lines = [
            "DOCUMENT CONTEXT:",
            "================",
        ]

        for index, document in enumerate(
            documents,
            start=1,
        ):
            lines.append(
                f"Document {index}:"
            )
            lines.append(
                f"Source: {document.get('source', '')}"
            )
            lines.append(
                f"Page: {document.get('page', '')}"
            )
            lines.append(
                f"Content: {document.get('text', '')}"
            )
            lines.append("")

        return "\n".join(lines)