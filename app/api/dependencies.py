from typing import Optional

from app.services.comparex_service import CompareXService


_service: Optional[CompareXService] = None


def set_comparex_service(
    service: CompareXService,
) -> None:
    global _service
    _service = service


def get_comparex_service() -> CompareXService:
    if _service is None:
        raise RuntimeError(
            "CompareXService has not been initialized."
        )

    return _service