from typing import Any

from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str

    description: str = ""

    specifications: dict[str, Any] = Field(default_factory=dict)

    price: float | None = None
    currency: str = "INR"

    rating: float | None = None
    review_count: int | None = None

    source: str | None = None

    def to_searchable_text(self) -> str:
        specification_text = ", ".join(
            f"{key}: {value}"
            for key, value in self.specifications.items()
        )

        parts = [
            f"Product: {self.name}",
            f"Brand: {self.brand}",
            f"Category: {self.category}",
            f"Description: {self.description}",
            f"Specifications: {specification_text}",
        ]

        if self.price is not None:
            parts.append(f"Price: {self.price} {self.currency}")

        if self.rating is not None:
            parts.append(f"Rating: {self.rating}")

        return "\n".join(parts)