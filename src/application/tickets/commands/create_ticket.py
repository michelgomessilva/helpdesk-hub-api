from dataclasses import dataclass

from mediatr.mediator import GenericQuery

from domain.entities import Ticket
from domain.repositories import TicketRepository


@dataclass
class CreateTicketCommand(GenericQuery[Ticket]):
    title: str
    description: str
    category: str
    status: str
    priority: str


class CreateTicketHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: CreateTicketCommand) -> Ticket:
        raise NotImplementedError
