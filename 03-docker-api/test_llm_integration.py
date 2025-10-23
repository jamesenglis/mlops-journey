"""
Test the LLM integration with Swarms Agent
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agent_service_flexible import FlexibleDockerMLOpsService

def test_llm_integration():
    print("🧪 Testing LLM Integration with Swarms Agent")
    print("=" * 50)
    
    # Test the flexible service
    service = FlexibleDockerMLOpsService()
    
    # Get agent info
    info = service.get_agent_info()
    print(f"✅ Agent Info:")
    print(f"   Name: {info['agent_name']}")
    print(f"   LLM Configured: {info['llm_configured']}")
    print(f"   Status: {info['status']}")
    
    # Test query processing
    import asyncio
    response = asyncio.run(service.process_docker_query(
        "How do I create a Dockerfile for a FastAPI application?"
    ))
    
    print(f"✅ Query Test:")
    print(f"   Status: {response['status']}")
    if response['status'] == 'processed':
        print(f"   Response: {response['response'][:200]}...")
    elif response['status'] == 'no_llm':
        print("   ⚠️  No LLM configured - see setup instructions below")
    else:
        print(f"   Error: {response.get('error', 'Unknown error')}")
    
    print(f"\n🔧 Setup Instructions:")
    print("   1. For OpenAI: export OPENAI_API_KEY=your_key_here")
    print("   2. For Anthropic: export ANTHROPIC_API_KEY=your_key_here") 
    print("   3. For Ollama: Install Ollama and run 'ollama pull llama2:7b'")
    print(f"\n🎯 Current Environment:")
    print(f"   OPENAI_API_KEY set: {bool(os.getenv('OPENAI_API_KEY'))}")
    print(f"   ANTHROPIC_API_KEY set: {bool(os.getenv('ANTHROPIC_API_KEY'))}")

if __name__ == "__main__":
    test_llm_integration()
