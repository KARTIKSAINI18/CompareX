from typing import Any
from app.rag.context_builder import ContextBuilder
from app.comparison.comparator import ProductComparator
from app.database.mongodb import MongoDB
from app.database.repository import ProductRepository
from app.models.requirements import ProductRequirements
from app.rag.service import RAGService
from app.retrieval.vector_search import VectorSearchService
from app.services.comparison_engine import ComparisonEngine
from app.services.product_matcher import ProductMatcher
from app.services.query_planner import QueryPlanner
from app.services.recommendation_engine import (
    RecommendationEngine,
)
from app.services.requirement_extractor import (
    RequirementExtractor,
)


class CompareXService:
    """Main application service for CompareX."""

    def __init__(
        self,
        database: MongoDB | None = None,
    ):
        self.database = database or MongoDB()

        self.repository = ProductRepository(
            self.database
        )

        self.vector_search = VectorSearchService(
            database=self.database
        )

        self.rag = RAGService(
            vector_search=self.vector_search
        )

        self.query_planner = QueryPlanner()

        self.requirement_extractor = (
            RequirementExtractor()
        )

        self.matcher = ProductMatcher(
            vector_search=self.vector_search
        )

        self.recommendation_engine = (
            RecommendationEngine()
        )

        self.comparison_engine = (
            ComparisonEngine()
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Perform semantic product search."""

        return self.vector_search.search(
            query=query,
            limit=limit,
        )

    def get_product(
        self,
        product_id: str,
    ) -> dict[str, Any] | None:
        """Retrieve a product by ID."""

        return self.repository.get_product(
            product_id
        )

    def compare(
        self,
        product_id_a: str,
        product_id_b: str,
    ) -> dict[str, Any]:
        """Compare two products."""

        product_a = self.repository.get_product(
            product_id_a
        )

        product_b = self.repository.get_product(
            product_id_b
        )

        if product_a is None:
            raise ValueError(
                f"Product not found: {product_id_a}"
            )

        if product_b is None:
            raise ValueError(
                f"Product not found: {product_id_b}"
            )

        return ProductComparator.compare(
            product_a,
            product_b,
        )

    def ask(
        self,
        query: str,
        limit: int = 3,
    ) -> dict[str, Any]:
        """Answer a product-related question using RAG."""

        return self.rag.answer(
            query=query,
            limit=limit,
        )

    def process(
        self,
        query: str,
        candidate_limit: int = 30,
        final_limit: int = 5,
    ) -> dict[str, Any]:
        """
        Process a natural-language CompareX request.

        This method orchestrates:
        query planning,
        requirement extraction,
        retrieval,
        matching,
        comparison,
        recommendation ranking,
        and RAG response generation.
        """

        # ---------------------------------------------------------
        # 1. Determine user intent
        # ---------------------------------------------------------
        plan = self.query_planner.plan(query)

        # ---------------------------------------------------------
        # 2. Extract structured requirements
        # ---------------------------------------------------------
        requirements = (
            self.requirement_extractor.extract(query)
        )

        # ---------------------------------------------------------
        # 3. Retrieve + match candidates
        # ---------------------------------------------------------
        candidates = self.matcher.match(
            query=query,
            requirements=requirements,
            candidate_limit=candidate_limit,
        )

        # ---------------------------------------------------------
        # 4. Handle FIND_BEST
        # ---------------------------------------------------------
        if (
            plan.intent.value == "find_best"
            and plan.comparison_field
        ):
            comparison = (
                self.comparison_engine.compare(
                    products=candidates,
                    field=plan.comparison_field.value,
                    direction=plan.comparison_direction,
                )
            )

            return {
                "query": query,
                "intent": plan.model_dump(),
                "requirements": (
                    requirements.model_dump()
                ),
                "candidates": candidates[
                    :final_limit
                ],
                "comparison": comparison,
            }

        # ---------------------------------------------------------
        # 5. Handle RECOMMEND
        # ---------------------------------------------------------
        if plan.intent.value == "recommend":
            ranked = (
                self.recommendation_engine.rank(
                    products=candidates,
                    requirements=requirements,
                )
            )

            return {
                "query": query,
                "intent": plan.model_dump(),
                "requirements": (
                    requirements.model_dump()
                ),
                "recommendations": ranked[
                    :final_limit
                ],
            }

        # ---------------------------------------------------------
        # 6. SEARCH / COMPARE baseline
        # ---------------------------------------------------------
        return {
            "query": query,
            "intent": plan.model_dump(),
            "requirements": (
                requirements.model_dump()
            ),
            "products": candidates[
                :final_limit
            ],
        }

    def answer_query(
        self,
        query: str,
        candidate_limit: int = 30,
        final_limit: int = 5,
    ) -> dict[str, Any]:
        """
        Run the complete CompareX pipeline and generate
        a grounded natural-language answer.
        """

        result = self.process(
            query=query,
            candidate_limit=candidate_limit,
            final_limit=final_limit,
        )

        context = ContextBuilder.build_result_context(
            result
        )
        

        documents = self.rag.retrieve_documents(
            query=query,
            limit=3,
        )

        document_context = self.rag.build_document_context(
            documents
        )

        combined_context = (
            context
            + "\n\n"
            + document_context
        )

        answer = self.rag.answer_from_context(
            query=query,
            context=combined_context,
        )

        result["answer"] = answer
        result["context"] = combined_context
        result["documents"] = documents

        return result

    def close(self):
        """Close the database connection."""

        self.database.close()