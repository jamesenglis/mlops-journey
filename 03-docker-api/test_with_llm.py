import sys
import os

print("🧪 Testing Agent with simple LLM...")

try:
    from swarms import Agent
    
    # Create agent with a simple, test-friendly LLM
    agent = Agent(
        agent_name="Chat Agent",
        system_prompt="You are a helpful assistant. Respond briefly.",
        llm=None,  # We'll keep it simple for now
        max_loops=2,
        verbose=True
    )
    
    print("✅ Agent created successfully!")
    print("Testing basic functionality...")
    
    # Try a simple task (if the agent has run method)
    if hasattr(agent, 'run'):
        result = agent.run("Hello, who are you?")
        print(f"✅ Agent response: {result}")
    else:
        print("ℹ️ Agent doesn't have run method, testing attributes:")
        print(f"Name: {agent.agent_name}")
        print(f"System prompt: {agent.system_prompt}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
