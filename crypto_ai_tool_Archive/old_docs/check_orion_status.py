#!/usr/bin/env python3
"""
Quick Orion Status Checker
"""
import os
import subprocess
import time

def check_orion_status():
    print("🔍 ORION SYSTEM STATUS CHECK")
    print("=" * 40)
    
    # Check if virtual environment exists
    if os.path.exists('.venv/bin/python3'):
        print("✅ Virtual environment: Found")
    else:
        print("❌ Virtual environment: Not found")
    
    # Check if main files exist
    important_files = [
        'run_orion_system.py',
        'requirements.txt',
        '.env'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing")
    
    # Check databases
    db_paths = [
        'databases/unified/market_data.db',
        'databases/sqlite_dbs/'
    ]
    
    print("\n📊 Database Status:")
    for db_path in db_paths:
        if os.path.exists(db_path):
            if os.path.isfile(db_path):
                size = os.path.getsize(db_path) / 1024 / 1024  # MB
                print(f"✅ {db_path}: {size:.1f} MB")
            else:
                files = len([f for f in os.listdir(db_path) if f.endswith('.db')])
                print(f"✅ {db_path}: {files} database files")
        else:
            print(f"❌ {db_path}: Missing")
    
    # Check for running processes
    print("\n⚡ Process Status:")
    try:
        # Check for Orion processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        orion_processes = [line for line in result.stdout.split('\n') if 'orion' in line.lower() or 'run_orion' in line.lower()]
        
        if orion_processes:
            print(f"✅ Orion processes: {len(orion_processes)} running")
            for proc in orion_processes[:3]:  # Show first 3
                print(f"   {proc.split()[1]}: {' '.join(proc.split()[10:])[:50]}...")
        else:
            print("❌ Orion processes: None running")
            
        # Check Ollama
        ollama_processes = [line for line in result.stdout.split('\n') if 'ollama' in line.lower()]
        if ollama_processes:
            print(f"✅ Ollama: Running ({len(ollama_processes)} processes)")
        else:
            print("❌ Ollama: Not running")
            
    except Exception as e:
        print(f"⚠️ Process check failed: {e}")
    
    # Test virtual environment packages
    print("\n📦 Package Status:")
    try:
        result = subprocess.run(['.venv/bin/python3', '-c', 
                               'import pandas, numpy, requests, flask; print("✅ Core packages working")'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("❌ Core packages: Missing")
    except:
        print("❌ Core packages: Cannot check")
    
    print("\n" + "=" * 40)
    print("🎯 RECOMMENDATION:")
    
    if os.path.exists('.venv/bin/python3') and os.path.exists('run_orion_system.py'):
        print("✅ Ready to run: source .venv/bin/activate && python run_orion_system.py")
    else:
        print("❌ Setup needed: Check missing files above")

if __name__ == "__main__":
    check_orion_status() 