import re

from app.models.requirements import ProductRequirements


class RequirementExtractor:
    """Extract common smartphone requirements from user queries."""

    def extract(self, query: str) -> ProductRequirements:
        text = query.lower()

        requirements = ProductRequirements()

        # ---------------------------------------------------------
        # Brand
        # ---------------------------------------------------------
        brands = [
            "samsung",
            "apple",
            "oneplus",
            "google",
            "motorola",
            "xiaomi",
            "redmi",
            "realme",
            "oppo",
            "vivo",
            "nokia",
            "sony",
            "asus",
        ]

        for brand in brands:
            if brand in text:
                requirements.brand = brand
                break

        # ---------------------------------------------------------
        # Platform
        # ---------------------------------------------------------
        if "android" in text:
            requirements.platform = "android"
        elif "iphone" in text or "ios" in text:
            requirements.platform = "ios"

        # ---------------------------------------------------------
        # Maximum price
        # ---------------------------------------------------------
        price_patterns = [
            r"(?:under|below|less than|max(?:imum)?|up to)\s*[₹rs.]?\s*([\d,]+)",
            r"[₹rs.]\s*([\d,]+)\s*(?:budget|max|maximum)?",
        ]

        for pattern in price_patterns:
            match = re.search(pattern, text)

            if match:
                value = match.group(1).replace(",", "")
                requirements.max_price = float(value)
                break

        # ---------------------------------------------------------
        # RAM
        # ---------------------------------------------------------
        ram_match = re.search(
            r"(?:at least|minimum|min)?\s*(\d+)\s*gb\s*ram",
            text,
        )

        if ram_match:
            requirements.min_ram_gb = float(
                ram_match.group(1)
            )

        # ---------------------------------------------------------
        # Storage
        # ---------------------------------------------------------
        storage_match = re.search(
            r"(?:at least|minimum|min)?\s*(\d+)\s*gb\s*(?:storage|rom)",
            text,
        )

        if storage_match:
            requirements.min_storage_gb = float(
                storage_match.group(1)
            )

        # ---------------------------------------------------------
        # Battery
        # ---------------------------------------------------------
        battery_match = re.search(
            r"(\d{4,5})\s*mah",
            text,
        )

        if battery_match:
            requirements.min_battery_mah = float(
                battery_match.group(1)
            )

        elif any(
            phrase in text
            for phrase in [
                "large battery",
                "big battery",
                "long battery",
                "long lasting battery",
            ]
        ):
            requirements.preferences.append(
                "large battery"
            )

        # ---------------------------------------------------------
        # Rating
        # ---------------------------------------------------------
        rating_match = re.search(
            r"(?:rating|rated)\s*(?:of|above|over|at least)?\s*(\d(?:\.\d)?)",
            text,
        )

        if rating_match:
            requirements.min_rating = float(
                rating_match.group(1)
            )

        # ---------------------------------------------------------
        # Camera
        # ---------------------------------------------------------
        if any(
            phrase in text
            for phrase in [
                "good camera",
                "great camera",
                "best camera",
                "camera quality",
            ]
        ):
            requirements.camera_preference = "good"

        # ---------------------------------------------------------
        # Performance
        # ---------------------------------------------------------
        if any(
            phrase in text
            for phrase in [
                "good performance",
                "high performance",
                "powerful",
                "gaming",
                "fast performance",
            ]
        ):
            requirements.performance_preference = "high"

        return requirements