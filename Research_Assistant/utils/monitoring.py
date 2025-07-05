import os
import json
import time
import uuid
from typing import Dict, Any, List, Optional
import datetime

# Directory for logs
LOG_DIR = "logs"

def ensure_log_dir():
    """Ensure log directory exists"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log_query(query: str, document_name: Optional[str] = None) -> str:
    """
    Log a user query.
    
    Args:
        query: User query
        document_name: Name of the document being queried
        
    Returns:
        Query ID
    """
    ensure_log_dir()
    
    # Generate query ID
    query_id = str(uuid.uuid4())
    
    # Create log entry
    log_entry = {
        "id": query_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "document": document_name
    }
    
    # Write to log file
    with open(os.path.join(LOG_DIR, "queries.jsonl"), "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return query_id

def log_response(query_id: str, response: str, metrics: Optional[Dict[str, float]] = None) -> None:
    """
    Log a response to a query.
    
    Args:
        query_id: ID of the query
        response: Generated response
        metrics: Quality metrics for the response
        
    Returns:
        None
    """
    ensure_log_dir()
    
    # Create log entry
    log_entry = {
        "query_id": query_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "response": response,
        "metrics": metrics or {}
    }
    
    # Write to log file
    with open(os.path.join(LOG_DIR, "responses.jsonl"), "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def log_error(error_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an error.
    
    Args:
        error_type: Type of error
        message: Error message
        details: Additional error details
        
    Returns:
        None
    """
    ensure_log_dir()
    
    # Create log entry
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": error_type,
        "message": message,
        "details": details or {}
    }
    
    # Write to log file
    with open(os.path.join(LOG_DIR, "errors.jsonl"), "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def get_query_history(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent query history.
    
    Args:
        limit: Maximum number of queries to return
        
    Returns:
        List of query log entries
    """
    ensure_log_dir()
    
    queries = []
    query_file = os.path.join(LOG_DIR, "queries.jsonl")
    
    if os.path.exists(query_file):
        with open(query_file, "r") as f:
            for line in f:
                queries.append(json.loads(line))
    
    # Sort by timestamp (newest first) and limit
    queries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return queries[:limit]

def get_response_metrics(days: int = 7) -> Dict[str, float]:
    """
    Get aggregated response metrics for a time period.
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary with aggregated metrics
    """
    ensure_log_dir()
    
    # Calculate cutoff timestamp
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    cutoff_str = cutoff.isoformat()
    
    responses = []
    response_file = os.path.join(LOG_DIR, "responses.jsonl")
    
    if os.path.exists(response_file):
        with open(response_file, "r") as f:
            for line in f:
                response = json.loads(line)
                if response.get("timestamp", "") >= cutoff_str:
                    responses.append(response)
    
    # Calculate aggregate metrics
    metrics = {
        "count": len(responses),
        "relevance": 0.0,
        "completeness": 0.0,
        "citation_quality": 0.0,
        "overall": 0.0
    }
    
    if responses:
        for response in responses:
            response_metrics = response.get("metrics", {})
            for key in ["relevance", "completeness", "citation_quality", "overall"]:
                metrics[key] += response_metrics.get(key, 0.0)
        
        # Calculate averages
        for key in ["relevance", "completeness", "citation_quality", "overall"]:
            metrics[key] /= metrics["count"] if metrics["count"] > 0 else 1
    
    return metrics 