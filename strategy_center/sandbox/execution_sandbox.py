#!/usr/bin/env python3
"""
Sandbox Trading Environment
Safe testing environment for crypto trading strategies before real money implementation
"""

import asyncio
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

@dataclass
class Position:
    position_id: str
    symbol: str
    side: str  # 'long' or 'short'
    size: float
    entry_price: float
    current_price: float
    pnl: float
    pnl_percentage: float
    opened_at: datetime
    metadata: Dict

@dataclass
class Trade:
    trade_id: str
    symbol: str
    side: str
    size: float
    entry_price: float
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percentage: Optional[float] = None
    opened_at: datetime = None
    closed_at: Optional[datetime] = None
    strategy: str = "manual"
    confidence: float = 0.5
    metadata: Dict = None

@dataclass
class Portfolio:
    total_value: float
    cash: float
    positions_value: float
    total_pnl: float
    total_pnl_percentage: float
    positions: List[Position]
    open_trades: int
    win_rate: float
    sharpe_ratio: float

class SandboxTradingEnvironment:
    """Comprehensive sandbox for testing crypto trading strategies"""
    
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.db_path = "data/sandbox_trading.db"
        self.setup_database()
        
        # Portfolio tracking
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[Trade] = []
        self.daily_pnl: List[float] = []
        
        # Risk management parameters
        self.max_position_size = 0.1  # 10% of portfolio per position
        self.max_total_exposure = 0.8  # 80% total exposure
        self.stop_loss_percentage = 0.05  # 5% stop loss
        self.take_profit_percentage = 0.15  # 15% take profit
        
        # Performance tracking
        self.performance_metrics = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "max_drawdown": 0.0,
            "best_trade": 0.0,
            "worst_trade": 0.0,
            "avg_trade_duration": 0.0
        }
        
    def setup_database(self):
        """Setup SQLite database for sandbox trading"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sandbox_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id TEXT UNIQUE NOT NULL,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                size REAL NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                pnl REAL,
                pnl_percentage REAL,
                opened_at REAL NOT NULL,
                closed_at REAL,
                strategy TEXT NOT NULL,
                confidence REAL NOT NULL,
                metadata TEXT
            )
        """)
        
        # Portfolio snapshots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                total_value REAL NOT NULL,
                cash REAL NOT NULL,
                positions_value REAL NOT NULL,
                total_pnl REAL NOT NULL,
                total_pnl_percentage REAL NOT NULL,
                open_trades INTEGER NOT NULL,
                metadata TEXT
            )
        """)
        
        # Strategy performance
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name TEXT NOT NULL,
                total_trades INTEGER NOT NULL,
                winning_trades INTEGER NOT NULL,
                losing_trades INTEGER NOT NULL,
                total_pnl REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                sharpe_ratio REAL NOT NULL,
                win_rate REAL NOT NULL,
                avg_return REAL NOT NULL,
                last_updated REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Sandbox trading database setup complete")
    
    async def execute_trade(self, symbol: str, side: str, size: float, 
                          current_price: float, strategy: str = "manual", 
                          confidence: float = 0.5, metadata: Dict = None) -> str:
        """Execute a trade in the sandbox environment"""
        
        # Risk management checks
        if not self._validate_trade(symbol, side, size, current_price):
            raise ValueError("Trade validation failed - risk management rules violated")
        
        trade_id = str(uuid.uuid4())
        
        # Calculate position size in dollars
        position_value = size * current_price
        
        # Check if we have enough capital
        if position_value > self.current_capital:
            raise ValueError(f"Insufficient capital. Required: ${position_value:.2f}, Available: ${self.current_capital:.2f}")
        
        # Create trade
        trade = Trade(
            trade_id=trade_id,
            symbol=symbol,
            side=side,
            size=size,
            entry_price=current_price,
            opened_at=datetime.now(),
            strategy=strategy,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        # Update capital and positions
        self.current_capital -= position_value
        
        position = Position(
            position_id=trade_id,
            symbol=symbol,
            side=side,
            size=size,
            entry_price=current_price,
            current_price=current_price,
            pnl=0.0,
            pnl_percentage=0.0,
            opened_at=datetime.now(),
            metadata={"strategy": strategy, "confidence": confidence}
        )
        
        self.positions[trade_id] = position
        self.trade_history.append(trade)
        
        # Store in database
        self._store_trade(trade)
        
        print(f"✅ Trade executed: {side.upper()} {size} {symbol} @ ${current_price:.2f}")
        print(f"   Trade ID: {trade_id}")
        print(f"   Strategy: {strategy}")
        print(f"   Remaining capital: ${self.current_capital:.2f}")
        
        return trade_id
    
    async def close_trade(self, trade_id: str, current_price: float, reason: str = "manual") -> float:
        """Close a trade and calculate P&L"""
        
        if trade_id not in self.positions:
            raise ValueError(f"Position {trade_id} not found")
        
        position = self.positions[trade_id]
        
        # Calculate P&L
        if position.side == "long":
            pnl = (current_price - position.entry_price) * position.size
        else:  # short
            pnl = (position.entry_price - current_price) * position.size
        
        pnl_percentage = (pnl / (position.entry_price * position.size)) * 100
        
        # Update trade in history
        for trade in self.trade_history:
            if trade.trade_id == trade_id:
                trade.exit_price = current_price
                trade.pnl = pnl
                trade.pnl_percentage = pnl_percentage
                trade.closed_at = datetime.now()
                break
        
        # Update capital
        position_value = position.size * current_price
        self.current_capital += position_value
        
        # Remove position
        del self.positions[trade_id]
        
        # Update performance metrics
        self._update_performance_metrics(pnl, pnl_percentage)
        
        # Update trade in database
        self._update_trade_in_db(trade_id, current_price, pnl, pnl_percentage)
        
        print(f"✅ Trade closed: {position.symbol} @ ${current_price:.2f}")
        print(f"   P&L: ${pnl:.2f} ({pnl_percentage:.2f}%)")
        print(f"   Reason: {reason}")
        print(f"   New capital: ${self.current_capital:.2f}")
        
        return pnl
    
    def update_positions(self, price_data: Dict[str, float]):
        """Update all positions with current market prices"""
        total_pnl = 0.0
        
        for position_id, position in self.positions.items():
            if position.symbol in price_data:
                current_price = price_data[position.symbol]
                
                # Calculate current P&L
                if position.side == "long":
                    pnl = (current_price - position.entry_price) * position.size
                else:  # short
                    pnl = (position.entry_price - current_price) * position.size
                
                pnl_percentage = (pnl / (position.entry_price * position.size)) * 100
                
                # Update position
                position.current_price = current_price
                position.pnl = pnl
                position.pnl_percentage = pnl_percentage
                
                total_pnl += pnl
                
                # Check stop loss and take profit
                self._check_risk_management(position_id, position)
        
        # Update total portfolio value
        positions_value = sum(pos.size * pos.current_price for pos in self.positions.values())
        total_value = self.current_capital + positions_value
        
        return total_value, total_pnl
    
    def get_portfolio_summary(self) -> Portfolio:
        """Get current portfolio summary"""
        positions_value = sum(pos.size * pos.current_price for pos in self.positions.values())
        total_value = self.current_capital + positions_value
        total_pnl = sum(pos.pnl for pos in self.positions.values())
        total_pnl_percentage = ((total_value - self.initial_capital) / self.initial_capital) * 100
        
        # Calculate win rate
        closed_trades = [t for t in self.trade_history if t.closed_at is not None]
        winning_trades = len([t for t in closed_trades if t.pnl and t.pnl > 0])
        win_rate = (winning_trades / len(closed_trades)) * 100 if closed_trades else 0
        
        # Calculate Sharpe ratio (simplified)
        returns = [t.pnl_percentage for t in closed_trades if t.pnl_percentage is not None]
        sharpe_ratio = (np.mean(returns) / np.std(returns)) if len(returns) > 1 and np.std(returns) > 0 else 0
        
        return Portfolio(
            total_value=total_value,
            cash=self.current_capital,
            positions_value=positions_value,
            total_pnl=total_pnl,
            total_pnl_percentage=total_pnl_percentage,
            positions=list(self.positions.values()),
            open_trades=len(self.positions),
            win_rate=win_rate,
            sharpe_ratio=sharpe_ratio
        )
    
    async def backtest_strategy(self, strategy_func, historical_data: pd.DataFrame, 
                         strategy_name: str = "backtest") -> Dict[str, Any]:
        """Backtest a trading strategy on historical data"""
        print(f"🔄 Backtesting strategy: {strategy_name}")
        
        # Reset environment
        self._reset_environment()
        
        backtest_results = {
            "strategy_name": strategy_name,
            "start_date": historical_data.index[0] if not historical_data.empty else datetime.now(),
            "end_date": historical_data.index[-1] if not historical_data.empty else datetime.now(),
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_return": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
            "win_rate": 0.0,
            "daily_returns": [],
            "equity_curve": []
        }
        
        # Track equity curve
        equity_values = [self.initial_capital]
        peak_value = self.initial_capital
        max_drawdown = 0.0
        
        # Iterate through historical data
        for i, (timestamp, row) in enumerate(historical_data.iterrows()):
            current_prices = {
                'BTC': row.get('BTC_price', 50000),
                'ETH': row.get('ETH_price', 3000),
                'ADA': row.get('ADA_price', 1.0)
            }
            
            # Update existing positions
            total_value, _ = self.update_positions(current_prices)
            
            # Call strategy function
            try:
                signals = strategy_func(row, self.get_portfolio_summary())
                
                # Execute signals
                for signal in signals:
                    symbol = signal.get('symbol', 'BTC')
                    action = signal.get('action', 'hold')
                    size = signal.get('size', 0.1)
                    confidence = signal.get('confidence', 0.5)
                    
                    if action == 'buy' and symbol in current_prices:
                        trade_id = await self.execute_trade(
                            symbol, 'long', size, current_prices[symbol], 
                            strategy_name, confidence
                        )
                    elif action == 'sell' and symbol in current_prices:
                        # Close any long positions
                        positions_to_close = [
                            pos_id for pos_id, pos in self.positions.items() 
                            if pos.symbol == symbol and pos.side == 'long'
                        ]
                        for pos_id in positions_to_close:
                            pnl = await self.close_trade(pos_id, current_prices[symbol], "strategy_signal")
                            
            except Exception as e:
                print(f"⚠️ Strategy error at {timestamp}: {e}")
                continue
            
            # Track equity curve
            total_value, _ = self.update_positions(current_prices)
            equity_values.append(total_value)
            
            # Calculate drawdown
            if total_value > peak_value:
                peak_value = total_value
            current_drawdown = (peak_value - total_value) / peak_value * 100
            max_drawdown = max(max_drawdown, current_drawdown)
            
            # Store daily returns
            if len(equity_values) > 1:
                daily_return = (equity_values[-1] - equity_values[-2]) / equity_values[-2] * 100
                backtest_results["daily_returns"].append(daily_return)
        
        # Calculate final metrics
        final_value = equity_values[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100
        
        closed_trades = [t for t in self.trade_history if t.closed_at is not None]
        winning_trades = len([t for t in closed_trades if t.pnl and t.pnl > 0])
        losing_trades = len([t for t in closed_trades if t.pnl and t.pnl <= 0])
        
        win_rate = (winning_trades / len(closed_trades)) * 100 if closed_trades else 0
        
        # Sharpe ratio
        returns = backtest_results["daily_returns"]
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if len(returns) > 1 and np.std(returns) > 0 else 0
        
        backtest_results.update({
            "total_trades": len(closed_trades),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "win_rate": win_rate,
            "equity_curve": equity_values,
            "final_value": final_value
        })
        
        print(f"✅ Backtest complete:")
        print(f"   Total Return: {total_return:.2f}%")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Max Drawdown: {max_drawdown:.2f}%")
        print(f"   Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"   Total Trades: {len(closed_trades)}")
        
        return backtest_results
    
    def _validate_trade(self, symbol: str, side: str, size: float, price: float) -> bool:
        """Validate trade against risk management rules"""
        position_value = size * price
        portfolio_value = self.current_capital + sum(pos.size * pos.current_price for pos in self.positions.values())
        
        # Check position size limit
        if position_value > (portfolio_value * self.max_position_size):
            print(f"❌ Position size too large: {position_value:.2f} > {portfolio_value * self.max_position_size:.2f}")
            return False
        
        # Check total exposure
        total_exposure = sum(pos.size * pos.current_price for pos in self.positions.values())
        if (total_exposure + position_value) > (portfolio_value * self.max_total_exposure):
            print(f"❌ Total exposure too high")
            return False
        
        return True
    
    def _check_risk_management(self, position_id: str, position: Position):
        """Check stop loss and take profit for a position"""
        # Stop loss check
        if position.pnl_percentage <= -self.stop_loss_percentage * 100:
            print(f"🛑 Stop loss triggered for {position.symbol}: {position.pnl_percentage:.2f}%")
            # Would normally close position here
        
        # Take profit check
        if position.pnl_percentage >= self.take_profit_percentage * 100:
            print(f"🎯 Take profit triggered for {position.symbol}: {position.pnl_percentage:.2f}%")
            # Would normally close position here
    
    def _update_performance_metrics(self, pnl: float, pnl_percentage: float):
        """Update overall performance metrics"""
        self.performance_metrics["total_trades"] += 1
        
        if pnl > 0:
            self.performance_metrics["winning_trades"] += 1
        else:
            self.performance_metrics["losing_trades"] += 1
        
        self.performance_metrics["total_pnl"] += pnl
        self.performance_metrics["best_trade"] = max(self.performance_metrics["best_trade"], pnl)
        self.performance_metrics["worst_trade"] = min(self.performance_metrics["worst_trade"], pnl)
    
    def _store_trade(self, trade: Trade):
        """Store trade in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sandbox_trades 
            (trade_id, symbol, side, size, entry_price, opened_at, strategy, confidence, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade.trade_id, trade.symbol, trade.side, trade.size, trade.entry_price,
            trade.opened_at.timestamp(), trade.strategy, trade.confidence,
            json.dumps(trade.metadata or {})
        ))
        
        conn.commit()
        conn.close()
    
    def _update_trade_in_db(self, trade_id: str, exit_price: float, pnl: float, pnl_percentage: float):
        """Update trade in database when closed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE sandbox_trades 
            SET exit_price = ?, pnl = ?, pnl_percentage = ?, closed_at = ?
            WHERE trade_id = ?
        """, (exit_price, pnl, pnl_percentage, datetime.now().timestamp(), trade_id))
        
        conn.commit()
        conn.close()
    
    def _reset_environment(self):
        """Reset trading environment for backtesting"""
        self.current_capital = self.initial_capital
        self.positions.clear()
        self.trade_history.clear()
        self.performance_metrics = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "max_drawdown": 0.0,
            "best_trade": 0.0,
            "worst_trade": 0.0,
            "avg_trade_duration": 0.0
        }

