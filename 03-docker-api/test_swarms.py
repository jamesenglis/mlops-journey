import sys
import os

print("🔍 Testing swarms installation...")

try:
    from swarms import Agent
    print("✅ SUCCESS: Imported Agent from swarms!")
    
    # Test creating an agent
    agent = Agent(
        agent_name="Test Agent",
        system_prompt="You are a helpful assistant.",
        llm=None,
        max_loops=1
    )
    print("✅ SUCCESS: Agent created!")
    print(f"Agent name: {agent.agent_name}")
    print(f"System prompt: {agent.system_prompt}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
