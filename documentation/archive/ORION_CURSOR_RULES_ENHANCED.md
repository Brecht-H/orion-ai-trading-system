# 🚀 ORION CURSOR RULES - ENHANCED V2.1
**Updated**: 2025-06-04 | **Status**: Production Ready | **Project**: ORION AI Trading System
**Migration**: Orion_project (clean) + crypto-ai-tool (legacy reference)

---

## ⚠️ MANDATORY LEGACY CHECKS - MOST IMPORTANT

### **🚨 BEFORE ANY NEW IMPLEMENTATION:**
```bash
# CRITICAL: Always check crypto-ai-tool first!
# Step 1: Search for existing functionality
find ../crypto-ai-tool -name "*.py" -exec grep -l "your_functionality" {} \;

# Step 2: Check all major directories  
ls -la ../crypto-ai-tool/orion_core/*/
ls -la ../crypto-ai-tool/src/*/
ls -la ../crypto-ai-tool/core/*/
ls -la ../crypto-ai-tool/knowledge_center/*/
ls -la ../crypto-ai-tool/research_center/*/

# Step 3: Check for working implementations
find ../crypto-ai-tool -name "*your_feature*" -type f
grep -r "class YourFeature" ../crypto-ai-tool/

# Step 4: Verify databases and configurations
ls ../crypto-ai-tool/data/
ls ../crypto-ai-tool/*.env*
ls ../crypto-ai-tool/*.db
```

### **Legacy Migration Protocol:**
1. **Discovery**: Search crypto-ai-tool for existing code
2. **Assessment**: Evaluate functionality and test status  
3. **Migration**: Copy working components to Orion_project
4. **Integration**: Adapt to new clean structure
5. **Testing**: Validate functionality in new environment
6. **Documentation**: Update with migration notes

---

## 🎯 CORE PRINCIPLES

### **🏗️ Architecture-First Development**
- **Single Source of Truth**: All decisions documented in `ORION_PROJECT_MASTER.md`
- **Modular Design**: Every component must be standalone, testable, and replaceable
- **Resource Efficiency**: Local-first processing, API calls only when necessary
- **Cost Control**: Target <€15/month operational cost, preserve €50 API budget for strategic use
- **Legacy Intelligence**: ALWAYS check crypto-ai-tool directory for existing implementations

### **💰 Budget-Efficient Operations**
- **Primary**: Local Ollama LLM processing (7 models available) + Mac Mini 2014 (Dilbert LLM)
- **Secondary**: Free APIs (CoinGecko, Reddit, Fear & Greed Index)  
- **Strategic**: Mistral + Codex (€50 credit), Together.AI API, HuggingFace Pro (€9/month)
- **Emergency**: Paid APIs only for critical failures or breakthrough analysis
- **Hardware**: Optimize for MacBook Air M2 8GB RAM + Mac Mini 2014 1TB storage

---

## 🤖 ENHANCED LLM ROLES & ORCHESTRATION SYSTEM

### **🐙 GitHub Integration Hub (New MCP Server)**
**Primary Role**: Version control, project management, automated workflows
- **Implementation**: MCP server for GitHub API integration  
- **Triggers**: `@github`, code management, CI/CD, project tracking
- **Responsibilities**:
  - Automated commit analysis and code quality checks
  - Issue creation from Guardian system insights
  - Pull request management and code review automation
  - Release management and deployment coordination
  - Project board synchronization with development status
- **Advanced Features**:
  - Auto-generate GitHub issues from gap analysis
  - Intelligent branch management for feature development
  - Code quality metrics and technical debt tracking
  - Automated changelog generation from commits
  - Repository cleanup and organization
- **Integration**: Direct GitHub API access, webhook handling, automated workflows

### **🛡️ Guardian System (Enhanced - Local Python)**
**Primary Role**: Autonomous project monitoring + legacy code detection
- **Enhanced Capabilities**:
  - Monitor both Orion_project AND crypto-ai-tool directories
  - Detect when new implementations duplicate existing functionality
  - Automated migration suggestions from legacy to clean structure
  - Cross-reference functionality gaps with existing solutions
- **Legacy Intelligence**:
  - Continuous scanning of crypto-ai-tool for reusable components
  - Smart detection of working implementations vs broken code
  - Migration priority recommendations based on functionality
  - Automated documentation of legacy component status

---

## 🚫 ENHANCED STRICTLY FORBIDDEN

### **Migration & Development Rules:**
- ❌ **Implementing new functionality without checking crypto-ai-tool first**
- ❌ **Ignoring existing working implementations in legacy directory**
- ❌ **Reinventing functionality that exists and works in old structure**
- ❌ **Missing critical components during development without legacy check**
- ❌ **Creating duplicate code when migration is the better option**

