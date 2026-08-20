from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_comparex_service
from app.services.comparex_service import CompareXService


router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


@router.get("/{product_id}")
def get_product(
    product_id: str,
    service: CompareXService = Depends(
        get_comparex_service
    ),
):
    product = service.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    product.pop("embedding", None)
    product.pop("_id", None)

    return product