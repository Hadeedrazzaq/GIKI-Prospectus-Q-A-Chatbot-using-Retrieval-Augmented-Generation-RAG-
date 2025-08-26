#!/usr/bin/env python3
"""
Launcher script for GIKI Prospectus Q&A Chatbot
Handles setup, testing, and launching automatically
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "streamlit", "langchain", "sentence_transformers", 
        "chromadb", "openai", "anthropic", "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {missing_packages}")
        print("Installing missing dependencies...")
        
        # Install missing packages
        for package in missing_packages:
            if not run_command(f"pip install {package}", f"Installing {package}", check=False):
                print(f"⚠️ Failed to install {package}")
        
        return False
    
    return True

def setup_environment():
    """Set up the environment file"""
    print("\n🔧 Setting up environment...")
    
    env_file = Path(".env")
    example_file = Path("env_example.txt")
    
    if not example_file.exists():
        print("❌ env_example.txt not found!")
        return False
    
    if not env_file.exists():
        print("Creating .env file...")
        if not run_command("python setup_openrouter.py", "Setting up OpenRouter configuration"):
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def test_system():
    """Test the system components"""
    print("\n🧪 Testing system components...")
    
    if not run_command("python test_system.py", "Running system tests", check=False):
        print("⚠️ Some tests failed, but continuing...")
        return True  # Continue anyway
    
    return True

def launch_app():
    """Launch the Streamlit application"""
    print("\n🚀 Launching GIKI Prospectus Q&A Chatbot...")
    print("=" * 60)
    print("🎓 GIKI Prospectus Q&A Chatbot")
    print("📚 Powered by RAG (Retrieval-Augmented Generation)")
    print("🤖 Using Google Gemini 2.0 Flash Experimental (FREE)")
    print("=" * 60)
    
    try:
        # Launch Streamlit
        subprocess.run("streamlit run app.py", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main launcher function"""
    print("🎓 GIKI Prospectus Q&A Chatbot Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️ Some dependencies may be missing, but continuing...")
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        return
    
    # Test system
    if not test_system():
        print("⚠️ System tests failed, but continuing...")
    
    # Launch app
    launch_app()

if __name__ == "__main__":
    main()
