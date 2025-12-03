#!/usr/bin/env python
"""
Comprehensive diagnostic script to identify why API endpoints aren't working.
Run this from the project root directory.
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("API Server Diagnostic Tool")
print("=" * 70)

errors = []
warnings = []

# 1. Check Python version
print("\n[1] Checking Python version...")
python_version = sys.version_info
print(f"   Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version < (3, 7):
    errors.append("Python 3.7+ required")
    print("   ❌ Python version too old!")
else:
    print("   ✅ Python version OK")

# 2. Check current directory
print("\n[2] Checking current directory...")
cwd = Path.cwd()
print(f"   Current directory: {cwd}")
if not (cwd / "AI-Agent-System" / "api" / "server.py").exists():
    errors.append("Not in project root or server.py not found")
    print("   ❌ Cannot find server.py")
    print(f"   Expected: {cwd / 'AI-Agent-System' / 'api' / 'server.py'}")
else:
    print("   ✅ Server file found")

# 3. Check Flask installation
print("\n[3] Checking Flask installation...")
try:
    import flask
    print(f"   ✅ Flask {flask.__version__} installed")
except ImportError:
    errors.append("Flask not installed")
    print("   ❌ Flask not installed!")
    print("   Fix: pip install Flask")

# 4. Check flask-cors
print("\n[4] Checking flask-cors...")
try:
    import flask_cors
    print("   ✅ flask-cors installed")
except ImportError:
    errors.append("flask-cors not installed")
    print("   ❌ flask-cors not installed!")
    print("   Fix: pip install flask-cors")

# 5. Check required modules
print("\n[5] Checking required modules...")
modules_to_check = [
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("sklearn", "scikit-learn"),
    ("pulp", "PuLP"),
    ("yaml", "PyYAML"),
]

for module_name, package_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"   ✅ {package_name} installed")
    except ImportError:
        warnings.append(f"{package_name} not installed (may be needed)")
        print(f"   ⚠️  {package_name} not installed")

# 6. Check server imports
print("\n[6] Testing server imports...")
server_path = Path("AI-Agent-System") / "api" / "server.py"
if server_path.exists():
    # Change to AI-Agent-System directory for imports
    original_cwd = os.getcwd()
    try:
        os.chdir("AI-Agent-System")
        sys.path.insert(0, os.getcwd())
        
        # Test import optimization.volunteer_allocator
        try:
            from optimization.volunteer_allocator import run_allocation
            print("   ✅ volunteer_allocator imported successfully")
        except Exception as e:
            errors.append(f"Cannot import volunteer_allocator: {e}")
            print(f"   ❌ Cannot import volunteer_allocator: {e}")
        
        # Test import shared.utils
        try:
            from shared.utils import get_utc_timestamp
            print("   ✅ shared.utils imported successfully")
        except Exception as e:
            errors.append(f"Cannot import shared.utils: {e}")
            print(f"   ❌ Cannot import shared.utils: {e}")
        
    except Exception as e:
        errors.append(f"Error testing imports: {e}")
        print(f"   ❌ Error: {e}")
    finally:
        os.chdir(original_cwd)

# 7. Check if port 8000 is in use
print("\n[7] Checking if port 8000 is available...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    if result == 0:
        warnings.append("Port 8000 is already in use")
        print("   ⚠️  Port 8000 is already in use!")
        print("   Another process may be using it, or server is already running")
    else:
        print("   ✅ Port 8000 is available")
except Exception as e:
    warnings.append(f"Could not check port: {e}")
    print(f"   ⚠️  Could not check port: {e}")

# 8. Try to start server (quick test)
print("\n[8] Testing server startup...")
if not errors:
    try:
        import subprocess
        import time
        
        # Change to AI-Agent-System directory
        original_cwd = os.getcwd()
        os.chdir("AI-Agent-System")
        
        # Try to start server in background
        print("   Attempting to start server...")
        process = subprocess.Popen(
            [sys.executable, "api/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Wait a bit
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("   ✅ Server process started successfully")
            # Try to connect
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("   ✅ Server is responding to requests!")
                    print(f"   Response: {response.json()}")
                else:
                    warnings.append(f"Server started but returned status {response.status_code}")
                    print(f"   ⚠️  Server returned status {response.status_code}")
            except ImportError:
                warnings.append("requests library not available for testing")
                print("   ⚠️  Cannot test HTTP requests (requests library not installed)")
            except Exception as e:
                warnings.append(f"Server started but not responding: {e}")
                print(f"   ⚠️  Server started but not responding: {e}")
            
            # Stop the server
            process.terminate()
            process.wait(timeout=2)
        else:
            # Process exited, get error
            stdout, stderr = process.communicate()
            error_msg = stderr.decode('utf-8', errors='ignore') or stdout.decode('utf-8', errors='ignore')
            errors.append(f"Server failed to start: {error_msg[:200]}")
            print(f"   ❌ Server failed to start!")
            if error_msg:
                print(f"   Error: {error_msg[:500]}")
        
        os.chdir(original_cwd)
    except Exception as e:
        warnings.append(f"Could not test server startup: {e}")
        print(f"   ⚠️  Could not test server startup: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

# Summary
print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)

if errors:
    print("\n❌ CRITICAL ERRORS (must fix):")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
else:
    print("\n✅ No critical errors found!")

if warnings:
    print("\n⚠️  WARNINGS:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")

# Recommendations
print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

if errors:
    print("\nTo fix the errors:")
    if any("Flask" in e for e in errors):
        print("   1. Install Flask: pip install Flask flask-cors")
    if any("import" in e.lower() for e in errors):
        print("   2. Make sure you're running from project root:")
        print("      cd G:\\multi_agent_system")
        print("      python AI-Agent-System\\api\\server.py")
    if any("port" in e.lower() for e in errors):
        print("   3. Check if another process is using port 8000")
        print("      netstat -ano | findstr :8000")
else:
    print("\n✅ Everything looks good! Try starting the server:")
    print("   cd AI-Agent-System")
    print("   python api\\server.py")
    print("\n   Then test endpoints:")
    print("   - http://localhost:8000/health")
    print("   - http://localhost:8000/test (for web interface)")

print("\n" + "=" * 70)

