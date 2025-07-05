import os
import requests
import json
from typing import List, Dict, Any, Optional
import time

def generate_response(query: str, 
                     pdf_sources: List[str], 
                     web_sources: List[Dict[str, str]],
                     temperature: float = 0.3) -> str:
    """
    Generate a response using Groq API.
    
    Args:
        query: User query
        pdf_sources: List of relevant PDF text chunks
        web_sources: List of web search results
        temperature: Temperature for response generation
        
    Returns:
        Generated response
    """
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ GROQ_API_KEY not found in environment variables. Cannot generate response."
    
    # Format sources
    pdf_context = "\n\n".join([f"[PDF] {s}" for s in pdf_sources])
    web_context = "\n\n".join([f"[Web] {s.get('title', 'No title')}: {s.get('snippet', 'No snippet')} (URL: {s.get('link', '#')})" for s in web_sources])
    
    # Combine contexts
    context = f"{pdf_context}\n\n{web_context}"
    
    # Prepare messages
    messages = [
        {
            "role": "system", 
            "content": """You are a helpful research assistant. Answer the user's query based on the provided sources.
            
1. Use ONLY the information from the provided sources to answer.
2. If the sources don't contain relevant information, say so honestly.
3. Always cite your sources using the format [PDF] or [Web: URL] at the end of each statement.
4. Prioritize information from more credible sources.
5. Present information in a clear, organized manner.
6. If sources contradict each other, acknowledge the different perspectives.
"""
        },
        {
            "role": "user", 
            "content": f"""Query: {query}

Sources:
{context}

Please provide a comprehensive answer based on these sources. Include citations."""
        }
    ]
    
    try:
        # Make API request
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": messages,
                "temperature": temperature
            }
        )
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"⚠️ Error generating response: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"

def format_response_with_citations(response: str) -> str:
    """
    Format response with proper citations.
    
    Args:
        response: Raw response from LLM
        
    Returns:
        Formatted response with citations
    """
    # This is a placeholder for more sophisticated citation formatting
    # In a real system, you might want to parse and standardize citations
    
    # Add citation formatting
    formatted = response
    
    # Add a sources section if not already present
    if "Sources:" not in response:
        # Extract citation patterns like [PDF] or [Web: URL]
        import re
        citations = re.findall(r'\[(PDF|Web:[^\]]+)\]', response)
        
        if citations:
            formatted += "\n\nSources:\n"
            for i, citation in enumerate(set(citations)):
                formatted += f"{i+1}. {citation}\n"
    
    return formatted

def evaluate_response_quality(query: str, response: str) -> Dict[str, float]:
    """
    Evaluate the quality of a generated response.
    
    Args:
        query: User query
        response: Generated response
        
    Returns:
        Dictionary with quality metrics
    """
    # This is a placeholder for more sophisticated evaluation
    # In a real system, you might use a separate model for evaluation
    
    metrics = {
        "relevance": 0.0,
        "completeness": 0.0,
        "citation_quality": 0.0,
        "overall": 0.0
    }
    
    # Check for citations
    citation_count = response.count("[PDF]") + response.count("[Web:")
    if citation_count > 0:
        metrics["citation_quality"] = min(1.0, citation_count / 5.0)
    
    # Check response length (very simple heuristic)
    if len(response) > 100:
        metrics["completeness"] = min(1.0, len(response) / 500.0)
    
    # Check if response contains query terms (very simple relevance check)
    query_terms = set(query.lower().split())
    response_lower = response.lower()
    matched_terms = sum(1 for term in query_terms if term in response_lower)
    if query_terms:
        metrics["relevance"] = matched_terms / len(query_terms)
    
    # Calculate overall score
    metrics["overall"] = (metrics["relevance"] + metrics["completeness"] + metrics["citation_quality"]) / 3.0
    
    return metrics 