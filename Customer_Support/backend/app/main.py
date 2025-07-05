from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tickets, knowledge
from .core.rag_pipeline import RAGPipeline
from .core.database import get_historical_tickets, get_company_docs

app = FastAPI(
    title="Customer Support RAG System",
    description="Intelligent customer support system using RAG architecture",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tickets.router)
app.include_router(knowledge.router)

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG pipeline with sample data on startup"""
    pipeline = RAGPipeline()
    
    # Load sample data into vector database
    historical_tickets = get_historical_tickets()
    company_docs = get_company_docs()
    
    pipeline.store_knowledge(tickets=historical_tickets, docs=company_docs)
    print(f"Loaded {len(historical_tickets)} historical tickets and {len(company_docs)} company documents into the knowledge base")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Support RAG API is running",
        "docs_url": "/docs",
        "endpoints": {
            "tickets": "/tickets",
            "knowledge": "/knowledge"
        }
    } 