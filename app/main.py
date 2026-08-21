# from fastapi import FastAPI

# from app.core.config import settings


# app = FastAPI(
#     title=settings.app_name,
#     version=settings.app_version,
# )


# @app.get("/health")
# def health_check():
#     return {
#         "status": "ok",
#         "service": settings.app_name,
#         "version": settings.app_version,
#     }

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.api.errors import unexpected_error_handler
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import set_comparex_service
from app.api.routes.ask import router as ask_router
from app.api.routes.compare import router as compare_router
from app.api.routes.health import router as health_router
from app.api.routes.products import router as products_router
from app.api.routes.search import router as search_router
from app.services.comparex_service import CompareXService


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = CompareXService()

    set_comparex_service(service)

    yield

    service.close()


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CompareX API",
    description=(
        "AI-powered product comparison "
        "and recommendation API"
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent






app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)


app.include_router(health_router)
app.include_router(products_router)
app.include_router(search_router)
app.include_router(compare_router)
app.include_router(ask_router)