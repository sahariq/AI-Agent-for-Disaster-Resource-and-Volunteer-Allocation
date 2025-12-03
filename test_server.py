#!/usr/bin/env python
"""
Quick test script to check if the server can start and dependencies are available.
"""
import sys
import os

print("=" * 60)
print("Server Diagnostic Test")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check if we're in the right directory
print(f"\n✓ Current directory: {os.getcwd()}")

# Check Flask
try:
    import flask
    print(f"✓ Flask version: {flask.__version__}")
except ImportError:
    print("✗ Flask not installed!")
    print("  Install with: pip install Flask")
    sys.exit(1)

# Check flask-cors
try:
    import flask_cors
    print(f"✓ flask-cors installed")
except ImportError:
    print("✗ flask-cors not installed!")
    print("  Install with: pip install flask-cors")
    sys.exit(1)

# Check if server file exists
server_path = os.path.join("AI-Agent-System", "api", "server.py")
if os.path.exists(server_path):
    print(f"✓ Server file found: {server_path}")
else:
    print(f"✗ Server file not found: {server_path}")
    print(f"  Current directory: {os.getcwd()}")
    sys.exit(1)

# Try to import server modules
print("\nChecking server dependencies...")
try:
    sys.path.insert(0, os.path.join("AI-Agent-System"))
    from optimization.volunteer_allocator import run_allocation
    print("✓ volunteer_allocator imported")
except Exception as e:
    print(f"✗ Error importing volunteer_allocator: {e}")

try:
    from shared.utils import get_utc_timestamp
    print("✓ shared.utils imported")
except Exception as e:
    print(f"✗ Error importing shared.utils: {e}")

print("\n" + "=" * 60)
print("Starting server test...")
print("=" * 60)

# Try to start the server
try:
    import subprocess
    import time
    import requests
    
    # Start server in background
    print("\nStarting server on http://localhost:8000...")
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    # Wait a bit for server to start
    time.sleep(3)
    
    # Test if server is responding
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and responding!")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Server not responding: {e}")
        print("  Make sure port 8000 is not in use by another application")
    
    # Stop the server
    process.terminate()
    process.wait()
    print("\n✓ Server test completed")
    
except ImportError:
    print("✗ requests library not available for testing")
    print("  Install with: pip install requests")
except Exception as e:
    print(f"✗ Error testing server: {e}")

print("\n" + "=" * 60)
print("To start the server manually:")
print("  cd AI-Agent-System")
print("  python api/server.py")
print("=" * 60)