### **Code Practices:**
- ❌ Direct database queries in UI components
- ❌ Hardcoded API keys, secrets, or private keys
- ❌ Trading operations without dry-run validation
- ❌ Breaking changes without @architect approval
- ❌ Creating duplicate implementations of existing functionality
- ❌ Adding files outside the approved structure without approval

---

## 🔧 ENHANCED IMPLEMENTATION COMMANDS

### **STEP 0: MANDATORY LEGACY CHECK**
```bash
# 🚨 ALWAYS RUN FIRST - Check for existing implementations
echo "Checking crypto-ai-tool for existing functionality..."
find ../crypto-ai-tool -name "*.py" -exec grep -l "your_feature_keyword" {} \;
ls ../crypto-ai-tool/*/your_module_area/
grep -r "def your_function" ../crypto-ai-tool/
```

### **STEP 1: Project Development**
```bash
# Only after legacy check is complete:
git checkout -b feature/new-component  
curl -s http://localhost:11434/api/tags | jq '.models'  # Verify Ollama models
python -m pytest tests/ -v  # Run full test suite
```

### **STEP 2: GitHub Integration (Proposed)**
```bash
# Setup GitHub MCP integration
npm install -g @anthropic/mcp-sdk
node mcp/github-server.js --init
gh auth login  # GitHub CLI authentication
```

---

## 📁 ORION PROJECT STRUCTURE (Clean Migration)

```
/Orion_project/                         # New clean structure
├── 📋 ORION_PROJECT_MASTER.md          # Single source of truth
├── 📋 CURSOR_RULES_AI_TRADING_PLATFORM_V2.md  # This file
├── 🔬 research_center/                 # Migrated from crypto-ai-tool
├── 📚 knowledge_center/                # Migrated from crypto-ai-tool  
├── 📈 strategy_center/                 # Migrated from crypto-ai-tool
├── 📊 technical_analysis_center/       # Migrated from crypto-ai-tool
├── 🛡️ risk_management_center/          # Migrated from crypto-ai-tool
├── 📱 notion_integration_hub/          # Migrated from crypto-ai-tool
├── 🧠 core_orchestration/              # Central coordination
├── 💾 databases/                       # All data storage
├── ⚙️ config/                          # Configuration files
├── 🧪 tests/                           # Test framework
├── 📚 documentation/                   # Project docs
└── 🔗 mcp/                            # MCP server implementations

/crypto-ai-tool/                        # Legacy reference (read-only)
├── [51K+ files - reference only]       # DO NOT MODIFY
└── [Use for component discovery]       # Migration source
```

---

## 🎮 WORKFLOW ENHANCEMENTS

### **Daily Operations with Legacy Intelligence:**
1. **Morning Briefing** (9:00 AM): @guardian scans both directories for changes
2. **Legacy Check** (Every 2 hours): Compare implementations between directories  
3. **Migration Opportunities**: Identify valuable components for migration
4. **System Health** (Every 4 hours): Validate all centers in clean structure

### **Enhanced Feature Development:**
```
1. @guardian: Check crypto-ai-tool for existing implementations
2. @architect: Design migration strategy or new implementation
3. @github: Create issue and branch for development
4. @dev: Implement with legacy intelligence
5. @qa: Validate against both old and new structures
6. @github: Automated testing and deployment
```

---

## 🔗 MCP INTEGRATION ROADMAP

### **Phase 1: Current Working (Guardian MCP)**
- ✅ Python-based Guardian system operational
- ✅ Database monitoring across both directories
- ✅ Autonomous health checks and gap analysis

### **Phase 2: Proposed GitHub MCP**
```javascript
// .cursor/mcp-config.json
{
  "mcpServers": {
    "guardian": {
      "command": "python",
      "args": ["./core_orchestration/guardian_system/mcp_server.py"],
      "env": {
        "ORION_ROOT": "/Users/allaerthartjes/Orion_project",
        "LEGACY_ROOT": "/Users/allaerthartjes/crypto-ai-tool"
      }
    },
    "github": {
      "command": "node", 
      "args": ["./mcp/github-server.js"],
      "env": {
        "GITHUB_TOKEN": "${Github_token}",
        "REPO_OWNER": "Brecht-H",
        "REPO_NAME": "crypto-ai-tool"
      }
    }
  }
}
```

### **Phase 3: Advanced Integration**
- Notion MCP for mobile dashboard
- Trading data MCP for real-time market integration
- Ollama MCP for local LLM orchestration

---

**🎯 ENHANCED MISSION**: Build the world's most advanced crypto AI trading system by intelligently combining enterprise-grade new architecture with battle-tested legacy implementations, achieving maximum functionality at minimum cost through smart migration and multi-LLM orchestration.

**🏆 COMPETITIVE ADVANTAGE**: Unique hybrid approach preserving 51K+ files of working implementations while building clean, scalable, enterprise-ready architecture - combining the best of both worlds. 