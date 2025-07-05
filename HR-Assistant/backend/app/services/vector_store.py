import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import json
import uuid

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        """Initialize the vector store with ChromaDB"""
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create collections if they don't exist
        self.collection = self.client.get_or_create_collection("hr_documents")
        self.metadata_collection = self.client.get_or_create_collection("document_metadata")
    
    def add_document_chunks(self, chunks: List[str], embeddings: List[List[float]], metadata_list: List[Dict[str, Any]]):
        """Add document chunks with their embeddings and metadata to the vector store"""
        # Generate IDs for each chunk
        ids = [f"chunk_{uuid.uuid4()}" for _ in range(len(chunks))]
        
        # Add chunks to the collection
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata_list,
            ids=ids
        )
        
        return ids
    
    def add_document_metadata(self, document_id: str, metadata: Dict[str, Any]):
        """Store document metadata separately"""
        self.metadata_collection.add(
            documents=[json.dumps(metadata)],
            metadatas=[{"document_id": document_id}],
            ids=[document_id]
        )
    
    def query(self, query_embedding: List[float], k: int = 5, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """Query the vector store for similar chunks"""
        # Prepare filter if categories are provided
        where_filter = None
        if categories and len(categories) > 0:
            where_filter = {"category": {"$in": categories}}
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_filter
        )
        
        return results
    
    def get_categories(self) -> List[str]:
        """Get all unique categories from the documents"""
        try:
            # Query all document metadata
            results = self.metadata_collection.get()
            
            # Extract categories from metadata
            categories = set()
            for doc in results["documents"]:
                metadata = json.loads(doc)
                if "category" in metadata:
                    categories.add(metadata["category"])
            
            return list(categories)
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """Get all document metadata"""
        try:
            results = self.metadata_collection.get()
            
            documents = []
            for i, doc in enumerate(results["documents"]):
                metadata = json.loads(doc)
                metadata["id"] = results["ids"][i]
                documents.append(metadata)
            
            return documents
        except Exception as e:
            print(f"Error getting documents: {e}")
            return []
    
    def delete_document(self, document_id: str):
        """Delete a document and its chunks from the vector store"""
        try:
            # Get document metadata to find associated chunks
            metadata_result = self.metadata_collection.get(ids=[document_id])
            
            if metadata_result["documents"]:
                metadata = json.loads(metadata_result["documents"][0])
                
                # Delete all chunks associated with this document
                if "chunk_ids" in metadata:
                    for chunk_id in metadata["chunk_ids"]:
                        try:
                            self.collection.delete(ids=[chunk_id])
                        except Exception as e:
                            print(f"Error deleting chunk {chunk_id}: {e}")
            
            # Delete the document metadata
            self.metadata_collection.delete(ids=[document_id])
            
            # Delete the actual file if path exists in metadata
            if metadata_result["documents"]:
                metadata = json.loads(metadata_result["documents"][0])
                if "file_path" in metadata and os.path.exists(metadata["file_path"]):
                    os.remove(metadata["file_path"])
                    
        except Exception as e:
            raise Exception(f"Error deleting document: {e}") 