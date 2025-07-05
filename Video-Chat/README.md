# Lecture Intelligence

A full-stack application that processes lecture videos, generates transcripts, and enables natural language conversations with the lecture content using RAG architecture.

## Features

- **Video Upload**: Upload lecture recordings (2-3 hours long)
- **Automated Transcription**: Generate transcripts from video using Whisper
- **RAG Pipeline**: Process transcripts with chunking and vector embeddings
- **Interactive Chat**: Ask questions about lecture content
- **Timestamp-Based Responses**: Get answers with references to specific video moments
- **Context-Aware Q&A**: Retrieve relevant lecture segments for accurate responses

## Tech Stack

### Backend
- FastAPI
- Whisper (OpenAI) for speech-to-text
- Sentence Transformers for embeddings
- ChromaDB for vector storage
- Groq LLaMA for response generation

### Frontend
- React
- React Router
- Axios for API calls
- Bootstrap for styling



## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- FFmpeg installed on your system

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`


4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example` and add your Groq API key.

6. Run the server:
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

3. Start the development server:
   ```
   npm start
   ```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Upload a lecture video
3. Wait for processing to complete
4. Start chatting with your lecture content!

## Sample Questions

- "What did the professor say about machine learning algorithms?"
- "Explain the concept discussed around minute 45"
- "Summarize the key points from the first hour"
- "What examples were given for neural networks?"
