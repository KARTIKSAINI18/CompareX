from typing import Any


class ProductComparator:
    """Deterministic product comparison engine."""

    COMPARABLE_FIELDS = {
        "price": "lower",
        "rating": "higher",
        "review_count": "higher",
    }

    @staticmethod
    def compare(
        product_a: dict[str, Any],
        product_b: dict[str, Any],
    ) -> dict[str, Any]:
        specifications = ProductComparator._compare_specifications(
            product_a.get("specifications", {}),
            product_b.get("specifications", {}),
        )

        top_level = ProductComparator._compare_top_level(
            product_a,
            product_b,
        )

        return {
            "product_a": product_a.get("name"),
            "product_b": product_b.get("name"),
            "top_level": top_level,
            "specifications": specifications,
        }

    @staticmethod
    def _compare_top_level(
        product_a: dict[str, Any],
        product_b: dict[str, Any],
    ) -> dict[str, Any]:

        result = {}

        for field, direction in ProductComparator.COMPARABLE_FIELDS.items():
            value_a = product_a.get(field)
            value_b = product_b.get(field)

            if value_a is None or value_b is None:
                continue

            if value_a == value_b:
                winner = "tie"
            elif direction == "higher":
                winner = (
                    product_a.get("name")
                    if value_a > value_b
                    else product_b.get("name")
                )
            else:
                winner = (
                    product_a.get("name")
                    if value_a < value_b
                    else product_b.get("name")
                )

            result[field] = {
                "product_a": value_a,
                "product_b": value_b,
                "winner": winner,
            }

        return result

    @staticmethod
    def _compare_specifications(
        specs_a: dict[str, Any],
        specs_b: dict[str, Any],
    ) -> dict[str, Any]:

        all_keys = sorted(
            set(specs_a.keys()) | set(specs_b.keys())
        )

        result = {}

        for key in all_keys:
            value_a = specs_a.get(key)
            value_b = specs_b.get(key)

            result[key] = {
                "product_a": value_a,
                "product_b": value_b,
                "same": value_a == value_b,
            }

        return result