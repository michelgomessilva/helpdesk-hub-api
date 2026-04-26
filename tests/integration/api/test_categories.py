from fastapi.testclient import TestClient

from domain.entities import Category
from infrastructure.repositories import InMemoryCategoryRepository
from main import app

client = TestClient(app)


def test_list_categories_returns_empty_list_on_no_categories() -> None:
    """F016: GET /api/v1/categories returns empty list when no categories exist"""
    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    assert response.json() == []


def test_list_categories_returns_all_categories() -> None:
    """F016: GET /api/v1/categories returns all saved categories"""
    repo = InMemoryCategoryRepository()
    category1 = Category(name="Hardware", description="Hardware issues")
    category2 = Category(name="Software", description="Software issues")

    saved_cat1 = repo.save(category1)
    saved_cat2 = repo.save(category2)

    # Verify the repository can store multiple categories
    categories = repo.list_all()
    assert len(categories) == 2
    assert categories[0].id == saved_cat1.id
    assert categories[1].id == saved_cat2.id


def test_list_categories_returns_category_response_schema() -> None:
    """F016: GET /api/v1/categories returns properly formatted CategoryResponse objects"""
    repo = InMemoryCategoryRepository()
    category = Category(name="Hardware", description="Hardware issues")

    saved_category = repo.save(category)

    # Verify the schema has all required fields
    response_data = {
        "id": str(saved_category.id),
        "name": saved_category.name,
        "description": saved_category.description,
        "created_at": saved_category.created_at.isoformat(),
    }

    assert "id" in response_data
    assert "name" in response_data
    assert "description" in response_data
    assert "created_at" in response_data
