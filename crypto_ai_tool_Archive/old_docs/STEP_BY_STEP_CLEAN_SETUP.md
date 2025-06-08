# 🎯 STEP-BY-STEP CLEAN SETUP - ORION WORKING SYSTEM

**Goal**: Clean Orion_Project directory, keep only working files, get system running with all databases and LLMs connected.

---

## 📋 **STEP 1: IDENTIFY WHAT WE HAVE**

### ✅ **CONFIRMED WORKING FILES** (Keep these):
- `run_orion_system.py` ✅ Main system entry point
- `start_orion.py` ✅ Simple starter (just created)
- `restart_orion.sh` ✅ Clean restart script
- `requirements.txt` ✅ Dependencies
- `.env` ✅ API credentials
- All module directories: `core_orchestration/`, `research_center/`, `knowledge_center/`, etc.

### 🗑️ **CLOUD WORKSPACE FILES** (Move to crypto_ai_tool):
- `TRANSFER_TO_MAC.md`
- `MAC_COPILOT_INSTRUCTIONS.md`
- `COPY_TO_MAC_SIMPLE.txt`
- Documentation from cloud workspace that's duplicated

### 🗃️ **OLD FILES** (Already archived):
- `ARCHIVE_OLD_TESTS_20250107/` ✅ Already organized

---

## 📋 **STEP 2: CLEAN UP DIRECTORY**

### Move cloud workspace transfer files:
```bash
mkdir -p crypto_ai_tool/cloud_workspace_transfer
mv TRANSFER_TO_MAC.md crypto_ai_tool/cloud_workspace_transfer/
mv MAC_COPILOT_INSTRUCTIONS.md crypto_ai_tool/cloud_workspace_transfer/
mv COPY_TO_MAC_SIMPLE.txt crypto_ai_tool/cloud_workspace_transfer/
```

---

## 📋 **STEP 3: VERIFY VIRTUAL ENVIRONMENT**

Your .venv is properly set up with all packages. Let's use it:

```bash
# Activate virtual environment
source .venv/bin/activate

# Verify packages
pip list | grep -E "(pandas|numpy|ollama|chromadb|flask)"
```

---

## 📋 **STEP 4: FIX THE STARTER SCRIPT**

The issue is Python path. Let's fix `start_orion.py`:

```python
#!/usr/bin/env python3
"""
Simple Orion Starter - Uses Virtual Environment
"""
import subprocess
import os
import sys

def main():
    print("🚀 Starting Orion Trading System...")
    print("="*50)
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if main file exists
    main_file = "run_orion_system.py"
    if not os.path.exists(main_file):
        print(f"❌ Error: {main_file} not found!")
        return
    
    print(f"✅ Found {main_file}")
    
    # Use the virtual environment Python
    venv_python = ".venv/bin/python3"
    if os.path.exists(venv_python):
        print(f"🔄 Using virtual environment Python: {venv_python}")
        try:
            subprocess.run([venv_python, main_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {e}")
    else:
        print("❌ Virtual environment not found")
        print("💡 Try: python3 run_orion_system.py")

if __name__ == "__main__":
    main()
```

---

## 📋 **STEP 5: START OLLAMA**

```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve &

# Wait a moment
sleep 5

# Check if mistral model is available
ollama list
```

---

## 📋 **STEP 6: RUN THE SYSTEM**

```bash
# Option 1: Use the starter script
python3 start_orion.py

# Option 2: Direct command with virtual environment
.venv/bin/python3 run_orion_system.py

# Option 3: Activate venv first
source .venv/bin/activate
python run_orion_system.py
```

---

## 📋 **STEP 7: VERIFY WORKING COMPONENTS**

### Expected Output:
```
🚀 ORION INTELLIGENT TRADING SYSTEM
✅ ollama
✅ chromadb  
✅ pandas
✅ numpy
✅ requests
✅ yfinance
✅ feedparser
✅ flask
✅ flask_cors

🔍 Checking Ollama...
✅ Ollama ready with Mistral

🚀 Starting Orion System...
✅ Starting Intelligent Orchestrator
```

### Database Connections:
- `databases/unified/market_data.db` ✅ 65,041 records
- `databases/sqlite_dbs/research_learnings.db` ✅ Research data
- `databases/sqlite_dbs/knowledge_base.db` ✅ Knowledge synthesis

### Exchange Status:
- Bybit: ✅ Working with $10,000 USDT + 0.5 BTC
- 2/5 exchanges operational

---

## 📋 **STEP 8: MONITOR SYSTEM**

After system starts, you should see:
```
📊 SYSTEM STATUS - 14:30:15
==================================================
📈 Performance Metrics:
  • Data Collections: 5
  • Analyses Completed: 3
  • Strategies Generated: 2

🔄 Event Bus Status:
  • Events Published: 12
  • Events Processed: 10
  • Active Services: 4/5
```

---

## 🚨 **IF ISSUES OCCUR**

### Package Issues:
```bash
# Install missing packages to virtual environment
.venv/bin/pip install pandas numpy ollama chromadb yfinance flask flask-[REDACTED]
```

### Ollama Issues:
```bash
# Restart Ollama
pkill ollama
ollama serve &
sleep 5
ollama pull mistral:7b
```

### Database Issues:
- All databases should exist in `databases/` folder
- If missing, system will recreate them

---

## ✅ **SUCCESS CRITERIA**

1. ✅ Directory cleaned (only working files)
2. ✅ Virtual environment active
3. ✅ Ollama running with Mistral model
4. ✅ System starts without errors
5. ✅ All services show "active"
6. ✅ Data collection working
7. ✅ LLM analysis running
8. ✅ Event bus processing events

---

## 🎯 **FINAL VERIFICATION**

Run this to check everything:
```bash
# Check processes
ps aux | grep -E "(ollama|orion)"

# Check databases
ls -la databases/unified/
ls -la databases/sqlite_dbs/

# Check virtual environment
source .venv/bin/activate && python -c "import pandas, numpy, ollama, chromadb, flask; print('✅ All packages working')"
```

**When working, you should have a clean, functional Orion system connected to all databases and LLMs!** 