import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
AUDIO_DIR = os.path.join(BASE_DIR, "data", "audio")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "data", "transcripts")
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")
VECTORDB_DIR = os.path.join(BASE_DIR, "data", "vectordb")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(VECTORDB_DIR, exist_ok=True)

# API settings
API_V1_STR = "/api/v1"
PROJECT_NAME = "Lecture Intelligence"

# Whisper model settings
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"

# Embedding model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# File upload settings
MAX_UPLOAD_SIZE = 1024 * 1024 * 1024 * 2  # 2GB

# Processing settings
MAX_CHUNK_WORDS = 100
TOP_K_RESULTS = 3 