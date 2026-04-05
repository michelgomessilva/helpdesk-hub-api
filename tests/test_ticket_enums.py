from datetime import datetime

from pydantic import ValidationError

from helpdesk_hub_api.schemas.ticket import TicketCreate, TicketResponse


def test_ticket_create_accepts_valid_status_and_priority_values() -> None:
    ticket = TicketCreate(
        title="Printer not working",
        description="The office printer stopped responding.",
        category="hardware",
        status="open",
        priority="high",
    )

    assert ticket.status.value == "open"
    assert ticket.priority.value == "high"
    assert ticket.category.value == "hardware"


def test_ticket_create_rejects_invalid_status() -> None:
    try:
        TicketCreate(
            title="Email issue",
            description="Mailbox is unavailable.",
            category="access",
            status="invalid-status",
            priority="medium",
        )
    except ValidationError as exc:
        assert "status" in str(exc)
    else:
        raise AssertionError("Expected ValidationError for invalid status")


def test_ticket_create_rejects_invalid_priority() -> None:
    try:
        TicketCreate(
            title="VPN issue",
            description="Cannot connect to VPN.",
            category="network",
            status="open",
            priority="super-high",
        )
    except ValidationError as exc:
        assert "priority" in str(exc)
    else:
        raise AssertionError("Expected ValidationError for invalid priority")


def test_ticket_create_rejects_invalid_category() -> None:
    try:
        TicketCreate(
            title="Unknown category",
            description="Category should be validated.",
            category="random",
            status="open",
            priority="low",
        )
    except ValidationError as exc:
        assert "category" in str(exc)
    else:
        raise AssertionError("Expected ValidationError for invalid category")


def test_ticket_create_rejects_blank_title() -> None:
    try:
        TicketCreate(
            title="",
            description="Blank title should not be accepted.",
            category="hardware",
            status="open",
            priority="low",
        )
    except ValidationError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("Expected ValidationError for blank title")


def test_ticket_response_exposes_consistent_contract() -> None:
    ticket = TicketResponse(
        id=1,
        title="Printer not working",
        description="The office printer stopped responding.",
        category="hardware",
        status="open",
        priority="high",
        created_at=datetime(2026, 4, 5, 22, 0, 0),
    )

    assert ticket.id == 1
    assert ticket.category.value == "hardware"
    assert ticket.status.value == "open"
    assert ticket.priority.value == "high"
