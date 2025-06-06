"""
FILE: core_orchestration/message_queue/event_bus.py
PURPOSE: Event-driven communication between microservices
CONTEXT: Core orchestration - DO NOT DUPLICATE
DEPENDENCIES: Uses asyncio for in-memory queue (no Redis needed initially)
MAINTAIN: Single message bus for all components

DO NOT:
- Create separate event systems
- Use external dependencies initially
- Skip message persistence
- Allow unbounded queues

ONLY MODIFY:
- publish() method
- subscribe() method
- process_events() method
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from collections import defaultdict
import pickle
import uuid


@dataclass
class Event:
    """Standard event structure for all services"""
    event_id: str
    event_type: str  # research.data_collected, knowledge.synthesized, etc.
    source_service: str
    target_service: Optional[str]  # None = broadcast
    timestamp: float
    data: Dict[str, Any]
    priority: int = 5  # 1-10, higher = more important
    correlation_id: Optional[str] = None  # For tracking related events


class EventBus:
    """
    Central event bus for microservice communication
    Starts with in-memory, can upgrade to Redis later
    """
    
    def __init__(self):
        self.setup_logging()
        self.setup_persistence()
        
        # In-memory queues per service
        self.service_queues: Dict[str, asyncio.Queue] = {}
        
        # Event subscribers
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Event history for replay
        self.event_history: List[Event] = []
        
        # Service health tracking
        self.service_status = {}
        
        # Statistics
        self.stats = {
            'events_published': 0,
            'events_processed': 0,
            'events_failed': 0
        }
        
        # Start event processor
        self.processor_task = None
        
    def setup_logging(self):
        """Setup event bus logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - EventBus - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_persistence(self):
        """Setup event persistence for reliability"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        self.db_path = "databases/sqlite_dbs/event_store.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Event store for persistence
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                source_service TEXT NOT NULL,
                target_service TEXT,
                timestamp REAL NOT NULL,
                data TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                correlation_id TEXT,
                processed BOOLEAN DEFAULT FALSE,
                processed_at REAL,
                error TEXT
            )
        """)
        
        # Service registry
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_name TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                last_heartbeat REAL NOT NULL,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    async def start(self):
        """Start the event bus processor"""
        self.logger.info("🚀 Starting Event Bus...")
        self.processor_task = asyncio.create_task(self.process_events())
        
        # Start heartbeat monitor
        asyncio.create_task(self._monitor_services())
        
    async def stop(self):
        """Stop the event bus"""
        if self.processor_task:
            self.processor_task.cancel()
            await self.processor_task
            
    def register_service(self, service_name: str, metadata: Dict = None):
        """Register a service with the event bus"""
        if service_name not in self.service_queues:
            self.service_queues[service_name] = asyncio.Queue(maxsize=1000)
            
        self.service_status[service_name] = {
            'status': 'active',
            'last_heartbeat': datetime.now().timestamp(),
            'metadata': metadata or {}
        }
        
        # Persist registration
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO services
            (service_name, status, last_heartbeat, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            service_name,
            'active',
            datetime.now().timestamp(),
            json.dumps(metadata or {})
        ))
        conn.commit()
        conn.close()
        
        self.logger.info(f"✅ Service registered: {service_name}")
        
    async def publish(self, event_type: str, source_service: str, 
                     data: Dict[str, Any], target_service: Optional[str] = None,
                     priority: int = 5, correlation_id: Optional[str] = None) -> str:
        """
        Publish an event to the bus
        Returns: event_id for tracking
        """
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source_service=source_service,
            target_service=target_service,
            timestamp=datetime.now().timestamp(),
            data=data,
            priority=priority,
            correlation_id=correlation_id
        )
        
        # Persist event first (for reliability)
        self._persist_event(event)
        
        # Route to appropriate queue(s)
        if target_service:
            # Direct message
            if target_service in self.service_queues:
                await self.service_queues[target_service].put(event)
            else:
                self.logger.warning(f"Target service not found: {target_service}")
        else:
            # Broadcast to all subscribers of this event type
            for service_name, queue in self.service_queues.items():
                if service_name != source_service:  # Don't send to self
                    try:
                        await queue.put(event)
                    except asyncio.QueueFull:
                        self.logger.warning(f"Queue full for service: {service_name}")
                        
        self.stats['events_published'] += 1
        self.event_history.append(event)
        
        # Limit history size
        if len(self.event_history) > 10000:
            self.event_history = self.event_history[-5000:]
            
        self.logger.info(f"📤 Published: {event_type} from {source_service}")
        return event.event_id
        
    def subscribe(self, service_name: str, event_types: List[str], 
                  handler: Callable[[Event], None]):
        """
        Subscribe to specific event types
        Handler should be async function
        """
        for event_type in event_types:
            key = f"{service_name}:{event_type}"
            self.subscribers[key].append(handler)
            
        self.logger.info(f"📥 {service_name} subscribed to: {event_types}")
        
    async def get_next_event(self, service_name: str, timeout: float = 1.0) -> Optional[Event]:
        """Get next event for a service"""
        if service_name not in self.service_queues:
            return None
            
        try:
            event = await asyncio.wait_for(
                self.service_queues[service_name].get(),
                timeout=timeout
            )
            return event
        except asyncio.TimeoutError:
            return None
            
    async def process_events(self):
        """Main event processing loop"""
        self.logger.info("🔄 Event processor started")
        
        while True:
            try:
                # Process events for each service
                for service_name, queue in self.service_queues.items():
                    if not queue.empty():
                        event = await queue.get()
                        await self._process_single_event(service_name, event)
                        
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Event processing error: {e}")
                await asyncio.sleep(1)
                
    async def _process_single_event(self, service_name: str, event: Event):
        """Process a single event for a service"""
        try:
            # Find matching handlers
            key = f"{service_name}:{event.event_type}"
            handlers = self.subscribers.get(key, [])
            
            # Also check for wildcard subscribers
            wildcard_key = f"{service_name}:*"
            handlers.extend(self.subscribers.get(wildcard_key, []))
            
            # Execute handlers
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    self.logger.error(f"Handler error: {e}")
                    
            # Mark as processed
            self._mark_event_processed(event.event_id)
            self.stats['events_processed'] += 1
            
        except Exception as e:
            self.logger.error(f"Event processing failed: {e}")
            self.stats['events_failed'] += 1
            self._mark_event_failed(event.event_id, str(e))
            
    def _persist_event(self, event: Event):
        """Persist event to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events
            (event_id, event_type, source_service, target_service,
             timestamp, data, priority, correlation_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_id,
            event.event_type,
            event.source_service,
            event.target_service,
            event.timestamp,
            json.dumps(event.data),
            event.priority,
            event.correlation_id
        ))
        
        conn.commit()
        conn.close()
        
    def _mark_event_processed(self, event_id: str):
        """Mark event as processed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE events
            SET processed = TRUE, processed_at = ?
            WHERE event_id = ?
        """, (datetime.now().timestamp(), event_id))
        
        conn.commit()
        conn.close()
        
    def _mark_event_failed(self, event_id: str, error: str):
        """Mark event as failed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE events
            SET error = ?
            WHERE event_id = ?
        """, (error, event_id))
        
        conn.commit()
        conn.close()
        
    async def _monitor_services(self):
        """Monitor service health"""
        while True:
            try:
                current_time = datetime.now().timestamp()
                
                for service_name, status in self.service_status.items():
                    # Check heartbeat
                    last_heartbeat = status['last_heartbeat']
                    if current_time - last_heartbeat > 60:  # 1 minute timeout
                        status['status'] = 'inactive'
                        self.logger.warning(f"⚠️ Service inactive: {service_name}")
                        
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Service monitoring error: {e}")
                await asyncio.sleep(30)
                
    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        return {
            **self.stats,
            'active_services': len([s for s in self.service_status.values() 
                                   if s['status'] == 'active']),
            'total_services': len(self.service_status),
            'queue_sizes': {name: queue.qsize() 
                           for name, queue in self.service_queues.items()}
        }


# Service wrapper for easy integration
class MicroService:
    """Base class for microservices using the event bus"""
    
    def __init__(self, service_name: str, event_bus: EventBus):
        self.service_name = service_name
        self.event_bus = event_bus
        self.logger = logging.getLogger(service_name)
        
        # Register with event bus
        self.event_bus.register_service(service_name)
        
    async def emit(self, event_type: str, data: Dict[str, Any], 
                   target: Optional[str] = None, priority: int = 5) -> str:
        """Emit an event"""
        return await self.event_bus.publish(
            event_type=event_type,
            source_service=self.service_name,
            data=data,
            target_service=target,
            priority=priority
        )
        
    def on(self, event_types: List[str], handler: Callable):
        """Subscribe to events"""
        self.event_bus.subscribe(self.service_name, event_types, handler)
        
    async def process_events(self):
        """Process incoming events"""
        while True:
            event = await self.event_bus.get_next_event(self.service_name)
            if event:
                # Process based on registered handlers
                pass
            await asyncio.sleep(0.1)


# Example services showing the pattern
class ResearchService(MicroService):
    """Example research service using event bus"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("research_service", event_bus)
        
        # Subscribe to relevant events
        self.on(["system.start", "market.update"], self.handle_market_update)
        
    async def handle_market_update(self, event: Event):
        """Handle market update events"""
        self.logger.info(f"Received market update: {event.data}")
        
        # Do research analysis...
        analysis_result = {"sentiment": "bullish", "confidence": 0.75}
        
        # Emit analysis complete event
        await self.emit(
            "research.analysis_complete",
            data=analysis_result,
            priority=7
        )


class KnowledgeService(MicroService):
    """Example knowledge service"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("knowledge_service", event_bus)
        
        # Subscribe to research results
        self.on(["research.analysis_complete"], self.handle_analysis)
        
    async def handle_analysis(self, event: Event):
        """Handle analysis from research"""
        self.logger.info(f"Synthesizing knowledge from: {event.data}")
        
        # Synthesize knowledge...
        strategy = {"name": "Bullish Momentum", "confidence": 0.8}
        
        # Emit strategy generated event
        await self.emit(
            "knowledge.strategy_generated",
            data=strategy,
            priority=8
        )


# Usage example
async def main():
    """Test the event bus system"""
    # Create event bus
    bus = EventBus()
    await bus.start()
    
    # Create services
    research = ResearchService(bus)
    knowledge = KnowledgeService(bus)
    
    # Simulate market update
    await bus.publish(
        "market.update",
        "market_data_collector",
        {"btc_price": 52000, "eth_price": 3200}
    )
    
    # Let events process
    await asyncio.sleep(2)
    
    # Show stats
    print("\n📊 Event Bus Statistics:")
    stats = bus.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
        
    await bus.stop()


if __name__ == "__main__":
    asyncio.run(main())