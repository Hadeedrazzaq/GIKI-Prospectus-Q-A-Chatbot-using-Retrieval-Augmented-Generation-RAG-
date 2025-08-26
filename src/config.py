"""
Configuration module for GIKI Prospectus Q&A Chatbot
"""
import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the GIKI Chatbot application"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # OpenRouter Configuration
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Application Settings
    MAX_DOCUMENTS = int(os.getenv("MAX_DOCUMENTS", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "3"))
    
    # Language Settings
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "en,ur").split(",")
    
    # File Upload Settings
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.doc'}
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    # Prompt Templates
    SYSTEM_PROMPT_EN = """You are a helpful assistant for GIKI (Ghulam Ishaq Khan Institute) 
    prospectus and academic information. Answer questions based on the provided context from 
    GIKI documents. If the information is not in the context, say so clearly. Always provide 
    accurate and helpful information about GIKI programs, policies, and procedures."""
    
    SYSTEM_PROMPT_UR = """آپ GIKI (غلام اسحاق خان انسٹیٹیٹ) کے پروسپیکٹس اور تعلیمی معلومات کے لیے 
    ایک مددگار اسسٹنٹ ہیں۔ GIKI دستاویزات سے فراہم کردہ سیاق و سباق کی بنیاد پر سوالات کا جواب دیں۔ 
    اگر معلومات سیاق و سباق میں نہیں ہے تو واضح طور پر کہیں۔ GIKI پروگراموں، پالیسیوں اور طریقہ کار 
    کے بارے میں ہمیشہ درست اور مددگار معلومات فراہم کریں۔"""
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of missing required settings"""
        missing = []
        
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY and not cls.OPENROUTER_API_KEY:
            missing.append("Either OPENAI_API_KEY, ANTHROPIC_API_KEY, or OPENROUTER_API_KEY is required")
        
        return missing
    
    @classmethod
    def get_system_prompt(cls, language: str = "en") -> str:
        """Get system prompt based on language"""
        if language == "ur":
            return cls.SYSTEM_PROMPT_UR
        return cls.SYSTEM_PROMPT_EN
