from dataclasses import dataclass

from mediatr.mediator import GenericQuery

from domain.entities import Category
from domain.repositories import CategoryRepository


@dataclass
class ListCategoriesQuery(GenericQuery[list[Category]]):
    pass


class ListCategoriesHandler:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo = repo

    async def handle(self, request: ListCategoriesQuery) -> list[Category]:
        return self._repo.list_all()
