"""
FILE: core_orchestration/intelligent_orchestrator.py
PURPOSE: Main orchestrator connecting all intelligent components
CONTEXT: Core orchestration - DO NOT DUPLICATE
DEPENDENCIES: Event bus, Research Intelligence, Knowledge Synthesis
MAINTAIN: Central coordination point for all services

DO NOT:
- Create separate orchestrators
- Skip the event bus
- Make direct service calls
- Allow services to drift apart

ONLY MODIFY:
- start() method
- coordinate_services() method
- monitor_performance() method
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))

# Import our components
from message_queue.event_bus import EventBus, MicroService, Event
from research_center.llm_analyzer import ResearchIntelligence
from research_center.collectors.free_sources_collector import FreeSourcesCollector
from knowledge_center.llm_synthesis import KnowledgeSynthesis


class IntelligentOrchestrator:
    """
    Master orchestrator that coordinates all intelligent services
    Using event-driven architecture for scalability
    """
    
    def __init__(self):
        self.setup_logging()
        
        # Initialize event bus
        self.event_bus = EventBus()
        
        # Service wrappers
        self.services = {}
        
        # Performance tracking
        self.performance_metrics = {
            'data_collections': 0,
            'analyses_completed': 0,
            'strategies_generated': 0,
            'total_events': 0
        }
        
        # Running state
        self.running = False
        
    def setup_logging(self):
        """Setup orchestrator logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - IntelligentOrchestrator - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """Start the intelligent orchestration system"""
        self.logger.info("🚀 Starting Intelligent Orchestrator...")
        
        # Start event bus
        await self.event_bus.start()
        
        # Initialize services
        await self._initialize_services()
        
        # Start coordination
        self.running = True
        
        # Run coordination tasks
        tasks = [
            asyncio.create_task(self._data_collection_loop()),
            asyncio.create_task(self._monitor_performance()),
            asyncio.create_task(self._handle_events())
        ]
        
        self.logger.info("✅ Orchestrator started - All services active")
        
        # Keep running
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutting down orchestrator...")
            await self.stop()
            
    async def stop(self):
        """Stop the orchestrator"""
        self.running = False
        await self.event_bus.stop()
        self.logger.info("✅ Orchestrator stopped")
        
    async def _initialize_services(self):
        """Initialize all intelligent services"""
        
        # 1. Data Collection Service
        class DataCollectionService(MicroService):
            def __init__(self, event_bus: EventBus, collector: FreeSourcesCollector):
                super().__init__("data_collection_service", event_bus)
                self.collector = collector
                
                # Subscribe to collection requests
                self.on(["orchestrator.collect_data"], self.handle_collection_request)
                
            async def handle_collection_request(self, event: Event):
                self.logger.info("📊 Starting data collection...")
                
                # Collect data
                data = await self.collector.collect_all_free_data()
                
                # Emit collected data event
                await self.emit(
                    "data.collected",
                    data=data,
                    priority=8
                )
                
        # 2. Research Analysis Service
        class ResearchAnalysisService(MicroService):
            def __init__(self, event_bus: EventBus, analyzer: ResearchIntelligence):
                super().__init__("research_analysis_service", event_bus)
                self.analyzer = analyzer
                
                # Subscribe to data events
                self.on(["data.collected"], self.handle_data)
                
            async def handle_data(self, event: Event):
                self.logger.info("🧠 Analyzing collected data...")
                
                # Get intelligence analysis if available
                if 'intelligence_analysis' in event.data:
                    analysis = event.data['intelligence_analysis']
                else:
                    # Run analysis
                    analysis = await self.analyzer.analyze_market_data(event.data)
                    
                # Emit analysis complete
                await self.emit(
                    "research.analysis_complete",
                    data=analysis,
                    priority=9
                )
                
        # 3. Knowledge Synthesis Service
        class KnowledgeSynthesisService(MicroService):
            def __init__(self, event_bus: EventBus, synthesizer: KnowledgeSynthesis):
                super().__init__("knowledge_synthesis_service", event_bus)
                self.synthesizer = synthesizer
                
                # Subscribe to analysis events
                self.on(["research.analysis_complete"], self.handle_analysis)
                
            async def handle_analysis(self, event: Event):
                self.logger.info("🎯 Synthesizing knowledge...")
                
                # Synthesize insights
                result = await self.synthesizer.synthesize_insights(event.data)
                
                if result['success']:
                    # Generate detailed strategies
                    strategies = await self.synthesizer.generate_strategies(result['knowledge'])
                    
                    # Emit strategies
                    await self.emit(
                        "knowledge.strategies_generated",
                        data={
                            'knowledge': result['knowledge'],
                            'strategies': strategies
                        },
                        priority=10
                    )
                    
        # 4. Strategy Execution Service (placeholder)
        class StrategyExecutionService(MicroService):
            def __init__(self, event_bus: EventBus):
                super().__init__("strategy_execution_service", event_bus)
                
                # Subscribe to strategy events
                self.on(["knowledge.strategies_generated"], self.handle_strategies)
                
            async def handle_strategies(self, event: Event):
                self.logger.info("📈 Received strategies for execution")
                
                strategies = event.data.get('strategies', [])
                
                # Log strategies (execution would happen here)
                for strategy in strategies:
                    self.logger.info(f"   Strategy: {strategy.get('name')} "
                                   f"(confidence: {strategy.get('confidence', 0):.2%})")
                    
                # Emit execution status
                await self.emit(
                    "execution.strategies_received",
                    data={'count': len(strategies)},
                    priority=5
                )
                
        # Initialize actual services
        self.services['data_collector'] = DataCollectionService(
            self.event_bus,
            FreeSourcesCollector()
        )
        
        self.services['research_analyzer'] = ResearchAnalysisService(
            self.event_bus,
            ResearchIntelligence()
        )
        
        self.services['knowledge_synthesizer'] = KnowledgeSynthesisService(
            self.event_bus,
            KnowledgeSynthesis()
        )
        
        self.services['strategy_executor'] = StrategyExecutionService(
            self.event_bus
        )
        
        self.logger.info(f"✅ Initialized {len(self.services)} intelligent services")
        
    async def _data_collection_loop(self):
        """Periodic data collection trigger"""
        while self.running:
            # Trigger data collection
            await self.event_bus.publish(
                "orchestrator.collect_data",
                "orchestrator",
                data={'timestamp': datetime.now().isoformat()},
                priority=7
            )
            
            self.performance_metrics['data_collections'] += 1
            
            # Wait before next collection (5 minutes)
            await asyncio.sleep(300)
            
    async def _handle_events(self):
        """Handle orchestrator-level events"""
        # Register orchestrator as a service
        self.event_bus.register_service("orchestrator")
        
        # Subscribe to completion events for tracking
        async def track_analysis(event: Event):
            self.performance_metrics['analyses_completed'] += 1
            self.logger.info(f"✅ Analysis completed: {self.performance_metrics['analyses_completed']}")
            
        async def track_strategies(event: Event):
            strategies = event.data.get('strategies', [])
            self.performance_metrics['strategies_generated'] += len(strategies)
            self.logger.info(f"✅ Strategies generated: {len(strategies)}")
            
        self.event_bus.subscribe("orchestrator", ["research.analysis_complete"], track_analysis)
        self.event_bus.subscribe("orchestrator", ["knowledge.strategies_generated"], track_strategies)
        
        # Process events
        while self.running:
            event = await self.event_bus.get_next_event("orchestrator", timeout=1.0)
            if event:
                self.performance_metrics['total_events'] += 1
            await asyncio.sleep(0.1)
            
    async def _monitor_performance(self):
        """Monitor system performance"""
        while self.running:
            # Get event bus stats
            bus_stats = self.event_bus.get_stats()
            
            # Log performance summary
            self.logger.info("\n📊 SYSTEM PERFORMANCE SUMMARY")
            self.logger.info(f"   Data Collections: {self.performance_metrics['data_collections']}")
            self.logger.info(f"   Analyses Completed: {self.performance_metrics['analyses_completed']}")
            self.logger.info(f"   Strategies Generated: {self.performance_metrics['strategies_generated']}")
            self.logger.info(f"   Total Events: {bus_stats['events_published']}")
            self.logger.info(f"   Active Services: {bus_stats['active_services']}/{bus_stats['total_services']}")
            
            # Check service health
            for service_name, status in self.event_bus.service_status.items():
                if status['status'] != 'active':
                    self.logger.warning(f"⚠️ Service {service_name} is {status['status']}")
                    
            # Wait before next check (1 minute)
            await asyncio.sleep(60)
            
    async def trigger_immediate_analysis(self):
        """Trigger immediate data collection and analysis"""
        self.logger.info("🚀 Triggering immediate analysis...")
        
        await self.event_bus.publish(
            "orchestrator.collect_data",
            "orchestrator",
            data={'immediate': True, 'timestamp': datetime.now().isoformat()},
            priority=10
        )


# Quick test interface
async def test_orchestrator():
    """Test the orchestrator with a single cycle"""
    orchestrator = IntelligentOrchestrator()
    
    # Start orchestrator
    start_task = asyncio.create_task(orchestrator.start())
    
    # Wait a bit for initialization
    await asyncio.sleep(2)
    
    # Trigger immediate analysis
    await orchestrator.trigger_immediate_analysis()
    
    # Let it run for a bit
    await asyncio.sleep(30)
    
    # Show final stats
    print("\n📊 Final Performance Metrics:")
    for key, value in orchestrator.performance_metrics.items():
        print(f"   {key}: {value}")
        
    # Stop
    await orchestrator.stop()
    start_task.cancel()


if __name__ == "__main__":
    # Install required packages first
    import subprocess
    packages = ['ollama', 'chromadb']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package, '--break-system-packages'])
    
    # Run test
    asyncio.run(test_orchestrator())