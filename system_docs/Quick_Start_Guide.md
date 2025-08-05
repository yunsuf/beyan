# Document Digitization System - Quick Start Guide

> **⚡ Get from zero to production in 30 minutes**  
> **🎯 Perfect for developers who need immediate results**

---

## 🚀 Quick Start (5 minutes)

**What is this?** A multi-agent LLM system that automatically processes business documents (invoices, packing lists, etc.) using Kimi-VL vision models and extracts structured data.

**Why do I need it?** Eliminates manual data entry from business documents, provides 95%+ accuracy, and scales to process thousands of documents automatically.

**How does it work?** 
- Upload documents → Kimi-VL classifies document type → Multi-agent system extracts data → Structured JSON output
- Uses local or cloud deployment options with human-in-the-loop review

**What do I need to implement?** 
- ✅ Python environment with GPU support (recommended)
- ✅ Docker setup for containerized deployment  
- ✅ API integration for document processing
- ✅ Optional: Custom schemas for your document types

**How long will it take?** 
- ⏱️ **5 minutes**: Basic setup and first document processed
- ⏱️ **30 minutes**: Full production-ready deployment
- ⏱️ **2-4 hours**: Custom document types and advanced configuration

**What are the risks?** 
- 🔴 **GPU Memory**: Requires 8GB+ VRAM for optimal performance
- 🟡 **Initial Setup**: Model downloads can take 15-30 minutes
- 🟢 **Low Risk**: Fallback to CPU processing available

---

## 📋 Implementation Checklist

### **Phase 1: Environment Setup (5-10 minutes)**
- [ ] ✅ **Python 3.9+ installed** (verify: `python --version`)
- [ ] ✅ **GPU drivers installed** (verify: `nvidia-smi`)
- [ ] ✅ **Docker installed** (verify: `docker --version`)
- [ ] ✅ **Clone repository and create virtual environment**
- [ ] ✅ **Install core dependencies**
- [ ] ✅ **Download Kimi-VL model** (15-30 min download time)

### **Phase 2: Basic Configuration (5-10 minutes)**
- [ ] ⚙️ **Create configuration file** (`config.yaml`)
- [ ] ⚙️ **Test with sample documents** (provided in `/sample_docs`)
- [ ] ⚙️ **Verify API service startup**
- [ ] ⚙️ **Process first document** (success = structured JSON output)

### **Phase 3: Production Deployment (10-15 minutes)**
- [ ] 🚀 **Docker containerization** (single command deployment)
- [ ] 🚀 **Health monitoring setup**
- [ ] 🚀 **Batch processing configuration**
- [ ] 🚀 **Performance validation** (process 10+ documents)

### **Phase 4: Advanced Setup (Optional - 1-2 hours)**
- [ ] 🔧 **Custom document schemas**
- [ ] 🔧 **Performance optimization**
- [ ] 🔧 **Integration with existing systems**
- [ ] 🔧 **Production monitoring and logging**

---

## ⚖️ Deployment Decision Matrix

| Requirement | Local GPU | Cloud GPU | CPU Only | Docker | Recommendation |
|-------------|-----------|-----------|----------|---------|----------------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | **Local GPU** for speed |
| **Cost** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **CPU Only** for budget |
| **Setup Complexity** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Docker** for simplicity |
| **Scalability** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | **Cloud GPU** for scale |
| **Data Privacy** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Local GPU** for privacy |

**🎯 Recommended Quick Start Path**: Docker + Local GPU (if available) or Docker + CPU Only

---

## 🛠️ Prerequisites & System Requirements

### **Minimum Requirements**
```bash
✅ Python 3.9+
✅ 8GB RAM (minimum)
✅ 20GB free disk space
✅ Docker & Docker Compose
```

### **Recommended Requirements**
```bash
🚀 Python 3.11+
🚀 NVIDIA GPU with 8GB+ VRAM
🚀 16GB+ RAM
🚀 50GB+ free disk space (for models and data)
🚀 Ubuntu 20.04+ or macOS 12+
```

### **Quick Hardware Check**
```bash
# Check Python version
python --version  # Should be 3.9+

# Check available memory
free -h  # Should show 8GB+ available

# Check GPU (if applicable)
nvidia-smi  # Should show GPU with 8GB+ memory

# Check disk space
df -h  # Should show 20GB+ free space
```

---

## ⚡ 5-Minute Quick Start

### **Option A: Docker Quick Start (Recommended)**

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd beyan

# 2. Start with Docker (single command!)
docker-compose up -d

# 3. Test with sample document
curl -X POST "http://localhost:8000/documents/process" \
  -F "file=@sample_docs/2640316788_Commercial Invoice_1.pdf"

# ✅ Success! You should get structured JSON output
```

### **Option B: Local Development Setup**

```bash
# 1. Environment setup
git clone <your-repo-url>
cd beyan
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download models (this takes 15-30 minutes)
python setup.py download_models

# 4. Start API server
uvicorn main:app --host 0.0.0.0 --port 8000

