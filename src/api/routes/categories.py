from fastapi import APIRouter

from api.schemas.category import CategoryResponse
from application.categories.queries.list_categories import ListCategoriesHandler, ListCategoriesQuery
from infrastructure.repositories import InMemoryCategoryRepository

router = APIRouter(prefix="/categories", tags=["categories"])

# Shared repository instance
_category_repository = InMemoryCategoryRepository()


@router.get("/", response_model=list[CategoryResponse])
async def list_categories() -> list[CategoryResponse]:
    """List all categories"""
    handler = ListCategoriesHandler(_category_repository)
    query = ListCategoriesQuery()
    categories = await handler.handle(query)
    return [
        CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
        )
        for category in categories
    ]
