from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app, create_app


client = TestClient(app)


def test_create_app_returns_fastapi_instance() -> None:
    created_app = create_app()

    assert isinstance(created_app, FastAPI)
    assert created_app.title == "HelpDesk Hub API"


def test_application_includes_api_router_endpoints() -> None:
    created_app = create_app()
    registered_paths = {route.path for route in created_app.routes}

    assert "/api/v1/" in registered_paths
    assert "/api/v1/health" in registered_paths


def test_root_endpoint_returns_project_metadata() -> None:
    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "HelpDesk Hub API",
        "status": "ok",
        "docs": "/docs",
    }


def test_health_endpoint_returns_healthy_status() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
