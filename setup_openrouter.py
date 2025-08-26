#!/usr/bin/env python3
"""
Setup script for OpenRouter API configuration
Automatically configures the .env file with your OpenRouter API key and Gemini model
"""

import os
import shutil
from pathlib import Path

def setup_openrouter():
    """Setup OpenRouter configuration"""
    print("🚀 Setting up OpenRouter API for GIKI Chatbot...")
    print("=" * 50)
    
    # Your OpenRouter API key
    OPENROUTER_API_KEY = "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"
    
    # Check if .env file exists
    env_file = Path(".env")
    example_file = Path("env_example.txt")
    
    if not example_file.exists():
        print("❌ Error: env_example.txt not found!")
        return False
    
    # Create .env file from example
    try:
        shutil.copy(example_file, env_file)
        print("✅ Created .env file from template")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    # Read the .env file
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Update the OpenRouter configuration
    lines = content.split('\n')
    updated_lines = []
    
    for line in lines:
        if line.startswith('OPENROUTER_API_KEY='):
            updated_lines.append(f'OPENROUTER_API_KEY={OPENROUTER_API_KEY}')
        elif line.startswith('OPENROUTER_MODEL='):
            updated_lines.append('OPENROUTER_MODEL=google/gemini-2.0-flash-exp')
        elif line.startswith('LLM_MODEL='):
            updated_lines.append('LLM_MODEL=google/gemini-2.0-flash-exp')
        else:
            updated_lines.append(line)
    
    # Write the updated content
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        print("✅ Updated .env file with your OpenRouter API key")
        print("✅ Set default model to Google Gemini 2.0 Flash Experimental")
    except Exception as e:
        print(f"❌ Error writing .env file: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 OpenRouter Setup Complete!")
    print("\n📋 Configuration Summary:")
    print(f"   • API Key: {OPENROUTER_API_KEY[:20]}...")
    print("   • Default Model: google/gemini-2.0-flash-exp")
    print("   • Status: Ready to use!")
    
    print("\n🚀 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Test the system: python test_system.py")
    print("   3. Start the app: streamlit run app.py")
    
    print("\n🎯 Available Free Models:")
    print("   • google/gemini-2.0-flash-exp (Default)")
    print("   • openai/gpt-3.5-turbo")
    print("   • meta-llama/llama-2-7b-chat")
    print("   • meta-llama/llama-2-13b-chat")
    print("   • anthropic/claude-instant-v1")
    print("   • google/palm-2-chat-bison")
    
    return True

if __name__ == "__main__":
    setup_openrouter()
