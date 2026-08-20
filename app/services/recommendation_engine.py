from typing import Any

from app.models.requirements import ProductRequirements


class RecommendationEngine:
    """Rank matched products according to user requirements."""

    def rank(
        self,
        products: list[dict[str, Any]],
        requirements: ProductRequirements,
    ) -> list[dict[str, Any]]:
        ranked = []

        for product in products:
            score = self._calculate_score(
                product,
                requirements,
            )

            product_copy = dict(product)
            product_copy["recommendation_score"] = round(
                score,
                4,
            )

            ranked.append(product_copy)

        ranked.sort(
            key=lambda product: product[
                "recommendation_score"
            ],
            reverse=True,
        )

        return ranked

    def _calculate_score(
        self,
        product: dict[str, Any],
        requirements: ProductRequirements,
    ) -> float:
        score = 0.0

        # ---------------------------------------------------------
        # Semantic relevance
        # ---------------------------------------------------------
        vector_score = product.get("score")

        if vector_score is not None:
            try:
                score += float(vector_score) * 50
            except (TypeError, ValueError):
                pass

        # ---------------------------------------------------------
        # Rating
        # ---------------------------------------------------------
        rating = product.get("rating")

        if rating is not None:
            try:
                rating_score = min(
                    float(rating) / 5.0,
                    1.0,
                )

                score += rating_score * 20
            except (TypeError, ValueError):
                pass

        # ---------------------------------------------------------
        # Brand match
        # ---------------------------------------------------------
        if requirements.brand:
            brand = str(
                product.get("brand") or ""
            ).lower()

            name = str(
                product.get("name") or ""
            ).lower()

            if (
                requirements.brand.lower() in brand
                or requirements.brand.lower() in name
            ):
                score += 10

        # ---------------------------------------------------------
        # Battery preference
        # ---------------------------------------------------------
        if (
            "large battery"
            in requirements.preferences
        ):
            battery = self._extract_spec_number(
                product,
                ["battery"],
                "mah",
            )

            if battery is not None:
                # Normalize around 5000mAh.
                battery_score = min(
                    battery / 5000.0,
                    1.0,
                )

                score += battery_score * 10

        # ---------------------------------------------------------
        # Camera preference
        # ---------------------------------------------------------
        if requirements.camera_preference:
            searchable_text = str(
                product.get("searchable_text") or ""
            ).lower()

            specifications = product.get(
                "specifications"
            )

            camera_text = ""

            if isinstance(specifications, dict):
                for key, value in specifications.items():
                    if "camera" in str(key).lower():
                        camera_text += (
                            " "
                            + str(value).lower()
                        )

            camera_text += " " + searchable_text

            if "camera" in camera_text:
                score += 5

            megapixel = self._extract_megapixel(
                camera_text
            )

            if megapixel is not None:
                score += min(
                    megapixel / 100.0,
                    1.0,
                ) * 5

        # ---------------------------------------------------------
        # Performance preference
        # ---------------------------------------------------------
        if requirements.performance_preference:
            searchable_text = str(
                product.get("searchable_text") or ""
            ).lower()

            performance_terms = [
                "snapdragon",
                "mediatek",
                "dimensity",
                "gaming",
                "octa-core",
                "8 gen",
                "pro processor",
                "bionic",
            ]

            matches = sum(
                term in searchable_text
                for term in performance_terms
            )

            score += min(matches, 3) * 2

        return score

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

        if isinstance(specifications, dict):
            for key, value in specifications.items():
                key_text = str(key).lower()

                if not any(
                    candidate in key_text
                    for candidate in keys
                ):
                    continue

                match = re.search(
                    rf"(\d+(?:\.\d+)?)\s*{unit}",
                    str(value).lower(),
                )

                if match:
                    return float(match.group(1))

        text = str(
            product.get("searchable_text") or ""
        ).lower()

        for key in keys:
            index = text.find(key)

            if index == -1:
                continue

            section = text[index:index + 100]

            match = re.search(
                rf"(\d+(?:\.\d+)?)\s*{unit}",
                section,
            )

            if match:
                return float(match.group(1))

        return None

    @staticmethod
    def _extract_megapixel(
        text: str,
    ) -> float | None:
        import re

        match = re.search(
            r"(\d+(?:\.\d+)?)\s*mp",
            text,
        )

        if not match:
            return None

        return float(match.group(1))