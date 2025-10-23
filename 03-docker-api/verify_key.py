"""
Verify your OpenAI API key is working
"""
import os
from openai import OpenAI

print("🔐 Verifying OpenAI API Key")
print("=" * 40)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY is not set")
    print("   Run: export OPENAI_API_KEY='sk-your-real-key'")
    exit(1)

print(f"✅ OPENAI_API_KEY is set")
print(f"   Key preview: {api_key[:10]}...{api_key[-4:]}")
print(f"   Length: {len(api_key)} characters")

# Check if it looks like a real key
if not api_key.startswith("sk-"):
    print("❌ Key does NOT start with 'sk-' - this is invalid!")
    print("   Get a real key from: https://platform.openai.com/api-keys")
    exit(1)

if len(api_key) < 20:
    print("❌ Key is too short - should be about 51 characters")
    exit(1)

print("🔧 Testing API key with OpenAI...")

try:
    client = OpenAI(api_key=api_key)
    
    # Make a simple, cheap test call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say just 'API test successful'"}],
        max_tokens=10
    )
    
    print("🎉 SUCCESS! API key is valid and working!")
    print(f"   Response: {response.choices[0].message.content}")
    print(f"   Model: {response.model}")
    print(f"   Tokens used: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"❌ API test failed: {e}")
    print()
    print("🔧 Troubleshooting:")
    print("   - Make sure you copied the ENTIRE key")
    print("   - Check for extra spaces in the key")
    print("   - Verify your OpenAI account has credits")
    print("   - Visit: https://platform.openai.com/account/api-keys")
