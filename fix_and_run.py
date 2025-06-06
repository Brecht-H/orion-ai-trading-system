#!/usr/bin/env python3
"""Fix aiohttp issue and run the system"""

import subprocess
import sys
import os

print("🔧 Fixing Orion System Issues...")

# 1. Check if aiohttp is in the file
print("\n📋 Checking research_center/llm_analyzer.py...")
with open('research_center/llm_analyzer.py', 'r') as f:
    content = f.read()
    if 'import aiohttp' in content:
        print("❌ Found aiohttp import - removing it...")
        content = content.replace('import aiohttp\n', '')
        content = content.replace('import aiohttp', '')
        with open('research_center/llm_analyzer.py', 'w') as fw:
            fw.write(content)
        print("✅ Removed aiohttp import")
    else:
        print("✅ No aiohttp import found - file is clean")

# 2. Clear Python cache
print("\n🧹 Clearing Python cache...")
subprocess.run(['find', '.', '-type', 'd', '-name', '__pycache__', '-exec', 'rm', '-rf', '{}', '+'], 
               stderr=subprocess.DEVNULL)
print("✅ Cache cleared")

# 3. Install required packages
print("\n📦 Installing required packages...")
required_packages = [
    'pandas', 'numpy', 'requests', 'flask', 'flask-cors',
    'yfinance', 'feedparser', 'ollama', 'chromadb'
]

for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"  ✅ {package} already installed")
    except ImportError:
        print(f"  📥 Installing {package}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                      capture_output=True)

print("\n🚀 Starting Orion System...")
print("="*60)
os.execvp(sys.executable, [sys.executable, 'run_orion_system.py'])