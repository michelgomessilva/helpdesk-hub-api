from uuid import UUID

from domain.enums import TicketCategory, TicketPriority, TicketStatus
from domain.entities import Ticket
from infrastructure.repositories import InMemoryTicketRepository


def test_save_assigns_uuid_id() -> None:
    repo = InMemoryTicketRepository()
    ticket = Ticket(
        title="Test ticket",
        description="Test description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )

    saved_ticket = repo.save(ticket)

    assert isinstance(saved_ticket.id, UUID)
    assert str(saved_ticket.id) != ""


def test_save_assigns_sequential_number() -> None:
    repo = InMemoryTicketRepository()
    ticket = Ticket(
        title="Test ticket",
        description="Test description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )

    saved_ticket = repo.save(ticket)

    assert saved_ticket.number == 1


def test_save_two_tickets_have_different_ids() -> None:
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

    assert saved_ticket1.id != saved_ticket2.id


def test_save_two_tickets_have_sequential_numbers() -> None:
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

    assert saved_ticket1.number == 1
    assert saved_ticket2.number == 2


def test_list_all_returns_empty_on_new_repository() -> None:
    repo = InMemoryTicketRepository()

    tickets = repo.list_all()

    assert tickets == []


def test_list_all_returns_all_saved_tickets() -> None:
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

    repo.save(ticket1)
    repo.save(ticket2)
    tickets = repo.list_all()

    assert len(tickets) == 2
    assert tickets[0].number == 1
    assert tickets[1].number == 2
    assert tickets[0].title == "Test ticket 1"
    assert tickets[1].title == "Test ticket 2"


def test_repositories_have_independent_counters() -> None:
    repo1 = InMemoryTicketRepository()
    repo2 = InMemoryTicketRepository()

    ticket1_r1 = Ticket(
        title="Repo1 ticket 1",
        description="Description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )
    ticket1_r2 = Ticket(
        title="Repo2 ticket 1",
        description="Description",
        category=TicketCategory.HARDWARE,
        status=TicketStatus.OPEN,
        priority=TicketPriority.MEDIUM,
    )

    saved1 = repo1.save(ticket1_r1)
    saved2 = repo2.save(ticket1_r2)

    assert saved1.number == 1
    assert saved2.number == 1
