import os
from typing import List, Dict, Any
import uuid
import pdfplumber
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import logging

from app.services.vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, vector_store: VectorStore):
        """Initialize the document processor with a vector store"""
        self.vector_store = vector_store
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " "]
        )
    
    def process_documents(self, file_infos: List[Dict[str, Any]]):
        """Process a list of documents"""
        for file_info in file_infos:
            try:
                self._process_single_document(file_info)
            except Exception as e:
                logger.error(f"Error processing document {file_info['original_name']}: {e}")
    
    def _process_single_document(self, file_info: Dict[str, Any]):
        """Process a single document"""
        file_path = file_info["saved_path"]
        category = file_info["category"]
        document_type = file_info["document_type"]
        original_name = file_info["original_name"]
        
        logger.info(f"Processing document: {original_name}")
        
        # Extract text based on file type
        text = self._extract_text(file_path)
        
        # Generate document ID
        document_id = f"doc_{uuid.uuid4()}"
        
        # Chunk the text
        chunks = self.text_splitter.split_text(text)
        
        # Generate embeddings
        embeddings = self.model.encode(chunks, show_progress_bar=False)
        
        # Prepare metadata for each chunk
        metadata_list = []
        for i, _ in enumerate(chunks):
            metadata_list.append({
                "document_id": document_id,
                "chunk_index": i,
                "category": category,
                "document_type": document_type,
                "original_name": original_name,
                "source": f"{original_name} (Chunk {i+1}/{len(chunks)})"
            })
        
        # Add chunks to vector store
        chunk_ids = self.vector_store.add_document_chunks(
            chunks=chunks,
            embeddings=[emb.tolist() for emb in embeddings],
            metadata_list=metadata_list
        )
        
        # Store document metadata
        document_metadata = {
            "original_name": original_name,
            "file_path": file_path,
            "category": category,
            "document_type": document_type,
            "chunk_count": len(chunks),
            "chunk_ids": chunk_ids
        }
        
        self.vector_store.add_document_metadata(document_id, document_metadata)
        
        logger.info(f"Successfully processed document: {original_name}")
        
        return document_id
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from a document based on its file extension"""
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == ".pdf":
            return self._read_pdf(file_path)
        elif file_extension.lower() == ".docx":
            return self._read_docx(file_path)
        elif file_extension.lower() == ".txt":
            return self._read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    def _read_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    def _read_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file"""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    def _read_txt(self, file_path: str) -> str:
        """Extract text from a TXT file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read() 