# Example strategy for testing
def simple_momentum_strategy(data_row, portfolio: Portfolio) -> List[Dict]:
    """Simple momentum strategy for testing"""
    signals = []
    
    # Simple buy signal: if price is above moving average and we have cash
    if hasattr(data_row, 'BTC_price') and portfolio.cash > 1000:
        if portfolio.open_trades < 3:  # Max 3 open positions
            signals.append({
                'symbol': 'BTC',
                'action': 'buy',
                'size': 0.01,  # Small position size
                'confidence': 0.6
            })
    
    return signals

if __name__ == "__main__":
    async def main():
        sandbox = SandboxTradingEnvironment(initial_capital=10000)
        
        print("🚀 Testing Sandbox Trading Environment...")
        
        # Test trade execution
        trade_id = await sandbox.execute_trade("BTC", "long", 0.1, 50000, "test_strategy", 0.8)
        
        # Simulate price change
        price_data = {"BTC": 52000}
        total_value, total_pnl = sandbox.update_positions(price_data)
        
        print(f"\n📊 Portfolio after price update:")
        portfolio = sandbox.get_portfolio_summary()
        print(f"   Total Value: ${portfolio.total_value:.2f}")
        print(f"   Total P&L: ${portfolio.total_pnl:.2f} ({portfolio.total_pnl_percentage:.2f}%)")
        print(f"   Open Trades: {portfolio.open_trades}")
        print(f"   Win Rate: {portfolio.win_rate:.1f}%")
        
        # Close trade
        pnl = await sandbox.close_trade(trade_id, 52000, "test_close")
        
        print("✅ Sandbox trading test complete!")
    
    asyncio.run(main()) 