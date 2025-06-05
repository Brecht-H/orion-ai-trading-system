# 🚀 ORION CURSOR RULES - UNIFIED V3.0
**Updated**: 2025-01-06 | **Status**: Production Ready | **Project**: ORION AI Trading System  
**Migration**: Orion_project (clean) + crypto-ai-tool (legacy reference)

---

## ⚠️ MANDATORY LEGACY CHECKS - ALWAYS FIRST

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
- **Cost Control**: Target <€15/month operational cost, preserve €100 API budget for strategic use
- **Legacy Intelligence**: ALWAYS check crypto-ai-tool directory for existing implementations

### **💰 Enhanced Budget-Efficient Operations**
- **Primary**: Local Ollama LLM processing (7 models available) + Mac Mini 2014 (Dilbert LLM)
- **Secondary**: Free APIs (CoinGecko, Reddit, Fear & Greed Index)  
- **Strategic**: Anthropic Claude (€50 credit) + Mistral + Codex (€50 credit), Together.AI API, HuggingFace Pro (€9/month)
- **Emergency**: Paid APIs only for critical failures or breakthrough analysis
- **Hardware**: Optimize for MacBook Air M2 8GB RAM + Mac Mini 2014 1TB storage

---

## 🤖 ENHANCED LLM ROLES & ORCHESTRATION SYSTEM

### **🏛️ Chief Architect (Claude-3 Sonnet - €50 Anthropic Credit)**
**Primary Role**: System design, architecture decisions, crisis management, active development assistance
- **Triggers**: `@architect`, structural changes, new components, crisis situations, active development
- **Responsibilities**:
  - Approve all structural changes to core system
  - Design interfaces between components  
  - Resolve conflicts between different implementations
  - Emergency project cleanup and optimization
  - Real-time development assistance and code review
- **Decision Authority**: Final say on project structure, dependencies, major refactoring
- **Availability**: Active in Cursor IDE for real-time assistance

### **💻 Lead Developer (GPT-4 - Cursor Code Pilot)**  
**Primary Role**: Code completion, feature implementation, code optimization
- **Triggers**: Code completion, `@dev`, feature implementation, code optimization
- **Responsibilities**:
  - Intelligent code completion and suggestions
  - Implement features according to architect specifications
  - Code quality and performance optimization
  - API integrations and data pipeline development
  - Trading strategy implementation
- **Constraints**: Must get architect approval for structural changes
- **Integration**: Built into Cursor IDE for seamless development

### **🧠 Advanced AI Processing (Mistral + Codex - €50 Credit)**
**Primary Role**: Complex reasoning, advanced code generation, specialized analysis
- **Available**: Mistral Large, Mistral 7B, Codex for advanced code generation
- **Budget**: €50 credit available for strategic use
- **Triggers**: `@mistral`, complex analysis, advanced code generation
- **Use Cases**: 
  - Complex trading algorithm development
  - Advanced mathematical modeling
  - Sophisticated code refactoring
  - Strategic decision analysis
- **Optimization**: Use for high-value tasks to preserve credit

### **🤗 Community AI (Hugging Face Pro - €9/month)**
**Primary Role**: Specialized models, fine-tuning, research access
- **Available**: Access to premium models, inference endpoints, AutoTrain
- **Triggers**: `@huggingface`, specialized model needs, fine-tuning
- **Use Cases**:
  - Custom model fine-tuning for crypto-specific tasks
  - Access to latest research models
  - Specialized NLP tasks (sentiment analysis, news processing)
  - Model experimentation and validation

### **⚡ High-Speed Processing (Together.AI)**
**Primary Role**: Fast inference, parallel processing, model experimentation
- **Triggers**: `@together`, fast processing needs, parallel analysis
- **Use Cases**:
  - High-frequency trading signal processing
  - Parallel market analysis across multiple timeframes
  - Fast model comparison and selection
  - Real-time sentiment analysis at scale

### **🔍 Quality Assurance (Local Ollama - 7 Models)**
**Primary Role**: Code review, testing, security validation, continuous monitoring
- **Available Models**: mistral:7b, codellama:13b, qwen2:7b, llama2:13b, deepseek-coder:6.7b, codellama:7b-code, phi3:mini
- **Triggers**: `@qa`, code review, security check, deployment validation
- **Responsibilities**:
  - Code review for bugs, security issues
  - Trading logic validation and risk calculations
  - Error handling and edge case testing
  - Deployment readiness assessment
- **Advantages**: No API costs, offline capability, 24/7 availability

