#!/usr/bin/env python
"""
Quick fix script for common API server issues.
This will:
1. Kill any process using port 8000
2. Verify dependencies
3. Start the server properly
"""

import sys
import os
import subprocess
import socket
import time
from pathlib import Path

def kill_port(port):
    """Kill process using a specific port (Windows)."""
    try:
        # Find process using port
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.split('\n')
        pid = None
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    break
        
        if pid:
            print(f"   Found process {pid} using port {port}")
            try:
                subprocess.run(["taskkill", "/F", "/PID", pid], check=True, capture_output=True)
                print(f"   ✅ Killed process {pid}")
                time.sleep(1)  # Wait for port to be released
                return True
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️  Could not kill process: {e}")
                return False
        else:
            print(f"   ✅ No process found using port {port}")
            return True
    except Exception as e:
        print(f"   ⚠️  Error checking port: {e}")
        return False

def check_port_available(port):
    """Check if port is available."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def main():
    print("=" * 70)
    print("API Server Fix Tool")
    print("=" * 70)
    
    # Step 1: Kill process on port 8000
    print("\n[1] Checking port 8000...")
    if not check_port_available(8000):
        print("   Port 8000 is in use. Attempting to free it...")
        kill_port(8000)
    else:
        print("   ✅ Port 8000 is available")
    
    # Step 2: Verify we're in the right directory
    print("\n[2] Checking directory...")
    if not Path("AI-Agent-System/api/server.py").exists():
        print("   ❌ Not in project root!")
        print("   Please run this from: G:\\multi_agent_system")
        return 1
    print("   ✅ In correct directory")
    
    # Step 3: Check dependencies
    print("\n[3] Checking dependencies...")
    try:
        import flask
        import flask_cors
        print("   ✅ Flask and flask-cors installed")
    except ImportError:
        print("   ⚠️  Installing Flask dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Flask", "flask-cors"], check=True)
        print("   ✅ Dependencies installed")
    
    # Step 4: Start server
    print("\n[4] Starting server...")
    print("   Changing to AI-Agent-System directory...")
    os.chdir("AI-Agent-System")
    
    print("\n" + "=" * 70)
    print("Starting Flask server on http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    try:
        # Start server
        subprocess.run([sys.executable, "api/server.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

