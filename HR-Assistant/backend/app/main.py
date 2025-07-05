from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import shutil
from pydantic import BaseModel
import uuid

from app.services.document_processor import DocumentProcessor
from app.services.query_engine import QueryEngine
from app.services.vector_store import VectorStore

app = FastAPI(title="HR Onboarding Knowledge Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_store = VectorStore()
document_processor = DocumentProcessor(vector_store)
query_engine = QueryEngine(vector_store)

# Create upload directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    categories: Optional[List[str]] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    category: str

@app.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    document_type: str = Form(...),
    category: str = Form(...)
):
    """Upload HR documents for processing"""
    
    saved_files = []
    
    try:
        for file in files:
            # Generate a unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join("uploads", unique_filename)
            
            # Save the file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_files.append({
                "original_name": file.filename,
                "saved_path": file_path,
                "category": category,
                "document_type": document_type
            })
        
        # Process documents in the background
        background_tasks.add_task(
            document_processor.process_documents, 
            saved_files
        )
        
        return JSONResponse(
            status_code=200,
            content={"message": f"Successfully uploaded {len(files)} files. Processing started."}
        )
    
    except Exception as e:
        # Clean up any saved files in case of error
        for file_info in saved_files:
            if os.path.exists(file_info["saved_path"]):
                os.remove(file_info["saved_path"])
        
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_hr_assistant(request: QueryRequest):
    """Query the HR assistant with a question"""
    try:
        result = query_engine.generate_response(
            request.query, 
            categories=request.categories
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    """Get all available document categories"""
    try:
        categories = vector_store.get_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    """Get all processed documents"""
    try:
        documents = vector_store.get_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the system"""
    try:
        vector_store.delete_document(document_id)
        return {"message": f"Document {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 