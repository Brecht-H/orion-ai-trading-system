#!/usr/bin/env python3
"""
Quick test to verify system components
"""

import sys
import os

print("🧪 ORION SYSTEM TEST")
print("=" * 50)

# Check Python version
print(f"✅ Python version: {sys.version}")

# Check working directory
print(f"✅ Working directory: {os.getcwd()}")

# Try imports
modules_to_test = [
    ('pandas', 'Data processing'),
    ('numpy', 'Numerical computing'),
    ('requests', 'HTTP requests'),
    ('flask', 'Web dashboard'),
    ('sqlite3', 'Database'),
    ('asyncio', 'Async operations')
]

print("\n📦 Checking modules:")
for module_name, description in modules_to_test:
    try:
        __import__(module_name)
        print(f"  ✅ {module_name} - {description}")
    except ImportError:
        print(f"  ❌ {module_name} - {description}")

# Check for critical files
print("\n📁 Checking critical files:")
critical_files = [
    'run_orion_system.py',
    'research_center/llm_analyzer.py',
    'knowledge_center/llm_synthesis.py',
    'dashboard/learning_dashboard.py',
    'COPILOT_CONTEXT.md'
]

for file_path in critical_files:
    if os.path.exists(file_path):
        print(f"  ✅ {file_path}")
    else:
        print(f"  ❌ {file_path}")

# Check Ollama
print("\n🤖 Checking Ollama:")
ollama_check = os.system("curl -s http://localhost:11434/api/tags > /dev/null 2>&1")
if ollama_check == 0:
    print("  ✅ Ollama is running")
else:
    print("  ❌ Ollama is NOT running (start with: ollama serve)")

print("\n✅ Test complete!")
print("\nTo run the full system:")
print("  python run_orion_system.py")