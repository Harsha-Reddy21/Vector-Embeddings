from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class VideoUploadResponse(BaseModel):
    video_id: str
    message: str


class TranscriptionStatus(BaseModel):
    video_id: str
    status: str
    progress: Optional[float] = None
    error: Optional[str] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    video_id: str
    message: str


class TimestampedChunk(BaseModel):
    text: str
    start: float
    end: float


class ChatResponse(BaseModel):
    message: str
    timestamps: List[Dict[str, float]] = Field(default_factory=list)
    source_chunks: List[TimestampedChunk] = Field(default_factory=list)


class VideoMetadata(BaseModel):
    video_id: str
    filename: str
    duration: Optional[float] = None
    upload_time: str
    status: str
    transcript_available: bool = False 