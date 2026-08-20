from typing import Any


class ComparisonEngine:
    """Perform factual comparisons across product candidates."""

    def compare(
        self,
        products: list[dict[str, Any]],
        field: str,
        direction: str = "max",
    ) -> dict[str, Any]:
        if not products:
            return {
                "field": field,
                "direction": direction,
                "winner": None,
                "products": [],
            }

        values = []

        for product in products:
            value = self._extract_value(
                product,
                field,
            )

            if value is None:
                continue

            values.append(
                {
                    "product": product,
                    "value": value,
                    "currency": product.get(
                        "currency"
                    ),
                }
            )

        # ---------------------------------------------------------
        # Price comparisons require compatible currencies.
        # ---------------------------------------------------------
        if field == "price":
            currencies = {
                item["currency"]
                for item in values
                if item["currency"]
            }

            if len(currencies) > 1:
                return {
                    "field": field,
                    "direction": direction,
                    "winner": None,
                    "products": [],
                    "error": (
                        "Price comparison requires "
                        "products with the same currency."
                    ),
                }

        if not values:
            return {
                "field": field,
                "direction": direction,
                "winner": None,
                "products": [],
            }

        if direction == "min":
            winner = min(
                values,
                key=lambda item: item["value"],
            )
        else:
            winner = max(
                values,
                key=lambda item: item["value"],
            )

        return {
            "field": field,
            "direction": direction,
            "winner": {
                "product_id": winner["product"].get(
                    "product_id"
                ),
                "name": winner["product"].get(
                    "name"
                ),
                "value": winner["value"],
                "currency": winner["currency"],
            },
            "products": [
                {
                    "product_id": item["product"].get(
                        "product_id"
                    ),
                    "name": item["product"].get(
                        "name"
                    ),
                    "value": item["value"],
                    "currency": item["currency"],
                }
                for item in values
            ],
        }

    def _extract_value(
        self,
        product: dict[str, Any],
        field: str,
    ) -> float | None:
        if field == "battery":
            return self._extract_spec_number(
                product,
                ["battery"],
                "mah",
            )

        if field == "ram":
            return self._extract_spec_number(
                product,
                ["ram", "memory"],
                "gb",
            )

        if field == "storage":
            return self._extract_spec_number(
                product,
                ["storage", "rom"],
                "gb",
            )

        if field == "price":
            price = product.get("price")

            if price is None:
                return None

            try:
                return float(price)
            except (TypeError, ValueError):
                return None

        if field == "rating":
            rating = product.get("rating")

            if rating is None:
                return None

            try:
                return float(rating)
            except (TypeError, ValueError):
                return None

        return None

    @staticmethod
    def _extract_spec_number(
        product: dict[str, Any],
        keys: list[str],
        unit: str,
    ) -> float | None:
        import re

        specifications = product.get(
            "specifications"
        )

        # ---------------------------------------------------------
        # 1. Structured specifications
        # ---------------------------------------------------------
        if isinstance(specifications, dict):
            for key, value in specifications.items():
                key_text = str(key).lower()
                value_text = str(value).lower()

                if not any(
                    candidate in key_text
                    for candidate in keys
                ):
                    continue

                match = re.search(
                    rf"(\d+(?:\.\d+)?)\s*{unit}",
                    value_text,
                )

                if match:
                    return float(
                        match.group(1)
                    )

        # ---------------------------------------------------------
        # 2. Searchable text
        # ---------------------------------------------------------
        text = str(
            product.get("searchable_text") or ""
        )

        lower_text = text.lower()

        # ---------------------------------------------------------
        # RAM
        # ---------------------------------------------------------
        if "ram" in keys:
            match = re.search(
                r"(\d+(?:\.\d+)?)\s*gb\s*ram\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

            match = re.search(
                r"\bram\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*gb\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

        # ---------------------------------------------------------
        # Storage
        # ---------------------------------------------------------
        if (
            "storage" in keys
            or "rom" in keys
        ):
            match = re.search(
                r"(\d+(?:\.\d+)?)\s*gb\s*(?:storage|rom)\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

            match = re.search(
                r"\b(?:storage|rom)\s*[:\-]?\s*"
                r"(\d+(?:\.\d+)?)\s*gb\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

        # ---------------------------------------------------------
        # Battery
        # ---------------------------------------------------------
        if "battery" in keys:
            match = re.search(
                r"(\d+(?:\.\d+)?)\s*mah\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

            match = re.search(
                r"\bbattery\s*[:\-]?\s*"
                r"(\d+(?:\.\d+)?)\s*mah\b",
                lower_text,
            )

            if match:
                return float(
                    match.group(1)
                )

        return None