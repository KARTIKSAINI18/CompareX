from fastapi import APIRouter, Depends

from app.api.dependencies import get_comparex_service
from app.api.schemas import AskRequest, AskResponse
from app.services.comparex_service import CompareXService


router = APIRouter(
    prefix="/api/v1/ask",
    tags=["AI"],
)


@router.post(
    "",
    response_model=AskResponse,
)
def ask(
    request: AskRequest,
    service: CompareXService = Depends(
        get_comparex_service
    ),
):

    result = service.answer_query(
        query=request.query,
        final_limit=request.limit,
    )

    return result