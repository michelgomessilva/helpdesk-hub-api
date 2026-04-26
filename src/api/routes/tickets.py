from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.schemas.tickets import TicketResponse, TicketUpdate
from application.tickets.commands.update_ticket import UpdateTicketCommand, UpdateTicketHandler
from application.tickets.queries.get_ticket_by_id import GetTicketByIdHandler, GetTicketByIdQuery
from application.tickets.queries.list_tickets import ListTicketsHandler, ListTicketsQuery
from infrastructure.repositories import InMemoryTicketRepository

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Shared repository instance
_ticket_repository = InMemoryTicketRepository()


@router.get("/", response_model=list[TicketResponse])
async def list_tickets() -> list[TicketResponse]:
    """List all tickets"""
    handler = ListTicketsHandler(_ticket_repository)
    query = ListTicketsQuery()
    tickets = await handler.handle(query)
    return [
        TicketResponse(
            id=ticket.id,
            number=ticket.number,
            title=ticket.title,
            description=ticket.description,
            category=ticket.category,
            status=ticket.status,
            priority=ticket.priority,
            created_at=ticket.created_at,
        )
        for ticket in tickets
    ]


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket_by_id(ticket_id: UUID) -> TicketResponse:
    """Get a ticket by ID"""
    handler = GetTicketByIdHandler(_ticket_repository)
    query = GetTicketByIdQuery(ticket_id=ticket_id)
    ticket = await handler.handle(query)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse(
        id=ticket.id,
        number=ticket.number,
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        status=ticket.status,
        priority=ticket.priority,
        created_at=ticket.created_at,
    )


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: UUID, payload: TicketUpdate) -> TicketResponse:
    """Update a ticket (status, priority, description)"""
    handler = UpdateTicketHandler(_ticket_repository)
    command = UpdateTicketCommand(
        ticket_id=ticket_id,
        status=payload.status,
        priority=payload.priority,
        description=payload.description,
    )
    ticket = await handler.handle(command)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse(
        id=ticket.id,
        number=ticket.number,
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        status=ticket.status,
        priority=ticket.priority,
        created_at=ticket.created_at,
    )
