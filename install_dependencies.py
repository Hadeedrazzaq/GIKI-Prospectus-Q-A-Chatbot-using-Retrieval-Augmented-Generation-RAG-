#!/usr/bin/env python3
"""
Dependency installation script for GIKI Prospectus Q&A Chatbot
Handles installation step by step to avoid compatibility issues
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install all dependencies step by step"""
    print("🚀 Installing Dependencies for GIKI Prospectus Q&A Chatbot")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️ Warning: Failed to upgrade pip, continuing anyway...")
    
    # Install core dependencies one by one
    dependencies = [
        ("python-dotenv", "Environment variables"),
        ("requests", "HTTP requests"),
        ("numpy", "Numerical computing"),
        ("pandas", "Data manipulation"),
        ("streamlit", "Web interface"),
        ("PyMuPDF", "PDF processing"),
        ("python-docx", "Word document processing"),
        ("sentence-transformers", "Text embeddings"),
        ("chromadb", "Vector database"),
        ("faiss-cpu", "Vector similarity search"),
        ("openai", "OpenAI API"),
        ("anthropic", "Anthropic API"),
        ("tiktoken", "Token counting"),
        ("nltk", "Natural language processing"),
        ("scikit-learn", "Machine learning utilities"),
    ]
    
    for package, description in dependencies:
        if not run_command(f"pip install {package}", f"Installing {description} ({package})"):
            print(f"⚠️ Warning: Failed to install {package}, trying to continue...")
    
    # Install LangChain packages with specific versions
    langchain_packages = [
        ("langchain>=0.1.0", "LangChain core"),
        ("langchain-community>=0.0.10", "LangChain community"),
        ("langchain-openai>=0.0.5", "LangChain OpenAI integration"),
        ("langchain-chroma>=0.1.2", "LangChain ChromaDB integration"),
    ]
    
    for package, description in langchain_packages:
        if not run_command(f"pip install {package}", f"Installing {description}"):
            print(f"⚠️ Warning: Failed to install {package}")
    
    # Optional: Install PyTorch for better performance
    print("\n🔄 Installing PyTorch (optional, for better performance)...")
    try:
        subprocess.run("pip install torch", shell=True, check=True)
        print("✅ PyTorch installed successfully!")
    except:
        print("⚠️ PyTorch installation failed, continuing without it...")
    
    print("\n" + "=" * 60)
    print("🎉 Dependency Installation Complete!")
    print("\n📋 Next Steps:")
    print("   1. Run setup: python setup_openrouter.py")
    print("   2. Test system: python test_system.py")
    print("   3. Start app: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    install_dependencies()
