#!/usr/bin/env python3
"""
Strategy Signal Bridge - ORION PHASE 2
Connects unified signals to trading strategies for intelligent execution
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import sys
import os

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core_orchestration.signal_aggregator import SignalAggregator, MarketSignal, UnifiedSignal

@dataclass
class StrategySignal:
    strategy_id: str
    symbol: str
    action: str  # "BUY", "SELL", "HOLD", "CLOSE"
    quantity: float
    confidence: float
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    reasoning: str
    source_signals: List[str]
    timestamp: float
    risk_score: float
    expected_return: float

@dataclass
class StrategyPerformance:
    strategy_id: str
    total_signals: int
    successful_signals: int
    failed_signals: int
    avg_return: float
    win_rate: float
    sharpe_ratio: float
    max_drawdown: float
    last_updated: float

class StrategySignalBridge:
    """
    Bridge between Signal Aggregator and Trading Strategies
    Translates market signals into actionable trading decisions
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/strategy_signals.db"
        self.logger = self.setup_logging()
        self.setup_database()
        
        # Strategy configurations
        self.strategy_configs = {
            "momentum_strategy": {
                "signal_threshold": 0.7,
                "risk_per_trade": 0.02,
                "max_positions": 3,
                "time_horizon": "SHORT",
                "signal_types": ["TWITTER", "RSS", "SENTIMENT"]
            },
            "mean_reversion_strategy": {
                "signal_threshold": 0.6,
                "risk_per_trade": 0.015,
                "max_positions": 5,
                "time_horizon": "MEDIUM",
                "signal_types": ["RSS", "ONCHAIN"]
            },
            "breakout_strategy": {
                "signal_threshold": 0.8,
                "risk_per_trade": 0.025,
                "max_positions": 2,
                "time_horizon": "SHORT",
                "signal_types": ["ONCHAIN", "TWITTER"]
            },
            "correlation_strategy": {
                "signal_threshold": 0.75,
                "risk_per_trade": 0.02,
                "max_positions": 4,
                "time_horizon": "MEDIUM",
                "signal_types": ["RSS", "TWITTER", "ONCHAIN", "SENTIMENT"]
            }
        }
        
        # Signal aggregator
        self.signal_aggregator = SignalAggregator()
        
        self.logger.info("🌉 Strategy Signal Bridge initialized - Phase 2 Enhanced Intelligence")
    
    def setup_database(self):
        """Setup strategy signals database"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Strategy signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity REAL NOT NULL,
                confidence REAL NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                reasoning TEXT NOT NULL,
                source_signals TEXT NOT NULL,
                timestamp REAL NOT NULL,
                risk_score REAL NOT NULL,
                expected_return REAL NOT NULL,
                executed BOOLEAN DEFAULT 0,
                result REAL DEFAULT 0.0
            )
        """)
        
        # Strategy performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id TEXT UNIQUE NOT NULL,
                total_signals INTEGER DEFAULT 0,
                successful_signals INTEGER DEFAULT 0,
                failed_signals INTEGER DEFAULT 0,
                avg_return REAL DEFAULT 0.0,
                win_rate REAL DEFAULT 0.0,
                sharpe_ratio REAL DEFAULT 0.0,
                max_drawdown REAL DEFAULT 0.0,
                last_updated REAL NOT NULL
            )
        """)
        
        # Active positions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                entry_price REAL NOT NULL,
                quantity REAL NOT NULL,
                stop_loss REAL,
                take_profit REAL,
                timestamp REAL NOT NULL,
                current_pnl REAL DEFAULT 0.0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def setup_logging(self):
        """Setup strategy signal bridge logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - StrategySignalBridge - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/strategy_signal_bridge.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def process_market_signals(self) -> Dict[str, Any]:
        """Process market signals and generate strategy signals"""
        self.logger.info("🔄 Processing market signals for strategy execution...")
        start_time = time.time()
        
        # 1. Get latest market signals from aggregator
        signal_summary = self.signal_aggregator.collect_all_signals()
        market_signals = self.get_recent_market_signals()
        
        # 2. Process signals for each strategy
        all_strategy_signals = []
        
        for strategy_id, config in self.strategy_configs.items():
            strategy_signals = self.generate_strategy_signals(strategy_id, market_signals, config)
            all_strategy_signals.extend(strategy_signals)
            
            # Store strategy signals
            for signal in strategy_signals:
                self.store_strategy_signal(signal)
        
        # 3. Update strategy performance
        self.update_strategy_performance()
        
        execution_time = time.time() - start_time
        
        summary = {
            "market_signals_processed": len(market_signals),
            "strategy_signals_generated": len(all_strategy_signals),
            "strategies_active": len(self.strategy_configs),
            "execution_time": execution_time,
            "signal_breakdown": signal_summary,
            "top_strategy_signals": [
                {
                    "strategy": signal.strategy_id,
                    "symbol": signal.symbol,
                    "action": signal.action,
                    "confidence": signal.confidence,
                    "expected_return": signal.expected_return
                } for signal in sorted(all_strategy_signals, key=lambda x: x.confidence, reverse=True)[:5]
            ]
        }
        
        self.logger.info(f"✅ Strategy signal processing complete ({execution_time:.2f}s)")
        self.logger.info(f"   📊 Market signals: {len(market_signals)}")
        self.logger.info(f"   🎯 Strategy signals: {len(all_strategy_signals)}")
        self.logger.info(f"   🏗️ Strategies active: {len(self.strategy_configs)}")
        
        return summary
    
    def generate_strategy_signals(self, strategy_id: str, market_signals: List[MarketSignal], config: Dict[str, Any]) -> List[StrategySignal]:
        """Generate trading signals for a specific strategy"""
        strategy_signals = []
        
        # Filter market signals based on strategy configuration
        relevant_signals = self.filter_signals_for_strategy(market_signals, config)
        
        for market_signal in relevant_signals:
            # Check if signal meets strategy threshold
            if market_signal.confidence_score < config["signal_threshold"]:
                continue
            
            # Check if we're already at max positions for this strategy
            active_positions = self.get_active_positions(strategy_id)
            if len(active_positions) >= config["max_positions"]:
                continue
            
            # Generate strategy signal based on strategy type
            if strategy_id == "momentum_strategy":
                signal = self.generate_momentum_signal(strategy_id, market_signal, config)
            elif strategy_id == "mean_reversion_strategy":
                signal = self.generate_mean_reversion_signal(strategy_id, market_signal, config)
            elif strategy_id == "breakout_strategy":
                signal = self.generate_breakout_signal(strategy_id, market_signal, config)
            elif strategy_id == "correlation_strategy":
                signal = self.generate_correlation_signal(strategy_id, market_signal, config)
            else:
                continue
            
            if signal:
                strategy_signals.append(signal)
        
        return strategy_signals
    
    def filter_signals_for_strategy(self, market_signals: List[MarketSignal], config: Dict[str, Any]) -> List[MarketSignal]:
        """Filter market signals based on strategy configuration"""
        filtered_signals = []
        
        for signal in market_signals:
            # Check if signal types match strategy requirements
            if any(source in config["signal_types"] for source in signal.dominant_sources):
                filtered_signals.append(signal)
        
        return filtered_signals
    
    def generate_momentum_signal(self, strategy_id: str, market_signal: MarketSignal, config: Dict[str, Any]) -> Optional[StrategySignal]:
        """Generate momentum strategy signal"""
        # Momentum strategy: Buy on strong bullish signals, sell on strong bearish signals
        
        if market_signal.overall_direction == "BULLISH" and market_signal.confidence_score > 0.7:
            action = "BUY"
            expected_return = market_signal.predicted_impact * 2  # Momentum amplification
        elif market_signal.overall_direction == "BEARISH" and market_signal.confidence_score > 0.7:
            action = "SELL"
            expected_return = market_signal.predicted_impact * 1.5
        else:
            return None
        
        # Calculate position size based on risk
        quantity = self.calculate_position_size(config["risk_per_trade"], market_signal.risk_score)
        
        # Set stop loss and take profit
        stop_loss_pct = 0.05 if action == "BUY" else -0.05  # 5% stop loss
        take_profit_pct = 0.15 if action == "BUY" else -0.15  # 15% take profit
        
        reasoning = f"Momentum signal: {market_signal.overall_direction} with {market_signal.confidence_score:.2f} confidence from {market_signal.signal_count} sources"
        
        return StrategySignal(
            strategy_id=strategy_id,
            symbol=market_signal.symbol,
            action=action,
            quantity=quantity,
            confidence=market_signal.confidence_score,
            entry_price=None,  # To be filled by execution engine
            stop_loss=stop_loss_pct,
            take_profit=take_profit_pct,
            reasoning=reasoning,
            source_signals=[f"MARKET_{market_signal.symbol}_{int(market_signal.timestamp)}"],
            timestamp=time.time(),
            risk_score=market_signal.risk_score,
            expected_return=expected_return
        )
    
    def generate_mean_reversion_signal(self, strategy_id: str, market_signal: MarketSignal, config: Dict[str, Any]) -> Optional[StrategySignal]:
        """Generate mean reversion strategy signal"""
        # Mean reversion: Buy on oversold conditions, sell on overbought conditions
        
        # Look for signals with high risk (conflicting directions) indicating potential reversal
        if market_signal.risk_score > 0.6 and market_signal.confidence_score > 0.6:
            # Contrarian approach - go opposite to current sentiment
            if market_signal.overall_direction == "BEARISH":
                action = "BUY"
                reasoning = "Mean reversion: Oversold condition detected"
            elif market_signal.overall_direction == "BULLISH":
                action = "SELL"
                reasoning = "Mean reversion: Overbought condition detected"
            else:
                return None
        else:
            return None
        
        quantity = self.calculate_position_size(config["risk_per_trade"], market_signal.risk_score)
        expected_return = market_signal.predicted_impact * 0.8  # Conservative expectation
        
        return StrategySignal(
            strategy_id=strategy_id,
            symbol=market_signal.symbol,
            action=action,
            quantity=quantity,
            confidence=market_signal.confidence_score * 0.8,  # Lower confidence for contrarian
            entry_price=None,
            stop_loss=0.03 if action == "BUY" else -0.03,  # Tighter stop loss
            take_profit=0.08 if action == "BUY" else -0.08,  # Conservative take profit
            reasoning=reasoning,
            source_signals=[f"MARKET_{market_signal.symbol}_{int(market_signal.timestamp)}"],
            timestamp=time.time(),
            risk_score=market_signal.risk_score,
            expected_return=expected_return
        )
    
    def generate_breakout_signal(self, strategy_id: str, market_signal: MarketSignal, config: Dict[str, Any]) -> Optional[StrategySignal]:
        """Generate breakout strategy signal"""
        # Breakout strategy: High confidence, high impact signals
        
        if (market_signal.confidence_score > 0.8 and 
            market_signal.predicted_impact > 0.05 and
            "ONCHAIN" in market_signal.dominant_sources):
            
            action = "BUY" if market_signal.overall_direction == "BULLISH" else "SELL"
            quantity = self.calculate_position_size(config["risk_per_trade"], market_signal.risk_score)
            expected_return = market_signal.predicted_impact * 3  # High return expectation
            
            reasoning = f"Breakout signal: High confidence ({market_signal.confidence_score:.2f}) with onchain confirmation"
            
            return StrategySignal(
                strategy_id=strategy_id,
                symbol=market_signal.symbol,
                action=action,
                quantity=quantity,
                confidence=market_signal.confidence_score,
                entry_price=None,
                stop_loss=0.04 if action == "BUY" else -0.04,
                take_profit=0.20 if action == "BUY" else -0.20,  # Aggressive take profit
                reasoning=reasoning,
                source_signals=[f"MARKET_{market_signal.symbol}_{int(market_signal.timestamp)}"],
                timestamp=time.time(),
                risk_score=market_signal.risk_score,
                expected_return=expected_return
            )
        
        return None
    
    def generate_correlation_signal(self, strategy_id: str, market_signal: MarketSignal, config: Dict[str, Any]) -> Optional[StrategySignal]:
        """Generate correlation strategy signal"""
        # Correlation strategy: Multiple source confirmation
        
        if (market_signal.signal_count >= 3 and 
            len(market_signal.dominant_sources) >= 2 and
            market_signal.confidence_score > 0.75):
            
            action = "BUY" if market_signal.overall_direction == "BULLISH" else "SELL"
            quantity = self.calculate_position_size(config["risk_per_trade"], market_signal.risk_score)
            expected_return = market_signal.predicted_impact * 1.5
            
            reasoning = f"Multi-source correlation: {market_signal.signal_count} signals from {len(market_signal.dominant_sources)} sources"
            
            return StrategySignal(
                strategy_id=strategy_id,
                symbol=market_signal.symbol,
                action=action,
                quantity=quantity,
                confidence=market_signal.confidence_score,
                entry_price=None,
                stop_loss=0.06 if action == "BUY" else -0.06,
                take_profit=0.12 if action == "BUY" else -0.12,
                reasoning=reasoning,
                source_signals=[f"MARKET_{market_signal.symbol}_{int(market_signal.timestamp)}"],
                timestamp=time.time(),
                risk_score=market_signal.risk_score,
                expected_return=expected_return
            )
        
        return None
    
    def calculate_position_size(self, risk_per_trade: float, risk_score: float) -> float:
        """Calculate position size based on risk management"""
        # Adjust position size based on signal risk
        base_position = 1000  # Base position size in USD
        risk_adjustment = 1 - (risk_score * 0.5)  # Reduce size for higher risk
        
        return base_position * risk_per_trade * risk_adjustment
    
    def get_recent_market_signals(self) -> List[MarketSignal]:
        """Get recent market signals from unified signals database"""
        market_signals = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/enhanced_signals.db")
            cursor = conn.cursor()
            
            # Get recent market signals
            recent_signals = cursor.execute("""
                SELECT symbol, overall_direction, confidence_score, signal_count,
                       bullish_signals, bearish_signals, dominant_sources,
                       predicted_impact, risk_score, timestamp
                FROM market_signals 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 20
            """, (time.time() - 3600,)).fetchall()  # Last hour
            
            conn.close()
            
            for signal_data in recent_signals:
                symbol, direction, confidence, count, bullish, bearish, sources, impact, risk, timestamp = signal_data
                
                market_signal = MarketSignal(
                    symbol=symbol,
                    overall_direction=direction,
                    confidence_score=confidence,
                    signal_count=count,
                    bullish_signals=bullish,
                    bearish_signals=bearish,
                    dominant_sources=json.loads(sources),
                    predicted_impact=impact,
                    risk_score=risk,
                    timestamp=timestamp
                )
                market_signals.append(market_signal)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error getting market signals: {e}")
        
        return market_signals
    
    def get_active_positions(self, strategy_id: str) -> List[Dict[str, Any]]:
        """Get active positions for a strategy"""
        positions = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            position_data = cursor.execute("""
                SELECT symbol, entry_price, quantity, stop_loss, take_profit, timestamp, current_pnl
                FROM active_positions 
                WHERE strategy_id = ?
            """, (strategy_id,)).fetchall()
            
            conn.close()
            
            for pos in position_data:
                symbol, entry, qty, sl, tp, ts, pnl = pos
                positions.append({
                    "symbol": symbol,
                    "entry_price": entry,
                    "quantity": qty,
                    "stop_loss": sl,
                    "take_profit": tp,
                    "timestamp": ts,
                    "current_pnl": pnl
                })
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error getting active positions: {e}")
        
        return positions
    
    def store_strategy_signal(self, signal: StrategySignal):
        """Store strategy signal in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO strategy_signals 
            (strategy_id, symbol, action, quantity, confidence, entry_price,
             stop_loss, take_profit, reasoning, source_signals, timestamp,
             risk_score, expected_return)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            signal.strategy_id, signal.symbol, signal.action, signal.quantity,
            signal.confidence, signal.entry_price, signal.stop_loss,
            signal.take_profit, signal.reasoning, json.dumps(signal.source_signals),
            signal.timestamp, signal.risk_score, signal.expected_return
        ))
        
        conn.commit()
        conn.close()
    
    def update_strategy_performance(self):
        """Update strategy performance metrics"""
        for strategy_id in self.strategy_configs.keys():
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Calculate performance metrics
                performance_data = cursor.execute("""
                    SELECT COUNT(*) as total, 
                           SUM(CASE WHEN result > 0 THEN 1 ELSE 0 END) as successful,
                           AVG(result) as avg_return,
                           MIN(result) as max_drawdown
                    FROM strategy_signals 
                    WHERE strategy_id = ? AND executed = 1
                """, (strategy_id,)).fetchone()
                
                if performance_data and performance_data[0] > 0:
                    total, successful, avg_return, max_drawdown = performance_data
                    win_rate = successful / total if total > 0 else 0
                    
                    # Store performance
                    cursor.execute("""
                        INSERT OR REPLACE INTO strategy_performance
                        (strategy_id, total_signals, successful_signals, failed_signals,
                         avg_return, win_rate, max_drawdown, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        strategy_id, total, successful, total - successful,
                        avg_return or 0, win_rate, abs(max_drawdown or 0), time.time()
                    ))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                self.logger.warning(f"⚠️ Error updating performance for {strategy_id}: {e}")

# Test function
async def main():
    """Test the Strategy Signal Bridge"""
    print("🌉 Testing Strategy Signal Bridge - Phase 2 Enhanced Intelligence...")
    
    bridge = StrategySignalBridge()
    results = bridge.process_market_signals()
    
    print(f"✅ Strategy Signal Processing Complete:")
    print(f"   📊 Market signals processed: {results['market_signals_processed']}")
    print(f"   🎯 Strategy signals generated: {results['strategy_signals_generated']}")
    print(f"   🏗️ Strategies active: {results['strategies_active']}")
    print(f"   ⏱️ Execution time: {results['execution_time']:.2f}s")
    
    print("\n🔥 Top Strategy Signals:")
    for signal in results['top_strategy_signals']:
        print(f"   {signal['strategy']}: {signal['action']} {signal['symbol']} (confidence: {signal['confidence']:.2f})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())