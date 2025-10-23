"""
Manual OpenAI integration that works alongside Swarms Agent
"""
import os
import logging
from typing import Dict, Any
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManualOpenAIService:
    """
    Manual OpenAI service that can be used alongside Swarms Agent
    """
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.startswith("sk-"):
            self.client = OpenAI(api_key=api_key)
            logger.info("✅ Manual OpenAI client initialized")
        else:
            logger.warning("❌ No valid OpenAI API key for manual service")
    
    async def chat_completion(self, query: str, system_prompt: str = None) -> Dict[str, Any]:
        """Manual chat completion using OpenAI directly"""
        if not self.client:
            return {
                "status": "error",
                "error": "OpenAI client not initialized. Check OPENAI_API_KEY."
            }
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": query})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "status": "success",
                "response": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

# Manual service instance
manual_openai_service = ManualOpenAIService()
