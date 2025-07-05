import chromadb
import os
from typing import List, Dict, Any
from pathlib import Path


class VectorStore:
    def __init__(self, persist_directory: str = "vectordb"):
        """
        Initialize the vector database.
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = Path(persist_directory)
        
        # Create directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
    
    def store_chunks(self, video_id: str, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """
        Store chunks and their embeddings in the vector database.
        
        Args:
            video_id: Unique identifier for the video
            chunks: List of text chunks with timestamps
            embeddings: List of embeddings for each chunk
        """
        # Create or get collection for the video
        collection = self.client.get_or_create_collection(name=f"video_{video_id}")
        
        # Prepare data for insertion
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"start": chunk["start"], "end": chunk["end"]} for chunk in chunks]
        
        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    def query(self, video_id: str, query_embedding: List[float], top_k: int = 3) -> Dict[str, Any]:
        """
        Query the vector database for similar chunks.
        
        Args:
            video_id: Unique identifier for the video
            query_embedding: Embedding of the query
            top_k: Number of results to return
            
        Returns:
            Query results with documents and metadata
        """
        try:
            collection = self.client.get_collection(name=f"video_{video_id}")
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results
        except Exception as e:
            print(f"Error querying vector database: {str(e)}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def collection_exists(self, video_id: str) -> bool:
        """
        Check if a collection exists for the given video ID.
        
        Args:
            video_id: Unique identifier for the video
            
        Returns:
            True if collection exists, False otherwise
        """
        try:
            self.client.get_collection(name=f"video_{video_id}")
            return True
        except Exception:
            return False 