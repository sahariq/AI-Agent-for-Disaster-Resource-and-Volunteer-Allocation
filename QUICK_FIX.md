# Quick Fix: API Endpoints Not Working

## Problem Identified ✅
Your API server endpoints weren't working because **port 8000 was already in use** by stuck processes.

## Solution Applied ✅
I've killed the processes using port 8000. The port is now free!

## Next Steps

### 1. Start the Server
```bash
# Option 1: Use the helper script
.\start_api_server.ps1

# Option 2: Manual start
cd AI-Agent-System
python api\server.py
```

### 2. Test the Endpoints

**In Browser:**
- Open: `http://localhost:8000/test` (web interface)
- Or: `http://localhost:8000/health` (health check)

**Using Python:**
```bash
python test_endpoints.py
```

**Using cURL:**
```bash
curl http://localhost:8000/health
```

## If It Happens Again

If endpoints stop working again (port conflict):

**Quick Fix:**
```bash
# PowerShell
.\kill_port_8000.ps1

# Command Prompt
kill_port_8000.bat

# Then restart server
.\start_api_server.ps1
```

**Or manually:**
```bash
# Find processes
netstat -ano | findstr :8000

# Kill specific process (replace <PID> with actual process ID)
taskkill /F /PID <PID>
```

## Diagnostic Tools

**Run full diagnostic:**
```bash
python diagnose_server.py
```

This will check:
- ✅ Python version
- ✅ Dependencies installed
- ✅ Server imports working
- ✅ Port availability
- ✅ Server startup test

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port 8000 in use | Run `kill_port_8000.ps1` |
| Import errors | Make sure you're in `AI-Agent-System` directory |
| Flask not found | `pip install Flask flask-cors` |
| Server won't start | Check `diagnose_server.py` output |

## Files Created

1. **`diagnose_server.py`** - Comprehensive diagnostic tool
2. **`kill_port_8000.ps1`** - Kill processes on port 8000 (PowerShell)
3. **`kill_port_8000.bat`** - Kill processes on port 8000 (CMD)
4. **`test_endpoints.py`** - Automated endpoint tester
5. **`HOW_TO_TEST_ENDPOINTS.md`** - Complete testing guide

---

**Your server should now work!** 🎉

Start it with `.\start_api_server.ps1` and test at `http://localhost:8000/test`

