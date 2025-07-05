from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union, Dict, Any
import os

# Cache for embedding model to avoid reloading
_embedding_model = None

def get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Get or initialize the embedding model.
    
    Args:
        model_name: Name of the SentenceTransformer model to use
        
    Returns:
        Initialized SentenceTransformer model
    """
    global _embedding_model
    
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(model_name)
    
    return _embedding_model

def generate_embeddings(texts: List[str], model: SentenceTransformer = None) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of texts to embed
        model: SentenceTransformer model (if None, will use get_embedding_model())
        
    Returns:
        List of embeddings as float lists
    """
    if model is None:
        model = get_embedding_model()
    
    embeddings = model.encode(texts)
    return embeddings.tolist()

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding
        embedding2: Second embedding
        
    Returns:
        Cosine similarity score (0-1)
    """
    # Convert to numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return dot_product / (norm1 * norm2)

def batch_cosine_similarity(query_embedding: List[float], 
                           document_embeddings: List[List[float]]) -> List[float]:
    """
    Calculate cosine similarity between a query embedding and multiple document embeddings.
    
    Args:
        query_embedding: Query embedding
        document_embeddings: List of document embeddings
        
    Returns:
        List of similarity scores
    """
    query_vec = np.array(query_embedding)
    doc_vecs = np.array(document_embeddings)
    
    # Calculate dot products
    dot_products = np.dot(doc_vecs, query_vec)
    
    # Calculate norms
    query_norm = np.linalg.norm(query_vec)
    doc_norms = np.linalg.norm(doc_vecs, axis=1)
    
    # Calculate similarities
    similarities = dot_products / (doc_norms * query_norm)
    
    # Replace NaN values with 0
    similarities = np.nan_to_num(similarities)
    
    return similarities.tolist() 