#!/usr/bin/env python3
"""
SIMPLE START - A clean way to run Orion without complications
"""

import subprocess
import time
import sys
import os

def main():
    print("🚀 SIMPLE ORION STARTER")
    print("="*50)
    
    # 1. Check Python
    print("✅ Using Python:", sys.executable)
    
    # 2. Check essential packages
    print("\n📦 Checking packages...")
    required = ['pandas', 'numpy', 'ollama', 'chromadb', 'flask', 'yfinance']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"  ❌ {pkg}")
    
    if missing:
        print(f"\n⚠️ Installing missing packages: {', '.join(missing)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
    
    # 3. Ensure Ollama is running
    print("\n🤖 Starting Ollama...")
    try:
        # Check if already running
        result = subprocess.run(['pgrep', '-x', 'ollama'], capture_output=True)
        if not result.stdout:
            subprocess.Popen(['ollama', 'serve'])
            time.sleep(3)
        print("  ✅ Ollama ready")
    except:
        print("  ⚠️ Please start Ollama manually: ollama serve")
    
    # 4. Start the system
    print("\n🎯 Starting Orion System...")
    print("="*50)
    
    # Run directly
    os.execvp(sys.executable, [sys.executable, 'run_orion_system.py'])

if __name__ == "__main__":
    main()