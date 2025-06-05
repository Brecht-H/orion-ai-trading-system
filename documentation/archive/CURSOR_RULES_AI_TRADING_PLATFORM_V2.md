# 🚀 CURSOR RULES - AI CRYPTO TRADING PLATFORM V2.0
**Updated**: 2025-01-06 | **Status**: Production Ready | **Project**: ORION AI Trading System

---

## 🎯 CORE PRINCIPLES

### **🏗️ Architecture-First Development**
- **Single Source of Truth**: All decisions documented in `ORION_PROJECT_MASTER.md`
- **Modular Design**: Every component must be standalone, testable, and replaceable
- **Resource Efficiency**: Local-first processing, API calls only when necessary
- **Cost Control**: Target <€15/month operational cost, preserve €50 API budget for strategic use

### **💰 Budget-Efficient Operations**
- **Primary**: Local Ollama LLM processing (7 models available) + Mac Mini 2014 (Dilbert LLM)
- **Secondary**: Free APIs (CoinGecko, Reddit, Fear & Greed Index)  
- **Strategic**: Mistral + Codex (€50 credit), Together.AI API, HuggingFace Pro (€9/month)
- **Emergency**: Paid APIs only for critical failures or breakthrough analysis
- **Hardware**: Optimize for MacBook Air M2 8GB RAM + Mac Mini 2014 1TB storage

---

## 🤖 LLM ROLES & ORCHESTRATION SYSTEM

### **🏛️ Chief Architect (Claude-3 Sonnet - Cursor Assistant €50 Credit)**
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

### **📊 Market Analyst (Gemini Pro)**
**Primary Role**: Market analysis, trading signals, research
- **Triggers**: `@market`, trading decisions, market analysis
- **Responsibilities**:
  - Real-time market analysis and signal generation
  - Research report generation and trend analysis
  - Portfolio optimization recommendations
  - Risk assessment for trading strategies

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

### **🛡️ Guardian System (Local Python - Autonomous Oversight)**
**Primary Role**: Autonomous project monitoring, requirement tracking, system health oversight
- **Implementation**: Python-based MCP alternative (when Node.js unavailable)
- **Triggers**: `@guardian`, autonomous monitoring, project health checks
- **Responsibilities**:
  - Autonomous project health analysis across all systems
  - Auto-generate user stories, epics, and milestones from project state
  - Monitor functionality gaps and incomplete implementations
  - Track chat history for unmet requirements and forgotten tasks
  - Database health monitoring and optimization recommendations
  - Cost analysis and resource allocation optimization
  - Pipeline recommendations and automated routing decisions
  - Generate dashboard insights and actionable alerts
- **Autonomous Features**:
  - Continuous monitoring without manual intervention
  - Smart detection of pending requirements from conversations
  - Automated user story generation based on project gaps
  - Proactive cost optimization recommendations
  - Health alerts and recovery suggestions
- **Integration**: Direct database access, chat analysis, real-time insights

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

## 📁 ENFORCED PROJECT STRUCTURE

```
/orion-ai-trading/
├── 📋 ORION_PROJECT_MASTER.md          # Single source of truth
├── 🚀 src/
│   ├── 🧠 core/                        # Core business logic
│   │   ├── mvp_orchestrator.py         # Main autonomous coordinator
│   │   ├── data_collector.py           # Free data source collection
│   │   └── signal_generator.py         # Trading signal generation
│   ├── 🔗 integrations/                # External API connections
│   │   ├── ollama_client.py            # Local LLM interface
│   │   ├── notion_client.py            # Dashboard integration
│   │   └── exchange_apis.py            # Trading platform APIs
│   ├── 📊 services/                    # Business services
│   │   ├── market_analysis.py          # Market data processing
│   │   ├── risk_management.py          # Risk calculation & limits
│   │   └── portfolio_manager.py        # Portfolio optimization
│   └── 🛠️ utils/                       # Helper functions
├── 🧪 tests/                           # Comprehensive test suite
├── 📚 docs/                            # Documentation only
├── 💾 data/                            # Local data storage
└── 🗄️ archive/                         # Legacy/backup code (read-only)
```

