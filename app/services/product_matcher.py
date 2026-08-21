from typing import Any

from app.models.requirements import ProductRequirements
from app.retrieval.vector_search import VectorSearchService


class ProductMatcher:
    """Retrieve and filter products against structured requirements."""

    def __init__(
        self,
        vector_search: VectorSearchService | None = None,
    ):
        self.vector_search = (
            vector_search or VectorSearchService()
        )

    def match(
        self,
        query: str,
        requirements: ProductRequirements,
        candidate_limit: int = 30,
    ) -> list[dict[str, Any]]:
        candidates = self.vector_search.search(
            query=query,
            limit=candidate_limit,
        )

        filtered = []

        for product in candidates:
            if self._matches_requirements(
                product,
                requirements,
            ):
                filtered.append(product)

        return filtered

    def _matches_requirements(
        self,
        product: dict[str, Any],
        requirements: ProductRequirements,
    ) -> bool:

        # ---------------------------------------------------------
        # Brand
        # ---------------------------------------------------------
        if requirements.brand:
            brand = str(
                product.get("brand") or ""
            ).lower()

            name = str(
                product.get("name") or ""
            ).lower()

            if (
                requirements.brand.lower() not in brand
                and requirements.brand.lower() not in name
            ):
                return False

        # ---------------------------------------------------------
        # Rating
        # ---------------------------------------------------------
        if requirements.min_rating is not None:
            rating = product.get("rating")

            if rating is None:
                return False

            try:
                if float(rating) < requirements.min_rating:
                    return False
            except (TypeError, ValueError):
                return False

        # ---------------------------------------------------------
        # Price
        # ---------------------------------------------------------
        if requirements.max_price is not None:
            price = product.get("price")
            if price is not None:
                try:
                    if float(price) > requirements.max_price:
                        return False
                except (TypeError, ValueError):
                    pass
                    
        if requirements.min_price is not None:
            price = product.get("price")
            if price is not None:
                try:
                    if float(price) < requirements.min_price:
                        return False
                except (TypeError, ValueError):
                    pass

        # ---------------------------------------------------------
        # RAM
        # ---------------------------------------------------------
        if requirements.min_ram_gb is not None:
            ram = self._extract_spec_number(
                product,
                ["ram", "memory"],
                unit="gb",
            )

            if ram is None or ram < requirements.min_ram_gb:
                return False

        # ---------------------------------------------------------
        # Storage
        # ---------------------------------------------------------
        if requirements.min_storage_gb is not None:
            storage = self._extract_spec_number(
                product,
                ["storage", "rom"],
                unit="gb",
            )

            if (
                storage is None
                or storage < requirements.min_storage_gb
            ):
                return False

        # ---------------------------------------------------------
        # Battery
        # ---------------------------------------------------------
        if requirements.min_battery_mah is not None:
            battery = self._extract_spec_number(
                product,
                ["battery"],
                unit="mah",
            )

            if (
                battery is None
                or battery < requirements.min_battery_mah
            ):
                return False

        # ---------------------------------------------------------
        # Platform
        # ---------------------------------------------------------
        if requirements.platform:
            searchable_text = str(
                product.get("searchable_text") or ""
            ).lower()

            product_name = str(
                product.get("name") or ""
            ).lower()

            combined = (
                searchable_text
                + " "
                + product_name
            )

            if requirements.platform.lower() not in combined:
                return False

        return True

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

    @staticmethod
    def _parse_number(
        value: Any,
        unit: str,
    ) -> float | None:
        import re

        text = str(value).lower()

        if unit == "gb":
            match = re.search(
                r"(\d+(?:\.\d+)?)\s*gb",
                text,
            )

        elif unit == "mah":
            match = re.search(
                r"(\d+(?:\.\d+)?)\s*mah",
                text,
            )

        else:
            return None

        if not match:
            return None

        return float(match.group(1))