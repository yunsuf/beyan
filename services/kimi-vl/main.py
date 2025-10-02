"""
Kimi-VL Service for Beyan Document Digitization System
n8n-compatible API wrapper for document processing models.
Supports multiple processing modes (local, openrouter).
"""

import os
import asyncio
import logging
import base64
import json
from typing import Dict, Any, Optional, Protocol, List
from datetime import datetime

import httpx
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import aiofiles
from dotenv import load_dotenv
import fitz  # PyMuPDF

# Optional LangSmith tracing
try:
    from langsmith.run_trees import RunTree  # type: ignore
except Exception:  # pragma: no cover - optional dep
    RunTree = None  # type: ignore

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
PROCESSING_MODE = os.getenv("PROCESSING_MODE", "openrouter")

# Local Model Config
MODEL_PATH = os.getenv("MODEL_PATH", "/models/kimi-vl")
DEVICE = os.getenv("DEVICE", "auto")

# OpenRouter Config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL_NAME = os.getenv("OPENROUTER_MODEL_NAME", "google/gemini-flash-1.5")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# API Server Config
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8001"))

# LangSmith config (optional)
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() in {"1", "true", "yes"}
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "beyan")

# Routing config (optional)
ROUTING_BUDGET = os.getenv("ROUTING_BUDGET", "low")
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "false").lower() in {"1", "true", "yes"}


