from datetime import datetime
from uuid import UUID, uuid4

from domain.entities import Ticket
from domain.repositories import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    def __init__(self) -> None:
        self._store: dict = {}
        self._next_number: int = 1

    def save(self, ticket: Ticket) -> Ticket:
        ticket.id = uuid4()
        ticket.number = self._next_number
        ticket.created_at = datetime.utcnow()
        self._next_number += 1
        self._store[ticket.id] = ticket
        return ticket

    def list_all(self) -> list[Ticket]:
        return list(self._store.values())

    def get_by_id(self, ticket_id: UUID) -> Ticket | None:
        return self._store.get(ticket_id)
