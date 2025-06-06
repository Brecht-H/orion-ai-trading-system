# 🚀 ORION CLEAN START GUIDE

## 🧹 Directory Cleanup Status

Your Orion project structure should be clean with only essential files in root:

### ✅ **Essential Root Files** (KEEP):
- `run_orion_system.py` - Main entry point
- `quick_setup.sh` - Setup script  
- `README.md` - Main documentation
- `.gitignore` - Git configuration
- `requirements.txt` - Dependencies

### 📁 **Files to Move** (CLEANUP):
These files should be moved from root to keep it clean:

**Documentation Files → `documentation/`**
- `START_HERE.md`
- `COPILOT_HANDOVER.md`
- `COMPLETE_SYSTEM_GUIDE.md`
- `INTELLIGENT_SYSTEM_GUIDE.md`
- `COPILOT_CONTEXT.md`

**Test Files → `tests/`**
- `test_system.py`
- `test_mcp_integration.py`

**Temporary Files → `Crypto_ai_tool/old_docs/`**
- `run_system_direct.py`
- `cleanup_root.sh`
- `cleanup_orion.py`
- `fix_and_run.py`

## 🔧 Quick Fix & Run

### Option 1: Use the Fix Script
```bash
python fix_and_run.py
```

This script will:
1. Remove any aiohttp imports
2. Clear Python cache
3. Install missing packages
4. Start the system

### Option 2: Manual Start
```bash
# Clear cache
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Run directly
python run_orion_system.py
```

## 📋 Manual Cleanup Commands

If you want to manually clean up the root directory:

```bash
# Move documentation files
mv START_HERE.md COPILOT_*.md COMPLETE_*.md INTELLIGENT_*.md documentation/ 2>/dev/null

# Move test files  
mv test_*.py tests/ 2>/dev/null

# Move temporary files
mkdir -p Crypto_ai_tool/old_docs
mv run_system_direct.py cleanup*.* fix_and_run.py Crypto_ai_tool/old_docs/ 2>/dev/null

# Rename requirements file
mv requirements_background_agent.txt requirements.txt 2>/dev/null
```

## ✅ Final Clean Structure

After cleanup, your root should only contain:
```
Orion_project/
├── run_orion_system.py          # Main entry
├── quick_setup.sh               # Setup
├── requirements.txt             # Dependencies  
├── README.md                    # Documentation
├── .gitignore                   # Git config
├── ORION_CLEAN_START.md        # This guide
│
├── core_orchestration/          # Core system
├── research_center/             # Data collection
├── knowledge_center/            # AI processing
├── strategy_center/             # Trading strategies
├── risk_management_center/      # Risk controls
├── trading_execution_center/    # Trade execution
├── technical_analysis_center/   # TA indicators
├── notion_integration_hub/      # Notion interface
├── dashboard/                   # Web dashboard
│
├── documentation/               # All docs
├── tests/                       # All tests
├── databases/                   # Data storage
├── logs/                        # System logs
├── config/                      # Configuration
├── deployment/                  # Deploy scripts
├── reports/                     # Generated reports
├── mcp/                         # MCP servers
└── Crypto_ai_tool/             # Archived old files
    └── old_docs/
```

## 🚨 Common Issues & Solutions

### Issue: "No module named 'aiohttp'"
**Solution**: This import was removed. Clear cache and restart:
```bash
rm -rf **/__pycache__
python run_orion_system.py
```

### Issue: Missing dependencies
**Solution**: Install all at once:
```bash
pip install pandas numpy requests flask flask-cors yfinance feedparser ollama chromadb
```

### Issue: Ollama not running
**Solution**: Start Ollama first:
```bash
ollama serve &
sleep 5
ollama pull mistral:7b
```

## 🎯 Quick Start Command

For a complete clean start:
```bash
# One command to rule them all
python fix_and_run.py
```

This will handle everything automatically!