---

## 🚫 STRICTLY FORBIDDEN

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

### **Project Management:**
- ❌ Multiple competing implementations of same feature
- ❌ Documentation that contradicts ORION_PROJECT_MASTER.md
- ❌ Backup files in main project directory
- ❌ Code commits without passing all mandatory checks

---

## 💡 OPTIMIZATION STRATEGIES

### **Performance & Cost:**
```python
# 1. Caching Strategy
@lru_cache(maxsize=128, ttl=300)  # 5-minute cache
def get_market_data(symbol: str):
    """Cache expensive API calls"""
    
# 2. Local-First Processing
def analyze_sentiment(text: str):
    """Use Ollama before falling back to paid APIs"""
    try:
        return ollama_client.analyze(text)
    except Exception:
        return fallback_to_paid_api(text)  # Only if critical
        
# 3. Resource Management
async def process_with_limits():
    """Respect system constraints"""
    if memory_usage() > 0.8:  # 80% of 8GB
        await cleanup_cache()
    if api_calls_today > daily_limit * 0.9:
        switch_to_local_processing()
```

### **Error Handling Patterns:**
```python
# Graceful degradation pattern
async def robust_operation():
    try:
        return await primary_method()
    except ExternalAPIError:
        logger.warning("External API failed, using local backup")
        return await local_backup_method()
    except CriticalError as e:
        logger.error(f"Critical failure: {e}")
        await emergency_shutdown()
        raise
```

---

## 🎛️ WORKFLOW & COLLABORATION

### **Daily Operations:**
1. **Morning Briefing** (9:00 AM): @market generates market overview
2. **System Health Check** (Every 4 hours): @qa validates all systems
3. **Performance Review** (6:00 PM): @dev analyzes day's performance
4. **Architecture Review** (Weekly): @architect reviews system health

### **Feature Development Workflow:**
```
1. @architect: Design & approve feature architecture
2. @dev: Implement according to specifications  
3. @qa: Validate implementation & security
4. @market: Test market data integration (if applicable)
5. Deploy to production after all validations pass
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

## 📈 SUCCESS METRICS & KPIs

### **Technical Performance:**
- ✅ System uptime >99% (target: 24/7 on Mac Mini)
- ✅ API response time <5 seconds (local LLM processing)
- ✅ Memory usage <6GB (stay within 8GB limit)
- ✅ Daily API costs <€0.50 (preserve €50 budget)

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

## 🔧 IMPLEMENTATION COMMANDS

### **Project Initialization:**
```bash
# Setup new feature branch
git checkout -b feature/new-component
curl -s http://localhost:11434/api/tags | jq '.models'  # Verify Ollama models
python -m pytest tests/ -v  # Run full test suite
```

### **Pre-Commit Validation:**
```bash
# Mandatory checks before any commit
python -m pytest tests/ --cov=src --cov-report=term-missing
python -m flake8 src/ --max-line-length=100
python scripts/security_audit.py
python scripts/resource_usage_check.py
```

### **Emergency Cleanup:**
```bash
# When project gets cluttered (use sparingly)
python scripts/emergency_cleanup.py --dry-run
python scripts/deduplicate_files.py --archive-old
git clean -fd  # Remove untracked files
```

---

## 🎯 CURRENT PROJECT PRIORITIES

### **Phase 1: Cleanup & Stabilization** (Week 1)
1. Execute emergency cleanup of 51K+ files
2. Validate MVP components actually work
3. Test end-to-end autonomous operation
4. Deploy to Mac Mini for 24/7 operation

### **Phase 2: Optimization** (Week 2-3)
1. Optimize local LLM usage patterns
2. Implement advanced trading strategies
3. Enhance Notion dashboard integration
4. Performance tuning and cost optimization

### **Phase 3: Scaling** (Month 2+)
1. Advanced multi-LLM orchestration
2. Integration with additional exchanges
3. Advanced portfolio management features
4. Mobile app development

---

## 🔗 MCP (Model Context Protocol) INTEGRATION

### **Enhanced Integration Options:**

#### **Option 1: Node.js MCP Servers (Full Integration)**
```json
// .cursor/mcp-config.json
{
  "mcpServers": {
    "notion": {
      "command": "node",
      "args": ["./mcp/notion-server.js"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}",
        "NOTION_DATABASE_ID": "${NOTION_DATABASE_ID}"
      }
    },
    "ollama": {
      "command": "node", 
      "args": ["./mcp/ollama-server.js"],
      "env": {
        "OLLAMA_HOST": "http://localhost:11434"
      }
    },
    "guardian": {
      "command": "node",
      "args": ["./mcp/guardian-server.js"],
      "env": {
        "DATABASE_PATHS": "./data"
      }
    },
    "trading-data": {
      "command": "node",
      "args": ["./mcp/trading-server.js"],
      "env": {
        "DATABASE_PATH": "./data/trading_data.db"
      }
    }
  }
}
```

#### **Option 2: Python Guardian MCP (Current Working Implementation)**
```python
# Direct Python integration (working now)
from setup_mcp_without_node import GuardianMCP

