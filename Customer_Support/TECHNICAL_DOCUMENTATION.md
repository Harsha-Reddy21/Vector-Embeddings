# Customer Support RAG System - Technical Documentation

This document provides technical details about the implementation of the Retrieval-Augmented Generation (RAG) pipeline and similarity matching in the Customer Support System.

## RAG Pipeline Architecture

The RAG pipeline consists of the following components:

1. **Text Preprocessing**
   - Input: Raw ticket text
   - Process: Cleaning, normalization, and tokenization
   - Output: Preprocessed text ready for embedding
   - Implementation: `clean_text()` function using regex for whitespace normalization

2. **Ticket Categorization**
   - Input: Preprocessed ticket text
   - Process: Embedding generation and category classification
   - Output: Category label and confidence score
   - Implementation: `categorize_ticket()` function using cosine similarity

3. **Vector Database Storage**
   - Input: Historical tickets and company documentation
   - Process: Embedding generation and storage in ChromaDB
   - Output: Indexed knowledge base
   - Implementation: `store_knowledge()` function

4. **Similarity-Based Retrieval**
   - Input: New ticket text
   - Process: Embedding generation and vector similarity search
   - Output: Top-k most similar documents
   - Implementation: `retrieve_similar()` function

5. **Response Generation**
   - Input: Ticket text and retrieved similar documents
   - Process: Context assembly and LLM prompt construction
   - Output: AI-generated response
   - Implementation: `generate_response()` function using Groq API

6. **Confidence Scoring and Escalation**
   - Input: Similarity scores and confidence thresholds
   - Process: Threshold comparison
   - Output: Escalation decision
   - Implementation: `should_escalate()` function

## Similarity Matching Details

### Embedding Model

We use the `all-MiniLM-L6-v2` model from Sentence Transformers, which:
- Produces 384-dimensional embeddings
- Is optimized for semantic similarity tasks
- Has a good balance between performance and computational efficiency

### Similarity Calculation

For both ticket categorization and document retrieval, we use cosine similarity:

```python
from sklearn.metrics.pairwise import cosine_similarity

# For categorization
ticket_emb = model.encode([ticket_text])[0]
sims = cosine_similarity([ticket_emb], category_embeddings)[0]
best_idx = sims.argmax()
category = CATEGORIES[best_idx]
confidence = sims[best_idx]

# For document retrieval (using ChromaDB)
query_emb = model.encode([ticket_text])
result = collection.query(query_embeddings=query_emb.tolist(), n_results=top_k)
```

### Confidence Scoring

The confidence score is determined by:
- For categorization: The cosine similarity score between the ticket embedding and the closest category embedding
- For response generation: The average similarity score of retrieved documents

Escalation is triggered when:
- Confidence score falls below a threshold (default: 0.75)
- No sufficiently similar documents are found in the knowledge base

## Response Generation

The response generation process:

1. **Context Assembly**
   - Concatenate retrieved documents
   - Include source metadata for transparency

2. **Prompt Construction**
   - System message: Defines the assistant's role
   - User message: Contains ticket text and retrieved context

3. **LLM Generation**
   - Model: Llama3-70B via Groq API
   - Temperature: 0.3 (relatively deterministic)
   - Response parsing and formatting

## Performance Considerations

- **Embedding Computation**: Performed once per ticket and cached
- **Vector Database**: ChromaDB provides efficient similarity search
- **Batch Processing**: Historical tickets are processed in batches
- **Caching**: Frequently accessed embeddings and responses are cached

## Scalability

For production deployment, consider:

1. **Database Migration**: Move from in-memory to persistent ChromaDB
2. **Embedding Service**: Dedicated service for embedding generation
3. **Async Processing**: Queue-based architecture for ticket processing
4. **Monitoring**: Track confidence scores and escalation rates
5. **Feedback Loop**: Incorporate agent feedback to improve the system

## Integration Points

- **Frontend**: React components for ticket submission and display
- **API**: FastAPI endpoints for ticket processing and knowledge management
- **Vector DB**: ChromaDB for similarity search
- **LLM**: Groq API for response generation 