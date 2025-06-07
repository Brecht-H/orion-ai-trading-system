#!/bin/bash
# Run Orion with the correct Python environment

echo "🚀 Starting Orion System..."
echo "Using Python: /usr/bin/python3"

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🤖 Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Run the system
/usr/bin/python3 run_orion_system.py
