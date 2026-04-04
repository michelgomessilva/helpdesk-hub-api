from fastapi.testclient import TestClient

from helpdesk_hub_api.main import app


client = TestClient(app)


def test_root_endpoint_returns_project_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "HelpDesk Hub API",
        "status": "ok",
        "docs": "/docs",
    }


def test_health_endpoint_returns_healthy_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