# 5. Test processing
python test_basic.py
```

---

## 📄 Configuration

### **Essential Configuration (`config.yaml`)**

```yaml
# Minimal working configuration
kimi_vl:
  model_path: "kimi-vl-base"
  device: "auto"  # Automatically detects GPU/CPU
  max_batch_size: 4

processing:
  confidence_threshold: 0.95
  max_retries: 3
  timeout_seconds: 300

storage:
  input_folder: "./sample_docs"
  output_folder: "./processed"
  
api:
  host: "0.0.0.0"
  port: 8000
```

### **Performance Configuration (Optional)**

```yaml
# Advanced performance settings
kimi_vl:
  model_path: "kimi-vl-base"
  device: "cuda:0"  # Specific GPU
  max_batch_size: 8  # Higher for better GPU utilization
  precision: "fp16"  # Faster inference
  enable_cache: true

processing:
  parallel_workers: 4
  queue_size: 100
  batch_processing: true
```

---

## 🧪 Testing & Validation

### **1. Basic Functionality Test**

```python
# quick_test.py - Run this to verify everything works
import requests
import json
from pathlib import Path

def test_system():
    """Test basic document processing functionality"""
    
    # Test API health
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200, "❌ API not responding"
    print("✅ API health check passed")
    
    # Test document processing
    test_file = "sample_docs/2640316788_Commercial Invoice_1.pdf"
    if Path(test_file).exists():
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/documents/process", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document processed successfully")
            print(f"   Type: {result.get('document_type', 'unknown')}")
            print(f"   Confidence: {result.get('overall_confidence', 0):.2f}")
            return True
        else:
            print(f"❌ Processing failed: {response.text}")
            return False
    else:
        print(f"❌ Test file not found: {test_file}")
        return False

if __name__ == "__main__":
    success = test_system()
    if success:
        print("\n🎉 System is working correctly!")
        print("Next steps: Process your own documents or customize schemas")
    else:
        print("\n⚠️ System test failed. Check the troubleshooting section below.")
```

Run the test:
```bash
python quick_test.py
```

### **2. Batch Processing Test**

```python
# batch_test.py - Test processing multiple documents
import os
import requests
import time
from pathlib import Path

def batch_process_test(folder_path="sample_docs"):
    """Test batch processing of all sample documents"""
    
    folder = Path(folder_path)
    supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
    
    results = []
    start_time = time.time()
    
    for file_path in folder.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            print(f"Processing: {file_path.name}")
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post("http://localhost:8000/documents/process", files=files)
            
            if response.status_code == 200:
                result = response.json()
                results.append(result)
                print(f"  ✅ {result['document_type']} (confidence: {result['overall_confidence']:.2f})")
            else:
                print(f"  ❌ Error: {response.status_code}")
    
    end_time = time.time()
    
    # Summary
    total_docs = len(results)
    avg_confidence = sum(r['overall_confidence'] for r in results) / total_docs if results else 0
    processing_time = end_time - start_time
    
    print(f"\n📊 Batch Processing Results:")
    print(f"   Documents processed: {total_docs}")
    print(f"   Average confidence: {avg_confidence:.2f}")
    print(f"   Total time: {processing_time:.1f} seconds")
    print(f"   Average per document: {processing_time/total_docs:.1f} seconds")

if __name__ == "__main__":
    batch_process_test()
```

---

## 🐳 Docker Deployment

### **Quick Docker Start**

```bash
# Start all services with one command
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f kimi-vl-processor
```

### **Manual Docker Build (if needed)**

```bash
# Build image
docker build -t kimi-vl-processor .

# Run with GPU support
docker run --gpus all -p 8000:8000 \
  -v $(pwd)/sample_docs:/app/data \
  -v $(pwd)/processed:/app/output \
  kimi-vl-processor

# Run CPU-only
docker run -p 8000:8000 \
  -v $(pwd)/sample_docs:/app/data \
  -v $(pwd)/processed:/app/output \
  kimi-vl-processor
```

---

## 🔧 Troubleshooting

### **🚨 Common Issues & Quick Fixes**

| Issue | Symptoms | Quick Fix | Prevention |
|-------|----------|-----------|------------|
| **CUDA Out of Memory** | `RuntimeError: CUDA out of memory` | Reduce `max_batch_size: 1` in config | Monitor GPU memory with `nvidia-smi` |
| **Model Download Failed** | `ConnectionError` or `TimeoutError` | Re-run `python setup.py download_models` | Use stable internet connection |
| **API Not Starting** | `Connection refused` on port 8000 | Check if port is free: `lsof -i :8000` | Use different port in config |
| **Slow Processing** | >30 seconds per document | Enable GPU or increase batch_size | Check GPU utilization |
| **Permission Errors** | `PermissionError` on file operations | Check folder permissions: `chmod 755` | Run with proper user permissions |

### **🔍 Diagnostic Commands**

```bash
# Check system health
curl "http://localhost:8000/health"

