from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import CrossEncoder
import chromadb
from sentence_transformers import SentenceTransformer

# Cache for cross-encoder model
_cross_encoder = None

def sparse_search(query: str, chunks: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    """
    Perform sparse retrieval using TF-IDF and cosine similarity.
    
    Args:
        query: Query string
        chunks: List of text chunks to search
        top_k: Number of results to return
        
    Returns:
        List of (chunk, score) tuples
    """
    # Initialize vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit on chunks
    X = vectorizer.fit_transform(chunks)
    
    # Transform query
    q_vec = vectorizer.transform([query])
    
    # Calculate similarity
    scores = sklearn_cosine_similarity(q_vec, X).flatten()
    
    # Rank results
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    
    return ranked[:top_k]

def dense_search(query: str, 
                collection: chromadb.Collection, 
                embedding_model: SentenceTransformer,
                top_k: int = 3) -> List[str]:
    """
    Perform dense retrieval using embeddings.
    
    Args:
        query: Query string
        collection: ChromaDB collection
        embedding_model: SentenceTransformer model
        top_k: Number of results to return
        
    Returns:
        List of text chunks
    """
    # Generate query embedding
    query_embedding = embedding_model.encode(query).tolist()
    
    # Query collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return results['documents'][0]

def hybrid_retrieval(query: str, 
                    chunks: List[str], 
                    collection: chromadb.Collection,
                    embedding_model: SentenceTransformer,
                    top_k: int = 5,
                    dense_weight: float = 0.7,
                    sparse_weight: float = 0.3) -> List[str]:
    """
    Perform hybrid retrieval combining dense and sparse search.
    
    Args:
        query: Query string
        chunks: List of text chunks
        collection: ChromaDB collection
        embedding_model: SentenceTransformer model
        top_k: Number of results to return
        dense_weight: Weight for dense retrieval scores
        sparse_weight: Weight for sparse retrieval scores
        
    Returns:
        List of text chunks
    """
    # Get dense results
    dense_results = dense_search(query, collection, embedding_model, top_k=top_k*2)
    
    # Get sparse results
    sparse_results = sparse_search(query, chunks, top_k=top_k*2)
    sparse_chunks = [chunk for chunk, _ in sparse_results]
    
    # Combine results (with fixed weights for simplicity)
    combined_chunks = []
    
    # Add dense results with weight
    for chunk in dense_results:
        if chunk in combined_chunks:
            continue
        combined_chunks.append(chunk)
    
    # Add sparse results with weight
    for chunk in sparse_chunks:
        if chunk in combined_chunks:
            continue
        combined_chunks.append(chunk)
    
    # Limit to top_k
    return combined_chunks[:top_k]

def get_cross_encoder(model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> CrossEncoder:
    """
    Get or initialize the cross-encoder model.
    
    Args:
        model_name: Name of the cross-encoder model
        
    Returns:
        Initialized CrossEncoder model
    """
    global _cross_encoder
    
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder(model_name)
    
    return _cross_encoder

def rerank_results(query: str, chunks: List[str], top_k: int = None) -> List[str]:
    """
    Rerank results using a cross-encoder model.
    
    Args:
        query: Query string
        chunks: List of text chunks to rerank
        top_k: Number of results to return (if None, return all reranked)
        
    Returns:
        List of reranked text chunks
    """
    if top_k is None:
        top_k = len(chunks)
    
    # Prepare input pairs
    pairs = [(query, chunk) for chunk in chunks]
    
    # Get cross-encoder
    cross_encoder = get_cross_encoder()
    
    # Get scores
    scores = cross_encoder.predict(pairs)
    
    # Sort by score
    ranked_results = [x for _, x in sorted(zip(scores, chunks), reverse=True)]
    
    return ranked_results[:top_k] 