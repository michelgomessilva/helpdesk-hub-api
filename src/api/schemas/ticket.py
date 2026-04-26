from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums import TicketCategory, TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)
    category: TicketCategory
    status: TicketStatus = TicketStatus.OPEN
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketResponse(BaseModel):
    id: UUID
    number: int
    title: str
    description: str
    category: TicketCategory
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
