#!/usr/bin/env python3
"""
🚀 ORION CEO DASHBOARD LAUNCHER
One-click startup for the complete desktop dashboard experience
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'flask-cors', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        print("✅ Dependencies installed")

def start_api_server():
    """Start the Flask API server"""
    print("🔧 Starting Orion Dashboard API server...")
    
    api_script = Path(__file__).parent / 'dashboard_api.py'
    if not api_script.exists():
        print("❌ dashboard_api.py not found!")
        return None
    
    # Start API server in background
    process = subprocess.Popen([
        sys.executable, str(api_script)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return process

def wait_for_server(timeout=30):
    """Wait for the API server to be ready"""
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get('http://localhost:5001/api/overview', timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    
    return False

def open_dashboard():
    """Open the dashboard in the default browser"""
    dashboard_url = 'http://localhost:5001'
    print(f"🌐 Opening dashboard at: {dashboard_url}")
    webbrowser.open(dashboard_url)

def main():
    """Main startup function"""
    print("🚀 ORION CEO DASHBOARD LAUNCHER")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server")
        return
    
    # Wait for server to be ready
    print("⏳ Waiting for API server to start...")
    if wait_for_server():
        print("✅ API server is ready")
        
        # Open dashboard
        time.sleep(2)  # Give server a moment to fully initialize
        open_dashboard()
        
        print("\n🎯 DASHBOARD READY!")
        print("=" * 50)
        print("📊 Dashboard URL: http://localhost:5001")
        print("🔧 API Base URL: http://localhost:5001/api")
        print("📱 Features:")
        print("   • Real-time portfolio tracking")
        print("   • System health monitoring")
        print("   • 35 action items from Notion")
        print("   • Trading performance analytics")
        print("   • Risk management metrics")
        print("   • Research center data")
        print("   • Knowledge center progress")
        print("\n⌨️  Press Ctrl+C to stop the dashboard")
        
        try:
            # Keep the script running
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down dashboard...")
            api_process.terminate()
            api_process.wait()
            print("✅ Dashboard stopped")
    else:
        print("❌ API server failed to start within timeout")
        api_process.terminate()

if __name__ == '__main__':
    main() 