import re
import os
import uuid
import requests
import chromadb
import numpy as np
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Categories for classification
CATEGORIES = [
    "Shipping Issue", "Return Request", "Payment Problem",
    "Product Quality", "Account/Login", "Technical Support", "General Inquiry"
]

class RAGPipeline:
    def __init__(self):
        # Initialize embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.category_embeddings = self.model.encode(CATEGORIES)
        
        # Initialize vector database
        self.client = chromadb.Client()
        # Check if collection exists, if not create it
        try:
            self.collection = self.client.get_collection("support_knowledge")
        except:
            self.collection = self.client.create_collection("support_knowledge")
        
        # Escalation threshold
        self.confidence_threshold = 0.75
    
    def clean_text(self, text):
        """Preprocess and clean the ticket text"""
        text = re.sub(r'\\s+', ' ', text)
        return text.strip().lower()
    
    def categorize_ticket(self, ticket_text):
        """Categorize the ticket based on its content"""
        ticket_emb = self.model.encode([ticket_text])[0]
        sims = cosine_similarity([ticket_emb], self.category_embeddings)[0]
        best_idx = sims.argmax()
        return CATEGORIES[best_idx], float(sims[best_idx])
    
    def store_knowledge(self, tickets=None, docs=None):
        """Store tickets and documentation in vector database"""
        if tickets:
            for i, t in enumerate(tickets):
                self.collection.add(
                    documents=[t["text"] + " " + t["solution"]],
                    ids=[f"ticket_{uuid.uuid4()}"],
                    metadatas=[{"type": "ticket", "source": t["text"]}]
                )
        
        if docs:
            for i, d in enumerate(docs):
                self.collection.add(
                    documents=[d["content"]],
                    ids=[f"doc_{uuid.uuid4()}"],
                    metadatas=[{"type": "doc", "source": d["title"]}]
                )
    
    def retrieve_similar(self, ticket_text, top_k=3):
        """Retrieve similar tickets and documentation"""
        query_emb = self.model.encode([ticket_text])
        result = self.collection.query(query_embeddings=query_emb.tolist(), n_results=top_k)
        
        if not result['documents']:
            return []
            
        docs = result['documents'][0]
        metas = result['metadatas'][0]
        return [{"text": d, "source": m["source"], "type": m["type"]} for d, m in zip(docs, metas)]
    
    def generate_response(self, ticket_text, retrieved_docs):
        """Generate response using LLM with retrieved context"""
        context = "\n\n".join([doc["text"] for doc in retrieved_docs])
        sources = "\n".join([f"- From {doc['type']}: {doc['source']}" for doc in retrieved_docs])

        messages = [
            {"role": "system", "content": "You are a smart support assistant. Use past ticket solutions and company docs to answer the new ticket."},
            {"role": "user", "content": f"""Ticket:
{ticket_text}

Relevant Knowledge:
{context}

Sources:
{sources}

Please generate a helpful, concise support response."""}
        ]

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": messages,
                    "temperature": 0.3
                }
            )
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
    
    def should_escalate(self, confidence_score):
        """Determine if the ticket should be escalated to a human"""
        return confidence_score < self.confidence_threshold
    
    def process_ticket(self, ticket):
        """Process a ticket through the entire pipeline"""
        # Clean text
        clean_text = self.clean_text(ticket.text)
        
        # Categorize
        category, confidence = self.categorize_ticket(clean_text)
        
        # Retrieve similar documents
        retrieved_docs = self.retrieve_similar(clean_text)
        
        # Generate response
        response = self.generate_response(clean_text, retrieved_docs)
        
        # Check if should escalate
        auto_resolved = not self.should_escalate(confidence)
        
        return {
            "ticket_id": ticket.id if ticket.id else str(uuid.uuid4()),
            "category": category,
            "confidence": confidence,
            "response": response,
            "sources": retrieved_docs,
            "auto_resolved": auto_resolved
        } 