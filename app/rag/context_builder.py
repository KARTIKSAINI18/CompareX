from typing import Any


class ContextBuilder:
    """Build grounded context for CompareX responses."""

    @staticmethod
    def build(
        products: list[dict[str, Any]],
    ) -> str:
        if not products:
            return "No relevant products were found."

        sections = []

        for index, product in enumerate(
            products,
            start=1,
        ):
            specifications = product.get(
                "specifications",
                {},
            )

            specification_text = "\n".join(
                f"- {key}: {value}"
                for key, value in specifications.items()
            )

            section = f"""
Product {index}
--------------
Product ID: {product.get("product_id")}
Name: {product.get("name")}
Brand: {product.get("brand")}
Category: {product.get("category")}
Price: {product.get("price")} {product.get("currency")}
Rating: {product.get("rating")}
Review Count: {product.get("review_count")}

Description:
{product.get("description", "")}

Specifications:
{specification_text}
""".strip()

            sections.append(section)

        return "\n\n".join(sections)

    @staticmethod
    def build_result_context(
        result: dict[str, Any],
    ) -> str:
        """
        Build grounded context from a verified
        CompareX pipeline result.
        """

        sections = []

        query = result.get("query")

        if query:
            sections.append(
                f"User Query:\n{query}"
            )

        # ---------------------------------------------------------
        # Comparison result
        # ---------------------------------------------------------
        comparison = result.get("comparison")

        if comparison:
            sections.append(
                ContextBuilder._build_comparison_context(
                    comparison
                )
            )

        # ---------------------------------------------------------
        # Recommendations
        # ---------------------------------------------------------
        recommendations = result.get(
            "recommendations"
        )

        if recommendations:
            sections.append(
                ContextBuilder.build(
                    recommendations
                )
            )

        # ---------------------------------------------------------
        # Search products
        # ---------------------------------------------------------
        products = result.get("products")

        if products:
            sections.append(
                ContextBuilder.build(products)
            )

        # ---------------------------------------------------------
        # Candidates
        # ---------------------------------------------------------
        candidates = result.get("candidates")

        if candidates:
            sections.append(
                ContextBuilder.build(candidates)
            )

        if not sections:
            return "No verified product information was found."

        return "\n\n".join(sections)

    @staticmethod
    def _build_comparison_context(
        comparison: dict[str, Any],
    ) -> str:
        lines = []

        field = comparison.get(
            "field",
            "unknown",
        )

        direction = comparison.get(
            "direction",
            "max",
        )

        lines.append(
            "Verified Comparison"
        )

        lines.append(
            f"Field: {field}"
        )

        lines.append(
            f"Direction: {direction}"
        )

        winner = comparison.get("winner")

        if winner:
            lines.append(
                f"Winner: {winner.get('name')}"
            )

            lines.append(
                f"Winner Product ID: "
                f"{winner.get('product_id')}"
            )

            lines.append(
                f"Winner Value: "
                f"{winner.get('value')}"
            )

        lines.append("")
        lines.append("Compared Products:")

        for product in comparison.get(
            "products",
            [],
        ):
            lines.append(
                f"- {product.get('name')}: "
                f"{product.get('value')}"
            )

        return "\n".join(lines)