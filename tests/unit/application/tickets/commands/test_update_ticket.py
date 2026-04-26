import pytest
from uuid import uuid4

from domain.entities import Ticket
from domain.enums import TicketCategory, TicketPriority, TicketStatus
from domain.repositories import TicketRepository
from application.tickets.commands.update_ticket import UpdateTicketCommand, UpdateTicketHandler


class MockTicketRepository(TicketRepository):
    def __init__(self):
        self.tickets = {}
        self.counter = 0

    def save(self, ticket: Ticket) -> Ticket:
        ticket.number = self.counter + 1
        self.counter += 1
        self.tickets[ticket.id] = ticket
        return ticket

    def list_all(self) -> list[Ticket]:
        return list(self.tickets.values())

    def get_by_id(self, ticket_id) -> Ticket | None:
        return self.tickets.get(ticket_id)


@pytest.fixture
def repository():
    return MockTicketRepository()


@pytest.fixture
async def ticket_with_data(repository):
    ticket = Ticket(
        title="Test Ticket",
        description="Original description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.LOW,
    )
    return repository.save(ticket)


@pytest.mark.asyncio
async def test_update_ticket_status(repository, ticket_with_data):
    handler = UpdateTicketHandler(repository)
    command = UpdateTicketCommand(
        ticket_id=ticket_with_data.id,
        status=TicketStatus.IN_PROGRESS,
    )
    result = await handler.handle(command)
    assert result is not None
    assert result.status == TicketStatus.IN_PROGRESS
    assert result.description == ticket_with_data.description


@pytest.mark.asyncio
async def test_update_ticket_priority(repository, ticket_with_data):
    handler = UpdateTicketHandler(repository)
    command = UpdateTicketCommand(
        ticket_id=ticket_with_data.id,
        priority=TicketPriority.HIGH,
    )
    result = await handler.handle(command)
    assert result is not None
    assert result.priority == TicketPriority.HIGH
    assert result.status == ticket_with_data.status


@pytest.mark.asyncio
async def test_update_ticket_description(repository, ticket_with_data):
    handler = UpdateTicketHandler(repository)
    new_description = "Updated description"
    command = UpdateTicketCommand(
        ticket_id=ticket_with_data.id,
        description=new_description,
    )
    result = await handler.handle(command)
    assert result is not None
    assert result.description == new_description


@pytest.mark.asyncio
async def test_update_ticket_multiple_fields(repository, ticket_with_data):
    handler = UpdateTicketHandler(repository)
    command = UpdateTicketCommand(
        ticket_id=ticket_with_data.id,
        status=TicketStatus.CLOSED,
        priority=TicketPriority.HIGH,
        description="Closed ticket",
    )
    result = await handler.handle(command)
    assert result is not None
    assert result.status == TicketStatus.CLOSED
    assert result.priority == TicketPriority.HIGH
    assert result.description == "Closed ticket"


@pytest.mark.asyncio
async def test_update_ticket_not_found(repository):
    handler = UpdateTicketHandler(repository)
    command = UpdateTicketCommand(
        ticket_id=uuid4(),
        status=TicketStatus.CLOSED,
    )
    result = await handler.handle(command)
    assert result is None
