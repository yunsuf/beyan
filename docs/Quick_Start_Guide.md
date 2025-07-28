# Document Digitization System - Quick Start Guide

> **Get up and running in 30 minutes**

---

## Prerequisites

- Python 3.9+
- NVIDIA GPU with 8GB+ VRAM (recommended)
- Docker and Docker Compose
- 16GB+ RAM
- 50GB+ free disk space

---

## Step 1: Environment Setup

### 1.1 Clone and Setup Project

```bash
# Clone the project
git clone <your-repo-url>
cd beyan

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Install Kimi-VL

```bash
# Install Kimi-VL (replace with actual installation command)
pip install kimi-vl

# Verify installation
python -c "import kimi_vl; print('Kimi-VL installed successfully')"
```

---

## Step 2: Basic Configuration

### 2.1 Create Configuration File

Create `config.yaml`:

```yaml
kimi_vl:
  model_path: "kimi-vl-base"
  max_batch_size: 4
  device: "cuda"  # or "cpu" if no GPU

processing:
  confidence_threshold: 0.95
  max_retries: 3
  timeout_seconds: 300

storage:
  input_folder: "./muaz"
  output_folder: "./processed"
  cache_folder: "./cache"

api:
  host: "0.0.0.0"
  port: 8000
```

### 2.2 Test with Sample Documents

```python
# test_basic.py
from kimi_vl import KimiVLService
from document_classifier import DocumentClassifier
from data_extractor import DataExtractor

def test_basic_processing():
    # Initialize services
    kimi_vl = KimiVLService()
    classifier = DocumentClassifier(kimi_vl)
    extractor = DataExtractor(kimi_vl)
    
    # Test with sample document
    sample_doc = "muaz/2640316788_Commercial Invoice_1.pdf"
    
    # Classify document
    classification = classifier.classify_document(sample_doc)
    print(f"Document Type: {classification['type']}")
    print(f"Confidence: {classification['confidence']}")
    
    # Extract data
    extracted_data = extractor.extract_data(sample_doc, classification['type'])
    print(f"Extracted Data: {extracted_data}")

if __name__ == "__main__":
    test_basic_processing()
```

Run the test:
```bash
python test_basic.py
```

---

## Step 3: Start Processing Pipeline

### 3.1 Start the API Service

```bash
# Start the document processing API
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3.2 Process Documents via API

```bash
# Process a single document
curl -X POST "http://localhost:8000/documents/process" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@muaz/2640316788_Commercial Invoice_1.pdf"

# Check processing status
curl "http://localhost:8000/documents/{document_id}"
```

### 3.3 Process Documents Programmatically

```python
# process_documents.py
import requests
import os
from pathlib import Path

def process_folder(folder_path: str, api_url: str = "http://localhost:8000"):
    """Process all documents in a folder"""
    
    folder = Path(folder_path)
    supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
    
    for file_path in folder.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            print(f"Processing: {file_path.name}")
            
            # Upload and process document
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{api_url}/documents/process", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Success: {result['document_type']} (confidence: {result['overall_confidence']:.2f})")
            else:
                print(f"✗ Error: {response.text}")

if __name__ == "__main__":
    process_folder("./muaz")
```

Run the batch processor:
```bash
python process_documents.py
```

---

## Step 4: Docker Deployment

### 4.1 Build and Run with Docker

```bash
# Build the Docker image
docker build -t kimi-vl-processor .

# Run with GPU support
docker run --gpus all -p 8000:8000 \
  -v $(pwd)/muaz:/app/data \
  -v $(pwd)/models:/app/models \
  kimi-vl-processor
```

### 4.2 Docker Compose Setup

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f kimi-vl-processor
```

---

## Step 5: Monitor and Validate

### 5.1 Check System Health

```bash
# Health check
curl "http://localhost:8000/health"

# Expected response:
# {"status": "healthy", "service": "kimi-vl-document-processor"}
```

### 5.2 Monitor Processing Results

```python
# monitor_results.py
import json
from pathlib import Path

def analyze_results(output_folder: str = "./processed"):
    """Analyze processing results"""
    
    output_path = Path(output_folder)
    results = []
    
    for result_file in output_path.glob("*.json"):
        with open(result_file, 'r') as f:
            result = json.load(f)
            results.append(result)
    
    # Calculate statistics
    total_docs = len(results)
    successful = len([r for r in results if r.get('status') == 'success'])
    avg_confidence = sum(r.get('overall_confidence', 0) for r in results) / total_docs
    
    print(f"Total Documents: {total_docs}")
    print(f"Successful: {successful}")
    print(f"Success Rate: {successful/total_docs*100:.1f}%")
    print(f"Average Confidence: {avg_confidence:.2f}")

if __name__ == "__main__":
    analyze_results()
```

---

## Step 6: Advanced Configuration

### 6.1 Custom Document Types

Add new document types to `schemas.py`:

```python
# schemas.py
CUSTOM_SCHEMAS = {
    "custom_invoice": {
        "invoice_number": "string",
        "custom_field": "string",
        "line_items": [{"description": "string", "amount": "number"}]
    }
}

# Update the DataExtractor
extractor.schemas.update(CUSTOM_SCHEMAS)
```

### 6.2 Performance Tuning

```python
# performance_config.py
PERFORMANCE_CONFIG = {
    "batch_size": 8,  # Increase for better GPU utilization
    "max_workers": 4,  # Parallel processing
    "cache_enabled": True,
    "gpu_memory_fraction": 0.8
}
```

---

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   ```bash
   # Reduce batch size in config
   max_batch_size: 2
   ```

2. **Model Loading Slow**
   ```bash
   # Pre-download model
   python -c "from kimi_vl import KimiVLModel; KimiVLModel.from_pretrained('kimi-vl-base')"
   ```

3. **API Connection Issues**
   ```bash
   # Check if service is running
   curl http://localhost:8000/health
   
   # Check logs
   docker-compose logs kimi-vl-processor
   ```

### Performance Optimization

1. **Enable GPU Acceleration**
   ```bash
   # Verify GPU is available
   nvidia-smi
   
   # Set environment variable
   export CUDA_VISIBLE_DEVICES=0
   ```

2. **Optimize Memory Usage**
   ```python
   # In your processing code
   torch.cuda.empty_cache()  # Clear GPU memory
   ```

---

## Next Steps

1. **Scale Up**: Deploy to production with proper monitoring
2. **Custom Training**: Fine-tune Kimi-VL for your specific documents
3. **Integration**: Connect with your existing business systems
4. **Automation**: Set up automated document processing workflows

---

## Support

- **Documentation**: See `docs/` folder for detailed guides
- **Issues**: Check GitHub issues or create new ones
- **Community**: Join our discussion forum

---

*This quick start guide gets you up and running with the document digitization system. For detailed implementation, refer to the comprehensive system design and technical implementation guides.* 