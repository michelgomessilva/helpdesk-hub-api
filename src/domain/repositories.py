from abc import ABC, abstractmethod

from domain.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        ...

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        ...
