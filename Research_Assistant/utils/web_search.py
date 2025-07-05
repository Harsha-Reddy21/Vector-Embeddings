import os
import requests
import json
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus

def web_search_serper(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web using Serper API.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of search result dictionaries
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        raise ValueError("❌ SERP_API_KEY is missing or not set in environment variables.")
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": num_results
    }
    
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            results = response.json().get("organic", [])
            return results
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error during web search: {str(e)}")
        return []

def extract_main_content(url: str) -> Optional[str]:
    """
    Extract main content from a webpage.
    
    Args:
        url: URL of the webpage
        
    Returns:
        Extracted main content or None if extraction fails
    """
    try:
        # Use a simple GET request (in a production system, you might want to use
        # a more sophisticated approach like newspaper3k or trafilatura)
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        
        if response.status_code == 200:
            # In a real system, you'd use proper HTML parsing here
            # This is a simplified version
            text = response.text
            return text[:10000]  # Return first 10K chars as a simple approach
        else:
            return None
    except Exception as e:
        print(f"❌ Error extracting content from {url}: {str(e)}")
        return None

def enrich_search_results(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Enrich search results with additional content.
    
    Args:
        results: List of search result dictionaries
        
    Returns:
        Enriched search results
    """
    enriched_results = []
    
    for result in results:
        try:
            # Extract URL
            url = result.get("link")
            
            # Skip if no URL
            if not url:
                continue
            
            # Get content
            content = extract_main_content(url)
            
            # Add content to result if available
            if content:
                result["full_content"] = content
            
            enriched_results.append(result)
        except Exception as e:
            print(f"❌ Error enriching result: {str(e)}")
    
    return enriched_results

def rate_source_credibility(source: Dict[str, str]) -> float:
    """
    Rate the credibility of a source.
    
    Args:
        source: Source dictionary
        
    Returns:
        Credibility score (0-1)
    """
    # This is a simplified implementation
    # In a real system, you'd use more sophisticated heuristics
    
    # Initialize score
    score = 0.5
    
    # Check if source has a link
    if not source.get("link"):
        return 0.0
    
    # Boost score for academic and trusted domains
    domain = source.get("link", "").lower()
    if any(trusted in domain for trusted in [
        ".edu", ".gov", ".org", "wikipedia.org", "scholar.google", 
        "researchgate", "nature.com", "science.org", "ieee.org"
    ]):
        score += 0.3
    
    # Penalize for untrusted domains or patterns
    if any(untrusted in domain for untrusted in [
        "blog.", "forum.", ".xyz", ".info"
    ]):
        score -= 0.2
    
    # Adjust based on snippet quality
    snippet = source.get("snippet", "")
    if snippet:
        # Boost for longer snippets (more information)
        if len(snippet) > 200:
            score += 0.1
        
        # Penalize for excessive punctuation or ALL CAPS (potential clickbait)
        if snippet.count("!") > 3 or snippet.count("?") > 3:
            score -= 0.1
        
        # Check for ALL CAPS words (excluding acronyms)
        caps_words = [w for w in snippet.split() if w.isupper() and len(w) > 2]
        if len(caps_words) > 3:
            score -= 0.1
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, score)) 