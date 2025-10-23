import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Starting Swarms Debug Test...")

try:
    from swarms import Agent
    print("✅ SUCCESS: Imported Agent!")
    
    agent = Agent(
        agent_name="Test Agent", 
        system_prompt="You are helpful", 
        llm=None, 
        max_loops=1
    )
    print("✅ SUCCESS: Created Agent!")
    print(f"Agent name: {agent.agent_name}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
