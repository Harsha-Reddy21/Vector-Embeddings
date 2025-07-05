from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Ticket(BaseModel):
    id: Optional[str] = None
    text: str
    customer_id: str
    submitted_at: Optional[datetime] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "pending"  # pending, in_progress, resolved, escalated
    
class TicketResponse(BaseModel):
    ticket_id: str
    response: str
    sources: List[dict]
    confidence: float
    auto_resolved: bool 