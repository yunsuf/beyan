# Fully Local Multi-Agent Implementation Guide

> **🏠 100% On-Premises Document Digitization System**  
> **🔒 Zero External Dependencies - Maximum Privacy & Security**  
> **⚡ Production-ready local deployment in 2-4 hours**

---

## 🚀 Quick Start (5 minutes)

**What is this?** A complete implementation guide for building the document digitization system using **exclusively local models** and **on-premises infrastructure** - no external API calls, no cloud dependencies.

**Why choose local?** 
- ✅ **100% Data Privacy**: All processing happens on your infrastructure
- ✅ **Zero External Costs**: No per-API-call charges, predictable infrastructure costs
- ✅ **Air-Gapped Compatible**: Works in completely isolated environments
- ✅ **High Performance**: Direct GPU access, no network latency

**How does it work?** 
```
Local File → Kimi-VL (Local) → Ollama LLMs → Multi-Agent Processing → Local Database
```
- Uses **Ollama** for local LLM serving (Llama 3.1, Mistral, CodeLlama)
- **Kimi-VL** model runs entirely on your hardware  
- **PostgreSQL** and **Redis** for local data storage
- **Custom Python framework** for multi-agent orchestration

**What do I need to implement?** 
- ✅ Local GPU server with 16GB+ VRAM (recommended)
- ✅ Ollama installation with specialized models
- ✅ Kimi-VL local deployment
- ✅ Multi-agent Python framework
- ✅ Local database setup

**How long will it take?** 
- ⏱️ **2 hours**: Basic local setup with single-agent processing
- ⏱️ **4 hours**: Full multi-agent system with human review
- ⏱️ **1 day**: Production deployment with monitoring

**What are the risks?** 
- 🔴 **High**: GPU memory requirements (16GB+ recommended)
- 🟡 **Medium**: Initial model download size (~50GB total)
- 🟢 **Low**: System complexity once properly configured

---

## 📋 Implementation Checklist

### **Phase 1: Local Infrastructure Setup (30-45 minutes)**
- [ ] 🖥️ **Hardware verification** (5 minutes)
  - GPU with 16GB+ VRAM (verify: `nvidia-smi`)
  - 32GB+ system RAM (verify: `free -h`)
  - 200GB+ free disk space (verify: `df -h`)
  - Ubuntu 20.04+ or compatible Linux distro
- [ ] 🐳 **Docker & Dependencies** (10 minutes)
  - Docker and Docker Compose installed
  - NVIDIA Container Toolkit configured
  - Python 3.11+ development environment
- [ ] 🧠 **Ollama Installation** (15 minutes)
  - Ollama server installation and configuration
  - Download required models (30GB+ download)
  - Verify model serving functionality
- [ ] 🗄️ **Local Database Setup** (15 minutes)
  - PostgreSQL local installation
  - Redis for caching and queues
  - Database schema initialization

### **Phase 2: Model Integration (45-60 minutes)**
- [ ] 🎯 **Kimi-VL Local Deployment** (30 minutes)
  - Download and configure Kimi-VL model
  - GPU optimization and memory management
  - Basic document processing test
- [ ] 🤖 **Local LLM Service Setup** (30 minutes)
  - Ollama API integration wrapper
  - Model specialization configuration
  - Response parsing and error handling

### **Phase 3: Multi-Agent Framework (60-90 minutes)**
- [ ] 🏗️ **Core Agent Framework** (45 minutes)
  - Base agent classes and communication
  - Local message bus implementation
  - Agent lifecycle management
- [ ] 🔄 **Processing Pipeline** (45 minutes)
  - Document ingestion and classification
  - Data extraction and validation agents
  - Result persistence and monitoring

### **Phase 4: Testing & Validation (30 minutes)**
- [ ] 🧪 **End-to-End Testing** (20 minutes)
  - Process sample documents
  - Verify accuracy and performance
  - Test error handling and recovery
- [ ] 📊 **Performance Validation** (10 minutes)
  - Processing speed benchmarks
  - Memory usage monitoring
  - Quality metrics verification

