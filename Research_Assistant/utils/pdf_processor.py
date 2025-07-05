import fitz  # PyMuPDF
import re
import os
import tempfile
from typing import List, Dict, Any

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def chunk_text(text: str, max_words: int = 100, overlap: int = 20) -> List[str]:
    """
    Split text into chunks of specified maximum word count with overlap.
    
    Args:
        text: Text to chunk
        max_words: Maximum number of words per chunk
        overlap: Number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Clean text - remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words
    words = text.split()
    
    # Create chunks with overlap
    chunks = []
    for i in range(0, len(words), max_words - overlap):
        chunk = " ".join(words[i:i + max_words])
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
    
    return chunks

def extract_metadata(pdf_path: str) -> Dict[str, Any]:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing metadata
    """
    try:
        doc = fitz.open(pdf_path)
        metadata = {
            "title": doc.metadata.get("title", "Unknown"),
            "author": doc.metadata.get("author", "Unknown"),
            "subject": doc.metadata.get("subject", ""),
            "keywords": doc.metadata.get("keywords", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
            "page_count": len(doc),
            "file_size": os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}

def save_uploaded_pdf(uploaded_file) -> str:
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file: Streamlit uploaded file
        
    Returns:
        Path to the saved file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name 