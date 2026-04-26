from dataclasses import dataclass
from uuid import UUID

from mediatr.mediator import GenericQuery

from domain.entities import Ticket
from domain.repositories import TicketRepository


@dataclass
class GetTicketByIdQuery(GenericQuery[Ticket | None]):
    ticket_id: UUID


class GetTicketByIdHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: GetTicketByIdQuery) -> Ticket | None:
        return self._repo.get_by_id(request.ticket_id)
