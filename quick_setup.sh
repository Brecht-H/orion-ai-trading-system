#!/bin/bash
# ORION QUICK SETUP SCRIPT

echo "🚀 ORION QUICK SETUP"
echo "===================="

# Install Python packages
echo "📦 Installing Python packages..."
python -m pip install pandas numpy requests flask flask-cors yfinance feedparser ollama chromadb matplotlib seaborn scipy --break-system-packages

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "🤖 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Start Ollama in background
echo "🤖 Starting Ollama..."
ollama serve &
OLLAMA_PID=$!
sleep 5

# Pull Mistral model
echo "📥 Downloading Mistral AI model..."
ollama pull mistral:7b

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the system:"
echo "  python run_orion_system.py"
echo ""
echo "To run the dashboard:"
echo "  python dashboard/learning_dashboard.py"
echo ""
echo "Ollama is running with PID: $OLLAMA_PID"