# Setup Guide - Anantapur Smart City Grievance Analysis Tool

This guide will walk you through setting up the grievance analysis tool from scratch.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip (Python package manager)
- [ ] Git (optional, for cloning)
- [ ] Internet connection (for downloading dependencies)
- [ ] At least 4GB free disk space (for Ollama and models)

## 🔧 Step-by-Step Installation

### Step 1: Install Ollama

Ollama is required to run the IBM Granite AI model locally.

#### Windows

1. Download Ollama from [https://ollama.ai/download](https://ollama.ai/download)
2. Run the installer
3. Ollama will start automatically

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS

```bash
brew install ollama
```

### Step 2: Verify Ollama Installation

Open a terminal/command prompt and run:

```bash
ollama --version
```

You should see the version number.

### Step 3: Start Ollama Server

```bash
ollama serve
```

Keep this terminal window open. Ollama needs to run in the background.

### Step 4: Pull IBM Granite Model

Open a **new** terminal window and run:

```bash
ollama pull granite3-dense:8b
```

This will download the IBM Granite model (~4.7GB). It may take several minutes depending on your internet speed.

**Note:** If `granite3-dense:8b` is not available, you can use alternatives:
```bash
# Alternative models
ollama pull granite3-dense:2b    # Smaller, faster
ollama pull llama2               # Fallback option
```

### Step 5: Verify Model Installation

```bash
ollama list
```

You should see `granite3-dense:8b` in the list.

### Step 6: Set Up Python Environment

#### Option A: Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd "Anantapur Smart city Grievance Analysis"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

#### Option B: Using System Python

Skip virtual environment and use system Python directly.

### Step 7: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web interface)
- Pandas (data processing)
- Ollama Python client
- Other required libraries

### Step 8: Configure Environment

```bash
# Copy example configuration
cp .env.example .env
```

Edit `.env` if needed (default values should work):

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3-dense:8b
APP_TITLE=Anantapur Smart City Grievance Analysis
APP_PORT=8501
DATA_DIR=./data
LOGS_DIR=./logs
```

### Step 9: Test the Installation

Run the test suite to verify everything is working:

```bash
python core/test_ollama.py
```

Expected output:
```
============================================================
ANANTAPUR SMART CITY GRIEVANCE ANALYSIS TOOL
Ollama Granite Integration Test Suite
============================================================
Testing Ollama Connection...
✓ Ollama server is running
✓ Model: granite3-dense:8b
...
```

### Step 10: Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Quick Start Usage

### Submit Your First Grievance

1. Open the web application
2. Navigate to "Submit Grievance"
3. Enter a grievance description:
   ```
   The garbage has not been collected from Gandhi Nagar 
   near the temple for 5 days. This is causing health issues.
   ```
4. Click "Submit & Analyze"
5. View the analysis results

### Try Batch Analysis

1. Navigate to "Batch Analysis"
2. Upload the sample CSV file: `data/sample_grievances.csv`
3. Click "Analyze All Grievances"
4. View statistics and download results

## 🔍 Troubleshooting

### Issue: "Ollama server not connected"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Pull the model again
ollama pull granite3-dense:8b

# Verify it's installed
ollama list
```

### Issue: "Import errors" or "Module not found"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# If using virtual environment, ensure it's activated
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Check if port 8501 is available
# Windows:
netstat -ano | findstr :8501
# Linux/macOS:
lsof -i :8501

# Use a different port if needed
streamlit run app.py --server.port 8502
```

### Issue: Slow performance

**Solutions:**
1. Use a smaller model: `ollama pull granite3-dense:2b`
2. Update `.env` to use the smaller model
3. Reduce batch size when processing multiple grievances
4. Ensure sufficient RAM (8GB+ recommended)

### Issue: Python version incompatibility

**Solution:**
```bash
# Check Python version
python --version

# Should be 3.8 or higher
# If not, install Python 3.8+ from python.org
```

## 📊 Testing with Sample Data

### Test Single Grievance

```python
from core.engine import GrievanceAnalysisEngine

engine = GrievanceAnalysisEngine()
result = engine.analyze_grievance(
    "Garbage not collected for 3 days in Gandhi Nagar"
)
print(result)
```

### Test Batch Processing

Use the provided sample file:
```bash
# In the web interface:
1. Go to "Batch Analysis"
2. Upload: data/sample_grievances.csv
3. Click "Analyze All Grievances"
```

## 🔐 Security Considerations

### PII Protection

The system automatically redacts:
- Phone numbers
- Email addresses
- Aadhaar numbers
- Personal names

Test PII redaction:
```python
from core.engine import GrievanceAnalysisEngine

engine = GrievanceAnalysisEngine()
result = engine.redact_pii(
    "My name is Mr. Ramesh. Call me at 9876543210"
)
print(result['redacted_text'])
# Output: "My name is [NAME_REDACTED]. Call me at [PHONE_REDACTED]"
```

## 📈 Performance Optimization

### For Better Performance:

1. **Use GPU acceleration** (if available):
   - Ollama automatically uses GPU if available
   - Check with: `nvidia-smi` (NVIDIA GPUs)

2. **Adjust model parameters**:
   - Lower temperature for more consistent results
   - Reduce max_tokens for faster responses

3. **Batch processing**:
   - Process multiple grievances together
   - Use the batch analysis feature

## 🔄 Updating the System

### Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Update Ollama

```bash
# Download latest version from ollama.ai
# Or use package manager
brew upgrade ollama  # macOS
```

### Update Models

```bash
ollama pull granite3-dense:8b
```

## 📞 Getting Help

### Check System Health

In the web interface:
- Look at the sidebar for system status
- Click "Refresh System Status" to check connection

### Run Diagnostics

```bash
python core/test_ollama.py
```

### Common Commands Reference

```bash
# Start Ollama
ollama serve

# List models
ollama list

# Pull a model
ollama pull <model-name>

# Remove a model
ollama rm <model-name>

# Run the app
streamlit run app.py

# Run tests
python core/test_ollama.py

# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
```

## ✅ Verification Checklist

After setup, verify:

- [ ] Ollama is running (`ollama list` works)
- [ ] Granite model is installed
- [ ] Python dependencies are installed
- [ ] Test suite passes
- [ ] Web application launches
- [ ] Can submit and analyze a grievance
- [ ] Batch analysis works with sample data
- [ ] Dashboard shows statistics

## 🎓 Next Steps

1. **Explore the Interface**: Try all features in the web app
2. **Test with Real Data**: Use actual grievance descriptions
3. **Customize Categories**: Edit `core/config.py` for your needs
4. **Integrate with Systems**: Connect to existing municipal databases
5. **Deploy**: Set up on a server for production use

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Streamlit Documentation](https://docs.streamlit.io)
- [IBM Granite Models](https://www.ibm.com/granite)
- [Project README](README.md)

---

**Need Help?** Contact the Anantapur Municipal Corporation IT Department

**Version:** 1.0.0  
**Last Updated:** June 2026