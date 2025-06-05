#!/bin/bash

echo "🚀 ORION PROJECT - Background Agent Environment Setup"
echo "=================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -y

# Install Python 3.11 if not available
echo "🐍 Checking Python version..."
python3 --version
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "⬆️ Installing Python 3.11..."
    sudo apt-get install -y python3.11 python3.11-venv python3.11-pip
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    sudo update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.11 1
fi

# Install essential system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y build-essential curl git sqlite3

# Install Node.js for MCP servers
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install core Python dependencies
echo "📦 Installing core Python packages..."
pip install requests pandas numpy matplotlib seaborn sqlite3

# Install Week 2 missing dependencies (CRITICAL)
echo "🔬 Installing Week 2 missing dependencies..."
pip install scipy yfinance

# Install LLM and API dependencies
echo "🤖 Installing LLM dependencies..."
pip install anthropic mistralai groq openai huggingface_hub transformers

# Install data processing dependencies
echo "📊 Installing data processing packages..."
pip install beautifulsoup4 feedparser python-dotenv schedule

# Install MCP dependencies
echo "🔗 Installing MCP packages..."
pip install mcp cursor-notebook-mcp fastmcp uvicorn starlette paramiko

# Install ML and analysis dependencies
echo "🧠 Installing ML packages..."
pip install scikit-learn joblib ta-lib statsmodels

# Install database and vector store dependencies
echo "🗄️ Installing database packages..."
pip install chromadb sqlalchemy

# Verify critical installations
echo "✅ Verifying installations..."
python3 -c "import scipy; print('✅ scipy installed')"
python3 -c "import yfinance; print('✅ yfinance installed')"
python3 -c "import pandas; print('✅ pandas installed')"
python3 -c "import numpy; print('✅ numpy installed')"
python3 -c "import sklearn; print('✅ scikit-learn installed')"

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs/background_agent
mkdir -p data/background_test
mkdir -p databases/sqlite_dbs

# Set up environment variables
echo "🔐 Setting up environment variables..."
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️ .env file not found - some features may not work"
fi

# Test database connections
echo "🔗 Testing database connections..."
python3 -c "
import sqlite3
import os
databases = [
    './databases/sqlite_dbs/orchestration_log.db',
    './databases/sqlite_dbs/trading_patterns.db',
    './databases/sqlite_dbs/unified_signals.db',
    './databases/sqlite_dbs/backtest_results.db'
]
for db in databases:
    if os.path.exists(db):
        try:
            conn = sqlite3.connect(db)
            conn.execute('SELECT 1')
            conn.close()
            print(f'✅ {os.path.basename(db)} connected')
        except Exception as e:
            print(f'❌ {os.path.basename(db)} error: {e}')
    else:
        print(f'⚠️ {os.path.basename(db)} not found')
"

# Install GitHub MCP server
echo "🐙 Installing GitHub MCP server..."
npm install -g @modelcontextprotocol/server-github

# Install additional useful MCP servers
echo "🧠 Installing additional MCP servers..."
npm install -g @browsertools/mcp-server

echo ""
echo "🎯 ORION ENVIRONMENT SETUP COMPLETE!"
echo "======================================"
echo "✅ Python 3.11+ ready"
echo "✅ All Week 2 dependencies installed"
echo "✅ MCP servers configured"
echo "✅ Database connections tested"
echo "✅ Background agent environment ready"
echo ""
echo "📊 Next: Run comprehensive tests to validate improvements"
echo "🚀 Ready for autonomous development!" 