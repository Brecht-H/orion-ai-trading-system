#!/usr/bin/env python3
"""
Enhanced Data-Driven Trading Orchestrator - Week 2 Implementation
Coordinates correlation analysis, pattern recognition, backtesting, and unified signal generation
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import sqlite3
from dataclasses import dataclass, asdict
import logging
import pandas as pd
import numpy as np

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def safe_json_serialize(obj):
    """Safely serialize objects to JSON, handling pandas/numpy types"""
    if obj is None:
        return None
    
    def convert_item(item):
        if isinstance(item, (pd.Timestamp, datetime)):
            return item.isoformat()
        elif isinstance(item, (np.integer, np.int64)):
            return int(item)
        elif isinstance(item, (np.floating, np.float64)):
            return float(item)
        elif isinstance(item, np.ndarray):
            return item.tolist()
        elif isinstance(item, dict):
            return {k: convert_item(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [convert_item(v) for v in item]
        else:
            return item
    
    try:
        converted = convert_item(obj)
        return json.dumps(converted)
    except Exception as e:
        # Fallback to string representation
        return json.dumps(str(obj))

@dataclass
class OrchestrationResults:
    timestamp: datetime
    execution_time_seconds: float
    components_executed: List[str]
    correlation_patterns_discovered: int
    trading_patterns_identified: int
    backtest_validations_completed: int
    unified_signals_generated: int
    market_regime: str
    overall_confidence: float
    recommended_actions: List[str]
    performance_metrics: Dict[str, float]
    error_count: int
    warnings: List[str]

class EnhancedTradingOrchestrator:
    """
    Enhanced orchestration system for data-driven predictive trading
    Coordinates all Week 2 enhancement components
    """
    
    def __init__(self):
        self.project_root = project_root
        self.db_path = "databases/sqlite_dbs/orchestration_log.db"
        self.setup_logging()
        self.setup_database()
        
        # Component status
        self.component_status = {
            'correlation_engine': False,
            'pattern_recognition': False,
            'backtesting': False,
            'signal_generation': False,
            'data_collection': False
        }
        
        # Execution parameters
        self.execution_interval = 15  # minutes
        self.max_execution_time = 300  # 5 minutes max
        self.error_threshold = 5  # max errors before circuit breaker
        
        # Performance tracking
        self.execution_history = []
        self.error_count = 0
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/trading_orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Enhanced Trading Orchestrator initialized")
        
    def setup_database(self):
        """Setup orchestration tracking database"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orchestration_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                execution_time_seconds REAL NOT NULL,
                components_executed TEXT NOT NULL,
                correlation_patterns_discovered INTEGER DEFAULT 0,
                trading_patterns_identified INTEGER DEFAULT 0,
                backtest_validations_completed INTEGER DEFAULT 0,
                unified_signals_generated INTEGER DEFAULT 0,
                market_regime TEXT DEFAULT 'unknown',
                overall_confidence REAL DEFAULT 0.0,
                recommended_actions TEXT NOT NULL,
                performance_metrics TEXT NOT NULL,
                error_count INTEGER DEFAULT 0,
                warnings TEXT NOT NULL,
                success BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS component_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                component_name TEXT NOT NULL,
                execution_time_seconds REAL NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                performance_data TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    async def run_enhanced_trading_cycle(self) -> OrchestrationResults:
        """
        Run complete enhanced trading cycle with all Week 2 components
        """
        start_time = datetime.now()
        self.logger.info("🚀 Starting enhanced trading cycle")
        
        components_executed = []
        results = {
            'correlation_patterns_discovered': 0,
            'trading_patterns_identified': 0,
            'backtest_validations_completed': 0,
            'unified_signals_generated': 0,
            'market_regime': 'unknown',
            'overall_confidence': 0.0,
            'recommended_actions': [],
            'performance_metrics': {},
            'warnings': []
        }
        
        try:
            # 1. Data Collection Refresh
            await self.execute_component('data_collection', self.run_data_collection)
            components_executed.append('data_collection')
            
            # 2. Correlation Analysis
            correlation_results = await self.execute_component('correlation_analysis', self.run_correlation_analysis)
            if correlation_results:
                results['correlation_patterns_discovered'] = correlation_results.get('new_patterns_discovered', 0)
                results['market_regime'] = correlation_results.get('market_regime', {}).get('regime_type', 'unknown')
            components_executed.append('correlation_analysis')
            
            # 3. Pattern Recognition
            pattern_results = await self.execute_component('pattern_recognition', self.run_pattern_recognition)
            if pattern_results:
                results['trading_patterns_identified'] = pattern_results.get('patterns_validated', 0)
            components_executed.append('pattern_recognition')
            
            # 4. Backtesting Validation
            backtest_results = await self.execute_component('backtesting', self.run_backtesting_validation)
            if backtest_results:
                results['backtest_validations_completed'] = backtest_results.get('patterns_tested', 0)
            components_executed.append('backtesting')
            
            # 5. Unified Signal Generation
            signal_results = await self.execute_component('signal_generation', self.run_signal_generation)
            if signal_results:
                results['unified_signals_generated'] = signal_results.get('final_signals', 0)
                results['overall_confidence'] = signal_results.get('signal_quality_score', 0.0)
            components_executed.append('signal_generation')
            
            # 6. Generate orchestration insights
            insights = await self.generate_orchestration_insights(results)
            results['recommended_actions'] = insights.get('recommended_actions', [])
            results['performance_metrics'] = insights.get('performance_metrics', {})
            
            # 7. Update component status
            await self.update_component_status(components_executed)
            
        except Exception as e:
            self.logger.error(f"❌ Critical error in trading cycle: {e}")
            self.error_count += 1
            results['warnings'].append(f"Critical error: {str(e)}")
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Create orchestration results
        orchestration_results = OrchestrationResults(
            timestamp=start_time,
            execution_time_seconds=execution_time,
            components_executed=components_executed,
            correlation_patterns_discovered=results['correlation_patterns_discovered'],
            trading_patterns_identified=results['trading_patterns_identified'],
            backtest_validations_completed=results['backtest_validations_completed'],
            unified_signals_generated=results['unified_signals_generated'],
            market_regime=results['market_regime'],
            overall_confidence=results['overall_confidence'],
            recommended_actions=results['recommended_actions'],
            performance_metrics=results['performance_metrics'],
            error_count=self.error_count,
            warnings=results['warnings']
        )
        
        # Store results
        await self.store_orchestration_results(orchestration_results)
        
        self.logger.info(f"✅ Enhanced trading cycle complete ({execution_time:.2f}s)")
        self.logger.info(f"   📊 Patterns discovered: {results['correlation_patterns_discovered']}")
        self.logger.info(f"   🎯 Signals generated: {results['unified_signals_generated']}")
        self.logger.info(f"   📈 Market regime: {results['market_regime']}")
        
        return orchestration_results
    
    async def execute_component(self, component_name: str, component_func) -> Optional[Dict[str, Any]]:
        """Execute a component with error handling and performance tracking"""
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔄 Executing {component_name}...")
            results = await component_func()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.component_status[component_name] = True
            
            await self.log_component_performance(component_name, execution_time, True, None, results)
            
            self.logger.info(f"✅ {component_name} completed successfully ({execution_time:.2f}s)")
            return results
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.component_status[component_name] = False
            
            await self.log_component_performance(component_name, execution_time, False, str(e), None)
            
            self.logger.error(f"❌ {component_name} failed: {e}")
            return None
    
    async def run_data_collection(self) -> Dict[str, Any]:
        """Run data collection refresh"""
        try:
            # Import and run free sources collector
            from research_center.collectors.free_sources_collector import FreeSourcesCollector
            
            collector = FreeSourcesCollector()
            results = await collector.collect_all_free_data()
            
            summary = collector.get_collection_summary()
            
            return {
                'sources_collected': len(results),
                'total_records': summary.get('total_records', 0),
                'collection_summary': summary
            }
            
        except ImportError as e:
            self.logger.warning(f"Data collection module not available: {e}")
            return {'sources_collected': 0, 'total_records': 0, 'simulated': True}
        except Exception as e:
            self.logger.error(f"Data collection error: {e}")
            raise
    
    async def run_correlation_analysis(self) -> Dict[str, Any]:
        """Run correlation analysis"""
        try:
            # Import and run correlation engine
            from research_center.analyzers.correlation_engine import AdvancedCorrelationEngine
            
            engine = AdvancedCorrelationEngine()
            results = await engine.run_comprehensive_correlation_analysis()
            
            return results
            
        except ImportError as e:
            self.logger.warning(f"Correlation analysis module not available: {e}")
            return {
                'new_patterns_discovered': 0,
                'signals_generated': 0,
                'market_regime': {'regime_type': 'unknown'},
                'simulated': True
            }
        except Exception as e:
            self.logger.error(f"Correlation analysis error: {e}")
            raise
    
    async def run_pattern_recognition(self) -> Dict[str, Any]:
        """Run pattern recognition"""
        try:
            # Import and run pattern recognition
            from strategy_center.pattern_recognition.trading_patterns import AdvancedPatternRecognition
            
            recognizer = AdvancedPatternRecognition()
            results = await recognizer.run_pattern_recognition()
            
            return results
            
        except ImportError as e:
            self.logger.warning(f"Pattern recognition module not available: {e}")
            return {
                'patterns_discovered': 0,
                'patterns_validated': 0,
                'signals_generated': 0,
                'simulated': True
            }
        except Exception as e:
            self.logger.error(f"Pattern recognition error: {e}")
            raise
    
    async def run_backtesting_validation(self) -> Dict[str, Any]:
        """Run backtesting validation"""
        try:
            # Import and run backtesting
            from strategy_center.backtesting.pattern_backtester import AdvancedPatternBacktester
            
            backtester = AdvancedPatternBacktester()
            results = await backtester.run_comprehensive_backtesting(lookback_days=7)
            
            return results
            
        except ImportError as e:
            self.logger.warning(f"Backtesting module not available: {e}")
            return {
                'patterns_tested': 0,
                'validation_results': [],
                'simulated': True
            }
        except Exception as e:
            self.logger.error(f"Backtesting error: {e}")
            raise
    
    async def run_signal_generation(self) -> Dict[str, Any]:
        """Run unified signal generation"""
        try:
            # Import and run signal generation
            from strategy_center.signal_integration.unified_signal_generator import UnifiedSignalGenerator
            
            generator = UnifiedSignalGenerator()
            results = await generator.generate_unified_signals()
            
            return results
            
        except ImportError as e:
            self.logger.warning(f"Signal generation module not available: {e}")
            return {
                'final_signals': 0,
                'signal_quality_score': 0.0,
                'unified_signals': [],
                'simulated': True
            }
        except Exception as e:
            self.logger.error(f"Signal generation error: {e}")
            raise
    
    async def generate_orchestration_insights(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from orchestration results"""
        insights = {
            'recommended_actions': [],
            'performance_metrics': {},
            'system_health': 'good'
        }
        
        # Analyze results and generate recommendations
        patterns_discovered = results.get('correlation_patterns_discovered', 0)
        signals_generated = results.get('unified_signals_generated', 0)
        confidence = results.get('overall_confidence', 0.0)
        
        # Performance metrics
        insights['performance_metrics'] = {
            'pattern_discovery_rate': patterns_discovered,
            'signal_generation_rate': signals_generated,
            'overall_confidence': confidence,
            'system_efficiency': self.calculate_system_efficiency()
        }
        
        # Recommendations
        if patterns_discovered == 0:
            insights['recommended_actions'].append("No new patterns discovered - consider expanding data sources")
        
        if signals_generated == 0:
            insights['recommended_actions'].append("No signals generated - review signal filtering criteria")
        elif signals_generated > 10:
            insights['recommended_actions'].append("High signal volume - consider stricter filtering")
        
        if confidence < 0.5:
            insights['recommended_actions'].append("Low confidence signals - increase validation requirements")
        elif confidence > 0.8:
            insights['recommended_actions'].append("High confidence signals - consider position sizing optimization")
        
        # Market regime specific recommendations
        market_regime = results.get('market_regime', 'unknown')
        if market_regime == 'trending_volatile':
            insights['recommended_actions'].append("Volatile trending market - use momentum strategies")
        elif market_regime == 'range_bound':
            insights['recommended_actions'].append("Range-bound market - use mean reversion strategies")
        
        return insights
    
    def calculate_system_efficiency(self) -> float:
        """Calculate overall system efficiency"""
        active_components = sum(1 for status in self.component_status.values() if status)
        total_components = len(self.component_status)
        
        if total_components == 0:
            return 0.0
        
        base_efficiency = active_components / total_components
        
        # Adjust for error rate
        if self.error_count > 0:
            error_penalty = min(self.error_count * 0.1, 0.5)  # Max 50% penalty
            base_efficiency = max(0.0, base_efficiency - error_penalty)
        
        return base_efficiency
    
    async def update_component_status(self, executed_components: List[str]):
        """Update component status tracking"""
        for component in self.component_status:
            if component in executed_components:
                self.component_status[component] = True
    
    async def log_component_performance(self, component_name: str, execution_time: float, 
                                      success: bool, error_message: Optional[str], 
                                      performance_data: Optional[Dict[str, Any]]):
        """Log component performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO component_performance
            (timestamp, component_name, execution_time_seconds, success, error_message, performance_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            component_name,
            execution_time,
            success,
            error_message,
            safe_json_serialize(performance_data) if performance_data else None
        ))
        
        conn.commit()
        conn.close()
    
    async def store_orchestration_results(self, results: OrchestrationResults):
        """Store orchestration results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orchestration_runs
            (timestamp, execution_time_seconds, components_executed, 
             correlation_patterns_discovered, trading_patterns_identified,
             backtest_validations_completed, unified_signals_generated,
             market_regime, overall_confidence, recommended_actions,
             performance_metrics, error_count, warnings, success)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            results.timestamp.isoformat(),
            results.execution_time_seconds,
            safe_json_serialize(results.components_executed),
            results.correlation_patterns_discovered,
            results.trading_patterns_identified,
            results.backtest_validations_completed,
            results.unified_signals_generated,
            results.market_regime,
            results.overall_confidence,
            safe_json_serialize(results.recommended_actions),
            safe_json_serialize(results.performance_metrics),
            results.error_count,
            safe_json_serialize(results.warnings),
            results.error_count == 0
        ))
        
        conn.commit()
        conn.close()
    
    async def run_continuous_orchestration(self, max_iterations: int = 100):
        """Run continuous orchestration cycles"""
        self.logger.info(f"🔄 Starting continuous orchestration (max {max_iterations} iterations)")
        
        for iteration in range(max_iterations):
            try:
                self.logger.info(f"📊 Starting iteration {iteration + 1}/{max_iterations}")
                
                # Run enhanced trading cycle
                results = await self.run_enhanced_trading_cycle()
                
                # Check circuit breaker
                if self.error_count >= self.error_threshold:
                    self.logger.error("🚨 Circuit breaker triggered - too many errors")
                    break
                
                # Log iteration summary
                self.logger.info(f"✅ Iteration {iteration + 1} complete:")
                self.logger.info(f"   Patterns: {results.correlation_patterns_discovered}")
                self.logger.info(f"   Signals: {results.unified_signals_generated}")
                self.logger.info(f"   Confidence: {results.overall_confidence:.2%}")
                
                # Wait for next iteration
                if iteration < max_iterations - 1:
                    await asyncio.sleep(self.execution_interval * 60)  # Convert to seconds
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Continuous orchestration stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Iteration {iteration + 1} failed: {e}")
                self.error_count += 1
                
                if self.error_count >= self.error_threshold:
                    self.logger.error("🚨 Circuit breaker triggered")
                    break
                
                # Wait before retry
                await asyncio.sleep(60)  # 1 minute backoff
        
        self.logger.info("🏁 Continuous orchestration completed")
    
    async def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current orchestration status"""
        conn = sqlite3.connect(self.db_path)
        
        # Get latest run
        latest_run_query = """
            SELECT * FROM orchestration_runs
            ORDER BY timestamp DESC
            LIMIT 1
        """
        
        latest_run = pd.read_sql_query(latest_run_query, conn)
        
        # Get component performance
        component_performance_query = """
            SELECT component_name, 
                   AVG(execution_time_seconds) as avg_time,
                   SUM(CASE WHEN success THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as success_rate
            FROM component_performance
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY component_name
        """
        
        component_perf = pd.read_sql_query(component_performance_query, conn)
        conn.close()
        
        status = {
            'component_status': self.component_status,
            'error_count': self.error_count,
            'system_efficiency': self.calculate_system_efficiency(),
            'latest_run': latest_run.to_dict('records')[0] if not latest_run.empty else None,
            'component_performance': component_perf.to_dict('records') if not component_perf.empty else []
        }
        
        return status

