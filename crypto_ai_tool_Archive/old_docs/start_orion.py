#!/usr/bin/env python3
"""
Simple Orion Starter - Just Works!
"""
import subprocess
import os
import sys

def main():
    print("🚀 Starting Orion Trading System...")
    print("="*50)
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if main file exists
    main_file = "run_orion_system.py"
    if not os.path.exists(main_file):
        print(f"❌ Error: {main_file} not found!")
        print(f"📍 Current directory: {os.getcwd()}")
        print(f"📋 Files available: {os.listdir('.')[:10]}...")
        return
    
    print(f"✅ Found {main_file}")
    
    # Use the virtual environment Python
    venv_python = ".venv/bin/python3"
    if os.path.exists(venv_python):
        print(f"🔄 Using virtual environment Python: {venv_python}")
        try:
            subprocess.run([venv_python, main_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {e}")
    else:
        print("❌ Virtual environment not found")
        print("💡 Try: python3 run_orion_system.py")

if __name__ == "__main__":
    main() 