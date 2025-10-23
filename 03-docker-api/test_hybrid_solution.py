"""
Test the hybrid Swarms + Manual OpenAI solution
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agent_service_compatible import CompatibleDockerMLOpsService
from app.manual_openai_service import ManualOpenAIService

def test_hybrid_solution():
    print("🧪 Testing Hybrid Solution")
    print("=" * 50)
    
    # Test Swarms Agent
    print("\n🤖 Testing Swarms Agent:")
    swarms_service = CompatibleDockerMLOpsService()
    swarms_info = swarms_service.get_agent_info()
    
    for key, value in swarms_info.items():
        print(f"   {key}: {value}")
    
    # Test Manual OpenAI
    print("\n🔧 Testing Manual OpenAI:")
    openai_service = ManualOpenAIService()
    print(f"   Client initialized: {openai_service.client is not None}")
    
    # Test queries
    import asyncio
    
    test_query = "How do I create a Dockerfile for a Python application?"
    
    print(f"\n🧪 Testing Swarms Agent with: '{test_query}'")
    swarms_response = asyncio.run(swarms_service.process_docker_query(test_query))
    print(f"   Status: {swarms_response['status']}")
    
    if openai_service.client:
        print(f"\n🧪 Testing Manual OpenAI with: '{test_query}'")
        openai_response = asyncio.run(openai_service.chat_completion(
            test_query, 
            "You are a Docker expert"
        ))
        print(f"   Status: {openai_response['status']}")
        if openai_response['status'] == 'success':
            print(f"   Response preview: {openai_response['response'][:100]}...")
    
    print(f"\n🎯 Recommendation:")
    if openai_service.client:
        print("   Use Manual OpenAI for full LLM capabilities")
    else:
        print("   Get OpenAI API key for full functionality, or use Swarms base agent")

if __name__ == "__main__":
    test_hybrid_solution()
