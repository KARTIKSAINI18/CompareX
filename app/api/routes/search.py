from fastapi import APIRouter, Depends

from app.api.dependencies import get_comparex_service
from app.api.schemas import SearchRequest, SearchResponse
from app.services.comparex_service import CompareXService


router = APIRouter(
    prefix="/api/v1/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
def search_products(
    request: SearchRequest,
    service: CompareXService = Depends(
        get_comparex_service
    ),
):

    results = service.search(
        query=request.query,
        limit=request.limit,
    )

    cleaned_results = []

    for result in results:
        cleaned_results.append(
            {
                "product_id": result["product_id"],
                "name": result["name"],
                "brand": result["brand"],
                "category": result["category"],
                "price": result["price"],
                "currency": result["currency"],
                "rating": result["rating"],
                "score": result["score"],
            }
        )

    return {
        "query": request.query,
        "results": cleaned_results,
    }