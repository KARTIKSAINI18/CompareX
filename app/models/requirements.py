from pydantic import BaseModel, Field
from typing import Optional


class ProductRequirements(BaseModel):
    """Structured requirements extracted from a user query."""

    category: str = "smartphone"

    brand: Optional[str] = None
    platform: Optional[str] = None

    max_price: Optional[float] = None
    min_price: Optional[float] = None

    min_ram_gb: Optional[float] = None
    min_storage_gb: Optional[float] = None

    min_battery_mah: Optional[float] = None
    min_rating: Optional[float] = None

    camera_preference: Optional[str] = None
    performance_preference: Optional[str] = None

    budget_currency: str = "INR"

    preferences: list[str] = Field(
        default_factory=list
    )