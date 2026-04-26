import pytest
from uuid import uuid4

from application.tickets.queries.get_ticket_by_id import GetTicketByIdHandler, GetTicketByIdQuery
from domain.enums import TicketCategory, TicketPriority, TicketStatus
from domain.entities import Ticket
from infrastructure.repositories import InMemoryTicketRepository


@pytest.mark.asyncio
async def test_get_ticket_by_id_handler_returns_ticket_when_exists() -> None:
    """F012: GetTicketByIdHandler returns ticket when it exists"""
    repo = InMemoryTicketRepository()
    ticket = Ticket(
        title="Test ticket",
        description="Test description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )

    saved_ticket = repo.save(ticket)
    handler = GetTicketByIdHandler(repo)
    query = GetTicketByIdQuery(ticket_id=saved_ticket.id)

    result = await handler.handle(query)

    assert result is not None
    assert result.id == saved_ticket.id
    assert result.title == "Test ticket"
    assert result.description == "Test description"


@pytest.mark.asyncio
async def test_get_ticket_by_id_handler_returns_none_when_not_found() -> None:
    """F012: GetTicketByIdHandler returns None when ticket doesn't exist"""
    repo = InMemoryTicketRepository()
    fake_id = uuid4()
    handler = GetTicketByIdHandler(repo)
    query = GetTicketByIdQuery(ticket_id=fake_id)

    result = await handler.handle(query)

    assert result is None


@pytest.mark.asyncio
async def test_get_ticket_by_id_handler_preserves_all_properties() -> None:
    """F012: GetTicketByIdHandler preserves all ticket properties"""
    repo = InMemoryTicketRepository()
    ticket = Ticket(
        title="Important ticket",
        description="Very important description",
        category=TicketCategory.NETWORK,
        status=TicketStatus.IN_PROGRESS,
        priority=TicketPriority.URGENT,
    )

    saved_ticket = repo.save(ticket)
    handler = GetTicketByIdHandler(repo)
    query = GetTicketByIdQuery(ticket_id=saved_ticket.id)

    result = await handler.handle(query)

    assert result is not None
    assert result.title == "Important ticket"
    assert result.description == "Very important description"
    assert result.category == TicketCategory.NETWORK
    assert result.status == TicketStatus.IN_PROGRESS
    assert result.priority == TicketPriority.URGENT
    assert result.number == 1
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_get_ticket_by_id_handler_finds_correct_ticket_among_many() -> None:
    """F012: GetTicketByIdHandler finds correct ticket among multiple"""
    repo = InMemoryTicketRepository()
    ticket1 = Ticket(
        title="Ticket 1",
        description="Description 1",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )
    ticket2 = Ticket(
        title="Ticket 2",
        description="Description 2",
        category=TicketCategory.SOFTWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.HIGH,
    )
    ticket3 = Ticket(
        title="Ticket 3",
        description="Description 3",
        category=TicketCategory.NETWORK,
        status=TicketStatus.CLOSED,
        priority=TicketPriority.LOW,
    )

    saved_ticket1 = repo.save(ticket1)
    saved_ticket2 = repo.save(ticket2)
    saved_ticket3 = repo.save(ticket3)

    handler = GetTicketByIdHandler(repo)
    query = GetTicketByIdQuery(ticket_id=saved_ticket2.id)

    result = await handler.handle(query)

    assert result is not None
    assert result.id == saved_ticket2.id
    assert result.title == "Ticket 2"
    assert result.number == 2
