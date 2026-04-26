from abc import ABC, abstractmethod

from domain.entities import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        ...

    @abstractmethod
    def list_all(self) -> list[Category]:
        ...
