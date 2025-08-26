@echo off
echo 🎓 GIKI Prospectus Q&A Chatbot
echo ================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️ .env file not found
    echo 📝 Creating .env file from template...
    copy env_example.txt .env
    echo.
    echo ⚠️ Please edit .env file with your API keys before running
    echo.
    pause
)

REM Run the application
echo 🚀 Starting Streamlit application...
echo.
echo The application will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run app.py

pause
