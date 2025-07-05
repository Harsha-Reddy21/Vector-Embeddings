from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any

from ..models.ticket import Ticket, TicketResponse
from ..core.rag_pipeline import RAGPipeline
from ..core.database import (
    create_ticket, get_ticket, get_all_tickets, update_ticket, 
    save_response, get_ticket_responses
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

@router.post("/", response_model=Dict[str, Any])
async def submit_ticket(ticket: Ticket):
    """Submit a new support ticket"""
    # Create the ticket in the database
    ticket_data = ticket.model_dump()
    created_ticket = create_ticket(ticket_data)
    
    # Process the ticket through the RAG pipeline
    result = rag_pipeline.process_ticket(ticket)
    
    # Update the ticket with category and confidence
    update_ticket(created_ticket["id"], {
        "category": result["category"],
        "confidence": result["confidence"],
        "status": "auto_resolved" if result["auto_resolved"] else "escalated"
    })
    
    # Save the response
    response_data = {
        "ticket_id": created_ticket["id"],
        "response": result["response"],
        "sources": result["sources"],
        "confidence": result["confidence"],
        "auto_resolved": result["auto_resolved"]
    }
    saved_response = save_response(response_data)
    
    # Return the combined result
    return {
        "ticket": get_ticket(created_ticket["id"]),
        "response": saved_response
    }

@router.get("/", response_model=List[Dict[str, Any]])
async def list_tickets():
    """Get all tickets"""
    return get_all_tickets()

@router.get("/{ticket_id}", response_model=Dict[str, Any])
async def get_ticket_details(ticket_id: str):
    """Get details for a specific ticket"""
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get responses for this ticket
    responses = get_ticket_responses(ticket_id)
    
    return {
        "ticket": ticket,
        "responses": responses
    }

@router.post("/{ticket_id}/respond", response_model=Dict[str, Any])
async def manual_respond(ticket_id: str, response_data: Dict[str, str]):
    """Add a manual response to a ticket"""
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Save the manual response
    response = {
        "ticket_id": ticket_id,
        "response": response_data["response"],
        "sources": [],
        "confidence": 1.0,
        "auto_resolved": False,
        "is_manual": True
    }
    saved_response = save_response(response)
    
    # Update ticket status
    update_ticket(ticket_id, {"status": "resolved"})
    
    return saved_response 