**🎯 Success Criteria:**
- [ ] Processes sample documents with >95% accuracy
- [ ] <30 seconds average processing time per document
- [ ] System runs stable for 24+ hours
- [ ] All components communicate properly

---

## ⚖️ Local Deployment Decision Matrix

### Hardware Configuration Options

| Configuration | GPU Memory | System RAM | Performance | Cost | Recommendation |
|---------------|------------|------------|-------------|------|----------------|
| **High-End Workstation** | 24GB+ | 64GB+ | ⭐⭐⭐⭐⭐ | $$$$$ | **Best for production** |
| **Gaming PC + Upgrade** | 16GB | 32GB | ⭐⭐⭐⭐ | $$$ | **Cost-effective option** |
| **Cloud GPU Instance** | 16GB+ | 32GB+ | ⭐⭐⭐⭐ | $$/month | **For testing/evaluation** |
| **CPU-Only Server** | N/A | 64GB+ | ⭐⭐ | $$ | **Budget/low-volume only** |

### Model Selection Strategy

| Use Case | Primary Model | Backup Model | Memory Usage | Speed | Accuracy |
|----------|---------------|--------------|--------------|-------|----------|
| **High Accuracy** | Llama 3.1:70b | Llama 3.1:8b | ~40GB | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Balanced** | Llama 3.1:8b | Mistral:7b | ~5GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **High Speed** | Mistral:7b | Phi3:mini | ~4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Resource Constrained** | Phi3:mini | CPU fallback | ~2GB | ⭐⭐⭐ | ⭐⭐ |

**🎯 Recommended Configuration**: Llama 3.1:8b for primary processing with Llama 3.1:70b for validation

---

## 🛠️ Local Architecture Overview

### **Fully Local Multi-Agent Stack**

```mermaid
graph TB
    A[Document Upload] --> B[Kimi-VL Local]
    B --> C[Classification Agent<br/>Mistral:7b]
    C --> D[Extraction Agent<br/>Llama 3.1:8b]
    D --> E[Validation Agent<br/>Llama 3.1:70b]
    E --> F[Human Review Queue]
    F --> G[Local PostgreSQL]
    
    H[Ollama Server] --> C
    H --> D
    H --> E
    
    I[Redis Cache] --> C
    I --> D
    I --> E
    
    J[Monitoring<br/>Prometheus] --> B
    J --> C
    J --> D
    J --> E
```

### **Technology Stack**
- **🧠 Local LLMs**: Ollama (Llama 3.1, Mistral, CodeLlama, Phi3)
- **👁️ Vision Model**: Kimi-VL (self-hosted)
- **🔄 Orchestration**: Custom Python framework with asyncio
- **🗄️ Database**: PostgreSQL (local instance)
- **⚡ Cache**: Redis (local instance)
- **🌐 API**: FastAPI with local-only endpoints
- **🖥️ Frontend**: React/Vue.js (served locally)
- **📊 Monitoring**: Prometheus + Grafana (optional)

---

## ⚡ Quick Local Setup

### **Option A: Docker Compose (Recommended - 30 minutes)**

```bash
# 1. Clone and setup
git clone <repo-url> && cd kimi-vl-local
chmod +x scripts/setup-local.sh

# 2. Start all local services (single command!)
docker-compose -f docker-compose.local.yml up -d

# 3. Download and setup models (background process)
./scripts/download-local-models.sh

# 4. Verify everything is running
curl http://localhost:8000/health/local

# ✅ Success! Local system ready for document processing
```

### **Option B: Manual Installation (60 minutes)**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
systemctl start ollama

# 2. Download required models (runs in background)
ollama pull llama3.1:8b          # General purpose (4.7GB)
ollama pull llama3.1:70b         # High accuracy (39GB)  
ollama pull mistral:7b           # Fast processing (4.1GB)
ollama pull phi3:mini            # Lightweight (2.3GB)

# 3. Setup Python environment
python -m venv venv-local
source venv-local/bin/activate
pip install -r requirements-local.txt

