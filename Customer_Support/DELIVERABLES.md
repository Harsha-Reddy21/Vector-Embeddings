# Customer Support RAG System - Deliverables

This document provides an overview of all the deliverables for the Customer Support RAG System project.

## 1. Complete Support System

### Backend (FastAPI)
- **Core RAG Pipeline**: Implementation of the complete RAG pipeline for ticket processing
- **API Endpoints**: RESTful API for ticket submission, retrieval, and knowledge base management
- **Database**: In-memory database with sample historical tickets and company documentation
- **Categorization**: Automatic ticket categorization using sentence embeddings
- **Confidence Scoring**: Confidence-based escalation logic for human intervention

**Files**:
- `backend/app/core/rag_pipeline.py`: Core RAG pipeline implementation
- `backend/app/core/database.py`: Database models and sample data
- `backend/app/models/ticket.py`: Pydantic models for tickets
- `backend/app/routers/tickets.py`: API endpoints for ticket operations
- `backend/app/routers/knowledge.py`: API endpoints for knowledge base operations
- `backend/app/main.py`: Main FastAPI application
- `backend/main.py`: Entry point for the backend

### Frontend (React)
- **Ticket Submission**: Form for submitting new support tickets
- **Ticket List**: Display of all tickets with filtering by status
- **Ticket Detail**: View of ticket details with AI-generated responses
- **Manual Response**: Interface for adding manual responses to escalated tickets
- **Knowledge Base Management**: Interface for managing historical tickets and company documentation

**Files**:
- `frontend/src/components/TicketForm.js`: Ticket submission form
- `frontend/src/components/TicketList.js`: Ticket list display
- `frontend/src/components/TicketDetail.js`: Ticket detail view
- `frontend/src/pages/HomePage.js`: Home page with ticket form and list
- `frontend/src/pages/TicketDetailPage.js`: Ticket detail page
- `frontend/src/pages/KnowledgeBasePage.js`: Knowledge base management page
- `frontend/src/services/api.js`: API service for backend communication
- `frontend/src/App.js`: Main React application with routing

## 2. RAG Pipeline Integration

The RAG pipeline integrates historical tickets and company knowledge through:

- **Vector Embeddings**: Using Sentence Transformers for semantic representation
- **Vector Database**: ChromaDB for efficient similarity search
- **Semantic Search**: Cosine similarity for finding relevant documents
- **Context Assembly**: Combining retrieved documents for LLM context
- **Response Generation**: Using Groq API with Llama3-70B for generating responses

**Key Integration Points**:
- Historical tickets and solutions are embedded and stored in ChromaDB
- Company documentation is embedded and stored in ChromaDB
- New tickets are embedded and used for similarity search
- Retrieved context is used to generate contextually relevant responses

## 3. Technical Documentation

Comprehensive technical documentation covering:

- **RAG Pipeline Architecture**: Detailed explanation of each component
- **Similarity Matching**: Technical details of embedding model and similarity calculation
- **Confidence Scoring**: Explanation of confidence calculation and escalation logic
- **Response Generation**: Details of context assembly and LLM prompt construction
- **Performance Considerations**: Notes on optimization and caching
- **Scalability**: Recommendations for production deployment

**File**: `TECHNICAL_DOCUMENTATION.md`

## 4. Demo

A demonstration script showcasing the functionality of the system:

- **Knowledge Base Demo**: Retrieving and adding historical tickets and company documentation
- **Ticket Processing Demo**: Processing sample tickets through the RAG pipeline
- **Ticket Details Demo**: Retrieving ticket details and responses

**File**: `demo.py`

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Demo
```bash
python demo.py
```

## Additional Resources

- `README.md`: Main project README with overview and setup instructions
- `backend/README.md`: Backend-specific README
- `frontend/README.md`: Frontend-specific README
- `experiments.ipynb`: Jupyter notebook with RAG pipeline experiments 