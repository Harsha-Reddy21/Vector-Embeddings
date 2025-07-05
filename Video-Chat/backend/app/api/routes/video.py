import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime

from app.core.config import UPLOAD_DIR, AUDIO_DIR, TRANSCRIPTS_DIR, CHUNKS_DIR, WHISPER_MODEL
from app.core.audio_processor import AudioProcessor
from app.core.transcriber import Transcriber
from app.core.text_processor import TextProcessor
from app.db.vector_store import VectorStore
from app.models.schemas import VideoUploadResponse, TranscriptionStatus, VideoMetadata

router = APIRouter(prefix="/videos", tags=["videos"])

# Initialize services
audio_processor = AudioProcessor(UPLOAD_DIR, AUDIO_DIR)
transcriber = Transcriber(WHISPER_MODEL, TRANSCRIPTS_DIR)
text_processor = TextProcessor(chunks_dir=CHUNKS_DIR)
vector_store = VectorStore()

# In-memory storage for video metadata and processing status
# In a production app, this would be stored in a database
video_metadata = {}
processing_status = {}


async def process_video(video_id: str, file_path: str):
    """
    Background task to process a video:
    1. Extract audio
    2. Transcribe audio
    3. Chunk transcript
    4. Create embeddings
    5. Store in vector database
    """
    try:
        # Update status
        processing_status[video_id] = {"status": "extracting_audio", "progress": 0.1}
        
        # Extract audio
        audio_path = audio_processor.extract_audio(video_id, os.path.basename(file_path))
        processing_status[video_id] = {"status": "transcribing", "progress": 0.3}
        
        # Transcribe audio
        segments = transcriber.transcribe(audio_path, video_id)
        processing_status[video_id] = {"status": "processing_text", "progress": 0.7}
        
        # Chunk transcript
        chunks = text_processor.chunk_transcript(segments, video_id)
        
        # Create embeddings and store in vector database
        embeddings = [text_processor.embed_text(chunk["text"]) for chunk in chunks]
        vector_store.store_chunks(video_id, chunks, embeddings)
        
        # Update status and metadata
        processing_status[video_id] = {"status": "completed", "progress": 1.0}
        if video_id in video_metadata:
            video_metadata[video_id]["status"] = "processed"
            video_metadata[video_id]["transcript_available"] = True
    
    except Exception as e:
        print(f"Error processing video {video_id}: {str(e)}")
        processing_status[video_id] = {"status": "error", "progress": 0, "error": str(e)}
        if video_id in video_metadata:
            video_metadata[video_id]["status"] = "error"


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload a video file and start processing it.
    """
    # Generate a unique ID for the video
    video_id = str(uuid.uuid4())
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Store metadata
    video_metadata[video_id] = {
        "video_id": video_id,
        "filename": file.filename,
        "upload_time": datetime.now().isoformat(),
        "status": "processing",
        "transcript_available": False
    }
    
    # Initialize processing status
    processing_status[video_id] = {"status": "queued", "progress": 0}
    
    # Start background processing
    background_tasks.add_task(process_video, video_id, file_path)
    
    return {"video_id": video_id, "message": "Video uploaded successfully and processing started"}


@router.get("/status/{video_id}", response_model=TranscriptionStatus)
async def get_processing_status(video_id: str):
    """
    Get the processing status of a video.
    """
    if video_id not in processing_status:
        raise HTTPException(status_code=404, detail="Video not found")
    
    status = processing_status[video_id]
    return {
        "video_id": video_id,
        "status": status.get("status", "unknown"),
        "progress": status.get("progress", 0),
        "error": status.get("error")
    }


@router.get("/", response_model=List[VideoMetadata])
async def list_videos():
    """
    List all uploaded videos and their metadata.
    """
    return list(video_metadata.values())


@router.get("/{video_id}", response_model=VideoMetadata)
async def get_video_metadata(video_id: str):
    """
    Get metadata for a specific video.
    """
    if video_id not in video_metadata:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video_metadata[video_id] 