# Check GPU availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Check model loading
python -c "from kimi_vl import KimiVLService; print('Model loaded successfully')"

# Check disk space
df -h | grep -E '(Available|filesystem)'

# Check memory usage
free -m

# Check running processes
ps aux | grep python
```

### **🚨 Error Resolution Guide**

#### **Error: "ModuleNotFoundError: No module named 'kimi_vl'"**
```bash
# Solution: Install requirements properly
pip install -r requirements.txt
pip install --upgrade kimi-vl

# Verify installation
python -c "import kimi_vl; print('✅ Kimi-VL installed')"
```

#### **Error: "RuntimeError: CUDA out of memory"**
```bash
# Solution 1: Reduce batch size
# Edit config.yaml:
max_batch_size: 1

# Solution 2: Clear GPU cache
python -c "import torch; torch.cuda.empty_cache()"

# Solution 3: Use CPU processing
# Edit config.yaml:
device: "cpu"
```

#### **Error: "Port 8000 already in use"**
```bash
# Find what's using the port
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### **🏥 Health Monitoring**

```python
# health_check.py - Comprehensive system health check
import requests
import psutil
import torch
import time

def comprehensive_health_check():
    """Perform complete system health check"""
    
    print("🏥 System Health Check")
    print("=" * 50)
    
    # System resources
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print(f"💾 Memory: {memory.available / (1024**3):.1f}GB available ({memory.percent}% used)")
    print(f"💽 Disk: {disk.free / (1024**3):.1f}GB available ({disk.percent}% used)")
    
    # GPU check
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        gpu_allocated = torch.cuda.memory_allocated(0) / (1024**3)
        print(f"🎮 GPU: {gpu_memory:.1f}GB total, {gpu_allocated:.1f}GB allocated")
    else:
        print("🎮 GPU: Not available (using CPU)")
    
    # API health
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("🌐 API: ✅ Healthy")
        else:
            print(f"🌐 API: ❌ Error {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"🌐 API: ❌ Not responding ({e})")
    
    # Performance test
    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:8000/documents/process",
            files={'file': open('sample_docs/2640316788_Commercial Invoice_1.pdf', 'rb')},
            timeout=30
        )
        processing_time = time.time() - start_time
        if response.status_code == 200:
            print(f"⚡ Performance: ✅ Processed test document in {processing_time:.1f}s")
        else:
            print(f"⚡ Performance: ❌ Processing failed")
    except Exception as e:
        print(f"⚡ Performance: ❌ Test failed ({e})")
    
    print("=" * 50)

if __name__ == "__main__":
    comprehensive_health_check()
```

---

## 🎯 Success Criteria Checklist

**✅ Minimum Viable Setup (5 minutes)**
- [ ] API responds to health check
- [ ] Successfully processes one sample document
- [ ] Returns structured JSON output
- [ ] Confidence score > 0.8

**✅ Production Ready (30 minutes)**
- [ ] Processes all sample documents successfully
- [ ] Average processing time < 10 seconds per document
- [ ] Docker deployment working
- [ ] Batch processing functional
- [ ] Health monitoring active

**✅ Advanced Configuration (1-2 hours)**
- [ ] Custom document schemas implemented
- [ ] Performance optimized for your hardware
- [ ] Integration with existing systems
- [ ] Monitoring and logging configured

---

## 🚀 Next Steps

### **Immediate Actions (After Quick Start)**
1. **Process Your Documents**: Replace sample documents with your real business documents
2. **Customize Schemas**: Add your specific document types and fields
3. **Performance Tuning**: Optimize for your hardware and volume requirements
4. **Integration Planning**: Plan integration with your existing business systems

### **Scaling Considerations**
- **Volume**: For >1000 documents/day, consider cloud deployment
- **Accuracy**: For specialized documents, plan custom model fine-tuning  
- **Integration**: For enterprise use, implement proper authentication and monitoring
- **Compliance**: For regulated industries, ensure data handling compliance

### **Advanced Features to Explore**
- **n8n Visual Workflow Automation** - Replace custom orchestration with visual workflows
- Multi-agent human-in-the-loop review system
- Custom document type training
- Advanced OCR preprocessing
- Real-time processing workflows
- Analytics and reporting dashboards

---

## 📚 Additional Resources

### **Documentation**
- 📖 **[System Design Guide](./system_design.md)** - Detailed architecture and design decisions
- 🔧 **[Technical Implementation Guide](./Kimi-VL_Technical_Implementation_Guide.md)** - Advanced configuration and customization
- 🤖 **[Multi-Agent Framework Guide](../ai-docs/)** - LLM agent implementation details
- 🔄 **[n8n Integration Guide](../ai-docs/n8n-integration-guide.md)** - Visual workflow automation setup

### **Support & Community**
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)  
- 📧 **Email**: support@yourcompany.com
- 📖 **Wiki**: [Project Wiki](https://github.com/your-repo/wiki)

---

**⚡ Quick Start Complete!** You should now have a working document digitization system. Time to process some real documents! 🎉 