# --- FastAPI App Initialization ---
app = FastAPI(
    title="Document Processing Service for Beyan",
    description="A configurable API wrapper for document processing models.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models for API ---
class ProcessingResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    filename: Optional[str] = None
    processing_time: Optional[str] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    processing_mode: str
    model_info: Dict[str, Any]
    timestamp: str


class OrchestrationResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    filename: Optional[str] = None
    processing_time: Optional[str] = None
    steps: Optional[List[str]] = None
    timestamp: str


# --- Processor Interface and Implementations ---

class DocumentProcessor(Protocol):
    """A protocol defining the interface for any document processor."""
    async def load(self) -> None:
        ... # pragma: no cover

    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        ... # pragma: no cover

    def get_status(self) -> Dict[str, Any]:
        ... # pragma: no cover

class LocalProcessor:
    """
    Processor for a locally hosted model.
    Currently uses mock data.
    """
    def __init__(self, model_path: str, device: str):
        self.model_path = model_path
        self.device = device
        self.model_loaded = False
        logger.info(f"Initializing LocalProcessor with model: {model_path}, device: {device}")

    async def load(self) -> None:
        """Load the Kimi-VL model."""
        try:
            logger.info("Simulating model loading for LocalProcessor...")
            await asyncio.sleep(2)
            self.model_loaded = True
            logger.info("Local model loaded successfully (mock).")
        except Exception as e:
            logger.error(f"Failed to load local model: {e}")
            raise

    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process document with the local model."""
        if not self.model_loaded:
            raise HTTPException(status_code=503, detail="Local model not loaded")

        logger.info(f"Processing '{filename}' with LocalProcessor (mock).")
        # Mock processing results (replace with actual local model processing)
        return {
            "text_content": f"Extracted text from {filename}\n\nThis is MOCK extracted text from the LOCAL processor.",
            "confidence": 0.92,
            "metadata": {
                "pages": 1,
                "language": "en",
                "document_type": "commercial_invoice",
                "processing_method": "local_mock",
                "model_name": self.model_path
            },
            "extracted_fields": {
                "invoice_number": "INV-LOCAL-MOCK",
                "date": "2024-01-28",
                "total_amount": 1250.00,
                "currency": "USD"
            }
        }

    def get_status(self) -> Dict[str, Any]:
        return {"model_path": self.model_path, "device": self.device, "loaded": self.model_loaded}


class OpenRouterProcessor:
    """Processor that uses the OpenRouter API."""
    def __init__(self, api_key: str, model_name: str):
        if not api_key or api_key == "your_openrouter_api_key_here":
            raise ValueError("OPENROUTER_API_KEY is not configured. Please set it in your .env file.")
        self.api_key = api_key
        self.model_name = model_name
        self.client = httpx.AsyncClient(timeout=120.0)
        logger.info(f"Initializing OpenRouterProcessor with model: {self.model_name}")

    async def load(self) -> None:
        """No model to load for API-based processor."""
        logger.info("OpenRouterProcessor is ready. No local model loading required.")
        await asyncio.sleep(0)

    def _get_extraction_prompt(self) -> str:
        """Returns the detailed prompt for invoice extraction."""
        # This schema is based on the analysis of the sample documents
        return '''
        You are an expert document analysis AI. A user has uploaded a document image.
        Your task is to meticulously extract all specified fields from the document and return the data in a valid JSON format.

        **Instructions:**
        1.  Analyze the document image provided.
        2.  Extract the data for the fields defined in the JSON schema below.
        3.  Pay close attention to line items. Extract every line item into the `line_items` array.
        4.  If a field is not present in the document, use `null` as the value.
        5.  Ensure all numbers are returned as numbers (e.g., 123.45), not strings.
        6.  Dates should be in YYYY-MM-DD format if possible.
        7.  Your final output must be ONLY the JSON object, with no surrounding text or markdown.

        **JSON Schema to Populate:**
        ```json
        {
          "invoice_number": "string",
          "invoice_date": "string",
          "po_number": "string",
          "seller": {
            "name": "string",
            "address": "string"
          },
          "buyer": {
            "name": "string",
            "address": "string"
          },
          "consignee": {
            "name": "string",
            "address": "string"
          },
          "delivery_and_payment_term": "string",
          "country_of_origin": "string",
          "line_items": [
            {
              "model_code": "string",
              "goods_description": "string",
              "quantity": "number",
              "unit_price": "number",
              "amount": "number"
            }
          ],
          "total_amount": "number",
          "total_currency": "string"
        }
        ```
        '''

    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process document by calling the OpenRouter API."""
        logger.info(f"Processing '{filename}' with OpenRouterProcessor.")
        
        base64_image = base64.b64encode(file_content).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": self._get_extraction_prompt()
                        }
                    ]
                }
            ]
        }

        try:
            response = await self.client.post(OPENROUTER_API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            response_json = response.json()
            message_content = response_json["choices"][0]["message"]["content"]
            
            # Clean up the response to get only the JSON part
            json_content_str = message_content.strip().lstrip("```json").rstrip("```")
            extracted_data = json.loads(json_content_str)

            # Build concise text summary for downstream classifiers
            try:
                invoice_number = extracted_data.get("invoice_number")
                invoice_date = extracted_data.get("invoice_date")
                buyer_name = (extracted_data.get("buyer") or {}).get("name")
                seller_name = (extracted_data.get("seller") or {}).get("name")
                total_amount = extracted_data.get("total_amount")
                total_currency = extracted_data.get("total_currency")
                line_items = extracted_data.get("line_items") or []
                text_content = (
                    f"Invoice {invoice_number or 'N/A'} dated {invoice_date or 'N/A'}; "
                    f"Buyer: {buyer_name or 'N/A'}; Seller: {seller_name or 'N/A'}; "
                    f"{len(line_items)} line items; Total: {total_amount if total_amount is not None else 'N/A'} "
                    f"{total_currency or ''}".strip()
                )
            except Exception:
                text_content = "Document extraction summary unavailable"

            # Compute a simple completeness-based confidence score (0..1)
            try:
                required_top = [
                    "invoice_number", "invoice_date", "total_amount", "total_currency",
                    "buyer", "seller"
                ]
                present = 0
                for k in required_top:
                    v = extracted_data.get(k)
                    if isinstance(v, dict):
                        # count as present if any non-empty value
                        present += 1 if any(bool(x) for x in v.values()) else 0
                    else:
                        present += 1 if (v is not None and v != "") else 0
                # Line items presence contributes as well
                li = extracted_data.get("line_items") or []
                present += 1 if len(li) > 0 else 0
                expected = len(required_top) + 1
                confidence = max(0.0, min(1.0, present / expected))
            except Exception:
                confidence = 0.5

            return {
                "text_content": text_content,
                "confidence": round(confidence, 2),
                "extracted_fields": extracted_data,
                "metadata": {
                    "processing_method": "openrouter",
                    "model_name": self.model_name
                }
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling OpenRouter: {e.response.status_code} {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"OpenRouter API error: {e.response.text}")
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"Failed to parse response from OpenRouter: {e}")
            logger.error(f"Raw response content: {message_content}")
            raise HTTPException(status_code=500, detail="Failed to parse model response.")
        except Exception as e:
            logger.error(f"An unexpected error occurred with OpenRouter: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_status(self) -> Dict[str, Any]:
        return {"model_name": self.model_name, "api_url": OPENROUTER_API_URL}

    async def process_with_prompt(self, file_content: bytes, filename: str, prompt: str) -> Dict[str, Any]:
        """Call OpenRouter with a custom prompt and return parsed JSON content.
        Returns a dict with keys: extracted_fields, raw_message (optional).
        """
        base64_image = base64.b64encode(file_content).decode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        }
        try:
            resp = await self.client.post(OPENROUTER_API_URL, headers=headers, json=data)
            resp.raise_for_status()
            response_json = resp.json()
            message_content = response_json["choices"][0]["message"]["content"]
            json_content_str = message_content.strip().lstrip("```json").rstrip("```")
            extracted = json.loads(json_content_str)
            return {"extracted_fields": extracted, "raw_message": message_content}
        except Exception as e:
            logger.error(f"process_with_prompt failed for {filename}: {e}")
            raise


# --- Global Processor Initialization ---

processor: DocumentProcessor

if PROCESSING_MODE == "local":
    processor = LocalProcessor(model_path=MODEL_PATH, device=DEVICE)
elif PROCESSING_MODE == "openrouter":
    try:
        processor = OpenRouterProcessor(api_key=OPENROUTER_API_KEY, model_name=OPENROUTER_MODEL_NAME)
    except ValueError as e:
        logger.warning(f"OpenRouter not configured ({e}). Falling back to LocalProcessor.")
        processor = LocalProcessor(model_path=MODEL_PATH, device=DEVICE)
else:
    raise ValueError(f"Invalid PROCESSING_MODE: '{PROCESSING_MODE}'. Choose 'local' or 'openrouter'.")


# --- FastAPI Events and Endpoints ---

@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup."""
    logger.info(f"Starting service in '{PROCESSING_MODE}' mode.")
    try:
        await processor.load()
        logger.info("Service started successfully.")
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        raise

@app.post("/process", response_model=ProcessingResponse)
async def process_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> ProcessingResponse:
    """
    Process a document using the configured processing mode.
    """
    timestamp = datetime.now().isoformat()
    start_time = datetime.now()

    # (no tracing for classic /process endpoint)

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"Processing document: {file.filename} ({len(content)} bytes)")
        
        result = await processor.process_document(content, file.filename)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        result["processing_time_seconds"] = processing_time
        
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
        logger.error(f"Unexpected error in /process endpoint for {file.filename}: {e}", exc_info=True)
        return ProcessingResponse(
            success=False,
            error=str(e),
            filename=file.filename,
            timestamp=timestamp
        )


# --- Smart Router Init (Phase 1, OpenRouter-only) ---
try:
    from router.registry import ModelRegistry
    from router.policy import RoutingPolicy
    from router.smart_router import SmartRouter
    from router.adapters.openrouter import OpenRouterAdapter

    _REGISTRY = ModelRegistry(portfolio_path="config/models.yml")
    _POLICY = RoutingPolicy(routing_path="config/routing.yml")
    _ROUTER = SmartRouter(registry=_REGISTRY, policy=_POLICY)
    _OPENROUTER_BASE = (_REGISTRY.get_provider("openrouter") or {}).get("base_url", "https://openrouter.ai/api/v1")
    _OR_ADAPTER = OpenRouterAdapter(api_key=OPENROUTER_API_KEY, base_url=_OPENROUTER_BASE)
    logger.info("Smart Router initialized (Phase 1)")
except Exception as e:
    _REGISTRY = None
    _POLICY = None
    _ROUTER = None
    _OR_ADAPTER = None
    logger.warning(f"Smart Router not initialized: {e}")

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="document-processor",
        version="1.1.0",
        processing_mode=PROCESSING_MODE,
        model_info=processor.get_status(),
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Document Processing Service for Beyan",
        "version": "1.1.0",
        "status": "running",
        "processing_mode": PROCESSING_MODE,
        "endpoints": {
            "process": "/process",
            "health": "/health",
            "docs": "/docs",
            "orchestrate": "/orchestrate"
        }
    }

async def save_processed_file(filename: str, content: bytes, result: Dict[str, Any]):
    """Save original file and results in the background."""
    try:
        os.makedirs("/processed", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = os.path.basename(filename).replace("/", "_")
        base_no_ext = os.path.splitext(safe_name)[0]
        target_dir = os.path.join("/processed", f"{ts}__{base_no_ext}")
        os.makedirs(target_dir, exist_ok=True)

        # Write original upload
        upload_path = os.path.join(target_dir, safe_name)
        async with aiofiles.open(upload_path, "wb") as f:
            await f.write(content)

        # Write output.json (model result)
        output_path = os.path.join(target_dir, "output.json")
        async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(result, ensure_ascii=False, indent=2))

        # Write metadata.json (service metadata)
        metadata = {
            "filename": filename,
            "saved_at": datetime.now().isoformat(),
            "processing_mode": PROCESSING_MODE,
            "version": "1.1.0"
        }
        meta_path = os.path.join(target_dir, "metadata.json")
        async with aiofiles.open(meta_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(metadata, ensure_ascii=False, indent=2))

        logger.info(f"Saved processed artifacts to {target_dir}")
    except Exception as e:
        logger.error(f"Failed to save processed file artifacts for {filename}: {e}", exc_info=True)


# --- Hybrid Orchestrator Utilities (LangGraph-style staging) ---

def _header_prompt() -> str:
    return (
        "Extract ONLY top-level header/footer fields for a commercial invoice and return valid JSON. "
        "Schema: {\n  \"invoice_number\": \"string\",\n  \"invoice_date\": \"YYYY-MM-DD\",\n  \"buyer\": {\"name\": \"string\", \"address\": \"string\"},\n  \"seller\": {\"name\": \"string\", \"address\": \"string\"},\n  \"total_amount\": \"number\",\n  \"total_currency\": \"string\"\n}"
    )


def _line_items_prompt() -> str:
    return (
        "Extract ONLY line items from the page and return valid JSON with key 'line_items' as an array of rows. "
        "Row Schema: {\n  \"model_code\": \"string\",\n  \"goods_description\": \"string\",\n  \"quantity\": \"number\",\n  \"unit_price\": \"number\",\n  \"amount\": \"number\"\n}"
    )


def _render_pdf_pages(pdf_bytes: bytes, dpi: int = 200) -> List[bytes]:
    """Render each PDF page to PNG bytes using PyMuPDF."""
    pages_png: List[bytes] = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        pages_png.append(pix.tobytes("png"))
    return pages_png


def _compute_confidence(extracted_fields: Dict[str, Any]) -> float:
    required_top = [
        "invoice_number",
        "invoice_date",
        "total_amount",
        "total_currency",
        "buyer",
        "seller",
    ]
    present = 0
    for k in required_top:
        v = extracted_fields.get(k)
        if isinstance(v, dict):
            present += 1 if any(bool(x) for x in v.values()) else 0
        else:
            present += 1 if (v is not None and v != "") else 0
    li = extracted_fields.get("line_items") or []
    present += 1 if len(li) > 0 else 0
    expected = len(required_top) + 1
    return max(0.0, min(1.0, present / expected))


def _build_summary(extracted_fields: Dict[str, Any]) -> str:
    invoice_number = extracted_fields.get("invoice_number")
    invoice_date = extracted_fields.get("invoice_date")
    buyer_name = (extracted_fields.get("buyer") or {}).get("name")
    seller_name = (extracted_fields.get("seller") or {}).get("name")
    total_amount = extracted_fields.get("total_amount")
    total_currency = extracted_fields.get("total_currency")
    line_items = extracted_fields.get("line_items") or []
    return (
        f"Invoice {invoice_number or 'N/A'} dated {invoice_date or 'N/A'}; "
        f"Buyer: {buyer_name or 'N/A'}; Seller: {seller_name or 'N/A'}; "
        f"{len(line_items)} line items; Total: {total_amount if total_amount is not None else 'N/A'} "
        f"{total_currency or ''}".strip()
    )


@app.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
) -> OrchestrationResponse:
    """Hybrid orchestrator endpoint using staged extraction steps.
    n8n should call this endpoint as a single step after ingestion.
    """
    timestamp = datetime.now().isoformat()
    start_time = datetime.now()
    steps: List[str] = []
    # Optional tracing root
    root_run = None
    if RunTree and LANGCHAIN_TRACING_V2:
        try:
            root_run = RunTree(name="orchestrate", inputs={"filename": getattr(file, "filename", None)}, project_name=LANGCHAIN_PROJECT)
        except Exception:
            root_run = None
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")

        logger.info(f"[Hybrid] Orchestrating document: {file.filename} ({len(content)} bytes)")
        steps.append("ingestion")

        # Split into page images if PDF
        page_images: List[bytes]
        if file.filename.lower().endswith(".pdf"):
            page_images = _render_pdf_pages(content)
            steps.append(f"split_pdf:{len(page_images)}_pages")
        else:
            page_images = [content]
            steps.append("single_image")

        router_meta: Dict[str, Any] = {"decisions": []}

        # Build routing features (Phase 1: simple heuristics)
        features_common = {
            "page_count": len(page_images),
            "doc_type": "invoice",  # TODO: plug a lightweight classifier
            "budget": ROUTING_BUDGET,
            "offline_mode": OFFLINE_MODE,
            "required_capabilities": ["vision", "json"],
        }

        header_result: Dict[str, Any]
        # Try Smart Router first
        used_router = False
        if _ROUTER is not None:
            try:
                sel = _ROUTER.select("header_extraction", features_common)
                router_meta["decisions"].append({"task": "header_extraction", **sel})
                if sel.get("provider") == "openrouter" and _OR_ADAPTER and _OR_ADAPTER.is_configured():
                    hdr = await _OR_ADAPTER.extract_json(_header_prompt(), [page_images[0]], sel.get("model_name"))
                    header_result = {"extracted_fields": hdr.get("extracted_fields", {})}
                    used_router = True
                    steps.append("extract_header(router)")
                else:
                    steps.append("extract_header(router_unavailable)")
            except Exception as e:
                logger.warning(f"Router header selection failed, fallback: {e}")

        if not used_router:
            if isinstance(processor, OpenRouterProcessor):
                header = await processor.process_with_prompt(page_images[0], f"{file.filename}#p1", _header_prompt())
                header_result = {"extracted_fields": header.get("extracted_fields", {})}
                steps.append("extract_header")
            else:
                # Fallback: use existing process and then subset
                interim = await processor.process_document(page_images[0], f"{file.filename}#p1")
                header_result = {"extracted_fields": {k: interim.get("extracted_fields", {}).get(k) for k in [
                    "invoice_number", "invoice_date", "buyer", "seller", "total_amount", "total_currency"
                ]}}
                steps.append("extract_header_fallback")

        # Extract line items from all pages
        aggregated_items: List[Dict[str, Any]] = []
        used_router_items = False
        if _ROUTER is not None:
            try:
                sel_items = _ROUTER.select("line_items", features_common)
                router_meta["decisions"].append({"task": "line_items", **sel_items})
                if sel_items.get("provider") == "openrouter" and _OR_ADAPTER and _OR_ADAPTER.is_configured():
                    for idx, img in enumerate(page_images, start=1):
                        li = await _OR_ADAPTER.extract_json(_line_items_prompt(), [img], sel_items.get("model_name"))
                        page_items = (li.get("extracted_fields", {}) or {}).get("line_items") or []
                        aggregated_items.extend(page_items)
                    used_router_items = True
                    steps.append("extract_line_items(router)")
            except Exception as e:
                logger.warning(f"Router line_items selection failed, fallback: {e}")

        if not used_router_items:
            if isinstance(processor, OpenRouterProcessor):
                for idx, img in enumerate(page_images, start=1):
                    li = await processor.process_with_prompt(img, f"{file.filename}#p{idx}", _line_items_prompt())
                    page_items = (li.get("extracted_fields", {}) or {}).get("line_items") or []
                    aggregated_items.extend(page_items)
                steps.append("extract_line_items")
            else:
                # Fallback: take whatever items already present
                try:
                    items = (interim.get("extracted_fields", {}) or {}).get("line_items") or []
                    aggregated_items.extend(items)
                except NameError:
                    # No interim available (e.g., header used router). Leave items empty.
                    logger.warning("No interim available for line_items fallback; continuing with empty items.")
                steps.append("extract_line_items_fallback")

        # Merge
        fields = header_result.get("extracted_fields", {}) or {}
        fields["line_items"] = aggregated_items
        steps.append("merge")

        # Compute confidence and summary
        confidence = round(_compute_confidence(fields), 2)
        text_content = _build_summary(fields)
        result = {
            "text_content": text_content,
            "confidence": confidence,
            "extracted_fields": fields,
            "metadata": {
                "processing_method": f"hybrid:{PROCESSING_MODE}",
                "pages": len(page_images),
                "router": router_meta,
            },
        }

        processing_time = (datetime.now() - start_time).total_seconds()
        result["processing_time_seconds"] = processing_time
        background_tasks.add_task(save_processed_file, file.filename, content, result)

        # End tracing if enabled
        if root_run is not None:
            try:
                root_run.end(outputs={"success": True, "filename": file.filename, "confidence": confidence, "steps": steps})
            except Exception:
                pass

        return OrchestrationResponse(
            success=True,
            data=result,
            filename=file.filename,
            processing_time=f"{processing_time:.2f}s",
            steps=steps,
            timestamp=timestamp,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /orchestrate for {file.filename}: {e}", exc_info=True)
        if root_run is not None:
            try:
                root_run.end(error=str(e), outputs={"success": False, "filename": getattr(file, "filename", None), "steps": steps})
            except Exception:
                pass
        return OrchestrationResponse(
            success=False,
            error=str(e),
            filename=file.filename,
            steps=steps,
            timestamp=timestamp,
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )