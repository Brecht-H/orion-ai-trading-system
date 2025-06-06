# 🎯 COPILOT CONTEXT - READ THIS FIRST

## 🚨 CRITICAL RULES FOR COPILOT

### NEVER DO THESE:
1. ❌ Create duplicate files with similar names
2. ❌ Move existing functionality to new files
3. ❌ Create new folders without explicit request
4. ❌ Modify core architecture files
5. ❌ Add test files randomly
6. ❌ Create "example" or "demo" files

### ALWAYS DO THESE:
1. ✅ Check if functionality already exists before creating
2. ✅ Modify existing files instead of creating new ones
3. ✅ Maintain current folder structure
4. ✅ Ask for clarification if unsure
5. ✅ Show file path before making changes

---

## 📁 PROJECT STRUCTURE - DO NOT CHANGE

```
/workspace/
├── research_center/          # Data collection & analysis
├── knowledge_center/         # Knowledge synthesis & storage
├── strategy_center/          # Strategy generation & backtesting
├── trading_execution_center/ # Order execution ONLY
├── risk_management_center/   # Risk controls
├── core_orchestration/       # LLM routing & coordination
├── databases/sqlite_dbs/     # All databases here
└── tests/                    # All tests here
```

---

## 🧠 CURRENT FOCUS

**PHASE**: Intelligence Layer Implementation
**MODULE**: Research Center
**TASK**: Add LLM intelligence to data collection
**DO NOT**: Work on trading execution yet

---

## 📝 WHEN ASKED TO CREATE FUNCTIONALITY

1. First response should be: "Let me check if this already exists..."
2. Search for similar files/functions
3. If exists: Modify it
4. If not: Ask where to create it
5. Show proposed file structure before creating

---

## 🔄 CONTEXT REMINDERS

- We're building INTELLIGENCE first, trading last
- Use LOCAL LLMs (mistral:7b) for 80% of tasks
- Every component must LEARN from its actions
- Cost optimization is critical ($34/month target)
- System must be self-improving

---

## ⚠️ IF YOU'RE ABOUT TO...

**Create a new file**: STOP! Check if it exists first
**Add a test**: Put it in `/tests/` only
**Add a strategy**: Modify existing strategy files
**Add trading logic**: DON'T - we're not there yet
**Restructure folders**: DON'T - ever

---

## 🎯 CURRENT FILE BEING WORKED ON

**File**: `research_center/llm_analyzer.py`
**Purpose**: Add intelligence to research data collection
**Status**: In progress
**Next**: `knowledge_center/llm_synthesis.py`