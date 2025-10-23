"""
Help you get a valid OpenAI API key
"""
print("🔑 Getting a Valid OpenAI API Key")
print("=" * 40)
print("\nFollow these steps:")
print("1. Go to: https://platform.openai.com/api-keys")
print("2. Sign in to your OpenAI account")
print("3. Click 'Create new secret key'")
print("4. Give it a name (e.g., 'Docker-API')")
print("5. Copy the key (it starts with 'sk-')")
print("6. Set it as an environment variable:\n")
print("   export OPENAI_API_KEY='sk-your-actual-key-here'")
print("\n⚠️  Important:")
print("   - The key should start with 'sk-'")
print("   - It should be about 51 characters long")
print("   - Don't share it or commit it to git")
print("   - You may need to add billing to your OpenAI account")

# Check current key issues
import os
current_key = os.getenv("OPENAI_API_KEY")
if current_key:
    print(f"\n🔍 Your current key analysis:")
    print(f"   Starts with: {current_key[:10]}...")
    print(f"   Length: {len(current_key)}")
    if not current_key.startswith("sk-"):
        print("   ❌ Does NOT start with 'sk-' - this is invalid!")
    if "your-opena" in current_key or "example" in current_key.lower():
        print("   ❌ You're using a placeholder key - get a real one!")
