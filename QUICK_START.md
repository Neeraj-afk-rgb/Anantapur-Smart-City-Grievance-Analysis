# 🚀 Quick Start Guide - Run the App in 5 Minutes

## Step 1: Install Dependencies (Choose One Method)

### Method A: Using the Installation Script (Easiest)

**Windows:**
```bash
# Double-click the file or run in terminal:
install_dependencies.bat
```

**Linux/Mac:**
```bash
# Make it executable and run:
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Method B: Manual Installation

```bash
# Install all dependencies at once
pip install streamlit pandas numpy ollama requests python-dotenv
```

### Method C: Using requirements.txt

```bash
pip install -r requirements.txt
```

## Step 2: Install and Setup Ollama

### Install Ollama

**Windows:**
1. Download from: https://ollama.ai/download
2. Run the installer
3. Ollama will start automatically

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Mac:**
```bash
brew install ollama
```

### Start Ollama Server

Open a terminal and run:
```bash
ollama serve
```

**Keep this terminal window open!** Ollama needs to run in the background.

### Download the AI Model

Open a **NEW** terminal window and run:
```bash
ollama pull granite3-dense:8b
```

This downloads the IBM Granite model (~4.7GB). Wait for it to complete.

**Verify installation:**
```bash
ollama list
```

You should see `granite3-dense:8b` in the list.

## Step 3: Run the Application

In your project directory, run:

```bash
streamlit run app.py
```

The app will automatically open in your browser at: **http://localhost:8501**

## 🎯 Using the Application

### Submit Your First Grievance

1. The app opens to the **"Submit Grievance"** page
2. Enter a grievance description, for example:
   ```
   The garbage has not been collected from Gandhi Nagar 
   near the temple for 5 days. This is causing health issues.
   ```
3. Click **"Submit & Analyze"**
4. View the results:
   - Ticket ID
   - Category
   - Urgency Level
   - Assigned Department
   - Location
   - PII Detection

### Try Batch Analysis

1. Click **"Batch Analysis"** in the sidebar
2. Upload the sample file: `data/sample_grievances.csv`
3. Click **"Analyze All Grievances"**
4. View statistics and download results

### View Dashboard

1. Click **"Dashboard"** in the sidebar
2. See analytics and visualizations
3. Track trends and department workload

## 🔧 Troubleshooting

### "Ollama server not connected"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve
```

### "Model not found"

**Solution:**
```bash
ollama pull granite3-dense:8b
```

### "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install streamlit pandas numpy ollama requests python-dotenv
```

### Port already in use

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

## 📝 Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama
ollama serve

# Pull AI model
ollama pull granite3-dense:8b

# Check installed models
ollama list

# Run the app
streamlit run app.py

# Run tests
python core/test_ollama.py
```

## ✅ Verification Checklist

Before running the app, ensure:

- [ ] Python 3.8+ is installed (`python --version`)
- [ ] Dependencies are installed (`pip list | grep streamlit`)
- [ ] Ollama is running (`curl http://localhost:11434/api/tags`)
- [ ] Granite model is downloaded (`ollama list`)

## 🎓 Next Steps

1. **Test with sample data**: Use `data/sample_grievances.csv`
2. **Explore all features**: Try all pages in the sidebar
3. **Customize**: Edit `core/config.py` for your needs
4. **Read full docs**: Check `README.md` and `SETUP_GUIDE.md`

## 💡 Tips

- **First run takes longer**: The AI model needs to load
- **Keep Ollama running**: Don't close the `ollama serve` terminal
- **Use sample data**: Test with provided CSV file first
- **Check system status**: Look at sidebar for connection status

## 🆘 Need Help?

1. **Check system health**: Click "Refresh System Status" in sidebar
2. **Run diagnostics**: `python core/test_ollama.py`
3. **Read detailed guide**: `SETUP_GUIDE.md`
4. **Check logs**: Look for error messages in terminal

---

**That's it! You're ready to analyze grievances! 🎉**

For detailed documentation, see:
- `README.md` - Full project documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `Smart_City_Grievance_Analysis_Tool_Proposal_v2.pdf` - Project proposal