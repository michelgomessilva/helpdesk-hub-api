import pytest

from application.tickets.queries.list_tickets import ListTicketsHandler, ListTicketsQuery
from domain.enums import TicketCategory, TicketPriority, TicketStatus
from domain.entities import Ticket
from infrastructure.repositories import InMemoryTicketRepository


@pytest.mark.asyncio
async def test_list_tickets_handler_returns_empty_list_on_no_tickets() -> None:
    """F011: ListTicketsHandler returns empty list when repository is empty"""
    repo = InMemoryTicketRepository()
    handler = ListTicketsHandler(repo)
    query = ListTicketsQuery()

    result = await handler.handle(query)

    assert result == []


@pytest.mark.asyncio
async def test_list_tickets_handler_returns_all_tickets() -> None:
    """F011: ListTicketsHandler returns all tickets from repository"""
    repo = InMemoryTicketRepository()
    ticket1 = Ticket(
        title="Test ticket 1",
        description="Test description 1",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )
    ticket2 = Ticket(
        title="Test ticket 2",
        description="Test description 2",
        category=TicketCategory.SOFTWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.HIGH,
    )

    saved_ticket1 = repo.save(ticket1)
    saved_ticket2 = repo.save(ticket2)
    handler = ListTicketsHandler(repo)
    query = ListTicketsQuery()

    result = await handler.handle(query)

    assert len(result) == 2
    assert result[0].id == saved_ticket1.id
    assert result[1].id == saved_ticket2.id
    assert result[0].title == "Test ticket 1"
    assert result[1].title == "Test ticket 2"


@pytest.mark.asyncio
async def test_list_tickets_handler_preserves_ticket_properties() -> None:
    """F011: ListTicketsHandler preserves all ticket properties"""
    repo = InMemoryTicketRepository()
    ticket = Ticket(
        title="Important ticket",
        description="Very important description",
        category=TicketCategory.NETWORK,
        status=TicketStatus.IN_PROGRESS,
        priority=TicketPriority.URGENT,
    )

    saved_ticket = repo.save(ticket)
    handler = ListTicketsHandler(repo)
    query = ListTicketsQuery()

    result = await handler.handle(query)

    assert len(result) == 1
    assert result[0].title == "Important ticket"
    assert result[0].description == "Very important description"
    assert result[0].category == TicketCategory.NETWORK
    assert result[0].status == TicketStatus.IN_PROGRESS
    assert result[0].priority == TicketPriority.URGENT
