#!/usr/bin/env python3
"""
🎯 REAL TRADING TRACKER - Expert CEO KPIs
$10K Portfolio starting June 4, 2025
"""

import sqlite3
from datetime import datetime, timedelta
import json
import logging

class RealTradingTracker:
    def __init__(self):
        self.db_path = "trading_tracker.db"
        self.starting_capital = 10000.00
        self.start_date = datetime(2025, 6, 4)
        self.setup_database()
        
    def setup_database(self):
        """Create trading tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Portfolio tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                portfolio_value REAL NOT NULL,
                daily_pnl REAL NOT NULL,
                total_pnl REAL NOT NULL,
                drawdown_pct REAL DEFAULT 0,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Individual trades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy TEXT NOT NULL,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,  -- BUY/SELL
                quantity REAL NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                entry_time TEXT NOT NULL,
                exit_time TEXT,
                pnl REAL DEFAULT 0,
                pnl_pct REAL DEFAULT 0,
                status TEXT DEFAULT 'OPEN',  -- OPEN/CLOSED
                notes TEXT
            )
        ''')
        
        # Strategy performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name TEXT NOT NULL,
                allocated_capital REAL NOT NULL,
                total_pnl REAL DEFAULT 0,
                total_trades INTEGER DEFAULT 0,
                winning_trades INTEGER DEFAULT 0,
                losing_trades INTEGER DEFAULT 0,
                win_rate REAL DEFAULT 0,
                max_drawdown REAL DEFAULT 0,
                sharpe_ratio REAL DEFAULT 0,
                last_updated TEXT NOT NULL
            )
        ''')
        
        # Risk metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                var_1day REAL DEFAULT 0,
                max_drawdown REAL DEFAULT 0,
                current_drawdown REAL DEFAULT 0,
                risk_per_trade REAL DEFAULT 2.0,
                positions_open INTEGER DEFAULT 0,
                total_exposure REAL DEFAULT 0,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize with starting values
        self.initialize_portfolio()
        
    def initialize_portfolio(self):
        """Initialize portfolio with starting values"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if we already have today's entry
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT * FROM portfolio_history WHERE date = ?', (today,))
        
        if not cursor.fetchone():
            # Add starting portfolio value
            cursor.execute('''
                INSERT INTO portfolio_history 
                (date, portfolio_value, daily_pnl, total_pnl, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (today, self.starting_capital, 0.0, 0.0, datetime.now().isoformat()))
            
        # Initialize strategies
        strategies = [
            'AI_Momentum_Breakout',
            'Mean_Reversion_Master', 
            'Lightning_Breakout_Pro',
            'Smart_Swing_Trader'
        ]
        
        for strategy in strategies:
            cursor.execute('SELECT * FROM strategy_performance WHERE strategy_name = ?', (strategy,))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO strategy_performance 
                    (strategy_name, allocated_capital, last_updated)
                    VALUES (?, ?, ?)
                ''', (strategy, 10000.0, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
    def get_expert_kpis(self):
        """Get expert-level KPIs for CEO dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest portfolio data
        cursor.execute('''
            SELECT * FROM portfolio_history 
            ORDER BY date DESC LIMIT 1
        ''')
        latest_portfolio = cursor.fetchone()
        
        # Get all trades
        cursor.execute('SELECT * FROM trades')
        all_trades = cursor.fetchall()
        
        # Get strategy performance
        cursor.execute('SELECT * FROM strategy_performance')
        strategies = cursor.fetchall()
        
        # Calculate expert metrics
        if latest_portfolio:
            current_value = latest_portfolio[2]  # portfolio_value
            total_pnl = latest_portfolio[4]      # total_pnl
        else:
            current_value = self.starting_capital
            total_pnl = 0.0
            
        # Trading statistics
        total_trades = len(all_trades)
        closed_trades = [t for t in all_trades if t[12] == 'CLOSED']  # status
        winning_trades = [t for t in closed_trades if t[9] > 0]       # pnl > 0
        losing_trades = [t for t in closed_trades if t[9] < 0]        # pnl < 0
        
        win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
        
        # Average win/loss
        avg_win = sum(t[9] for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t[9] for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        # Days trading
        days_trading = (datetime.now() - self.start_date).days
        
        # Strategy data
        strategy_data = {}
        for strategy in strategies:
            strategy_data[strategy[1]] = {  # strategy_name
                'allocated_capital': strategy[2],
                'pnl': strategy[3],
                'trades': strategy[4],
                'win_rate': strategy[6],
                'status': 'Live Trading' if strategy[4] > 0 else 'Sandbox Testing'
            }
        
        conn.close()
        
        return {
            # CORE METRICS
            'portfolio_value': current_value,
            'starting_value': self.starting_capital,
            'total_pnl': total_pnl,
            'total_return_pct': (total_pnl / self.starting_capital * 100) if self.starting_capital > 0 else 0,
            'daily_pnl': total_pnl / max(days_trading, 1) if days_trading > 0 else 0,
            
            # TRADING METRICS
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'average_win': avg_win,
            'average_loss': avg_loss,
            
            # RISK METRICS (Critical for CEO)
            'max_drawdown': 0.0,  # Will calculate from history
            'current_drawdown': 0.0,
            'risk_per_trade': 2.0,  # 2% per trade (expert recommendation)
            'max_daily_loss_limit': 250.0,  # 2.5% of $10K
            
            # STRATEGY ALLOCATION
            'strategies': strategy_data,
            
            # TIME METRICS
            'days_trading': days_trading,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'last_update': datetime.now().isoformat()
        }
    
    def add_trade(self, strategy, symbol, side, quantity, entry_price, notes=""):
        """Add a new trade to tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trades 
            (strategy, symbol, side, quantity, entry_price, entry_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (strategy, symbol, side, quantity, entry_price, datetime.now().isoformat(), notes))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Trade added: {side} {quantity} {symbol} @ ${entry_price}")
        
    def close_trade(self, trade_id, exit_price):
        """Close a trade and calculate P&L"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get trade details
        cursor.execute('SELECT * FROM trades WHERE id = ?', (trade_id,))
        trade = cursor.fetchone()
        
        if trade and trade[12] == 'OPEN':  # status
            entry_price = trade[5]
            quantity = trade[4]
            side = trade[3]
            
            # Calculate P&L
            if side == 'BUY':
                pnl = (exit_price - entry_price) * quantity
            else:  # SELL
                pnl = (entry_price - exit_price) * quantity
                
            pnl_pct = (pnl / (entry_price * quantity)) * 100
            
            # Update trade
            cursor.execute('''
                UPDATE trades 
                SET exit_price = ?, exit_time = ?, pnl = ?, pnl_pct = ?, status = 'CLOSED'
                WHERE id = ?
            ''', (exit_price, datetime.now().isoformat(), pnl, pnl_pct, trade_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Trade closed: P&L ${pnl:.2f} ({pnl_pct:.2f}%)")
            return pnl
        else:
            conn.close()
            print("❌ Trade not found or already closed")
            return 0
            
    def update_portfolio_value(self, new_value):
        """Update daily portfolio value"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get previous day value
        cursor.execute('''
            SELECT portfolio_value FROM portfolio_history 
            WHERE date < ? ORDER BY date DESC LIMIT 1
        ''', (today,))
        
        previous_value = cursor.fetchone()
        previous_value = previous_value[0] if previous_value else self.starting_capital
        
        daily_pnl = new_value - previous_value
        total_pnl = new_value - self.starting_capital
        
        # Update or insert today's value
        cursor.execute('''
            INSERT OR REPLACE INTO portfolio_history 
            (date, portfolio_value, daily_pnl, total_pnl, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (today, new_value, daily_pnl, total_pnl, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"📊 Portfolio updated: ${new_value:.2f} (Daily P&L: ${daily_pnl:.2f})")

# Initialize tracker
if __name__ == "__main__":
    tracker = RealTradingTracker()
    kpis = tracker.get_expert_kpis()
    print("🎯 Expert KPIs initialized for $10K portfolio")
    print(json.dumps(kpis, indent=2)) 