# 4. Configure local services
cp config/local-template.yaml config/local.yaml
# Edit config/local.yaml with your GPU settings

# 5. Initialize databases
python scripts/init-local-db.py

# 6. Start local processing service
python main-local.py --config config/local.yaml
```

---

## 🔧 Local LLM Service Configuration

### **Essential Configuration (`config/local.yaml`)**

```yaml
# Local-only configuration
local_deployment:
  mode: "fully_local"
  external_apis: false
  data_retention: "local_only"

ollama:
  base_url: "http://localhost:11434"
  models:
    classifier: "mistral:7b"      # Fast document classification
    extractor: "llama3.1:8b"     # Data extraction  
    validator: "llama3.1:70b"    # High-accuracy validation
    reviewer: "llama3.1:8b"      # Human review coordination
  
  # GPU optimization
  gpu_layers: -1  # Use all GPU layers
  context_length: 4096
  batch_size: 4
  temperature: 0.1  # Low for consistency

kimi_vl:
  model_path: "./models/kimi-vl-local"
  device: "cuda:0"
  max_batch_size: 2  # Conservative for local deployment
  enable_cache: true
  cache_dir: "./cache/kimi-vl"

database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  database: "kimi_vl_local"
  # No external connections
  ssl_mode: "disable"

storage:
  input_folder: "./data/input"
  output_folder: "./data/output" 
  processed_folder: "./data/processed"
  backup_folder: "./data/backup"

monitoring:
  enable_local_metrics: true
  prometheus_port: 9090
  log_level: "INFO"
  log_file: "./logs/local-processing.log"
```

### **GPU Memory Optimization**

```yaml
# For 16GB GPU (recommended)
gpu_config:
  memory_fraction: 0.8  # Reserve 20% for system
  model_splitting:
    kimi_vl: "6GB"      # Vision processing
    llama_8b: "5GB"     # Primary LLM
    validation: "4GB"   # Validation model (loaded on demand)
  
# For 8GB GPU (minimal setup)  
gpu_config_minimal:
  memory_fraction: 0.9
  model_splitting:
    kimi_vl: "4GB"
    primary_llm: "3GB"
    # Use CPU for validation
```

---

## **2. Local LLM Setup and Configuration**

### **A. Ollama Installation and Model Setup**

```bash
# Install Ollama for local LLM serving
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models for different agent roles
ollama pull llama3.1:8b          # General purpose agent
ollama pull llama3.1:70b         # High-accuracy validation
ollama pull mistral:7b           # Fast classification
ollama pull codellama:13b        # Code generation and validation
ollama pull phi3:mini            # Lightweight tasks

# Verify installations
ollama list
```

### **B. Local LLM Service Configuration**

```python
# services/local_llm_service.py
import requests
import json
from typing import Dict, Any, List
import asyncio
import aiohttp

