"""
LLM manager for GIKI Prospectus Q&A Chatbot
Handles different language models for generating responses
"""
from typing import List, Dict, Any, Optional
import openai
import anthropic
import requests
import logging
from abc import ABC, abstractmethod

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLLM(ABC):
    """Abstract base class for LLM implementations"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM is available"""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.LLM_MODEL
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return bool(self.api_key)
    
    def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """Generate response using OpenAI"""
        try:
            if not self.is_available():
                raise ValueError("OpenAI API key not configured")
            
            # Build system prompt
            system_prompt = Config.get_system_prompt(language)
            
            # Build user message
            if context:
                user_message = f"Context from GIKI documents:\n{context}\n\nQuestion: {prompt}"
            else:
                user_message = prompt
            
            # Make API call
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            raise

class AnthropicLLM(BaseLLM):
    """Anthropic Claude LLM implementation"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        self.model = model
        self.client = None
        
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if Anthropic is available"""
        return bool(self.api_key and self.client)
    
    def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """Generate response using Anthropic Claude"""
        try:
            if not self.is_available():
                raise ValueError("Anthropic API key not configured")
            
            # Build system prompt
            system_prompt = Config.get_system_prompt(language)
            
            # Build user message
            if context:
                user_message = f"Context from GIKI documents:\n{context}\n\nQuestion: {prompt}"
            else:
                user_message = prompt
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generating Anthropic response: {str(e)}")
            raise

class OpenRouterLLM(BaseLLM):
    """OpenRouter LLM implementation for free models"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.model = model or "openai/gpt-3.5-turbo"  # Default to working model
        self.base_url = base_url or Config.OPENROUTER_BASE_URL
        
        # Free models available on OpenRouter
        self.free_models = [
            "openai/gpt-3.5-turbo",  # Most reliable free model
            "openai/gpt-3.5-turbo-16k",
            "meta-llama/llama-2-7b-chat",
            "meta-llama/llama-2-13b-chat",
            "google/palm-2-chat-bison",
            "anthropic/claude-instant-v1",
            "microsoft/dialo-gpt-medium",
            "microsoft/dialo-gpt-large"
        ]
    
    def is_available(self) -> bool:
        """Check if OpenRouter is available"""
        return bool(self.api_key)
    
    def get_available_models(self) -> List[str]:
        """Get list of available free models"""
        return self.free_models
    
    def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """Generate response using OpenRouter"""
        try:
            if not self.is_available():
                raise ValueError("OpenRouter API key not configured")
            
            # Build system prompt
            system_prompt = Config.get_system_prompt(language)
            
            # Build user message
            if context:
                user_message = f"Context from GIKI documents:\n{context}\n\nQuestion: {prompt}"
            else:
                user_message = prompt
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://giki-chatbot.com",  # Your app URL
                "X-Title": "GIKI Prospectus Q&A Chatbot"
            }
            
            # Prepare payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Make API call
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                error_msg = f"OpenRouter API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
        except Exception as e:
            logger.error(f"Error generating OpenRouter response: {str(e)}")
            raise

class LLMManager:
    """Manages different LLM providers"""
    
    def __init__(self, provider: str = "openrouter"):
        self.provider = provider
        self.openai_llm = OpenAILLM()
        self.anthropic_llm = AnthropicLLM()
        self.openrouter_llm = OpenRouterLLM()
        self.current_llm = self._select_llm()
    
    def _select_llm(self) -> BaseLLM:
        """Select the best available LLM"""
        # Prioritize OpenRouter (free models) first
        if self.provider == "openrouter" and self.openrouter_llm.is_available():
            logger.info("Using OpenRouter LLM")
            return self.openrouter_llm
        elif self.provider == "openai" and self.openai_llm.is_available():
            logger.info("Using OpenAI LLM")
            return self.openai_llm
        elif self.provider == "anthropic" and self.anthropic_llm.is_available():
            logger.info("Using Anthropic LLM")
            return self.anthropic_llm
        # Auto-selection with OpenRouter priority
        elif self.openrouter_llm.is_available():
            logger.info("Auto-selected OpenRouter LLM (recommended for free models)")
            return self.openrouter_llm
        elif self.openai_llm.is_available():
            logger.info("Auto-selected OpenAI LLM")
            return self.openai_llm
        elif self.anthropic_llm.is_available():
            logger.info("Auto-selected Anthropic LLM")
            return self.anthropic_llm
        else:
            raise ValueError("No LLM provider available. Please configure API keys.")
    
    def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """Generate response using the selected LLM"""
        return self.current_llm.generate_response(prompt, context, language)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers"""
        providers = []
        if self.openai_llm.is_available():
            providers.append("openai")
        if self.anthropic_llm.is_available():
            providers.append("anthropic")
        if self.openrouter_llm.is_available():
            providers.append("openrouter")
        return providers
    
    def get_openrouter_models(self) -> List[str]:
        """Get list of available OpenRouter models"""
        if self.openrouter_llm.is_available():
            return self.openrouter_llm.get_available_models()
        return []
    
    def switch_provider(self, provider: str):
        """Switch to a different LLM provider"""
        if provider == "openai" and self.openai_llm.is_available():
            self.current_llm = self.openai_llm
            self.provider = "openai"
            logger.info("Switched to OpenAI LLM")
        elif provider == "anthropic" and self.anthropic_llm.is_available():
            self.current_llm = self.anthropic_llm
            self.provider = "anthropic"
            logger.info("Switched to Anthropic LLM")
        elif provider == "openrouter" and self.openrouter_llm.is_available():
            self.current_llm = self.openrouter_llm
            self.provider = "openrouter"
            logger.info("Switched to OpenRouter LLM")
        else:
            raise ValueError(f"Provider {provider} not available")
