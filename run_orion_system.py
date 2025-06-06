#!/usr/bin/env python3
"""
ORION INTELLIGENT SYSTEM - MAIN RUNNER
Complete system startup and monitoring interface
"""

import asyncio
import sys
import os
from datetime import datetime
import subprocess
import signal
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/workspace')

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class OrionSystemRunner:
    """Main system runner with monitoring"""
    
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def print_header(self):
        """Print system header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("=" * 60)
        print("🚀 ORION INTELLIGENT TRADING SYSTEM")
        print("=" * 60)
        print(f"{Colors.END}\n")
        
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        print(f"{Colors.CYAN}🔍 Checking dependencies...{Colors.END}")
        
        dependencies = {
            'ollama': 'ollama',
            'chromadb': 'chromadb',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'requests': 'requests',
            'yfinance': 'yfinance'
        }
        
        missing = []
        for name, import_name in dependencies.items():
            try:
                __import__(import_name)
                print(f"  ✅ {name}")
            except ImportError:
                print(f"  ❌ {name}")
                missing.append(name)
                
        if missing:
            print(f"\n{Colors.WARNING}⚠️  Missing dependencies: {', '.join(missing)}{Colors.END}")
            print(f"Installing missing packages...")
            
            for package in missing:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', 
                    package, '--break-system-packages'
                ], capture_output=True)
                
            print(f"{Colors.GREEN}✅ Dependencies installed{Colors.END}")
        else:
            print(f"{Colors.GREEN}✅ All dependencies satisfied{Colors.END}")
            
    def check_ollama(self):
        """Check if Ollama is running and model is available"""
        print(f"\n{Colors.CYAN}🤖 Checking Ollama...{Colors.END}")
        
        try:
            # Check if Ollama is running
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/tags'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"{Colors.WARNING}⚠️  Ollama not running. Starting...{Colors.END}")
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                asyncio.run(asyncio.sleep(3))
                
            # Check for mistral model
            import json
            try:
                models_data = json.loads(result.stdout)
                models = [m['name'] for m in models_data.get('models', [])]
                
                if not any('mistral' in m for m in models):
                    print(f"{Colors.WARNING}⚠️  Mistral model not found. Pulling...{Colors.END}")
                    subprocess.run(['ollama', 'pull', 'mistral:7b'])
                    print(f"{Colors.GREEN}✅ Mistral model ready{Colors.END}")
                else:
                    print(f"{Colors.GREEN}✅ Ollama ready with Mistral{Colors.END}")
            except:
                print(f"{Colors.WARNING}⚠️  Installing Mistral model...{Colors.END}")
                subprocess.run(['ollama', 'pull', 'mistral:7b'])
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Ollama check failed: {e}{Colors.END}")
            print("Please install Ollama from: https://ollama.ai")
            return False
            
        return True
        
    async def start_system(self):
        """Start the Orion system"""
        print(f"\n{Colors.CYAN}🚀 Starting Orion System...{Colors.END}")
        
        # Import orchestrator
        from core_orchestration.intelligent_orchestrator import IntelligentOrchestrator
        
        self.orchestrator = IntelligentOrchestrator()
        self.running = True
        
        # Start orchestrator
        print(f"{Colors.GREEN}✅ Starting Intelligent Orchestrator{Colors.END}")
        self.orchestrator_task = asyncio.create_task(self.orchestrator.start())
        
        # Wait for initialization
        await asyncio.sleep(3)
        
        # Start monitoring
        self.monitor_task = asyncio.create_task(self.monitor_system())
        
        # Trigger immediate analysis
        print(f"\n{Colors.CYAN}🔄 Triggering initial analysis...{Colors.END}")
        await self.orchestrator.trigger_immediate_analysis()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SYSTEM FULLY OPERATIONAL{Colors.END}")
        print(f"\n{Colors.CYAN}Press Ctrl+C to stop{Colors.END}\n")
        
    async def monitor_system(self):
        """Monitor system health and performance"""
        while self.running:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            if hasattr(self, 'orchestrator'):
                # Get system stats
                stats = self.orchestrator.event_bus.get_stats()
                metrics = self.orchestrator.performance_metrics
                
                # Print status update
                print(f"\n{Colors.BLUE}{'=' * 50}")
                print(f"📊 SYSTEM STATUS - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'=' * 50}{Colors.END}")
                
                print(f"📈 Performance Metrics:")
                print(f"  • Data Collections: {metrics['data_collections']}")
                print(f"  • Analyses Completed: {metrics['analyses_completed']}")
                print(f"  • Strategies Generated: {metrics['strategies_generated']}")
                
                print(f"\n🔄 Event Bus Status:")
                print(f"  • Events Published: {stats['events_published']}")
                print(f"  • Events Processed: {stats['events_processed']}")
                print(f"  • Active Services: {stats['active_services']}/{stats['total_services']}")
                
                # Check for issues
                if stats['events_failed'] > 0:
                    print(f"{Colors.WARNING}  ⚠️  Failed Events: {stats['events_failed']}{Colors.END}")
                    
                if stats['active_services'] < stats['total_services']:
                    print(f"{Colors.WARNING}  ⚠️  Some services inactive{Colors.END}")
                    
    def signal_handler(self, signum, frame):
        """Handle shutdown signal"""
        print(f"\n{Colors.WARNING}🛑 Shutting down Orion System...{Colors.END}")
        self.running = False
        
        if hasattr(self, 'orchestrator'):
            asyncio.create_task(self.orchestrator.stop())
            
        sys.exit(0)
        
    async def run(self):
        """Main run method"""
        # Setup signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Print header
        self.print_header()
        
        # Check dependencies
        self.check_dependencies()
        
        # Check Ollama
        if not self.check_ollama():
            return
            
        # Start system
        await self.start_system()
        
        # Keep running
        try:
            await asyncio.gather(
                self.orchestrator_task,
                self.monitor_task
            )
        except asyncio.CancelledError:
            pass
            
        print(f"{Colors.GREEN}✅ System stopped gracefully{Colors.END}")


# Quick commands for system management
class OrionCommands:
    """Utility commands for system management"""
    
    @staticmethod
    def status():
        """Check system status"""
        print("🔍 Checking Orion System Status...\n")
        
        # Check databases
        db_files = [
            "data/free_sources_data.db",
            "databases/sqlite_dbs/research_learnings.db",
            "databases/sqlite_dbs/knowledge_base.db",
            "databases/sqlite_dbs/event_store.db"
        ]
        
        for db in db_files:
            if os.path.exists(db):
                size = os.path.getsize(db) / 1024  # KB
                print(f"✅ {db} ({size:.1f} KB)")
            else:
                print(f"❌ {db} (not found)")
                
        # Check recent data
        import sqlite3
        try:
            conn = sqlite3.connect("data/free_sources_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM free_data WHERE date = date('now')")
            count = cursor.fetchone()[0]
            print(f"\n📊 Records collected today: {count}")
            conn.close()
        except:
            pass
            
    @staticmethod
    def clean():
        """Clean temporary files"""
        print("🧹 Cleaning temporary files...\n")
        
        patterns = [
            "*_copy.py",
            "*_backup.py", 
            "*_old.py",
            "*_v2.py",
            "*.pyc",
            "__pycache__"
        ]
        
        count = 0
        for pattern in patterns:
            result = subprocess.run(
                f"find . -name '{pattern}' -type f -delete",
                shell=True,
                capture_output=True
            )
            
        print(f"✅ Cleanup complete")
        
    @staticmethod
    def logs():
        """Show recent system logs"""
        print("📜 Recent System Activity:\n")
        
        # Show recent events
        import sqlite3
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/event_store.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT event_type, source_service, timestamp 
                FROM events 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            events = cursor.fetchall()
            for event in events:
                dt = datetime.fromtimestamp(event[2])
                print(f"{dt.strftime('%H:%M:%S')} - {event[0]} from {event[1]}")
                
            conn.close()
        except:
            print("No events found")


# Main entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Orion Intelligent Trading System')
    parser.add_argument('command', nargs='?', default='run',
                       choices=['run', 'status', 'clean', 'logs'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        runner = OrionSystemRunner()
        asyncio.run(runner.run())
    elif args.command == 'status':
        OrionCommands.status()
    elif args.command == 'clean':
        OrionCommands.clean()
    elif args.command == 'logs':
        OrionCommands.logs()