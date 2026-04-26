from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.enums import TicketCategory, TicketPriority, TicketStatus


@dataclass
class Ticket:
    title: str
    description: str
    category: TicketCategory
    status: TicketStatus
    priority: TicketPriority
    id: UUID = field(default_factory=uuid4)
    number: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
