"""
Hybrid FastAPI routes using both Swarms Agent and manual OpenAI
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from .agent_service_compatible import agent_service
from .manual_openai_service import manual_openai_service

router = APIRouter(prefix="/agent", tags=["agent"])

@router.get("/status")
async def get_agent_status():
    """Get the current status of both services"""
    agent_info = agent_service.get_agent_info()
    openai_ready = manual_openai_service.client is not None
    
    return {
        "swarms_agent": agent_info,
        "manual_openai": {
            "ready": openai_ready,
            "service": "available" if openai_ready else "needs_api_key"
        },
        "recommended_approach": "manual_openai" if openai_ready else "swarms_base"
    }

@router.post("/chat")
async def chat_with_agent(query: str, use_manual: bool = False):
    """
    Chat with the agent using either Swarms or manual OpenAI
    
    Args:
        query: Your question about Docker, FastAPI, or MLOps
        use_manual: If True, uses manual OpenAI instead of Swarms agent
    """
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if use_manual:
            # Use manual OpenAI service
            if not manual_openai_service.client:
                raise HTTPException(status_code=400, detail="Manual OpenAI not configured. Set OPENAI_API_KEY.")
            
            system_prompt = "You are an expert in Docker, FastAPI, and MLOps. Provide practical advice with code examples."
            response = await manual_openai_service.chat_completion(query, system_prompt)
            
            return {
                "service": "manual_openai",
                "query": query,
                **response
            }
        else:
            # Use Swarms agent
            response = await agent_service.process_docker_query(query)
            return {
                "service": "swarms_agent",
                **response
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/chat/docker")
async def chat_docker_specific(query: str):
    """Specialized endpoint for Docker/MLOps questions using the best available service"""
    try:
        # Use manual OpenAI if available, otherwise Swarms agent
        if manual_openai_service.client:
            system_prompt = """You are a Docker and MLOps expert. Specialize in:
            - Docker containerization best practices
            - FastAPI application development
            - Machine learning model deployment
            - API design and optimization
            Provide practical, actionable advice with code examples."""
            
            response = await manual_openai_service.chat_completion(query, system_prompt)
            return {"service": "manual_openai", "query": query, **response}
        else:
            response = await agent_service.process_docker_query(query)
            return {"service": "swarms_agent", **response}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/capabilities")
async def get_capabilities():
    """Get information about available capabilities"""
    agent_info = agent_service.get_agent_info()
    
    capabilities = {
        "swarms_agent": {
            "status": agent_info["status"],
            "llm_available": agent_info["llm_configured"],
            "can_process_queries": True
        },
        "manual_openai": {
            "status": "ready" if manual_openai_service.client else "needs_api_key",
            "requires": "OPENAI_API_KEY environment variable",
            "model": "gpt-3.5-turbo"
        },
        "recommendation": "Use manual_openai if you have API key, otherwise use swarms_agent for basic functionality"
    }
    
    return capabilities
