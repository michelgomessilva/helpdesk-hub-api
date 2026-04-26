from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        ...

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        ...

    @abstractmethod
    def get_by_id(self, ticket_id: UUID) -> Ticket | None:
        ...
