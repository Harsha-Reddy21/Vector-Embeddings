from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any

from ..core.rag_pipeline import RAGPipeline
from ..core.database import get_historical_tickets, get_company_docs

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

@router.get("/historical-tickets", response_model=List[Dict[str, Any]])
async def list_historical_tickets():
    """Get all historical tickets"""
    return get_historical_tickets()

@router.get("/company-docs", response_model=List[Dict[str, Any]])
async def list_company_docs():
    """Get all company documentation"""
    return get_company_docs()

@router.post("/add-ticket", response_model=Dict[str, str])
async def add_historical_ticket(ticket_data: Dict[str, str]):
    """Add a new historical ticket to the knowledge base"""
    if "text" not in ticket_data or "solution" not in ticket_data:
        raise HTTPException(status_code=400, detail="Both text and solution are required")
    
    # Add to vector database
    rag_pipeline.store_knowledge(tickets=[ticket_data])
    
    return {"status": "success", "message": "Historical ticket added to knowledge base"}

@router.post("/add-document", response_model=Dict[str, str])
async def add_company_document(doc_data: Dict[str, str]):
    """Add a new company document to the knowledge base"""
    if "title" not in doc_data or "content" not in doc_data:
        raise HTTPException(status_code=400, detail="Both title and content are required")
    
    # Add to vector database
    rag_pipeline.store_knowledge(docs=[doc_data])
    
    return {"status": "success", "message": "Company document added to knowledge base"} 