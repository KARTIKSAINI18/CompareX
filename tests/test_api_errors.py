from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.errors import unexpected_error_handler


def test_unexpected_error_handler():
    test_app = FastAPI()

    test_app.add_exception_handler(
        Exception,
        unexpected_error_handler,
    )

    @test_app.get("/error")
    def error():
        raise RuntimeError("internal failure")

    with TestClient(
        test_app,
        raise_server_exceptions=False,
    ) as client:

        response = client.get("/error")

        assert response.status_code == 500

        data = response.json()

        assert data["error"] == "Internal server error"
        assert data["detail"] == (
            "An unexpected error occurred."
        )