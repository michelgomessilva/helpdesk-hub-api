from dataclasses import dataclass

from mediatr.mediator import GenericQuery

from domain.entities import Ticket
from domain.repositories import TicketRepository


@dataclass
class ListTicketsQuery(GenericQuery[list[Ticket]]):
    pass


class ListTicketsHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: ListTicketsQuery) -> list[Ticket]:
        return self._repo.list_all()
