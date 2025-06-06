# 🚀 **START HERE - QUICK SETUP GUIDE**

## ✅ **STEP 1: INSTALL OLLAMA**

```bash
# Check if Ollama is installed
ollama --version

# If not installed, install it:
# On Mac/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows: Download from https://ollama.ai
```

## ✅ **STEP 2: START OLLAMA**

```bash
# In a terminal, start Ollama:
ollama serve

# Keep this terminal open!
```

## ✅ **STEP 3: RUN THE SYSTEM**

```bash
# In a NEW terminal:
cd /workspace
python run_orion_system.py

# If you get errors about missing packages, the script will install them automatically
# Just run it again after installation completes
```

## ✅ **STEP 4: OPEN THE DASHBOARD**

```bash
# In ANOTHER new terminal:
cd /workspace
python dashboard/learning_dashboard.py

# Then open your browser to:
# http://localhost:5002
```

---

## 🎯 **WHAT YOU SHOULD SEE**

### **In Terminal 1 (Ollama)**
```
Ollama is running on http://127.0.0.1:11434
```

### **In Terminal 2 (System)**
```
🚀 ORION INTELLIGENT TRADING SYSTEM
✅ Dependencies satisfied
✅ Ollama ready with Mistral
✅ Starting Intelligent Orchestrator
✅ SYSTEM FULLY OPERATIONAL

Then every 30 seconds:
📊 SYSTEM STATUS
  • Data Collections: X
  • Analyses Completed: X
  • Strategies Generated: X
```

### **In Terminal 3 (Dashboard)**
```
🚀 Starting Orion Learning Dashboard...
📊 Open http://localhost:5002 in your browser
```

### **In Your Browser**
A beautiful dashboard showing:
- Real-time statistics
- Confidence charts
- Recent learnings
- Generated strategies
- Event timeline

---

## ⚠️ **TROUBLESHOOTING**

### **"command not found: python"**
```bash
# Try python3 instead:
python3 run_orion_system.py
```

### **"No module named 'ollama'"**
```bash
# Install missing packages:
python3 -m pip install ollama chromadb pandas numpy yfinance requests feedparser flask flask-cors --break-system-packages
```

### **"Ollama not running"**
```bash
# Make sure Terminal 1 is running:
ollama serve
```

### **"Port already in use"**
```bash
# Kill existing processes:
pkill -f "python.*dashboard"
pkill -f "python.*run_orion"
```

---

## 📁 **KEY FILES FOR COPILOT**

When working with Copilot, tell it to read these files FIRST:

1. **COPILOT_CONTEXT.md** - Rules for development
2. **COPILOT_HANDOVER.md** - Current system state
3. **COMPLETE_SYSTEM_GUIDE.md** - Full documentation

---

## 🎉 **SUCCESS CHECKLIST**

- [ ] Ollama is running
- [ ] System shows "FULLY OPERATIONAL"
- [ ] Dashboard opens at http://localhost:5002
- [ ] You see data being collected every 5 minutes
- [ ] Strategies appear in the dashboard

**If all boxes are checked, YOUR SYSTEM IS RUNNING!** 🚀