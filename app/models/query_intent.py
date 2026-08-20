from enum import Enum

from pydantic import BaseModel, Field


class QueryIntentType(str, Enum):
    SEARCH = "search"
    RECOMMEND = "recommend"
    COMPARE = "compare"
    FIND_BEST = "find_best"


class ComparisonField(str, Enum):
    BATTERY = "battery"
    RAM = "ram"
    STORAGE = "storage"
    RATING = "rating"
    PRICE = "price"


class QueryIntent(BaseModel):
    intent: QueryIntentType = QueryIntentType.SEARCH

    comparison_field: ComparisonField | None = None

    comparison_direction: str = "max"

    requirements: dict = Field(
        default_factory=dict
    )