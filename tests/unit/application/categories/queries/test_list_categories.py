import pytest

from domain.entities import Category
from domain.repositories import CategoryRepository
from application.categories.queries.list_categories import ListCategoriesQuery, ListCategoriesHandler


class MockCategoryRepository(CategoryRepository):
    def __init__(self):
        self.categories = {}

    def save(self, category: Category) -> Category:
        self.categories[category.id] = category
        return category

    def list_all(self) -> list[Category]:
        return list(self.categories.values())


@pytest.fixture
def repository():
    return MockCategoryRepository()


@pytest.mark.asyncio
async def test_list_empty_categories(repository):
    handler = ListCategoriesHandler(repository)
    query = ListCategoriesQuery()
    result = await handler.handle(query)
    assert result == []


@pytest.mark.asyncio
async def test_list_single_category(repository):
    category = Category(name="Hardware", description="Hardware issues")
    repository.save(category)
    handler = ListCategoriesHandler(repository)
    query = ListCategoriesQuery()
    result = await handler.handle(query)
    assert len(result) == 1
    assert result[0].name == "Hardware"


@pytest.mark.asyncio
async def test_list_multiple_categories(repository):
    cat1 = Category(name="Hardware", description="Hardware issues")
    cat2 = Category(name="Software", description="Software issues")
    cat3 = Category(name="Network", description="Network issues")
    repository.save(cat1)
    repository.save(cat2)
    repository.save(cat3)
    handler = ListCategoriesHandler(repository)
    query = ListCategoriesQuery()
    result = await handler.handle(query)
    assert len(result) == 3
    assert all(isinstance(c, Category) for c in result)