### **🖥️ Local Production Server (Mac Mini 2014 - 1TB + Dilbert LLM)**
**Primary Role**: 24/7 autonomous operation, local processing, data storage
- **Hardware**: Mac Mini 2014, 1TB storage, Dilbert LLM available
- **Triggers**: Production deployment, 24/7 operation, local processing
- **Responsibilities**:
  - Autonomous 24/7 trading system operation
  - Local data storage and processing
  - Backup processing when MacBook Air is unavailable
  - Long-term data retention and analysis
- **Use Cases**: Production deployment, continuous operation, data archival

### **🛡️ Guardian System (Enhanced - Local Python + MCP)**
**Primary Role**: Autonomous project monitoring + legacy code detection + system oversight
- **Implementation**: Python-based MCP alternative with enhanced capabilities
- **Triggers**: `@guardian`, autonomous monitoring, project health checks
- **Responsibilities**:
  - Monitor both Orion_project AND crypto-ai-tool directories
  - Detect when new implementations duplicate existing functionality
  - Automated migration suggestions from legacy to clean structure
  - Cross-reference functionality gaps with existing solutions
  - Auto-generate user stories, epics, and milestones from project state
  - Database health monitoring and optimization recommendations
  - Cost analysis and resource allocation optimization
- **Enhanced Capabilities**:
  - Continuous scanning of crypto-ai-tool for reusable components
  - Smart detection of working implementations vs broken code
  - Migration priority recommendations based on functionality
  - Automated documentation of legacy component status
  - Continuous monitoring without manual intervention
- **Integration**: Direct database access, chat analysis, real-time insights

### **🐙 GitHub Integration Hub (MCP Server)**
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

---

## 🚫 STRICTLY FORBIDDEN

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

### **Resource Management:**
- ❌ API calls when local processing is sufficient
- ❌ Loading >3 Ollama models simultaneously (RAM limit)
- ❌ Creating files >1GB without cleanup strategy
- ❌ Infinite loops without circuit breakers
- ❌ Memory allocation >2GB without explicit approval

---

## 🚨 MANDATORY VALIDATION CHECKS

### **Before ANY Code Changes:**
```bash
# 1. Architecture Approval Required For:
- New dependencies or external services
- Database schema changes
- New API integrations
- Core component modifications
- File structure changes affecting >10 files

# 2. Developer Implementation Checklist:
- [ ] Unit tests written and passing
- [ ] Error handling implemented with graceful degradation
- [ ] Logging added with appropriate levels (DEBUG/INFO/WARN/ERROR)
- [ ] Resource usage validated (memory, API calls, disk space)
- [ ] Documentation updated (docstrings, README, API docs)

# 3. QA Security & Trading Validation:
- [ ] Input validation (amounts, addresses, API keys)
- [ ] Rate limiting implemented for all external APIs
- [ ] Fallback strategies for API failures
- [ ] Dry-run mode available for all trading operations
- [ ] Risk limits and circuit breakers functional
```

### **Critical Trading/Crypto Validations:**
```python
# Required validation patterns:
def validate_trading_operation(operation):
    assert operation.amount > 0, "Amount must be positive"
    assert operation.dry_run == True, "Always start with dry-run"
    assert operation.stop_loss_set == True, "Stop loss required"
    assert operation.risk_percent <= 2.0, "Max 2% risk per trade"
    
# API security patterns:
def secure_api_call(endpoint, params):
    assert "api_key" not in params, "No API keys in logs"
    assert rate_limit_check(endpoint), "Rate limit exceeded"
    return call_with_retry(endpoint, params, max_retries=3)
```

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

### **STEP 2: MCP Integration Testing**
```bash
# Test current MCP capabilities
python core_orchestration/guardian_system/guardian_dashboard_pipeline.py
python notion_integration_hub/sync/real_time_sync.py
python research_center/collectors/free_sources_collector.py
```

---

## 📁 UNIFIED PROJECT STRUCTURE

```
/Orion_project/                         # New clean structure
├── 📋 ORION_PROJECT_MASTER.md          # Single source of truth
├── 📋 ORION_CURSOR_RULES_UNIFIED.md    # This unified rules file
├── 🔬 research_center/                 # Market data & analysis ✅
├── 📚 knowledge_center/                # AI learning system ✅  
├── 📈 strategy_center/                 # Trading strategies ✅
├── 📊 technical_analysis_center/       # TA indicators ✅
├── 🛡️ risk_management_center/          # Risk controls ✅
├── 📱 notion_integration_hub/          # Executive dashboard ✅
├── 🧠 core_orchestration/              # Central coordination ✅
├── 💾 databases/                       # All data storage ✅
├── ⚙️ config/                          # Configuration files ✅
├── 🧪 tests/                           # Test framework ✅
├── 📚 documentation/                   # Project docs ✅
└── 🔗 mcp/                            # MCP server implementations 🚧

/crypto-ai-tool/                        # Legacy reference (read-only)
├── [51K+ files - reference only]       # DO NOT MODIFY
└── [Use for component discovery]       # Migration source
```

