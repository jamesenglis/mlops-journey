"""
Flexible Swarms Agent Service that tries multiple LLM providers
"""
from swarms import Agent
from typing import Dict, Any, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlexibleDockerMLOpsService:
    """
    A flexible service that tries multiple LLM providers in order of preference
    """
    
    def __init__(self):
        self.agent = self._initialize_agent_with_fallback()
        logger.info(f"Flexible agent service initialized with: {self.agent.agent_name}")
    
    def _initialize_agent_with_fallback(self) -> Agent:
        """Try providers in order: OpenAI -> Anthropic -> Ollama -> Base Agent"""
        
        # 1. Try OpenAI first
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                from swarms.models import OpenAIChat
                openai_model = OpenAIChat(
                    openai_api_key=openai_key,
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                )
                logger.info("Using OpenAI GPT-3.5-Turbo")
                return Agent(
                    agent_name="Docker-MLOps-OpenAI-Agent",
                    system_prompt="Expert in Docker, FastAPI, and MLOps",
                    llm=openai_model,
                    max_loops=3,
                    verbose=True
                )
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")
        
        # 2. Try Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                from swarms.models import Anthropic
                anthropic_model = Anthropic(
                    anthropic_api_key=anthropic_key,
                    model_name="claude-3-haiku-20240307",
                    temperature=0.7,
                )
                logger.info("Using Anthropic Claude")
                return Agent(
                    agent_name="Docker-MLOps-Claude-Agent",
                    system_prompt="Expert in Docker, FastAPI, and MLOps",
                    llm=anthropic_model,
                    max_loops=3,
                    verbose=True
                )
            except Exception as e:
                logger.warning(f"Anthropic initialization failed: {e}")
        
        # 3. Try Ollama (local)
        try:
            from swarms.models import Ollama
            ollama_model = Ollama(
                model_name="llama2:7b",
                temperature=0.7,
            )
            logger.info("Using Ollama with Llama2")
            return Agent(
                agent_name="Docker-MLOps-Ollama-Agent",
                system_prompt="Expert in Docker, FastAPI, and MLOps",
                llm=ollama_model,
                max_loops=3,
                verbose=True
            )
        except Exception as e:
            logger.warning(f"Ollama initialization failed: {e}")
        
        # 4. Fallback to base agent (no LLM)
        logger.info("No LLM provider available, using base agent")
        return Agent(
            agent_name="Docker-MLOps-Base-Agent",
            system_prompt="Expert in Docker and MLOps (No LLM configured)",
            llm=None,
            max_loops=1,
            verbose=True
        )
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the configured agent"""
        llm_configured = self.agent.llm is not None
        return {
            "agent_name": self.agent.agent_name,
            "llm_configured": llm_configured,
            "max_loops": self.agent.max_loops,
            "status": "active" if llm_configured else "no_llm"
        }
    
    async def process_docker_query(self, query: str) -> Dict[str, Any]:
        """Process queries with the available agent"""
        try:
            if self.agent.llm is None:
                return {
                    "query": query,
                    "status": "no_llm",
                    "response": "No LLM configured. Please set up OpenAI, Anthropic, or Ollama.",
                    "setup_required": True
                }
            
            response = self.agent.run(query)
            return {
                "query": query,
                "status": "processed",
                "response": response,
                "agent": self.agent.agent_name
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }

# Use the flexible service as default
agent_service = FlexibleDockerMLOpsService()
