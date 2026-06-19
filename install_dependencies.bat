@echo off
echo ========================================
echo Installing Dependencies
echo Anantapur Smart City Grievance Analysis
echo ========================================
echo.

echo Installing Python packages...
python -m pip install --upgrade pip
python -m pip install streamlit>=1.28.0
python -m pip install pandas>=2.0.0
python -m pip install numpy>=1.24.0
python -m pip install ollama>=0.1.0
python -m pip install requests>=2.31.0
python -m pip install python-dotenv>=1.0.0

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Install Ollama from https://ollama.ai
echo 2. Run: ollama serve
echo 3. Run: ollama pull granite3-dense:8b
echo 4. Run: streamlit run app.py
echo.
pause

@REM Made with Bob
