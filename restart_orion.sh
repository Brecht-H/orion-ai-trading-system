#!/bin/bash
# Restart Orion System cleanly

echo "🔄 Restarting Orion System..."

# Kill any existing processes
echo "🛑 Stopping existing processes..."
pkill -f "run_orion_system.py" 2>/dev/null
pkill -f "learning_dashboard.py" 2>/dev/null
sleep 2

# Clear Python cache
echo "🧹 Clearing cache..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Ensure Ollama is running
echo "🤖 Checking Ollama..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "  Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Start the system
echo "🚀 Starting Orion..."
/usr/bin/python3 run_orion_system.py &

echo ""
echo "✅ Orion System restarted!"
echo ""
echo "📊 To monitor: tail -f logs/background_agent/agent.log"
echo "🌐 Dashboard will be at: http://localhost:5002"