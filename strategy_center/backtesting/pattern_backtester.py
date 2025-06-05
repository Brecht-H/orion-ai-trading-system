#!/usr/bin/env python3
"""
Advanced Pattern Backtesting Framework - Week 2 Enhancement
Validates trading patterns against historical data with comprehensive metrics
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import sqlite3
from pathlib import Path
import json
from dataclasses import dataclass, asdict
import warnings
warnings.filterwarnings('ignore')

@dataclass
class BacktestResult:
    pattern_id: str
    symbol: str
    start_date: datetime
    end_date: datetime
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_return: float
    total_return_percentage: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    calmar_ratio: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    avg_trade_duration: float
    best_trade: float
    worst_trade: float
    volatility: float
    metadata: Dict[str, Any]

@dataclass
class PatternBacktestResult:
    pattern_type: str
    total_patterns_tested: int
    successful_patterns: int
    pattern_success_rate: float
    avg_performance_metrics: Dict[str, float]
    best_performing_pattern: str
    worst_performing_pattern: str
    recommended_parameters: Dict[str, Any]
    market_conditions_analysis: Dict[str, Any]
    improvement_suggestions: List[str]

class AdvancedPatternBacktester:
    """
    Advanced backtesting framework for trading patterns
    Provides comprehensive validation and performance analysis
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/backtest_results.db"
        self.patterns_db = "databases/sqlite_dbs/trading_patterns.db"
        self.setup_databases()
        
        # Backtesting parameters
        self.initial_capital = 10000
        self.commission_rate = 0.001  # 0.1% commission
        self.slippage_rate = 0.0005   # 0.05% slippage
        
        # Performance metrics
        self.risk_free_rate = 0.02    # 2% annual risk-free rate
        
    def setup_databases(self):
        """Initialize backtesting databases"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Backtest results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backtest_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                total_trades INTEGER NOT NULL,
                winning_trades INTEGER NOT NULL,
                losing_trades INTEGER NOT NULL,
                win_rate REAL NOT NULL,
                total_return REAL NOT NULL,
                total_return_percentage REAL NOT NULL,
                sharpe_ratio REAL NOT NULL,
                sortino_ratio REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                calmar_ratio REAL NOT NULL,
                profit_factor REAL NOT NULL,
                avg_win REAL NOT NULL,
                avg_loss REAL NOT NULL,
                avg_trade_duration REAL NOT NULL,
                best_trade REAL NOT NULL,
                worst_trade REAL NOT NULL,
                volatility REAL NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        # Pattern performance summary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_performance_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                test_date TEXT NOT NULL,
                total_patterns_tested INTEGER NOT NULL,
                successful_patterns INTEGER NOT NULL,
                pattern_success_rate REAL NOT NULL,
                avg_win_rate REAL NOT NULL,
                avg_sharpe_ratio REAL NOT NULL,
                avg_max_drawdown REAL NOT NULL,
                recommended_parameters TEXT NOT NULL,
                improvement_suggestions TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Backtesting databases initialized")
    
    async def run_comprehensive_backtesting(self, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Run comprehensive backtesting on all available patterns
        """
        print(f"📊 Running comprehensive backtesting (lookback: {lookback_days} days)...")
        
        # 1. Load patterns to test
        patterns = await self.load_patterns_for_testing()
        
        # 2. Load historical market data
        historical_data = await self.load_historical_data(lookback_days)
        
        # 3. Run backtests for each pattern
        backtest_results = []
        for pattern in patterns:
            try:
                result = await self.backtest_single_pattern(pattern, historical_data)
                if result:
                    backtest_results.append(result)
            except Exception as e:
                print(f"⚠️ Error backtesting pattern {pattern.get('pattern_id', 'unknown')}: {e}")
                continue
        
        # 4. Analyze results by pattern type
        pattern_analysis = await self.analyze_pattern_performance(backtest_results)
        
        # 5. Generate improvement recommendations
        recommendations = await self.generate_improvement_recommendations(backtest_results)
        
        # 6. Create comprehensive report
        comprehensive_results = {
            'timestamp': datetime.now().isoformat(),
            'lookback_days': lookback_days,
            'patterns_tested': len(patterns),
            'successful_backtests': len(backtest_results),
            'backtest_results': [asdict(result) for result in backtest_results],
            'pattern_analysis': pattern_analysis,
            'improvement_recommendations': recommendations,
            'overall_performance': await self.calculate_overall_performance(backtest_results)
        }
        
        # 7. Store results
        await self.store_backtest_results(comprehensive_results)
        
        print(f"✅ Backtesting complete:")
        print(f"   📊 Patterns tested: {len(patterns)}")
        print(f"   ✅ Successful backtests: {len(backtest_results)}")
        print(f"   📈 Avg win rate: {comprehensive_results['overall_performance']['avg_win_rate']:.2%}")
        
        return comprehensive_results
    
    async def load_patterns_for_testing(self) -> List[Dict[str, Any]]:
        """Load trading patterns for backtesting"""
        try:
            conn = sqlite3.connect(self.patterns_db)
            
            query = """
                SELECT * FROM trading_patterns 
                WHERE confidence > 0.5 
                ORDER BY confidence DESC 
                LIMIT 20
            """
            
            patterns_df = pd.read_sql_query(query, conn)
            conn.close()
            
            if patterns_df.empty:
                print("⚠️ No patterns found for backtesting, creating sample patterns...")
                return await self.create_sample_patterns()
            
            # Convert to list of dictionaries
            patterns = patterns_df.to_dict('records')
            
            # Parse JSON fields
            for pattern in patterns:
                pattern['symbols'] = json.loads(pattern['symbols'])
                pattern['entry_conditions'] = json.loads(pattern['entry_conditions'])
                pattern['exit_conditions'] = json.loads(pattern['exit_conditions'])
                pattern['risk_parameters'] = json.loads(pattern['risk_parameters'])
                pattern['metadata'] = json.loads(pattern['metadata'])
            
            return patterns
            
        except Exception as e:
            print(f"⚠️ Error loading patterns: {e}")
            return await self.create_sample_patterns()
    
    async def create_sample_patterns(self) -> List[Dict[str, Any]]:
        """Create sample patterns for testing"""
        sample_patterns = [
            {
                'pattern_id': 'sample_momentum_breakout_001',
                'pattern_type': 'momentum_breakout',
                'symbols': ['BTC'],
                'confidence': 0.7,
                'strength': 4,
                'entry_conditions': {'min_confidence': 0.6, 'breakout_threshold': 0.02},
                'exit_conditions': {'stop_loss_percentage': 0.02, 'take_profit_ratio': 2.5},
                'risk_parameters': {'max_position_size': 0.05, 'stop_loss_percentage': 0.02},
                'expected_duration': 120,
                'historical_success_rate': 0.65,
                'metadata': {'test_pattern': True}
            },
            {
                'pattern_id': 'sample_mean_reversion_001',
                'pattern_type': 'mean_reversion',
                'symbols': ['ETH'],
                'confidence': 0.6,
                'strength': 3,
                'entry_conditions': {'min_confidence': 0.5, 'rsi_oversold': 30},
                'exit_conditions': {'stop_loss_percentage': 0.015, 'take_profit_ratio': 2.0},
                'risk_parameters': {'max_position_size': 0.04, 'stop_loss_percentage': 0.015},
                'expected_duration': 180,
                'historical_success_rate': 0.60,
                'metadata': {'test_pattern': True}
            }
        ]
        
        return sample_patterns
    
    async def load_historical_data(self, lookback_days: int) -> pd.DataFrame:
        """Load historical market data for backtesting"""
        try:
            # Try to load from free sources database
            free_data_db = "databases/sqlite_dbs/free_sources_data.db"
            if Path(free_data_db).exists():
                conn = sqlite3.connect(free_data_db)
                
                end_date = datetime.now()
                start_date = end_date - timedelta(days=lookback_days)
                
                query = """
                    SELECT timestamp, source_name, data_type, symbol, value
                    FROM free_data 
                    WHERE timestamp >= ? AND timestamp <= ?
                    AND (data_type = 'price' OR data_type = 'volume')
                    ORDER BY timestamp
                """
                
                df = pd.read_sql_query(query, conn, params=[start_date.timestamp(), end_date.timestamp()])
                conn.close()
                
                if not df.empty:
                    return self.process_historical_data(df)
            
            # Generate sample historical data
            return await self.generate_sample_historical_data(lookback_days)
            
        except Exception as e:
            print(f"⚠️ Error loading historical data: {e}")
            return await self.generate_sample_historical_data(lookback_days)
    
    def process_historical_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process raw historical data into backtesting format"""
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Create pivot table
        pivot_df = df.pivot_table(
            index='datetime',
            columns=['source_name', 'data_type'],
            values='value',
            aggfunc='mean'
        )
        
        # Flatten column names
        pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]
        
        # Forward fill missing values
        pivot_df = pivot_df.fillna(method='ffill').fillna(method='bfill')
        
        return pivot_df
    
    async def generate_sample_historical_data(self, lookback_days: int) -> pd.DataFrame:
        """Generate sample historical data for backtesting"""
        print(f"🔧 Generating {lookback_days} days of sample historical data...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        dates = pd.date_range(start=start_date, end=end_date, freq='1H')
        
        np.random.seed(42)  # For reproducible results
        
        # Generate price data with realistic movements
        btc_prices = []
        eth_prices = []
        
        btc_start = 50000
        eth_start = 3000
        
        for i in range(len(dates)):
            # Add some trending and volatility
            trend_factor = 0.0001 * i  # Slight upward trend
            volatility = np.random.randn() * 0.02  # 2% volatility
            
            btc_price = btc_start * (1 + trend_factor + volatility)
            eth_price = eth_start * (1 + trend_factor + volatility * 0.8)  # ETH slightly less volatile
            
            btc_prices.append(btc_price)
            eth_prices.append(eth_price)
            
            # Update starts for next iteration (cumulative)
            btc_start = btc_price
            eth_start = eth_price
        
        sample_data = pd.DataFrame(index=dates)
        sample_data['BTC_price'] = btc_prices
        sample_data['ETH_price'] = eth_prices
        sample_data['BTC_volume'] = np.random.exponential(1000000, len(dates))
        sample_data['ETH_volume'] = np.random.exponential(500000, len(dates))
        
        return sample_data
    
    async def backtest_single_pattern(self, pattern: Dict[str, Any], historical_data: pd.DataFrame) -> Optional[BacktestResult]:
        """Backtest a single pattern against historical data"""
        try:
            pattern_id = pattern['pattern_id']
            symbols = pattern['symbols']
            
            # For each symbol in the pattern
            for symbol in symbols:
                # Get price data for this symbol
                price_column = f"{symbol}_price"
                if price_column not in historical_data.columns:
                    continue
                
                price_data = historical_data[price_column].dropna()
                if len(price_data) < 50:  # Need minimum data points
                    continue
                
                # Run the backtest simulation
                trades = await self.simulate_pattern_trades(pattern, price_data)
                
                if not trades:
                    continue
                
                # Calculate performance metrics
                performance = self.calculate_performance_metrics(trades, price_data)
                
                # Create backtest result
                result = BacktestResult(
                    pattern_id=pattern_id,
                    symbol=symbol,
                    start_date=price_data.index[0].to_pydatetime(),
                    end_date=price_data.index[-1].to_pydatetime(),
                    total_trades=performance['total_trades'],
                    winning_trades=performance['winning_trades'],
                    losing_trades=performance['losing_trades'],
                    win_rate=performance['win_rate'],
                    total_return=performance['total_return'],
                    total_return_percentage=performance['total_return_percentage'],
                    sharpe_ratio=performance['sharpe_ratio'],
                    sortino_ratio=performance['sortino_ratio'],
                    max_drawdown=performance['max_drawdown'],
                    calmar_ratio=performance['calmar_ratio'],
                    profit_factor=performance['profit_factor'],
                    avg_win=performance['avg_win'],
                    avg_loss=performance['avg_loss'],
                    avg_trade_duration=performance['avg_trade_duration'],
                    best_trade=performance['best_trade'],
                    worst_trade=performance['worst_trade'],
                    volatility=performance['volatility'],
                    metadata={
                        'pattern_type': pattern['pattern_type'],
                        'pattern_confidence': pattern['confidence'],
                        'trades_data': trades[:10]  # Store sample trades
                    }
                )
                
                return result
                
        except Exception as e:
            print(f"⚠️ Error backtesting pattern {pattern.get('pattern_id', 'unknown')}: {e}")
            return None
        
        return None
    
    async def simulate_pattern_trades(self, pattern: Dict[str, Any], price_data: pd.Series) -> List[Dict[str, Any]]:
        """Simulate trades based on pattern logic"""
        trades = []
        
        # Simple pattern simulation
        entry_conditions = pattern['entry_conditions']
        exit_conditions = pattern['exit_conditions']
        
        # Calculate some basic indicators
        returns = price_data.pct_change()
        sma_20 = price_data.rolling(window=20).mean()
        volatility = returns.rolling(window=20).std()
        
        position = None
        
        for i in range(20, len(price_data) - 1):  # Start after SMA calculation
            current_price = price_data.iloc[i]
            current_return = returns.iloc[i]
            current_sma = sma_20.iloc[i]
            
            # Entry logic based on pattern type
            should_enter = False
            
            if pattern['pattern_type'] == 'momentum_breakout':
                # Simple breakout logic
                if current_price > current_sma * 1.02 and abs(current_return) > 0.01:
                    should_enter = True
            elif pattern['pattern_type'] == 'mean_reversion':
                # Simple mean reversion logic  
                if current_price < current_sma * 0.98 and current_return < -0.015:
                    should_enter = True
            
            # Enter position
            if should_enter and position is None:
                stop_loss_pct = exit_conditions.get('stop_loss_percentage', 0.02)
                take_profit_ratio = exit_conditions.get('take_profit_ratio', 2.0)
                
                position = {
                    'entry_time': price_data.index[i],
                    'entry_price': current_price,
                    'stop_loss': current_price * (1 - stop_loss_pct),
                    'take_profit': current_price * (1 + stop_loss_pct * take_profit_ratio),
                    'position_size': self.initial_capital * pattern['risk_parameters'].get('max_position_size', 0.05) / current_price
                }
                continue
            
            # Exit logic
            if position is not None:
                # Check stop loss
                if current_price <= position['stop_loss']:
                    pnl = (current_price - position['entry_price']) * position['position_size']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': price_data.index[i],
                        'entry_price': position['entry_price'],
                        'exit_price': current_price,
                        'position_size': position['position_size'],
                        'pnl': pnl,
                        'pnl_percentage': (current_price - position['entry_price']) / position['entry_price'],
                        'exit_reason': 'stop_loss'
                    })
                    position = None
                # Check take profit
                elif current_price >= position['take_profit']:
                    pnl = (current_price - position['entry_price']) * position['position_size']
                    trades.append({
                        'entry_time': position['entry_time'],
                        'exit_time': price_data.index[i],
                        'entry_price': position['entry_price'],
                        'exit_price': current_price,
                        'position_size': position['position_size'],
                        'pnl': pnl,
                        'pnl_percentage': (current_price - position['entry_price']) / position['entry_price'],
                        'exit_reason': 'take_profit'
                    })
                    position = None
        
        return trades
    
    def calculate_performance_metrics(self, trades: List[Dict[str, Any]], price_data: pd.Series) -> Dict[str, float]:
        """Calculate comprehensive performance metrics"""
        if not trades:
            return self.get_empty_performance_metrics()
        
        # Basic trade statistics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = total_trades - winning_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # PnL calculations
        pnls = [t['pnl'] for t in trades]
        total_return = sum(pnls)
        total_return_percentage = total_return / self.initial_capital
        
        # Win/Loss analysis
        wins = [t['pnl'] for t in trades if t['pnl'] > 0]
        losses = [t['pnl'] for t in trades if t['pnl'] <= 0]
        
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0
        best_trade = max(pnls) if pnls else 0
        worst_trade = min(pnls) if pnls else 0
        
        # Profit factor
        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 1
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Risk metrics
        returns = [t['pnl_percentage'] for t in trades]
        volatility = np.std(returns) if len(returns) > 1 else 0
        
        # Sharpe ratio (annualized)
        if volatility > 0:
            avg_return = np.mean(returns)
            daily_risk_free = (1 + self.risk_free_rate) ** (1/365) - 1
            sharpe_ratio = (avg_return - daily_risk_free) / volatility * np.sqrt(252)
        else:
            sharpe_ratio = 0
        
        # Sortino ratio
        negative_returns = [r for r in returns if r < 0]
        downside_deviation = np.std(negative_returns) if len(negative_returns) > 1 else 0
        
        if downside_deviation > 0:
            avg_return = np.mean(returns)
            daily_risk_free = (1 + self.risk_free_rate) ** (1/365) - 1
            sortino_ratio = (avg_return - daily_risk_free) / downside_deviation * np.sqrt(252)
        else:
            sortino_ratio = sharpe_ratio
        
        # Maximum drawdown
        cumulative_returns = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = running_max - cumulative_returns
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        # Calmar ratio
        calmar_ratio = total_return_percentage / max_drawdown if max_drawdown > 0 else 0
        
        # Average trade duration
        durations = [(t['exit_time'] - t['entry_time']).total_seconds() / 3600 for t in trades]  # hours
        avg_trade_duration = np.mean(durations) if durations else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'total_return_percentage': total_return_percentage,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'volatility': volatility,
            'avg_trade_duration': avg_trade_duration
        }
    
    def get_empty_performance_metrics(self) -> Dict[str, float]:
        """Return empty performance metrics"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'total_return': 0,
            'total_return_percentage': 0,
            'sharpe_ratio': 0,
            'sortino_ratio': 0,
            'max_drawdown': 0,
            'calmar_ratio': 0,
            'profit_factor': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'best_trade': 0,
            'worst_trade': 0,
            'volatility': 0,
            'avg_trade_duration': 0
        }
    
    async def analyze_pattern_performance(self, results: List[BacktestResult]) -> Dict[str, Any]:
        """Analyze performance by pattern type"""
        if not results:
            return {}
        
        # Group by pattern type
        pattern_types = {}
        for result in results:
            pattern_type = result.metadata.get('pattern_type', 'unknown')
            if pattern_type not in pattern_types:
                pattern_types[pattern_type] = []
            pattern_types[pattern_type].append(result)
        
        analysis = {}
        for pattern_type, type_results in pattern_types.items():
            avg_metrics = {
                'win_rate': np.mean([r.win_rate for r in type_results]),
                'total_return_percentage': np.mean([r.total_return_percentage for r in type_results]),
                'sharpe_ratio': np.mean([r.sharpe_ratio for r in type_results]),
                'max_drawdown': np.mean([r.max_drawdown for r in type_results]),
                'profit_factor': np.mean([r.profit_factor for r in type_results])
            }
            
            analysis[pattern_type] = {
                'pattern_count': len(type_results),
                'avg_performance': avg_metrics,
                'best_pattern': max(type_results, key=lambda r: r.total_return_percentage).pattern_id,
                'worst_pattern': min(type_results, key=lambda r: r.total_return_percentage).pattern_id
            }
        
        return analysis
    
    async def generate_improvement_recommendations(self, results: List[BacktestResult]) -> List[str]:
        """Generate recommendations for improving patterns"""
        recommendations = []
        
        if not results:
            recommendations.append("No backtest results available - ensure patterns are properly configured")
            return recommendations
        
        # Analyze overall performance
        avg_win_rate = np.mean([r.win_rate for r in results])
        avg_sharpe = np.mean([r.sharpe_ratio for r in results])
        avg_drawdown = np.mean([r.max_drawdown for r in results])
        
        if avg_win_rate < 0.5:
            recommendations.append("Low win rate detected - consider tighter entry conditions or better exit timing")
        
        if avg_sharpe < 1.0:
            recommendations.append("Low Sharpe ratio - focus on reducing volatility or improving returns")
        
        if avg_drawdown > 0.15:
            recommendations.append("High drawdown risk - implement better risk management and position sizing")
        
        # Pattern-specific recommendations
        poor_patterns = [r for r in results if r.total_return_percentage < 0]
        if len(poor_patterns) > len(results) * 0.3:
            recommendations.append("30%+ patterns show negative returns - review pattern identification logic")
        
        high_volatility_patterns = [r for r in results if r.volatility > 0.05]
        if high_volatility_patterns:
            recommendations.append("High volatility patterns detected - consider smaller position sizes")
        
        return recommendations
    
    async def calculate_overall_performance(self, results: List[BacktestResult]) -> Dict[str, float]:
        """Calculate overall performance metrics"""
        if not results:
            return {}
        
        return {
            'avg_win_rate': np.mean([r.win_rate for r in results]),
            'avg_return_percentage': np.mean([r.total_return_percentage for r in results]),
            'avg_sharpe_ratio': np.mean([r.sharpe_ratio for r in results]),
            'avg_max_drawdown': np.mean([r.max_drawdown for r in results]),
            'avg_profit_factor': np.mean([r.profit_factor for r in results]),
            'best_pattern_return': max([r.total_return_percentage for r in results]),
            'worst_pattern_return': min([r.total_return_percentage for r in results]),
            'patterns_with_positive_returns': len([r for r in results if r.total_return_percentage > 0])
        }
    
    async def store_backtest_results(self, results: Dict[str, Any]):
        """Store backtesting results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store individual backtest results
        for result_dict in results.get('backtest_results', []):
            cursor.execute("""
                INSERT INTO backtest_results
                (pattern_id, symbol, start_date, end_date, total_trades,
                 winning_trades, losing_trades, win_rate, total_return,
                 total_return_percentage, sharpe_ratio, sortino_ratio,
                 max_drawdown, calmar_ratio, profit_factor, avg_win,
                 avg_loss, avg_trade_duration, best_trade, worst_trade,
                 volatility, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result_dict['pattern_id'],
                result_dict['symbol'],
                result_dict['start_date'],
                result_dict['end_date'],
                result_dict['total_trades'],
                result_dict['winning_trades'],
                result_dict['losing_trades'],
                result_dict['win_rate'],
                result_dict['total_return'],
                result_dict['total_return_percentage'],
                result_dict['sharpe_ratio'],
                result_dict['sortino_ratio'],
                result_dict['max_drawdown'],
                result_dict['calmar_ratio'],
                result_dict['profit_factor'],
                result_dict['avg_win'],
                result_dict['avg_loss'],
                result_dict['avg_trade_duration'],
                result_dict['best_trade'],
                result_dict['worst_trade'],
                result_dict['volatility'],
                datetime.now().isoformat(),
                json.dumps(result_dict['metadata'])
            ))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    async def main():
        backtester = AdvancedPatternBacktester()
        results = await backtester.run_comprehensive_backtesting(lookback_days=7)
        
        print("\n🎯 BACKTESTING RESULTS:")
        print(f"Patterns Tested: {results['patterns_tested']}")
        print(f"Successful Backtests: {results['successful_backtests']}")
        print(f"Avg Win Rate: {results['overall_performance']['avg_win_rate']:.2%}")
        print(f"Avg Return: {results['overall_performance']['avg_return_percentage']:.2%}")
        print(f"Avg Sharpe Ratio: {results['overall_performance']['avg_sharpe_ratio']:.2f}")
    
    asyncio.run(main()) 