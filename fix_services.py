#!/usr/bin/env python3
"""Fix inactive services by properly initializing the event bus"""

import asyncio
import sys
sys.path.insert(0, '.')

async def activate_services():
    # Import after path is set
    from core_orchestration.message_queue.event_bus import EventBus
    from core_orchestration.intelligent_orchestrator import IntelligentOrchestrator
    
    print("🔧 Activating services...")
    
    # Initialize event bus
    event_bus = EventBus()
    await event_bus.start()
    
    # Initialize orchestrator
    orchestrator = IntelligentOrchestrator()
    await orchestrator.initialize()
    
    print("✅ Services activated!")
    print("🚀 Starting normal operation...")
    
    # Run the orchestrator
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(activate_services())