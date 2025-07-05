import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import logging
import requests
from dotenv import load_dotenv

from app.services.vector_store import VectorStore

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryEngine:
    def __init__(self, vector_store: VectorStore):
        """Initialize the query engine with a vector store"""
        self.vector_store = vector_store
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Get API keys from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Default to OpenAI if available, otherwise use Groq
        self.llm_provider = "openai" if self.openai_api_key else "groq"
    
    def generate_response(self, query: str, categories: Optional[List[str]] = None, k: int = 5):
        """Generate a response for a user query"""
        try:
            # Generate embedding for the query
            query_embedding = self.model.encode(query).tolist()
            
            # Retrieve relevant chunks
            results = self.vector_store.query(
                query_embedding=query_embedding,
                k=k,
                categories=categories
            )
            
            # Extract chunks and their sources
            chunks = results["documents"][0]
            sources = [metadata["source"] for metadata in results["metadatas"][0]]
            
            # Determine query category
            query_category = self._categorize_query(query)
            
            # Generate response using LLM
            if self.llm_provider == "openai" and self.openai_api_key:
                answer = self._generate_with_openai(query, chunks)
            elif self.llm_provider == "groq" and self.groq_api_key:
                answer = self._generate_with_groq(query, chunks)
            else:
                raise ValueError("No valid LLM provider configured")
            
            return {
                "answer": answer,
                "sources": sources,
                "category": query_category
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e
    
    def _generate_with_openai(self, query: str, context_chunks: List[str]) -> str:
        """Generate a response using OpenAI API"""
        try:
            import openai
            
            openai.api_key = self.openai_api_key
            
            # Combine chunks into context
            context = "\n\n".join(context_chunks)
            
            system_prompt = """You are an expert HR assistant. Use the provided HR policy context to accurately 
            answer the user's question. Always cite the policy sections if applicable. If the context doesn't 
            contain relevant information to answer the question, politely state that you don't have that 
            specific information and suggest contacting HR."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error with OpenAI: {e}")
            raise e
    
    def _generate_with_groq(self, query: str, context_chunks: List[str]) -> str:
        """Generate a response using Groq API"""
        try:
            # Combine chunks into context
            context = "\n\n".join(context_chunks)
            
            system_prompt = """You are an expert HR assistant. Use the provided HR policy context to accurately 
            answer the user's question. Always cite the policy sections if applicable. If the context doesn't 
            contain relevant information to answer the question, politely state that you don't have that 
            specific information and suggest contacting HR."""
            
            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                "temperature": 0.3
            }
            
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            return response.json()['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error with Groq: {e}")
            raise e
    
    def _categorize_query(self, query: str) -> str:
        """Categorize the query into HR topics"""
        # Map of keywords to categories
        category_keywords = {
            "benefits": ["benefits", "insurance", "health", "dental", "vision", "401k", "retirement"],
            "leave": ["leave", "vacation", "sick", "pto", "time off", "holiday", "maternity", "paternity"],
            "compensation": ["salary", "pay", "bonus", "compensation", "raise", "review"],
            "remote_work": ["remote", "work from home", "wfh", "hybrid", "office"],
            "conduct": ["conduct", "behavior", "harassment", "ethics", "code", "policy"],
            "onboarding": ["onboarding", "orientation", "training", "new hire", "first day"],
            "offboarding": ["offboarding", "resignation", "termination", "quit", "leave company"]
        }
        
        # Convert query to lowercase for matching
        query_lower = query.lower()
        
        # Check for keyword matches
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return category
        
        # Default category if no matches
        return "general" 