guardian = GuardianMCP()

# Available functions:
guardian.analyze_project_health('all')
guardian.generate_user_stories('technical_debt', 'high') 
guardian.database_health_check('all')
guardian.cost_optimization_analysis('all')
guardian.generate_dashboard_insights('pending_actions')
guardian.track_chat_requirements(chat_content)
```

### **Database MCP Integration Opportunities:**
Your project has **9+ databases** that benefit from MCP access:

1. **`orion_project_management.db`** (76KB) - ✅ Guardian monitoring
2. **`free_sources_data.db`** (44KB) - ✅ Working, 3 tables
3. **`sandbox_trading.db`** (24KB) - ✅ Working, 4 tables  
4. **`discovered_patterns.db`** (24KB) - ✅ Working, 4 tables
5. **`unified_data.db`** (20KB) - ✅ Working, 4 tables
6. **`notion_backup.db`** (16KB) - ✅ Working, 3 tables
7. **Notion databases** - auto_execution, llm_agents, morning_briefing, system_monitor
8. **Trading databases** - orion_coordination.db, trading_data.db
9. **Integration databases** - orion_integration_bridge.db

### **Advanced Cursor Functionality Benefits:**

#### **1. Enhanced Code Completion Context:**
- **Database schemas** directly accessible for accurate code completion
- **Real-time project state** awareness for contextual suggestions
- **Cost optimization** hints during API call implementations
- **Pattern recognition** from discovered_patterns.db for better suggestions

#### **2. Intelligent Error Detection:**
- **Database inconsistencies** detected during coding
- **Resource usage warnings** when approaching limits
- **Architecture violation** alerts based on Guardian analysis
- **Missing dependency** detection from project health monitoring

#### **3. Autonomous Development Assistant:**
- **Auto-generated tasks** from functionality gap analysis
- **Proactive refactoring** suggestions from code duplication detection
- **Cost optimization** recommendations during development
- **Real-time health monitoring** during active development

#### **4. Context-Aware Documentation:**
- **Auto-updated documentation** based on code changes
- **Real-time API documentation** from database schemas
- **Interactive tutorials** based on current project needs
- **Contextual help** from Guardian system insights

**🎯 Remember: This project has incredible potential. Following these rules ensures we build it correctly, efficiently, and profitably while staying within resource constraints.** 

## 💰 COMPREHENSIVE RESOURCE MANAGEMENT

### **Current Monthly Budget Breakdown:**
```
Monthly Operating Cost: €9-15 maximum
├── Hugging Face Pro: €9/month (specialized models, fine-tuning)
├── Local Processing: €0 (Ollama + Mac Mini Dilbert LLM)
├── Free APIs: €0 (CoinGecko, Reddit, Fear & Greed)
├── Optional Notion: €0-5/month (graceful offline fallback available)
└── Reserved Credits: €50 Mistral + Together.AI (strategic use only)
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
    
    # Mistral credits for complex strategic analysis (preserve budget)
    elif complexity == 'high' and budget_impact == 'strategic':
        return mistral_api['large_model']
    
    # Fallback to local processing
    else:
        return ollama_models['codellama:13b']
``` 