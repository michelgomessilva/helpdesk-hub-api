from dataclasses import dataclass
from uuid import UUID

from mediatr.mediator import GenericQuery

from domain.entities import Ticket
from domain.enums import TicketPriority, TicketStatus
from domain.repositories import TicketRepository


@dataclass
class UpdateTicketCommand(GenericQuery[Ticket | None]):
    ticket_id: UUID
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    description: str | None = None


class UpdateTicketHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: UpdateTicketCommand) -> Ticket | None:
        ticket = self._repo.get_by_id(request.ticket_id)
        if not ticket:
            return None

        if request.status is not None:
            ticket.status = request.status
        if request.priority is not None:
            ticket.priority = request.priority
        if request.description is not None:
            ticket.description = request.description

        return ticket
