"""
Deep exploration of your swarms installation
"""
import swarms
from swarms import Agent

print("🔍 Deep Exploration of Swarms Structure")
print("=" * 50)

# Explore each submodule
submodules = ['agents', 'structs', 'tools']  # Most promising ones

for submodule_name in submodules:
    try:
        module = __import__(f'swarms.{submodule_name}', fromlist=[''])
        print(f"\n📦 {submodule_name.upper()} submodule:")
        
        # Get interesting classes/functions
        items = [item for item in dir(module) if not item.startswith('_')]
        for item in items[:10]:  # Show first 10 items
            print(f"  - {item}")
            
        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more")
            
    except ImportError as e:
        print(f"❌ Could not import swarms.{submodule_name}: {e}")

# Check the Agent class in detail
print(f"\n🤖 Agent Class Deep Inspection:")
agent_methods = [method for method in dir(Agent) if not method.startswith('_')]
print(f"Agent methods: {agent_methods}")

# Check if we can create an agent and see what happens
print(f"\n🧪 Testing Agent Creation:")
try:
    test_agent = Agent(
        agent_name="Test-Agent",
        system_prompt="Test",
        llm=None,
        max_loops=1
    )
    print(f"✅ Agent created successfully")
    print(f"   Type: {type(test_agent)}")
    print(f"   Available attributes: {[attr for attr in dir(test_agent) if not attr.startswith('_')][:10]}")
    
    # Check if it has run method and what it expects
    if hasattr(test_agent, 'run'):
        print(f"   Has run method: Yes")
        import inspect
        sig = inspect.signature(test_agent.run)
        print(f"   Run method signature: {sig}")
    
except Exception as e:
    print(f"❌ Agent creation failed: {e}")
