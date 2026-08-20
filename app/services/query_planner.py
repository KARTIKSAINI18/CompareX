import re

from app.models.query_intent import (
    ComparisonField,
    QueryIntent,
    QueryIntentType,
)


class QueryPlanner:
    """Determine what operation CompareX should perform."""

    def plan(self, query: str) -> QueryIntent:
        text = query.lower().strip()

        # ---------------------------------------------------------
        # Comparison language must indicate that the user wants
        # an extremum or direct comparison.
        # ---------------------------------------------------------
        comparison_field = self._detect_comparison_field(
            text
        )

        explicit_best_language = any(
            phrase in text
            for phrase in [
                "largest",
                "biggest",
                "highest",
                "most",
                "maximum",
                "max",
                "smallest",
                "lowest",
                "least",
                "minimum",
                "min",
                "cheapest",
                "most expensive",
            ]
        )

        if (
            comparison_field
            and explicit_best_language
        ):
            direction = self._detect_direction(
                text
            )

            return QueryIntent(
                intent=QueryIntentType.FIND_BEST,
                comparison_field=comparison_field,
                comparison_direction=direction,
            )

        # ---------------------------------------------------------
        # Explicit product comparison
        # ---------------------------------------------------------
        if any(
            phrase in text
            for phrase in [
                "compare",
                "comparison",
                "difference between",
                "vs",
                "versus",
            ]
        ):
            return QueryIntent(
                intent=QueryIntentType.COMPARE
            )

        # ---------------------------------------------------------
        # Recommendation
        # ---------------------------------------------------------
        if any(
            phrase in text
            for phrase in [
                "recommend",
                "recommendation",
                "best phone for me",
                "which phone should i buy",
                "which one should i buy",
                "suggest",
            ]
        ):
            return QueryIntent(
                intent=QueryIntentType.RECOMMEND
            )

        # ---------------------------------------------------------
        # Default: search
        # ---------------------------------------------------------
        return QueryIntent(
            intent=QueryIntentType.SEARCH
        )

    @staticmethod
    def _detect_comparison_field(
        text: str,
    ) -> ComparisonField | None:

        if any(
            term in text
            for term in [
                "battery",
                "battery capacity",
                "mah",
            ]
        ):
            return ComparisonField.BATTERY

        if any(
            term in text
            for term in [
                "ram",
                "memory",
            ]
        ):
            return ComparisonField.RAM

        if any(
            term in text
            for term in [
                "storage",
                "rom",
            ]
        ):
            return ComparisonField.STORAGE

        if any(
            term in text
            for term in [
                "rating",
                "rated",
                "reviews",
            ]
        ):
            return ComparisonField.RATING

        if any(
            term in text
            for term in [
                "price",
                "cheapest",
                "lowest price",
                "most affordable",
            ]
        ):
            return ComparisonField.PRICE

        return None

    @staticmethod
    def _detect_direction(
        text: str,
    ) -> str:

        if any(
            term in text
            for term in [
                "cheapest",
                "lowest",
                "least",
                "smallest",
                "lowest price",
            ]
        ):
            return "min"

        return "max"