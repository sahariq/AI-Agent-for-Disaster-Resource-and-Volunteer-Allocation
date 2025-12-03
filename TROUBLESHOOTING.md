# Troubleshooting: Server Won't Start

If `http://localhost:8000` won't open, follow these steps:

## Quick Fixes

### 1. Check if Server is Running

Open a terminal and run:
```bash
# Windows PowerShell
cd AI-Agent-System
python api\server.py

# Or use the helper script from project root
.\start_api_server.ps1
```

You should see:
```
 * Running on http://127.0.0.1:8000
```

### 2. Check Dependencies

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

**Important:** Make sure `flask-cors` is installed:
```bash
pip install flask-cors
```

### 3. Check Port Availability

Port 8000 might be in use. Check with:
```bash
# Windows
netstat -ano | findstr :8000

# If something is using it, either:
# - Stop that application, OR
# - Change the port in api/server.py (line 343)
```

### 4. Run Diagnostic Script

Run the diagnostic script:
```bash
python test_server.py
```

This will check:
- Python version
- Required packages
- Server file location
- If server can start

## Common Errors

### Error: "ModuleNotFoundError: No module named 'flask_cors'"

**Solution:**
```bash
pip install flask-cors
```

### Error: "Address already in use"

**Solution:** Port 8000 is already in use. Either:
1. Stop the other application using port 8000
2. Change the port in `AI-Agent-System/api/server.py` (line 343):
   ```python
   app.run(host="0.0.0.0", port=8001, debug=False)  # Changed to 8001
   ```
   Then update the base URL in `api_test.html` to `http://localhost:8001`

### Error: "Cannot find server.py"

**Solution:** Make sure you're running from the correct directory:
```bash
# From project root
cd AI-Agent-System
python api\server.py
```

### Error: "ImportError: cannot import name 'run_allocation'"

**Solution:** Make sure you're in the `AI-Agent-System` directory when starting the server:
```bash
cd AI-Agent-System
python api\server.py
```

## Manual Start (Step by Step)

1. **Open terminal/PowerShell**

2. **Navigate to project root:**
   ```bash
   cd G:\multi_agent_system
   ```

3. **Activate virtual environment (if using one):**
   ```bash
   .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Navigate to AI-Agent-System:**
   ```bash
   cd AI-Agent-System
   ```

6. **Start server:**
   ```bash
   python api\server.py
   ```

7. **Open browser:**
   - Go to: `http://localhost:8000/test`
   - Or: `http://localhost:8000/health`

## Test Server is Working

Once the server starts, test it:

1. **In browser:** `http://localhost:8000/health`
   - Should return: `{"status": "UP", "agent": "Worker_Disaster", "version": "0.1.0"}`

2. **Or use curl:**
   ```bash
   curl http://localhost:8000/health
   ```

## Still Not Working?

1. Check Python version (should be 3.7+):
   ```bash
   python --version
   ```

2. Check if Flask is installed:
   ```bash
   python -c "import flask; print(flask.__version__)"
   ```

3. Check server logs for errors when starting

4. Try running the server with debug mode:
   ```python
   # In api/server.py, change line 343 to:
   app.run(host="0.0.0.0", port=8000, debug=True)
   ```
   This will show more detailed error messages.

