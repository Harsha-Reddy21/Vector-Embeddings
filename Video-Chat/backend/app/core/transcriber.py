import whisper
import os
import json
from pathlib import Path
from typing import List, Dict, Any


class Transcriber:
    def __init__(self, model_name: str = "base", transcripts_dir: str = "transcripts"):
        """
        Initialize the transcriber with the specified Whisper model.
        
        Args:
            model_name: Whisper model name ("tiny", "base", "small", "medium", "large")
            transcripts_dir: Directory to save transcripts
        """
        self.model_name = model_name
        self.model = None  # Lazy loading to save memory
        self.transcripts_dir = Path(transcripts_dir)
        
        # Create transcript directory if it doesn't exist
        os.makedirs(self.transcripts_dir, exist_ok=True)
    
    def _load_model(self):
        """Load the Whisper model if not already loaded."""
        if self.model is None:
            self.model = whisper.load_model(self.model_name)
    
    def transcribe(self, audio_path: str, video_id: str) -> List[Dict[str, Any]]:
        """
        Transcribe audio file and save the result.
        
        Args:
            audio_path: Path to the audio file
            video_id: Unique identifier for the video
            
        Returns:
            List of transcript segments with timestamps
        """
        self._load_model()
        
        # Perform transcription
        result = self.model.transcribe(audio_path, verbose=False)
        segments = result.get('segments', [])
        
        # Save transcript to file
        transcript_path = self.transcripts_dir / f"{video_id}.json"
        with open(transcript_path, 'w') as f:
            json.dump(segments, f)
        
        return segments
    
    def get_transcript(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get transcript for a video if it exists.
        
        Args:
            video_id: Unique identifier for the video
            
        Returns:
            List of transcript segments with timestamps
        """
        transcript_path = self.transcripts_dir / f"{video_id}.json"
        
        if not transcript_path.exists():
            return []
        
        with open(transcript_path, 'r') as f:
            return json.load(f) 