"""
Debug OpenAI integration with Swarms
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Debugging OpenAI Integration")
print("=" * 50)

# Test 1: Check if API key is properly set
api_key = os.getenv("OPENAI_API_KEY")
print(f"✅ OPENAI_API_KEY is set: {bool(api_key)}")
if api_key:
    print(f"   Key preview: {api_key[:10]}...{api_key[-4:]}")

# Test 2: Test direct OpenAI API call
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    # Simple test call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello World'"}],
        max_tokens=10
    )
    print("✅ Direct OpenAI API call: SUCCESS")
    print(f"   Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Direct OpenAI API call failed: {e}")

# Test 3: Test Swarms OpenAIChat model
try:
    from swarms.models import OpenAIChat
    
    model = OpenAIChat(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=100
    )
    
    # Test the model directly
    response = model("Say 'Hello from Swarms'")
    print("✅ Swarms OpenAIChat model: SUCCESS")
    print(f"   Response: {response}")
    
except Exception as e:
    print(f"❌ Swarms OpenAIChat failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test Agent with simpler configuration
try:
    from swarms import Agent
    from swarms.models import OpenAIChat
    
    # Use simpler configuration
    llm = OpenAIChat(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.5,  # Lower temperature for more consistent results
        max_tokens=150,   # Limit tokens
    )
    
    agent = Agent(
        agent_name="Test-Agent",
        system_prompt="You are a helpful assistant. Respond briefly.",
        llm=llm,
        max_loops=1,      # Reduce loops
        verbose=True
    )
    
    print("✅ Agent created with OpenAI")
    
    # Test with a very simple query
    response = agent.run("Say hello in one word.")
    print(f"✅ Agent run: SUCCESS")
    print(f"   Response: {response}")
    
except Exception as e:
    print(f"❌ Agent with OpenAI failed: {e}")
    import traceback
    traceback.print_exc()
