import ffmpeg
import os
from pathlib import Path


class AudioProcessor:
    def __init__(self, upload_dir: str, audio_dir: str):
        """
        Initialize the audio processor.
        
        Args:
            upload_dir: Directory where uploaded videos are stored
            audio_dir: Directory where extracted audio will be stored
        """
        self.upload_dir = Path(upload_dir)
        self.audio_dir = Path(audio_dir)
        
        # Create directories if they don't exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def extract_audio(self, video_id: str, video_filename: str) -> str:
        """
        Extract audio from a video file.
        
        Args:
            video_id: Unique identifier for the video
            video_filename: Name of the video file
            
        Returns:
            Path to the extracted audio file
        """
        video_path = self.upload_dir / video_filename
        audio_filename = f"{video_id}.wav"
        audio_path = self.audio_dir / audio_filename
        
        try:
            (
                ffmpeg
                .input(str(video_path))
                .output(str(audio_path), format='wav', acodec='pcm_s16le', ac=1, ar='16000')
                .overwrite_output()
                .run(quiet=True)
            )
            return str(audio_path)
        except ffmpeg.Error as e:
            print(f"Error extracting audio: {e.stderr.decode() if e.stderr else str(e)}")
            raise Exception(f"Failed to extract audio from video: {str(e)}") 