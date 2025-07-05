# Customer Support RAG System - Backend

This is the backend for the Customer Support RAG (Retrieval-Augmented Generation) system. It provides API endpoints for ticket submission, categorization, and response generation.

## Features

- Automatic ticket categorization using sentence embeddings
- RAG pipeline for retrieving relevant historical tickets and company documentation
- LLM-based response generation using Groq API
- Confidence scoring and automatic escalation
- Knowledge base management

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the backend directory with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

3. Run the server:
   ```bash
   python main.py
   ```

4. The API will be available at http://localhost:8000

## API Endpoints

- `GET /`: Root endpoint with API information
- `POST /tickets/`: Submit a new ticket
- `GET /tickets/`: List all tickets
- `GET /tickets/{ticket_id}`: Get details for a specific ticket
- `POST /tickets/{ticket_id}/respond`: Add a manual response to a ticket
- `GET /knowledge/historical-tickets`: List all historical tickets
- `GET /knowledge/company-docs`: List all company documentation
- `POST /knowledge/add-ticket`: Add a new historical ticket to the knowledge base
- `POST /knowledge/add-document`: Add a new company document to the knowledge base

## API Documentation

Interactive API documentation is available at http://localhost:8000/docs 