import pytest

from infrastructure.repositories import InMemoryTicketRepository


@pytest.fixture
def ticket_repository() -> InMemoryTicketRepository:
    """Provide a fresh InMemoryTicketRepository for each test"""
    return InMemoryTicketRepository()
