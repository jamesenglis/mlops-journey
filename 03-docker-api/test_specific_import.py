# Try different import patterns
try:
    # Method 1: Direct import
    from swarms import Agent
    print("✅ Method 1: from swarms import Agent")
except ImportError as e:
    print(f"❌ Method 1 failed: {e}")
    
try:
    # Method 2: Import the package first
    import swarms
    from swarms.agents import Agent
    print("✅ Method 2: import swarms + from swarms.agents import Agent")
except ImportError as e:
    print(f"❌ Method 2 failed: {e}")
    
try:
    # Method 3: Check what's available
    import swarms
    print(f"✅ Swarms module contents: {dir(swarms)}")
except ImportError as e:
    print(f"❌ Could not import swarms at all: {e}")
