from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "ok"
        assert data["service"] == "CompareX"


def test_get_product():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/products/phone_001"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["product_id"] == "phone_001"
        assert "embedding" not in data


def test_compare():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/compare",
            json={
                "product_id_a": "phone_001",
                "product_id_b": "phone_002",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "product_a" in data
        assert "product_b" in data
        assert "top_level" in data
        assert "specifications" in data


def test_search():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/search",
            json={
                "query": "smartphone with a large battery",
                "limit": 2,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["query"] == (
            "smartphone with a large battery"
        )

        assert len(data["results"]) > 0


def test_ask():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ask",
            json={
                "query": "Which smartphone has the largest battery?",
                "limit": 3,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "answer" in data
        assert len(data["answer"]) > 0
        assert "products" in data