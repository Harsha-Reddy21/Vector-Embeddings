from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.core.text_processor import TextProcessor
from app.core.llm_service import LLMService
from app.db.vector_store import VectorStore
from app.models.schemas import ChatRequest, ChatResponse, TimestampedChunk
from app.core.config import TOP_K_RESULTS

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services
text_processor = TextProcessor()
vector_store = VectorStore()
llm_service = LLMService()


@router.post("", response_model=ChatResponse)
async def chat_with_video(request: ChatRequest):
    """
    Chat with a video's content using RAG.
    """
    video_id = request.video_id
    user_message = request.message
    
    # Check if video exists in vector store
    if not vector_store.collection_exists(video_id):
        raise HTTPException(status_code=404, detail="Video not found or not processed yet")
    
    try:
        # Generate embedding for the query
        query_embedding = text_processor.embed_text(user_message)
        
        # Query vector store for relevant chunks
        results = vector_store.query(video_id, query_embedding, top_k=TOP_K_RESULTS)
        
        # Extract documents and metadata
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        # Create context chunks with text and timestamps
        context_chunks = []
        for i, doc in enumerate(documents):
            if i < len(metadatas):
                context_chunks.append({
                    "text": doc,
                    "start": metadatas[i].get('start', 0),
                    "end": metadatas[i].get('end', 0)
                })
        
        # Generate response using LLM
        llm_response = llm_service.generate_response(user_message, context_chunks)
        
        # Extract timestamps for the response
        timestamps = [{"start": chunk.get('start', 0), "end": chunk.get('end', 0)} for chunk in context_chunks]
        
        # Create source chunks for the response
        source_chunks = [TimestampedChunk(
            text=chunk.get('text', ''),
            start=chunk.get('start', 0),
            end=chunk.get('end', 0)
        ) for chunk in context_chunks]
        
        return ChatResponse(
            message=llm_response,
            timestamps=timestamps,
            source_chunks=source_chunks
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}") 