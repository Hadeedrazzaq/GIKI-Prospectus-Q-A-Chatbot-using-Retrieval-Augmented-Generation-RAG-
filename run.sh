#!/bin/bash

echo "🎓 GIKI Prospectus Q&A Chatbot"
echo "================================"
echo ""

echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found"
    echo "📝 Creating .env file from template..."
    cp env_example.txt .env
    echo ""
    echo "⚠️ Please edit .env file with your API keys before running"
    echo ""
    read -p "Press Enter to continue..."
fi

# Run the application
echo "🚀 Starting Streamlit application..."
echo ""
echo "The application will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
