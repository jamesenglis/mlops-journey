"""
Swarms Agent Service compatible with your installation
Uses only available modules and features
"""
from swarms import Agent
from typing import Dict, Any, Optional
import logging
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompatibleDockerMLOpsService:
    """
    A service that works with your current swarms installation
    """
    
    def __init__(self):
        self.agent = self._initialize_compatible_agent()
        logger.info("Compatible Docker MLOps Service initialized")
    
    def _initialize_compatible_agent(self) -> Agent:
        """Initialize agent using only available components"""
        
        # Since we don't have swarms.models, we have a few options:
        
        # Option 1: Try to find LLM integration in structs or agents
        llm_instance = self._try_find_llm()
        
        if llm_instance:
            logger.info("✅ Found LLM integration")
            return Agent(
                agent_name="Docker-MLOps-LLM-Agent",
                system_prompt="""You are an expert in Docker, FastAPI, and MLOps. 
                Provide practical, actionable advice with code examples.""",
                llm=llm_instance,
                max_loops=2,
                verbose=True
            )
        
        # Option 2: Try to use OpenAI directly if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.startswith("sk-"):
            logger.info("🔄 Trying OpenAI direct integration...")
            return self._try_openai_direct(api_key)
        
        # Option 3: Base agent without LLM
        logger.info("📝 Using base agent (no LLM)")
        return Agent(
            agent_name="Docker-MLOps-Base-Agent",
            system_prompt="Expert in Docker and MLOps. Currently operating in limited mode.",
            llm=None,
            max_loops=1,
            verbose=True
        )
    
    def _try_find_llm(self):
        """Try to find LLM classes in available modules"""
        try:
            # Check structs module (common location for models)
            from swarms import structs
            llm_classes = [cls for cls in dir(structs) if 'LLM' in cls or 'Model' in cls]
            if llm_classes:
                logger.info(f"Found potential LLM classes in structs: {llm_classes}")
                # Try to instantiate the first one
                if 'OpenAI' in llm_classes[0]:
                    return getattr(structs, llm_classes[0])()
        except Exception as e:
            logger.debug(f"No LLM in structs: {e}")
        
        return None
    
    def _try_openai_direct(self, api_key: str) -> Agent:
        """Try to integrate OpenAI directly"""
        try:
            # Some swarms versions might accept API key as parameter
            agent = Agent(
                agent_name="Docker-MLOps-OpenAI-Agent",
                system_prompt="Expert in Docker, FastAPI, and MLOps",
                openai_api_key=api_key,
                max_loops=2,
                verbose=True
            )
            logger.info("✅ Created agent with OpenAI parameters")
            return agent
        except Exception as e:
            logger.warning(f"OpenAI direct parameters failed: {e}")
            
            # Fallback to base agent but store API key for manual use
            agent = Agent(
                agent_name="Docker-MLOps-Manual-LLM-Agent",
                system_prompt="Expert in Docker and MLOps",
                llm=None,
                max_loops=1,
                verbose=True
            )
            agent._openai_api_key = api_key  # Store for potential manual use
            return agent
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the configured agent"""
        has_llm = self.agent.llm is not None
        agent_name = getattr(self.agent, 'agent_name', 'Unknown')
        
        # Check various LLM indicators
        has_openai_key = hasattr(self.agent, 'openai_api_key') or hasattr(self.agent, '_openai_api_key')
        api_key_available = os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY").startswith("sk-")
        
        return {
            "agent_name": agent_name,
            "llm_configured": has_llm,
            "openai_key_available": api_key_available,
            "agent_has_openai_key": has_openai_key,
            "max_loops": getattr(self.agent, 'max_loops', 1),
            "status": "active_with_llm" if has_llm else "active_no_llm" if api_key_available else "base_agent"
        }
    
    async def process_docker_query(self, query: str) -> Dict[str, Any]:
        """Process queries with the available agent"""
        start_time = time.time()
        
        try:
            logger.info(f"Processing query: {query}")
            
            # Check if agent has run method
            if not hasattr(self.agent, 'run'):
                return {
                    "query": query,
                    "status": "agent_has_no_run",
                    "response": "This agent version doesn't support the run method",
                    "processing_time": round(time.time() - start_time, 2)
                }
            
            # Try to run the query
            response = self.agent.run(query)
            
            return {
                "query": query,
                "status": "success",
                "response": response,
                "agent": getattr(self.agent, 'agent_name', 'Unknown'),
                "processing_time": round(time.time() - start_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            
            # Provide helpful error response
            error_msg = str(e)
            if "llm" in error_msg.lower() or "model" in error_msg.lower():
                suggestion = "LLM not properly configured. Check your OpenAI API key."
            elif "run" in error_msg.lower():
                suggestion = "Run method not available in this agent version."
            else:
                suggestion = "Check agent configuration and dependencies."
            
            return {
                "status": "error",
                "error": error_msg,
                "suggestion": suggestion,
                "query": query,
                "processing_time": round(time.time() - start_time, 2)
            }

# Use the compatible service
agent_service = CompatibleDockerMLOpsService()
