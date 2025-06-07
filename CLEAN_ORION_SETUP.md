# 🚀 CLEAN ORION SETUP GUIDE

## ❌ THE PROBLEM:
- Services showing 0/5 active (they're not starting properly)
- Copilot confusion (different environments, conflicting files)
- Complex setup causing errors

## ✅ THE SOLUTION: Clean, Simple Setup

### 📁 **Option 1: Use Current Folder (Recommended)**
Keep everything where it is but fix the issues:

```bash
# 1. Exit virtual environment if active
deactivate 2>/dev/null

# 2. Use system Python directly
/usr/bin/python3 simple_start.py
```

### 📁 **Option 2: Fresh Clean Folder**
If you want to start completely fresh:

```bash
# 1. Create clean folder
mkdir ~/OrionClean
cd ~/OrionClean

# 2. Copy ONLY the working files
cp -r /workspace/core_orchestration .
cp -r /workspace/research_center .
cp -r /workspace/knowledge_center .
cp -r /workspace/strategy_center .
cp -r /workspace/risk_management_center .
cp -r /workspace/dashboard .
cp -r /workspace/databases .
cp /workspace/run_orion_system.py .
cp /workspace/.env .
cp /workspace/simple_start.py .
cp /workspace/requirements.txt .

# 3. Run the clean system
/usr/bin/python3 simple_start.py
```

## 🔧 **FIXING THE INACTIVE SERVICES**

The services are inactive because they're waiting for the event bus to initialize properly. Here's the fix:

1. **Create a service activator** (`fix_services.py`):
```python
#!/usr/bin/env python3
"""Fix inactive services by properly initializing the event bus"""

import asyncio
import sys
sys.path.insert(0, '.')

async def activate_services():
    # Import after path is set
    from core_orchestration.message_queue.event_bus import EventBus
    from core_orchestration.intelligent_orchestrator import IntelligentOrchestrator
    
    print("🔧 Activating services...")
    
    # Initialize event bus
    event_bus = EventBus()
    await event_bus.start()
    
    # Initialize orchestrator
    orchestrator = IntelligentOrchestrator()
    await orchestrator.initialize()
    
    print("✅ Services activated!")
    print("🚀 Starting normal operation...")
    
    # Run the orchestrator
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(activate_services())
```

2. **Run this instead of run_orion_system.py**:
```bash
/usr/bin/python3 fix_services.py
```

## 📋 **COPILOT INSTRUCTIONS FILE**
Create `COPILOT_INSTRUCTIONS.txt` in your project root:

```
ORION AI TRADING SYSTEM - COPILOT RULES

1. NEVER create duplicate files
2. ALWAYS use /usr/bin/python3 (NOT virtual env)
3. Core files:
   - run_orion_system.py (main entry)
   - simple_start.py (easy starter)
   - fix_services.py (service activator)

4. To run system: /usr/bin/python3 simple_start.py
5. To check status: ps aux | grep orion
6. To view logs: tail -f logs/background_agent/agent.log

7. DO NOT modify working code without testing
8. DO NOT use pip install without --break-system-packages flag
9. DO NOT create new architecture - use existing modules

10. If services show 0/5: Run fix_services.py
```

## 💰 **COST-FRIENDLY TIPS**

1. **Use Local LLMs Only**:
   - Ollama with mistral:7b (FREE)
   - Disable cloud APIs in .env

2. **Limit Data Collection**:
   ```python
   # In run_orion_system.py, change:
   check_interval=300  # to check_interval=3600 (1 hour)
   ```

3. **Use Mock Mode for Testing**:
   ```bash
   export ORION_MODE=mock
   python simple_start.py
   ```

## 🎯 **IMMEDIATE ACTION PLAN**

1. **Right Now - Fix Services**:
   ```bash
   cd /workspace
   /usr/bin/python3 simple_start.py
   ```

2. **If Still Having Issues**:
   ```bash
   # Kill everything
   pkill -f python
   pkill -f ollama
   
   # Restart clean
   ollama serve &
   sleep 5
   /usr/bin/python3 simple_start.py
   ```

3. **Monitor Success**:
   ```bash
   # In another terminal:
   tail -f logs/background_agent/agent.log | grep -E "(Active Services|ERROR)"
   ```

## ✅ **SUCCESS INDICATORS**
- You'll see "Active Services: 5/5"
- Data collections increase
- Analyses start completing
- No more "Service inactive" warnings

## 🚨 **IF NOTHING WORKS**
Use the minimal trader that definitely works:
```bash
/usr/bin/python3 SIMPLE_WORKING_TRADER.py
```

This bypasses all the complex orchestration and just trades!