if __name__ == "__main__":
    async def main():
        orchestrator = EnhancedTradingOrchestrator()
        
        print("🚀 Enhanced Trading Orchestrator - Week 2")
        print("=" * 50)
        
        # Run single cycle
        results = await orchestrator.run_enhanced_trading_cycle()
        
        print(f"\n📊 ORCHESTRATION RESULTS:")
        print(f"Execution Time: {results.execution_time_seconds:.2f}s")
        print(f"Components Executed: {len(results.components_executed)}")
        print(f"Correlation Patterns: {results.correlation_patterns_discovered}")
        print(f"Trading Patterns: {results.trading_patterns_identified}")
        print(f"Backtest Validations: {results.backtest_validations_completed}")
        print(f"Unified Signals: {results.unified_signals_generated}")
        print(f"Market Regime: {results.market_regime}")
        print(f"Overall Confidence: {results.overall_confidence:.2%}")
        
        print(f"\n💡 RECOMMENDED ACTIONS:")
        for i, action in enumerate(results.recommended_actions, 1):
            print(f"{i}. {action}")
        
        # Ask if user wants continuous mode
        choice = input("\n🔄 Run continuous orchestration? (y/n): ").lower().strip()
        if choice == 'y':
            await orchestrator.run_continuous_orchestration(max_iterations=10)
    
    asyncio.run(main()) 