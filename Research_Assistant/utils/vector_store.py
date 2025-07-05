import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os
import time
from sentence_transformers import SentenceTransformer

def create_collection(collection_name: str, 
                     persist_directory: Optional[str] = None) -> chromadb.Collection:
    """
    Create or get a ChromaDB collection.
    
    Args:
        collection_name: Name of the collection
        persist_directory: Directory to persist the collection (if None, in-memory only)
        
    Returns:
        ChromaDB collection
    """
    # Configure client
    if persist_directory:
        client = chromadb.PersistentClient(path=persist_directory)
    else:
        client = chromadb.Client()
    
    # Create or get collection
    try:
        # Try to get existing collection
        collection = client.get_collection(collection_name)
    except:
        # Create new collection if it doesn't exist
        collection = client.create_collection(
            name=collection_name,
            metadata={"created_at": time.time()}
        )
    
    return collection

def store_chunks(chunks: List[str], 
                collection: chromadb.Collection, 
                embedding_model: SentenceTransformer,
                batch_size: int = 100) -> None:
    """
    Store text chunks in a ChromaDB collection.
    
    Args:
        chunks: List of text chunks to store
        collection: ChromaDB collection
        embedding_model: SentenceTransformer model for embeddings
        batch_size: Number of chunks to process at once
        
    Returns:
        None
    """
    # Process in batches to avoid memory issues
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        batch_ids = [f"chunk_{i+j}" for j in range(len(batch))]
        
        # Generate embeddings
        embeddings = embedding_model.encode(batch).tolist()
        
        # Add to collection
        collection.add(
            documents=batch,
            ids=batch_ids,
            embeddings=embeddings
        )

def query_collection(collection: chromadb.Collection,
                    query: str,
                    embedding_model: SentenceTransformer,
                    n_results: int = 5) -> Dict[str, Any]:
    """
    Query a ChromaDB collection.
    
    Args:
        collection: ChromaDB collection
        query: Query string
        embedding_model: SentenceTransformer model for embeddings
        n_results: Number of results to return
        
    Returns:
        Dictionary with query results
    """
    # Generate query embedding
    query_embedding = embedding_model.encode(query).tolist()
    
    # Query collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

def delete_collection(collection_name: str, persist_directory: Optional[str] = None) -> bool:
    """
    Delete a ChromaDB collection.
    
    Args:
        collection_name: Name of the collection to delete
        persist_directory: Directory where the collection is persisted
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if persist_directory:
            client = chromadb.PersistentClient(path=persist_directory)
        else:
            client = chromadb.Client()
        
        client.delete_collection(collection_name)
        return True
    except Exception as e:
        print(f"Error deleting collection: {str(e)}")
        return False 