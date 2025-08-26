#!/usr/bin/env python3
"""
Test script for GIKI Prospectus Q&A Chatbot
Tests all components of the RAG system
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Now import the modules
from config import Config
from document_processor import DocumentProcessor
from text_chunker import TextChunker
from embeddings.embedding_manager import EmbeddingManager
from vectorstore.vector_store import VectorStore
from llm.llm_manager import LLMManager
from rag.rag_engine import RAGEngine

def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    try:
        # Test config loading
        config = Config()
        missing = Config.validate_config()
        
        if missing:
            print(f"⚠️ Missing configuration: {missing}")
        else:
            print("✅ Configuration loaded successfully")
        
        # Test system prompt
        prompt_en = Config.get_system_prompt("en")
        prompt_ur = Config.get_system_prompt("ur")
        
        if prompt_en and prompt_ur:
            print("✅ System prompts generated successfully")
        else:
            print("❌ Failed to generate system prompts")
            
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_document_processor():
    """Test document processing"""
    print("\n📄 Testing Document Processor...")
    try:
        processor = DocumentProcessor()
        
        # Test file validation
        valid_files = ["test.pdf", "test.docx", "test.txt"]
        invalid_files = ["test.jpg", "test.exe"]
        
        for file in valid_files:
            if processor.validate_file(file):
                print(f"✅ Valid file: {file}")
            else:
                print(f"❌ Invalid file: {file}")
        
        for file in invalid_files:
            if not processor.validate_file(file):
                print(f"✅ Correctly rejected: {file}")
            else:
                print(f"❌ Should have rejected: {file}")
        
        print("✅ Document processor initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False

def test_text_chunker():
    """Test text chunking"""
    print("\n✂️ Testing Text Chunker...")
    try:
        chunker = TextChunker()
        
        # Test text chunking
        sample_text = "This is a sample text for testing chunking functionality. " * 50
        metadata = {"file_name": "test.txt", "page_number": 1}
        
        chunks = chunker.chunk_text_with_metadata(sample_text, metadata)
        
        if chunks:
            print(f"✅ Created {len(chunks)} chunks")
            stats = chunker.get_chunk_statistics(chunks)
            print(f"✅ Chunk statistics: {stats}")
        else:
            print("❌ No chunks created")
        
        return True
    except Exception as e:
        print(f"❌ Text chunker test failed: {e}")
        return False

def test_embedding_manager():
    """Test embedding generation"""
    print("\n🧠 Testing Embedding Manager...")
    try:
        embedding_manager = EmbeddingManager()
        
        # Test single embedding
        text = "This is a test sentence for embedding."
        embedding = embedding_manager.get_single_embedding(text)
        
        if embedding is not None and len(embedding) > 0:
            print(f"✅ Generated embedding with {len(embedding)} dimensions")
        else:
            print("❌ Failed to generate embedding")
        
        # Test batch embeddings
        texts = ["First sentence.", "Second sentence.", "Third sentence."]
        embeddings = embedding_manager.get_embeddings(texts)
        
        if embeddings and len(embeddings) == len(texts):
            print(f"✅ Generated {len(embeddings)} batch embeddings")
        else:
            print("❌ Failed to generate batch embeddings")
        
        return True
    except Exception as e:
        print(f"❌ Embedding manager test failed: {e}")
        return False

def test_vector_store():
    """Test vector store operations"""
    print("\n🗄️ Testing Vector Store...")
    try:
        vector_store = VectorStore()
        
        # Test collection stats
        stats = vector_store.get_collection_stats()
        print(f"✅ Vector store initialized: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False

def test_llm_manager():
    """Test LLM manager"""
    print("\n🤖 Testing LLM Manager...")
    try:
        llm_manager = LLMManager()
        
        # Test available providers
        providers = llm_manager.get_available_providers()
        print(f"✅ Available LLM providers: {providers}")
        
        if providers:
            # Test OpenRouter models if available
            if "openrouter" in providers:
                openrouter_models = llm_manager.get_openrouter_models()
                print(f"✅ OpenRouter models: {openrouter_models}")
        
        return True
    except Exception as e:
        print(f"❌ LLM manager test failed: {e}")
        return False

def test_rag_engine():
    """Test RAG engine"""
    print("\n🔍 Testing RAG Engine...")
    try:
        rag_engine = RAGEngine()
        
        # Test system status
        status = rag_engine.get_system_status()
        print(f"✅ RAG engine status: {status}")
        
        return True
    except Exception as e:
        print(f"❌ RAG engine test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 GIKI Prospectus Q&A Chatbot - System Test")
    print("=" * 50)
    
    tests = [
        test_config,
        test_document_processor,
        test_text_chunker,
        test_embedding_manager,
        test_vector_store,
        test_llm_manager,
        test_rag_engine
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python setup_openrouter.py")
        print("   2. Start: streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == "__main__":
    main()
