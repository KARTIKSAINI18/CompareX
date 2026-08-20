from typing import Any

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    price: float | None = None
    currency: str
    rating: float
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


class CompareRequest(BaseModel):
    product_id_a: str
    product_id_b: str


class CompareResponse(BaseModel):
    product_a: str
    product_b: str
    top_level: dict[str, Any]
    specifications: dict[str, Any]


class AskRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=10)


class AskResponse(BaseModel):
    query: str
    answer: str
    products: list[dict[str, Any]]
    documents: list[dict[str, Any]] = Field(
        default_factory=list
    )