#!/usr/bin/env python3
"""
🎯 LIVE STRATEGY COORDINATOR
Connects proven sandbox strategies with live trading execution

This coordinator validates strategy signals and coordinates with the 
live trading engine to execute trades with institutional risk controls.
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import asyncio

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_execution_center.core.live_trading_engine import LiveTradingEngine, TradeOrder

class LiveStrategyCoordinator:
    """
    LIVE STRATEGY COORDINATOR
    
    CAPABILITIES:
    - Validate strategy signals from sandbox testing
    - Coordinate with live trading engine
    - Monitor strategy performance in real-time
    - Automatic strategy adjustment based on performance
    - CEO approval pipeline for high-risk strategies
    """
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        
        # Initialize live trading engine (testnet for now)
        self.trading_engine = LiveTradingEngine(testnet=True)
        
        # Strategy performance thresholds
        self.performance_thresholds = {
            'minimum_win_rate': 55.0,      # 55% minimum win rate
            'minimum_sharpe_ratio': 1.5,   # 1.5 minimum Sharpe ratio
            'maximum_drawdown': 15.0,      # 15% maximum drawdown
            'minimum_trades': 10,          # 10 trades minimum for validation
            'performance_window_days': 30   # 30-day rolling performance window
        }
        
        # Strategy allocation based on performance
        self.strategy_allocations = {
            'momentum_breakout': {
                'base_allocation': 2500.0,  # $2.5K base allocation
                'max_allocation': 5000.0,   # $5K maximum allocation
                'performance_multiplier': 1.2,
                'enabled': True
            },
            'mean_reversion': {
                'base_allocation': 2500.0,
                'max_allocation': 5000.0,
                'performance_multiplier': 1.3,  # Higher multiplier for better performer
                'enabled': True
            },
            'smart_swing': {
                'base_allocation': 2500.0,
                'max_allocation': 4000.0,
                'performance_multiplier': 1.1,
                'enabled': True
            },
            'lightning_breakout': {
                'base_allocation': 0.0,      # Disabled - requires CEO approval
                'max_allocation': 2500.0,
                'performance_multiplier': 0.8,
                'enabled': False,
                'ceo_approval_required': True
            }
        }
        
    def setup_logging(self):
        """Setup strategy coordinator logging"""
        log_dir = Path("logs/strategy_coordination")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - StrategyCoordinator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'strategy_coordination.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("🎯 Live Strategy Coordinator initialized")
        
    def setup_database(self):
        """Setup strategy coordination database"""
        db_path = Path("databases/sqlite_dbs/strategy_coordination.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Strategy signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                strategy_name TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                confidence REAL NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                position_size REAL,
                status TEXT DEFAULT 'pending',
                executed_order_id TEXT,
                execution_timestamp REAL,
                execution_price REAL,
                pnl REAL DEFAULT 0
            )
        """)
        
        # Strategy performance tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                strategy_name TEXT NOT NULL,
                performance_window_days INTEGER NOT NULL,
                total_trades INTEGER NOT NULL,
                winning_trades INTEGER NOT NULL,
                win_rate REAL NOT NULL,
                total_pnl REAL NOT NULL,
                sharpe_ratio REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                current_allocation REAL NOT NULL,
                performance_score REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        
        # CEO approval queue
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ceo_approval_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                strategy_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                risk_assessment TEXT NOT NULL,
                expected_impact TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                ceo_decision TEXT,
                decision_timestamp REAL,
                decision_notes TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        self.db_path = db_path
        
    def validate_strategy_signal(self, strategy_name: str, signal_data: Dict) -> Tuple[bool, str]:
        """Validate strategy signal before execution"""
        
        # Check if strategy is enabled
        if strategy_name not in self.strategy_allocations:
            return False, f"Strategy {strategy_name} not found in allocations"
            
        strategy_config = self.strategy_allocations[strategy_name]
        if not strategy_config['enabled']:
            return False, f"Strategy {strategy_name} is disabled"
            
        # Check CEO approval requirement
        if strategy_config.get('ceo_approval_required', False):
            return False, f"Strategy {strategy_name} requires CEO approval"
            
        # Validate signal confidence
        confidence = signal_data.get('confidence', 0)
        if confidence < 0.6:  # 60% minimum confidence
            return False, f"Signal confidence {confidence:.2f} below minimum threshold"
            
        # Check recent strategy performance
        performance = self.get_strategy_performance(strategy_name)
        if performance and performance['win_rate'] < self.performance_thresholds['minimum_win_rate']:
            return False, f"Strategy win rate {performance['win_rate']:.1f}% below threshold"
            
        # Validate position sizing
        position_size = signal_data.get('position_size', 0)
        max_allocation = strategy_config['max_allocation']
        if position_size > max_allocation:
            return False, f"Position size ${position_size} exceeds max allocation ${max_allocation}"
            
        return True, "Signal validation passed"
        
    def process_strategy_signal(self, strategy_name: str, signal_data: Dict) -> Dict:
        """Process strategy signal and execute if validated"""
        
        try:
            # Validate signal
            valid, validation_message = self.validate_strategy_signal(strategy_name, signal_data)
            if not valid:
                self.logger.warning(f"⚠️ Signal validation failed: {validation_message}")
                return {'success': False, 'error': validation_message}
                
            # Record signal in database
            signal_id = self.record_strategy_signal(strategy_name, signal_data)
            
            # Create trade order
            trade_order = TradeOrder(
                symbol=signal_data['symbol'],
                side=signal_data['direction'],
                order_type=signal_data.get('order_type', 'Market'),
                qty=signal_data['position_size'],
                price=signal_data.get('entry_price'),
                stop_loss=signal_data.get('stop_loss'),
                take_profit=signal_data.get('take_profit'),
                strategy=strategy_name,
                risk_percent=2.0  # 2% risk per trade
            )
            
            # Execute trade through live trading engine
            execution_result = self.trading_engine.place_order(trade_order)
            
            if execution_result['success']:
                # Update signal record with execution details
                self.update_signal_execution(signal_id, execution_result)
                
                self.logger.info(f"✅ Strategy signal executed: {strategy_name} - {signal_data['symbol']} {signal_data['direction']}")
                return {
                    'success': True,
                    'signal_id': signal_id,
                    'order_id': execution_result['order_id'],
                    'strategy': strategy_name
                }
            else:
                self.logger.error(f"❌ Trade execution failed: {execution_result['error']}")
                return {'success': False, 'error': execution_result['error']}
                
        except Exception as e:
            self.logger.error(f"❌ Error processing strategy signal: {e}")
            return {'success': False, 'error': str(e)}
            
    def record_strategy_signal(self, strategy_name: str, signal_data: Dict) -> int:
        """Record strategy signal in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO strategy_signals 
                (timestamp, strategy_name, signal_type, symbol, direction, confidence,
                 entry_price, stop_loss, take_profit, position_size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().timestamp(),
                strategy_name,
                signal_data.get('signal_type', 'trade'),
                signal_data['symbol'],
                signal_data['direction'],
                signal_data['confidence'],
                signal_data.get('entry_price'),
                signal_data.get('stop_loss'),
                signal_data.get('take_profit'),
                signal_data['position_size']
            ))
            
            signal_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return signal_id
            
        except Exception as e:
            self.logger.error(f"❌ Error recording strategy signal: {e}")
            return 0
            
    def update_signal_execution(self, signal_id: int, execution_result: Dict):
        """Update signal record with execution details"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE strategy_signals 
                SET status = 'executed', executed_order_id = ?, execution_timestamp = ?
                WHERE id = ?
            """, (
                execution_result['order_id'],
                datetime.now().timestamp(),
                signal_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"❌ Error updating signal execution: {e}")
            
    def get_strategy_performance(self, strategy_name: str) -> Optional[Dict]:
        """Get recent performance metrics for strategy"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get latest performance record
            cursor.execute("""
                SELECT * FROM strategy_performance 
                WHERE strategy_name = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (strategy_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'strategy_name': result[2],
                    'total_trades': result[4],
                    'winning_trades': result[5],
                    'win_rate': result[6],
                    'total_pnl': result[7],
                    'sharpe_ratio': result[8],
                    'max_drawdown': result[9],
                    'current_allocation': result[10],
                    'performance_score': result[11],
                    'status': result[12]
                }
                
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting strategy performance: {e}")
            return None
            
    def update_strategy_allocations(self):
        """Update strategy allocations based on performance"""
        try:
            for strategy_name, config in self.strategy_allocations.items():
                if not config['enabled']:
                    continue
                    
                performance = self.get_strategy_performance(strategy_name)
                if performance:
                    # Calculate new allocation based on performance
                    base_allocation = config['base_allocation']
                    performance_multiplier = config['performance_multiplier']
                    
                    # Adjust multiplier based on win rate and Sharpe ratio
                    win_rate_factor = performance['win_rate'] / 70.0  # Target 70% win rate
                    sharpe_factor = performance['sharpe_ratio'] / 2.0  # Target 2.0 Sharpe ratio
                    
                    adjusted_multiplier = performance_multiplier * min(win_rate_factor, sharpe_factor)
                    new_allocation = min(base_allocation * adjusted_multiplier, config['max_allocation'])
                    
                    # Update allocation
                    config['current_allocation'] = new_allocation
                    
                    self.logger.info(f"📊 Updated {strategy_name} allocation: ${new_allocation:.2f}")
                    
        except Exception as e:
            self.logger.error(f"❌ Error updating strategy allocations: {e}")
            
    def get_coordination_status(self) -> Dict:
        """Get comprehensive coordination status"""
        try:
            # Get trading engine status
            trading_status = self.trading_engine.get_trading_status()
            
            # Get strategy performance summary
            strategy_performances = {}
            for strategy_name in self.strategy_allocations.keys():
                performance = self.get_strategy_performance(strategy_name)
                if performance:
                    strategy_performances[strategy_name] = performance
                    
            # Get recent signals
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT strategy_name, COUNT(*) as signal_count
                FROM strategy_signals 
                WHERE timestamp > ? 
                GROUP BY strategy_name
            """, (datetime.now().timestamp() - 86400,))  # Last 24 hours
            
            daily_signals = dict(cursor.fetchall())
            conn.close()
            
            return {
                'trading_engine_status': trading_status,
                'strategy_allocations': self.strategy_allocations,
                'strategy_performances': strategy_performances,
                'daily_signal_count': daily_signals,
                'performance_thresholds': self.performance_thresholds,
                'coordination_status': 'active',
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting coordination status: {e}")
            return {'error': str(e)}

# Test function for development
async def main():
    """Test function for strategy coordinator"""
    
    coordinator = LiveStrategyCoordinator()
    
    # Get coordination status
    status = coordinator.get_coordination_status()
    print("🎯 Strategy Coordination Status:")
    
    trading_status = status.get('trading_engine_status', {})
    print(f"   Portfolio Value: ${trading_status.get('portfolio_value', 0):.2f}")
    print(f"   Active Positions: {trading_status.get('position_count', 0)}")
    print(f"   Daily P&L: ${trading_status.get('daily_pnl', 0):.2f}")
    
    print(f"\n📊 Strategy Allocations:")
    for strategy, config in status.get('strategy_allocations', {}).items():
        enabled_status = "✅ ENABLED" if config['enabled'] else "❌ DISABLED"
        print(f"   {strategy}: ${config.get('base_allocation', 0):.0f} - {enabled_status}")
        
    # Test signal processing with a sample signal
    test_signal = {
        'symbol': 'BTCUSDT',
        'direction': 'Buy',
        'confidence': 0.75,
        'position_size': 100.0,  # $100 test position
        'signal_type': 'momentum_breakout',
        'entry_price': 45000.0,
        'stop_loss': 44100.0,    # 2% stop loss
        'take_profit': 46800.0   # 4% take profit (2:1 risk-reward)
    }
    
    print(f"\n🧪 Testing signal validation...")
    valid, message = coordinator.validate_strategy_signal('momentum_breakout', test_signal)
    print(f"   Validation: {'✅ PASSED' if valid else '❌ FAILED'}")
    print(f"   Message: {message}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 