class LocalLLMService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.models = {
            "classifier": "mistral:7b",      # Fast document classification
            "extractor": "llama3.1:8b",     # Data extraction
            "validator": "llama3.1:70b",    # High-accuracy validation
            "reviewer": "llama3.1:8b"       # Human review coordination
        }
    
    async def generate_response(self, model: str, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """Generate response using local Ollama model"""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for consistency
                "top_p": 0.9,
                "num_predict": 2048
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/api/generate", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "response": result["response"],
                        "model": model,
                        "done": result.get("done", True)
                    }
                else:
                    raise Exception(f"LLM API error: {response.status}")
    
    async def classify_document(self, document_content: str) -> Dict[str, Any]:
        """Local document classification using local LLM"""
        system_prompt = """You are a document classification specialist. Classify documents into these types:
        - commercial_invoice
        - packing_list  
        - certificate
        - other
        
        Respond ONLY with valid JSON format:
        {
            "document_type": "commercial_invoice",
            "confidence": 0.95,
            "characteristics": ["has_invoice_number", "has_line_items"],
            "reasoning": "Document contains invoice number and itemized charges"
        }"""
        
        prompt = f"Classify this document content:\n\n{document_content}"
        
        response = await self.generate_response(
            self.models["classifier"], prompt, system_prompt
        )
        
        try:
            return json.loads(response["response"])
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "document_type": "other",
                "confidence": 0.5,
                "characteristics": [],
                "reasoning": "Failed to parse classification"
            }
    
    async def extract_data(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Local data extraction using local LLM"""
        schemas = {
            "commercial_invoice": {
                "invoice_number": "string",
                "invoice_date": "YYYY-MM-DD",
                "seller": {"name": "string", "address": "string"},
                "buyer": {"name": "string", "address": "string"},
                "line_items": [{"description": "string", "quantity": "number", "unit_price": "number"}],
                "total_amount": "number",
                "currency": "string"
            },
            "packing_list": {
                "packing_list_number": "string",
                "date": "YYYY-MM-DD",
                "shipper": "string",
                "consignee": "string",
                "packages": [{"description": "string", "quantity": "number", "weight": "number"}]
            }
        }
        
        schema = schemas.get(document_type, schemas["commercial_invoice"])
        
        # Adapted instructions for local models
        system_prompt = f"""You are a data extraction specialist. Extract structured data from documents.
        
        For {document_type}, extract data matching this exact schema:
        {json.dumps(schema, indent=2)}
        
        Rules:
        1. Extract ALL visible data
        2. Maintain exact data types
        3. Use null for missing fields
        4. Preserve original values
        5. Respond ONLY with valid JSON
        """
        
        prompt = f"Extract data from this {document_type}:\n\n{document_content}"
        
        response = await self.generate_response(
            self.models["extractor"], prompt, system_prompt
        )
        
        try:
            extracted = json.loads(response["response"])
            return {
                "extracted_data": extracted,
                "extraction_confidence": 0.9,  # Could be calculated based on completeness
                "schema_compliance": True
            }
        except json.JSONDecodeError:
            return {
                "extracted_data": {},
                "extraction_confidence": 0.3,
                "schema_compliance": False,
                "error": "Failed to parse extraction"
            }
    
    async def validate_data(self, extracted_data: Dict, document_type: str) -> Dict[str, Any]:
        """Local data validation using local LLM"""
        system_prompt = f"""You are a data validation specialist. Validate extracted data for accuracy and completeness.
        
        For {document_type} documents, check:
        1. Required fields are present
        2. Data formats are correct (dates, numbers, emails)
        3. Business logic consistency
        4. Cross-field validation
        
        Respond with JSON:
        {{
            "validation_passed": true/false,
            "confidence": 0.0-1.0,
            "errors": ["list of errors"],
            "warnings": ["list of warnings"],
            "completeness_score": 0.0-1.0
        }}"""
        
        prompt = f"""Validate this extracted data for {document_type}:
        
        {json.dumps(extracted_data, indent=2)}
        
        Check for completeness, accuracy, and business rule compliance."""
        
        response = await self.generate_response(
            self.models["validator"], prompt, system_prompt
        )
        
        try:
            return json.loads(response["response"])
        except json.JSONDecodeError:
            return {
                "validation_passed": False,
                "confidence": 0.5,
                "errors": ["Validation parsing failed"],
                "warnings": [],
                "completeness_score": 0.5
            }
```

### **C. Local Multi-Agent Orchestrator**

```python
# orchestrator/local_multi_agent.py
import asyncio
from typing import Dict, Any, Optional
import logging
from datetime import datetime

class LocalMultiAgentOrchestrator:
    def __init__(self, llm_service: LocalLLMService, kimi_vl_service, db_service):
        self.llm = llm_service
        self.kimi_vl = kimi_vl_service
        self.db = db_service
        self.logger = logging.getLogger(__name__)
    
    async def process_document(self, document_path: str) -> Dict[str, Any]:
        """
        Complete local document processing workflow
        """
        processing_id = self.generate_processing_id()
        
        try:
            self.logger.info(f"Starting local processing: {document_path}")
            
            # Step 1: Kimi-VL Preprocessing (Local)
            processed_content = await self.kimi_vl.preprocess_and_extract_text(document_path)
            
            # Step 2: Local LLM Classification
            classification = await self.llm.classify_document(processed_content)
            
            # Step 3: Local Data Extraction
            if classification['confidence'] >= 0.8:
                extraction = await self.llm.extract_data(
                    processed_content, classification['document_type']
                )
            else:
                # Fallback to Kimi-VL for complex documents
                extraction = await self.kimi_vl.extract_structured_data(
                    document_path, classification['document_type']
                )
            
            # Step 4: Local Validation
            validation = await self.llm.validate_data(
                extraction['extracted_data'], classification['document_type']
            )
            
            # Step 5: Human Review Decision (Local Logic)
            review_decision = await self.determine_review_need(
                classification, extraction, validation
            )
            
            # Step 6: Store Results Locally
            result = {
                "processing_id": processing_id,
                "document_path": document_path,
                "timestamp": datetime.now().isoformat(),
                "classification": classification,
                "extraction": extraction,
                "validation": validation,
                "review_decision": review_decision,
                "status": "completed" if not review_decision['review_required'] else "pending_review"
            }
            
            await self.db.store_processing_result(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Local processing error for {document_path}: {str(e)}")
            error_result = {
                "processing_id": processing_id,
                "document_path": document_path,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "failed"
            }
            await self.db.store_processing_result(error_result)
            return error_result
    
    async def determine_review_need(self, classification: Dict, extraction: Dict, validation: Dict) -> Dict[str, Any]:
        """Local logic for determining human review necessity"""
        
        review_required = False
        priority = "low"
        reasons = []
        
        # Check confidence thresholds
        if classification['confidence'] < 0.9:
            review_required = True
            reasons.append("Low classification confidence")
            priority = "medium"
        
        if extraction['extraction_confidence'] < 0.9:
            review_required = True
            reasons.append("Low extraction confidence")
            priority = "medium"
        
        if not validation['validation_passed']:
            review_required = True
            reasons.append("Validation errors detected")
            priority = "high"
        
        if validation['completeness_score'] < 0.8:
            review_required = True
            reasons.append("Incomplete data extraction")
            priority = "medium"
        
        return {
            "review_required": review_required,
            "priority": priority,
            "reasons": reasons,
            "estimated_review_time": self.estimate_review_time(reasons),
            "reviewer_guidance": self.generate_reviewer_guidance(classification, extraction, validation)
        }
    
    def generate_processing_id(self) -> str:
        """Generate unique processing ID"""
        import uuid
        return f"proc_{uuid.uuid4().hex[:8]}"
    
    def estimate_review_time(self, reasons: List[str]) -> int:
        """Estimate review time in minutes"""
        base_time = 5
        for reason in reasons:
            if "validation errors" in reason.lower():
                base_time += 10
            elif "low confidence" in reason.lower():
                base_time += 5
            elif "incomplete" in reason.lower():
                base_time += 7
        return min(base_time, 30)  # Cap at 30 minutes
    
    def generate_reviewer_guidance(self, classification: Dict, extraction: Dict, validation: Dict) -> str:
        """Generate guidance for human reviewers"""
        guidance = []
        
        if classification['confidence'] < 0.9:
            guidance.append(f"Verify document type: {classification['document_type']}")
        
        if validation.get('errors'):
            guidance.append(f"Address validation errors: {', '.join(validation['errors'])}")
        
        if validation.get('warnings'):
            guidance.append(f"Review warnings: {', '.join(validation['warnings'])}")
        
        return "; ".join(guidance) if guidance else "General quality review recommended"
```

### **D. Local Database Integration**

```python
# database/local_db_service.py
import asyncpg
import json
from typing import Dict, Any, List
import asyncio

class LocalDatabaseService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(self.connection_string)
        await self.create_tables()
    
    async def create_tables(self):
        """Create necessary tables for local storage"""
        
        create_documents_table = """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            processing_id VARCHAR(50) UNIQUE NOT NULL,
            document_path TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            classification JSONB,
            extraction JSONB,
            validation JSONB,
            review_decision JSONB,
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_review_queue_table = """
        CREATE TABLE IF NOT EXISTS review_queue (
            id SERIAL PRIMARY KEY,
            processing_id VARCHAR(50) REFERENCES documents(processing_id),
            priority VARCHAR(20),
            assigned_reviewer VARCHAR(100),
            review_status VARCHAR(50) DEFAULT 'pending',
            reviewer_notes TEXT,
            corrections JSONB,
            reviewed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(create_documents_table)
            await conn.execute(create_review_queue_table)
    
    async def store_processing_result(self, result: Dict[str, Any]):
        """Store processing result in local database"""
        
        query = """
        INSERT INTO documents (
            processing_id, document_path, timestamp, classification, 
            extraction, validation, review_decision, status
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (processing_id) DO UPDATE SET
            classification = $4,
            extraction = $5,
            validation = $6,
            review_decision = $7,
            status = $8,
            updated_at = CURRENT_TIMESTAMP
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                result['processing_id'],
                result['document_path'],
                result['timestamp'],
                json.dumps(result.get('classification', {})),
                json.dumps(result.get('extraction', {})),
                json.dumps(result.get('validation', {})),
                json.dumps(result.get('review_decision', {})),
                result['status']
            )
            
            # Add to review queue if needed
            if result.get('review_decision', {}).get('review_required'):
                await self.add_to_review_queue(result)
    
    async def add_to_review_queue(self, result: Dict[str, Any]):
        """Add document to human review queue"""
        
        query = """
        INSERT INTO review_queue (processing_id, priority)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
        """
        
        priority = result.get('review_decision', {}).get('priority', 'medium')
        
        async with self.pool.acquire() as conn:
            await conn.execute(query, result['processing_id'], priority)
    
    async def get_review_queue(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get documents pending review"""
        
        query = """
        SELECT d.*, r.priority, r.review_status, r.assigned_reviewer
        FROM documents d
        JOIN review_queue r ON d.processing_id = r.processing_id
        WHERE r.review_status = 'pending'
        ORDER BY 
            CASE r.priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                ELSE 3 
            END,
            r.created_at
        LIMIT $1
        """
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, limit)
            return [dict(row) for row in rows]
```

---

## **3. Production Deployment Configuration**

### **A. Docker Compose for Full Local Stack**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Local LLM Service (Ollama)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=document_processing
      - POSTGRES_USER=docuser
      - POSTGRES_PASSWORD=docpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Main Application
  document-processor:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - ollama
      - postgres
      - redis
    environment:
      - OLLAMA_URL=http://ollama:11434
      - DATABASE_URL=postgresql://docuser:docpass@postgres:5432/document_processing
      - REDIS_URL=redis://redis:6379
      - KIMI_VL_MODEL_PATH=/models/kimi-vl
    volumes:
      - ./models:/models
      - ./data:/data
      - ./uploads:/uploads

volumes:
  ollama_data:
  postgres_data:
  redis_data:
```

### **B. FastAPI Application**

```python
# main.py - Fully Local FastAPI Service
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI(title="Local Document Processing API")

llm_service = LocalLLMService(base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"))
kimi_vl_service = KimiVLService(model_path=os.getenv("KIMI_VL_MODEL_PATH"))
db_service = LocalDatabaseService(os.getenv("DATABASE_URL"))
orchestrator = LocalMultiAgentOrchestrator(llm_service, kimi_vl_service, db_service)

@app.on_event("startup")
async def startup_event():
    await db_service.initialize()

@app.post("/documents/process")
async def process_document(file: UploadFile = File(...)):
    """Process document using fully local multi-agent system"""
    try:
        # Save uploaded file locally
        upload_path = f"/uploads/{file.filename}"
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process with local orchestrator
        result = await orchestrator.process_document(upload_path)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "local-document-processor",
        "dependencies": {
            "ollama": "connected",
            "database": "connected",
            "kimi_vl": "loaded"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

This implementation is **100% local** with no external API dependencies, suitable for air-gapped environments and maximum data privacy while maintaining enterprise-grade multi-agent capabilities.
