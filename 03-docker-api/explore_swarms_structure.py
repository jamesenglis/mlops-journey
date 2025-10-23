"""
Explore what's actually available in your swarms installation
"""
import swarms
import inspect

print("🔍 Exploring Swarms Structure")
print("=" * 50)

# Check what's in the main swarms module
print("Main swarms module contents:")
for item in dir(swarms):
    if not item.startswith('_'):
        print(f"  - {item}")

# Check if there's a models submodule
print("\n📦 Checking for models submodule:")
try:
    import swarms.models
    print("✅ swarms.models exists")
    print("Contents:", dir(swarms.models))
except ImportError as e:
    print(f"❌ swarms.models does not exist: {e}")

# Check the actual Agent class to see what LLM parameter it expects
print("\n🤖 Checking Agent class signature:")
try:
    from swarms import Agent
    sig = inspect.signature(Agent.__init__)
    print("Agent __init__ parameters:")
    for name, param in sig.parameters.items():
        if name == 'llm':
            print(f"  - llm: {param}")
            print(f"    annotation: {param.annotation}")
except Exception as e:
    print(f"Error checking Agent: {e}")

# Check what LLM classes are available
print("\n🔍 Looking for LLM classes in swarms:")
llm_classes = []
for item in dir(swarms):
    obj = getattr(swarms, item)
    if hasattr(obj, '__name__') and 'LLM' in obj.__name__.upper():
        llm_classes.append(obj.__name__)
        
if llm_classes:
    print("Found LLM-related classes:", llm_classes)
else:
    print("No LLM classes found in main swarms module")

# Check submodules
print("\n📚 Available submodules:")
import pkgutil
for importer, modname, ispkg in pkgutil.iter_modules(swarms.__path__):
    print(f"  - {modname}")
