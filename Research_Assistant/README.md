# Research Assistant

A powerful research assistant that combines PDF document analysis with web search to provide comprehensive answers to your questions.

## Features

- **PDF Document Processing**: Upload and analyze PDF documents
- **Web Search Integration**: Get real-time information from the web
- **Hybrid Retrieval**: Combine document content with web search results
- **Advanced Retrieval Methods**:
  - Dense Retrieval (semantic search using embeddings)
  - Sparse Retrieval (keyword matching with TF-IDF)
  - Hybrid Retrieval (combines dense and sparse approaches)
  - Re-ranking with cross-encoders
- **Source Verification and Citation**: Automatically cite sources in responses
- **Response Quality Monitoring**: Track and evaluate response quality

## Installation



1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key
SERP_API_KEY=your_serp_api_key
```

## Usage

Run the Streamlit app:
```bash
streamlit run research_assistant.py
```

Then:
1. Upload a PDF document
2. Ask questions about the document
3. Get comprehensive answers with citations from both the document and the web



## Advanced Configuration

The application provides several configuration options in the sidebar:
- **Retrieval Method**: Choose between Hybrid, Dense Only, or Sparse Only
- **Cross-Encoder Reranking**: Enable/disable reranking for improved precision
- **Web Results**: Control the number of web search results to include
- **Temperature**: Adjust the creativity of the response generation
