import swarms

print("🔍 Exploring Swarms Package Structure")
print("=" * 50)

# List all available classes
all_items = dir(swarms)
classes = [item for item in all_items if not item.startswith('_')]
print(f"Available classes: {classes}")

print("\n🧪 Testing key components...")

# Test Agent class
try:
    from swarms import Agent
    agent = Agent(
        agent_name="Explorer Agent",
        system_prompt="You are helpful",
        llm=None,
        max_loops=1
    )
    print("✅ Agent class works")
except Exception as e:
    print(f"❌ Agent failed: {e}")

# Test BaseSwarm class
try:
    from swarms import BaseSwarm
    print("✅ BaseSwarm class available")
except Exception as e:
    print(f"❌ BaseSwarm: {e}")

# Test workflows
try:
    from swarms import BatchedGridWorkflow
    print("✅ BatchedGridWorkflow available")
except Exception as e:
    print(f"❌ BatchedGridWorkflow: {e}")

# Test tools
try:
    from swarms import BaseTool
    print("✅ BaseTool available")
except Exception as e:
    print(f"❌ BaseTool: {e}")

print(f"\n📊 Total classes found: {len(classes)}")
