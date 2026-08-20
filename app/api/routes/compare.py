from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_comparex_service
from app.api.schemas import (
    CompareRequest,
    CompareResponse,
)
from app.services.comparex_service import CompareXService


router = APIRouter(
    prefix="/api/v1/compare",
    tags=["Comparison"],
)


@router.post(
    "",
    response_model=CompareResponse,
)
def compare_products(
    request: CompareRequest,
    service: CompareXService = Depends(
        get_comparex_service
    ),
):

    try:
        result = service.compare(
            product_id_a=request.product_id_a,
            product_id_b=request.product_id_b,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return result