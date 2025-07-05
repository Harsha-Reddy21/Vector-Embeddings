# HR Onboarding Knowledge Assistant

A powerful AI assistant that allows new employees to instantly query company policies, benefits, leave policies, and employment terms from uploaded HR documents.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Intelligent Chunking**: Breaks down documents into manageable pieces for better retrieval
- **Vector Embeddings**: Uses semantic search to find the most relevant information
- **Conversational Interface**: Natural language queries with context-aware responses
- **Policy Citations**: Responses include references to source documents
- **Category Filtering**: Filter queries by document categories
- **Admin Dashboard**: Easily manage uploaded documents

## Tech Stack

- **Backend**: FastAPI, LangChain, ChromaDB, Sentence-Transformers
- **Frontend**: React, Material-UI
- **LLM Integration**: OpenAI/Groq API

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   GROQ_API_KEY=your_groq_key_here
   ```

4. Run the backend server:
   ```
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```

## Usage

1. **Upload Documents**: Go to the Admin Panel to upload HR documents
2. **Categorize Documents**: Assign categories to documents for better organization
3. **Ask Questions**: Use the Chat interface to ask questions about HR policies
4. **View Sources**: See which documents and sections were used to answer your questions

## Sample Queries

- "How many vacation days do I get as a new employee?"
- "What's the process for requesting parental leave?"
- "Can I work remotely and what are the guidelines?"
- "How do I enroll in health insurance?"

## Project Structure

```
HR-Assistant/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── document_processor.py
│   │   │   ├── query_engine.py
│   │   │   └── vector_store.py
│   │   └── main.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
└── README.md
``` 