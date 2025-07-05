import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMService:
    def __init__(self):
        """
        Initialize the LLM service.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"
    
    def generate_response(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a response using the LLM based on the query and context chunks.
        
        Args:
            query: User's question
            context_chunks: List of relevant context chunks with timestamps
            
        Returns:
            Generated response from the LLM
        """
        # Format context and timestamps
        context = "\n\n".join([c.get('text', '') for c in context_chunks])
        timestamps = "\n".join([f"- [{c.get('start', 0):.2f} → {c.get('end', 0):.2f}]" for c in context_chunks])
        
        # Prepare messages for the API
        messages = [
            {"role": "system", "content": "You are a helpful AI lecture assistant. Answer questions based on the provided lecture context. Include references to video timestamps when relevant."},
            {"role": "user", "content": f"""Lecture Context:
{context}

Timestamps:
{timestamps}

Question: {query}

Answer the question based on the lecture context. Include references to timestamps when relevant to help the user find the information in the video.
"""}
        ]
        
        try:
            # Make API request
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3
                },
                timeout=30
            )
            
            # Parse response
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return f"Sorry, I couldn't generate a response. Error: {response.status_code}"
        
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            return "Sorry, I encountered an error while generating a response." 