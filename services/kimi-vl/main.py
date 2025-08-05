"""
Kimi-VL Service for Beyan Document Digitization System
n8n-compatible API wrapper for Kimi-VL model
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import aiofiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Kimi-VL Service for Beyan",
    description="n8n-compatible API wrapper for Kimi-VL document processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "/models/kimi-vl")
DEVICE = os.getenv("DEVICE", "auto")
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "4"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8001"))

# Response models
class ProcessingResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    filename: Optional[str] = None
    processing_time: Optional[str] = None
    timestamp: str

class  HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool
    device: str
    timestamp: str

# Mock Kimi-VL Processor (replace with actual implementation)
class KimiVLProcessor:
    def __init__(self, model_path: str, device: str):
        self.model_path = model_path
        self.device = device
        self.model_loaded = False
        logger.info(f"Initializing Kimi-VL processor with model: {model_path}, device: {device}")
        
    async def load_model(self):
        """Load the Kimi-VL model"""
        try:
            # Simulate model loading
            await asyncio.sleep(2)
            self.model_loaded = True
            logger.info("Kimi-VL model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Kimi-VL model: {e}")
            raise
    
    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process document with Kimi-VL"""
        if not self.model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        start_time = datetime.now()
        
        try:
            # Simulate document processing
            await asyncio.sleep(1)  # Simulate processing time
            
            # Mock processing results (replace with actual Kimi-VL processing)
            result = {
                "text_content": f"Extracted text from {filename}\n\nThis is mock extracted text content.",
                "confidence": 0.92,
                "metadata": {
                    "pages": 1,
                    "language": "en",
                    "document_type": "commercial_invoice",
                    "processing_method": "kimi-vl",
                    "model_version": "1.0.0"
                },
                "extracted_fields": {
                    "invoice_number": "INV-2024-001",
                    "date": "2024-01-28",
                    "total_amount": 1250.00,
                    "currency": "USD"
                }
            }
            
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_time_seconds"] = processing_time
            
            logger.info(f"Successfully processed {filename} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# Initialize processor
processor = KimiVLProcessor(MODEL_PATH, DEVICE)

@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup"""
    logger.info("Starting Kimi-VL service...")
    try:
        await processor.load_model()
        logger.info("Kimi-VL service started successfully")
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        raise

@app.post("/process", response_model=ProcessingResponse)
async def process_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> ProcessingResponse:
    """
    Process document using Kimi-VL model
    n8n-compatible endpoint for document processing
    """
    timestamp = datetime.now().isoformat()
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Read file content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"Processing document: {file.filename} ({len(content)} bytes)")
        
        # Process with Kimi-VL
        start_time = datetime.now()
        result = await processor.process_document(content, file.filename)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Save processed file (background task)
        background_tasks.add_task(save_processed_file, file.filename, content, result)
        
        return ProcessingResponse(
            success=True,
            data=result,
            filename=file.filename,
            processing_time=f"{processing_time:.2f}s",
            timestamp=timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing {file.filename}: {e}")
        return ProcessingResponse(
            success=False,
            error=str(e),
            filename=file.filename,
            timestamp=timestamp
        )

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if processor.model_loaded else "unhealthy",
        service="kimi-vl",
        version="1.0.0",
        model_loaded=processor.model_loaded,
        device=DEVICE,
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Kimi-VL Service for Beyan",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "process": "/process",
            "health": "/health",
            "docs": "/docs"
        }
    }

async def save_processed_file(filename: str, content: bytes, result: Dict[str, Any]):
    """Save processed file and results (background task)"""
    try:
        # Save original file
        upload_path = f"/uploads/{filename}"
        async with aiofiles.open(upload_path, "wb") as f:
            await f.write(content)
        
        # Save processing results
        result_path = f"/processed/{filename}.json"
        import json
        async with aiofiles.open(result_path, "w") as f:
            await f.write(json.dumps(result, indent=2))
        
        logger.info(f"Saved processed results for {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save processed file {filename}: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
