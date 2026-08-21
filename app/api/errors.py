from fastapi import Request
from fastapi.responses import JSONResponse


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
):
    import traceback
    tb_str = traceback.format_exc()
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) + "\n\n" + tb_str,
        },
    )