---

## 🎮 ENHANCED WORKFLOW

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

### **Emergency Procedures:**
```
🚨 CRITICAL ERROR DETECTED:
1. Immediate: Stop all trading operations
2. @architect: Assess situation and approve emergency fix
3. @dev: Implement fix with @qa validation
4. Resume operations only after full system validation
```

---

## 🔗 MCP INTEGRATION ROADMAP

### **Phase 1: Current Working (Guardian MCP)**
- ✅ Python-based Guardian system operational
- ✅ Database monitoring across both directories
- ✅ Autonomous health checks and gap analysis

### **Phase 2: GitHub MCP Implementation**
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

## 💰 COMPREHENSIVE RESOURCE MANAGEMENT

### **Updated Monthly Budget Breakdown:**
```
Monthly Operating Cost: €9-15 maximum
├── Hugging Face Pro: €9/month (specialized models, fine-tuning)
├── Local Processing: €0 (Ollama + Mac Mini Dilbert LLM)
├── Free APIs: €0 (CoinGecko, Reddit, Fear & Greed)
├── Optional Notion: €0-5/month (graceful offline fallback available)
└── Reserved Credits: €50 Anthropic + €50 Mistral + Together.AI (strategic use only)
```

### **LLM Resource Optimization Strategy:**
```python
# Resource selection hierarchy
def select_optimal_llm(task_type, complexity, budget_impact):
    """Smart LLM selection based on task requirements"""
    
    # Local first (no cost)
    if task_type in ['code_review', 'basic_analysis', '24_7_monitoring']:
        return ollama_models['mistral:7b']  # or dilbert_llm on Mac Mini
    
    # HuggingFace for specialized tasks (fixed monthly cost)
    elif task_type in ['sentiment_analysis', 'custom_models', 'research']:
        return huggingface_endpoints['specialized_model']
    
    # Together.AI for speed-critical tasks
    elif task_type in ['real_time_trading', 'high_frequency']:
        return together_ai['fast_inference']
    
    # Claude for architecture and complex reasoning (preserve credit)
    elif complexity == 'high' and task_type in ['architecture', 'strategic_decisions']:
        return anthropic_claude['sonnet_3_5']
    
    # Mistral credits for complex analysis (preserve budget)
    elif complexity == 'high' and budget_impact == 'strategic':
        return mistral_api['large_model']
    
    # Fallback to local processing
    else:
        return ollama_models['codellama:13b']
```

---

## 📈 SUCCESS METRICS & KPIs

### **Technical Performance:**
- ✅ System uptime >99% (target: 24/7 on Mac Mini)
- ✅ API response time <5 seconds (local LLM processing)
- ✅ Memory usage <6GB (stay within 8GB limit)
- ✅ Daily API costs <€0.50 (preserve credit budgets)

### **Trading Performance:**
- ✅ Signal generation every 15 minutes
- ✅ Risk per trade ≤2% of portfolio
- ✅ Monthly ROI >0% (profit target)
- ✅ Maximum drawdown <10%

### **Development Velocity:**
- ✅ All commits pass mandatory checks
- ✅ Test coverage >80% for trading components
- ✅ Documentation updated within 24 hours of changes
- ✅ Emergency response time <30 minutes

---

## 🎯 CURRENT PROJECT PRIORITIES

### **Phase 1: MCP Integration & Validation** (Current Week)
1. ✅ Verify all external LLM access (Anthropic, Mistral, HuggingFace, Together.AI)
2. ✅ Validate Notion dashboard functionality 
3. ✅ Test database connectivity and health
4. 🚧 Complete MCP server configuration for Cursor integration
5. 🚧 Validate end-to-end data flow from collection to decision

### **Phase 2: Enhancement & Optimization** (Next 2 weeks)
1. Complete GitHub MCP server implementation
2. Enhance Guardian system with legacy detection
3. Optimize LLM orchestration for cost efficiency
4. Performance tuning and monitoring improvements

### **Phase 3: Production Scaling** (Month 2+)
1. Deploy to Mac Mini for 24/7 operation
2. Advanced portfolio management features
3. Integration with additional exchanges
4. Mobile app development for remote monitoring

---

**🎯 UNIFIED MISSION**: Build the world's most advanced crypto AI trading system by intelligently combining enterprise-grade new architecture with battle-tested legacy implementations, achieving maximum functionality at minimum cost through smart migration and multi-LLM orchestration with enhanced budget management.

**🏆 COMPETITIVE ADVANTAGE**: Unique hybrid approach preserving 51K+ files of working implementations while building clean, scalable, enterprise-ready architecture - combining the best of both worlds with optimized AI resource allocation and comprehensive MCP integration. 