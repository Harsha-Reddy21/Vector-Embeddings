from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import os
import json
from pathlib import Path


class TextProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", chunks_dir: str = "chunks"):
        """
        Initialize the text processor with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence transformer model
            chunks_dir: Directory to save chunked transcripts
        """
        self.model = SentenceTransformer(model_name)
        self.chunks_dir = Path(chunks_dir)
        
        # Create chunks directory if it doesn't exist
        os.makedirs(self.chunks_dir, exist_ok=True)
    
    def chunk_transcript(self, segments: List[Dict[str, Any]], video_id: str, max_chunk_words: int = 100) -> List[Dict[str, Any]]:
        """
        Chunk transcript into smaller segments for better retrieval.
        
        Args:
            segments: List of transcript segments with timestamps
            video_id: Unique identifier for the video
            max_chunk_words: Maximum number of words per chunk
            
        Returns:
            List of chunked transcript segments with timestamps
        """
        chunks = []
        current_chunk = []
        current_start = None

        for seg in segments:
            words = seg.get('text', '').strip().split()
            if not current_chunk:
                current_start = seg.get('start', 0)

            current_chunk.extend(words)

            if len(current_chunk) >= max_chunk_words:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "start": current_start,
                    "end": seg.get('end', 0)
                })
                current_chunk = []

        # Add the last chunk if there's any
        if current_chunk and segments:
            chunks.append({
                "text": " ".join(current_chunk),
                "start": current_start,
                "end": segments[-1].get('end', 0)
            })
        
        # Save chunks to file
        chunks_path = self.chunks_dir / f"{video_id}.json"
        with open(chunks_path, 'w') as f:
            json.dump(chunks, f)
        
        return chunks
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a text string.
        
        Args:
            text: Text to embed
            
        Returns:
            List of embedding values
        """
        return self.model.encode(text).tolist()
    
    def get_chunks(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get chunked transcript for a video if it exists.
        
        Args:
            video_id: Unique identifier for the video
            
        Returns:
            List of chunked transcript segments with timestamps
        """
        chunks_path = self.chunks_dir / f"{video_id}.json"
        
        if not chunks_path.exists():
            return []
        
        with open(chunks_path, 'r') as f:
            return json.load(f) 