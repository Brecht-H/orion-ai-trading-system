#!/usr/bin/env python3
"""
Start and Monitor Orion System
"""
import os
import subprocess
import time
import signal
import sys

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama: Running")
            return True
        else:
            print("❌ Ollama: Not responding")
            return False
    except:
        print("❌ Ollama: Not running")
        return False

def start_ollama():
    """Start Ollama if not running"""
    print("🤖 Starting Ollama...")
    subprocess.Popen(['ollama', 'serve'], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL)
    time.sleep(5)

def check_databases():
    """Check database status"""
    print("\n📊 Database Status:")
    
    # Check unified database
    unified_db = 'databases/unified/market_data.db'
    if os.path.exists(unified_db):
        size = os.path.getsize(unified_db) / 1024 / 1024
        print(f"✅ Unified database: {size:.1f} MB")
    
    # Check sqlite databases
    sqlite_dir = 'databases/sqlite_dbs/'
    if os.path.exists(sqlite_dir):
        db_files = [f for f in os.listdir(sqlite_dir) if f.endswith('.db')]
        print(f"✅ SQLite databases: {len(db_files)} files")
        
        # Show some important ones
        important_dbs = ['research_learnings.db', 'knowledge_base.db', 'event_store.db']
        for db in important_dbs:
            if db in db_files:
                print(f"   ✅ {db}")

def main():
    print("🚀 ORION START & MONITOR")
    print("=" * 50)
    
    # Check virtual environment
    if not os.path.exists('.venv/bin/python3'):
        print("❌ Virtual environment not found!")
        print("💡 Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt")
        return
    
    print("✅ Virtual environment: Found")
    
    # Check Ollama
    if not check_ollama():
        start_ollama()
        if not check_ollama():
            print("❌ Failed to start Ollama")
            return
    
    # Check databases
    check_databases()
    
    # Start the system
    print("\n🎯 Starting Orion System...")
    print("📝 Output will show below (Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        # Start with virtual environment Python
        env = os.environ.copy()
        env['PATH'] = f"{os.path.abspath('.venv/bin')}:{env['PATH']}"
        
        process = subprocess.Popen(
            ['.venv/bin/python3', 'run_orion_system.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor output
        start_time = time.time()
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Add timestamp to output
                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] {output.strip()}")
                
                # Check for key indicators
                if "SYSTEM FULLY OPERATIONAL" in output:
                    print(f"\n🎉 SUCCESS! System is fully operational!")
                    
                if "ollama" in output.lower() and "✅" in output:
                    print(f"🤖 Ollama confirmed working")
                    
                if "Event Bus Status" in output:
                    print(f"📡 Event system active")
            
            # Check if system is taking too long
            if time.time() - start_time > 300:  # 5 minutes
                print(f"\n⚠️ System taking longer than expected...")
                break
                
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping system...")
        process.terminate()
        process.wait()
        print(f"✅ System stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 