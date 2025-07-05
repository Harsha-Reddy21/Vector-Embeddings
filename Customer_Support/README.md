# Customer Support RAG System

An intelligent customer support system that automatically categorizes incoming tickets and generates smart responses using RAG (Retrieval-Augmented Generation) architecture. The system analyzes historical tickets and company knowledge base to provide contextually relevant solutions.

## Project Structure

- `backend/`: FastAPI backend with RAG pipeline implementation
- `frontend/`: React frontend with Material UI components
- `experiments.ipynb`: Jupyter notebook with RAG pipeline experiments

## Features

- Ticket submission with automatic categorization
- RAG pipeline for historical ticket analysis
- Smart response generation based on similar past tickets
- Automated tagging and priority assignment
- Integration of company product/service knowledge base
- Confidence scoring and escalation logic

## Technical Implementation

- Core RAG pipeline:
  - Ticket ingestion and preprocessing
  - Historical ticket database with resolutions
  - Company knowledge base (products, services, FAQs)
  - Vector embedding storage for tickets and documentation
  - Semantic search for similar past tickets
  - Multi-source retrieval and response generation
  - Confidence scoring and escalation triggers

## Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

4. Run the server:
   ```bash
   python main.py
   ```

5. The API will be available at http://localhost:8000

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm start
   ```

4. The application will be available at http://localhost:3000

## API Documentation

Interactive API documentation is available at http://localhost:8000/docs

## Technologies Used

- **Backend**:
  - FastAPI
  - Sentence Transformers
  - ChromaDB
  - Scikit-learn
  - Groq API (LLM)

- **Frontend**:
  - React
  - Material UI
  - React Router
  - Axios 