from datetime import datetime
from uuid import uuid4

from domain.entities import Category
from domain.repositories import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self) -> None:
        self._store: dict = {}

    def save(self, category: Category) -> Category:
        category.id = uuid4()
        category.created_at = datetime.utcnow()
        self._store[category.id] = category
        return category

    def list_all(self) -> list[Category]:
        return list(self._store.values())
