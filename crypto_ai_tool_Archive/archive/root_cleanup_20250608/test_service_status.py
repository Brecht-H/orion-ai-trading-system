#!/usr/bin/env python3
"""Quick test to check service status"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core_orchestration.intelligent_orchestrator import IntelligentOrchestrator

async def test_services():
    print("🔍 Testing service status...")
    
    orchestrator = IntelligentOrchestrator()
    await orchestrator.start()
    
    # Wait a bit for services to initialize
    await asyncio.sleep(5)
    
    # Check service status
    stats = orchestrator.event_bus.get_stats()
    print(f"\n📊 Service Status:")
    print(f"Active Services: {stats['active_services']}/{stats['total_services']}")
    
    print(f"\n🔧 Individual Service Status:")
    for name, status in orchestrator.event_bus.service_status.items():
        status_icon = "✅" if status['status'] == 'active' else "❌"
        print(f"  {status_icon} {name}: {status['status']}")
        
    # Trigger a test cycle
    print(f"\n🚀 Triggering test analysis...")
    await orchestrator.trigger_immediate_analysis()
    
    # Wait for processing
    await asyncio.sleep(3)
    
    # Check again
    stats = orchestrator.event_bus.get_stats()
    print(f"\n📊 After Test Cycle:")
    print(f"Active Services: {stats['active_services']}/{stats['total_services']}")
    
    await orchestrator.stop()
    print(f"\n✅ Test complete")

if __name__ == "__main__":
    asyncio.run(test_services()) 