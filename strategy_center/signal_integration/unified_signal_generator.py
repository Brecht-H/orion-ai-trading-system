#!/usr/bin/env python3
"""
Unified Signal Generation System - Week 2 Enhancement
Combines correlation analysis, pattern recognition, and backtesting for superior signals
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
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"
    HOLD = "HOLD"

class ConfidenceLevel(Enum):
    VERY_HIGH = "very_high"    # >90%
    HIGH = "high"              # 70-90%
    MEDIUM = "medium"          # 50-70%
    LOW = "low"                # 30-50%
    VERY_LOW = "very_low"      # <30%

@dataclass
class UnifiedSignal:
    signal_id: str
    timestamp: datetime
    symbol: str
    signal_type: SignalType
    confidence_level: ConfidenceLevel
    confidence_score: float
    entry_price: float
    target_price: Optional[float]
    stop_loss: Optional[float]
    position_size: float
    time_horizon: int  # minutes
    risk_reward_ratio: float
    supporting_evidence: Dict[str, Any]
    validation_score: float
    market_regime_factor: float
    correlation_strength: float
    pattern_reliability: float
    backtest_performance: float
    execution_priority: int  # 1-5, 5 being highest
    metadata: Dict[str, Any]

@dataclass
class SignalPerformanceMetrics:
    total_signals: int
    successful_signals: int
    average_return: float
    win_rate: float
    sharpe_ratio: float
    max_drawdown: float
    profit_factor: float
    avg_holding_time: float
    best_performing_patterns: List[str]
    correlation_accuracy: float

class UnifiedSignalGenerator:
    """
    Unified signal generation system that combines multiple analysis layers
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/unified_signals.db"
        self.correlation_db = "databases/sqlite_dbs/correlation_analysis.db"
        self.patterns_db = "databases/sqlite_dbs/trading_patterns.db"
        self.backtest_db = "databases/sqlite_dbs/backtest_results.db"
        self.setup_databases()
        
        # Signal generation parameters
        self.min_confidence_threshold = 0.6
        self.max_signals_per_hour = 10
        self.position_sizing_model = "kelly_criterion"
        
        # Risk management
        self.max_portfolio_risk = 0.02  # 2% max risk per signal
        self.max_correlation_exposure = 0.15  # 15% in correlated positions
        
        # Performance tracking
        self.signal_history: List[UnifiedSignal] = []
        self.performance_metrics = SignalPerformanceMetrics(
            total_signals=0, successful_signals=0, average_return=0.0,
            win_rate=0.0, sharpe_ratio=0.0, max_drawdown=0.0,
            profit_factor=1.0, avg_holding_time=0.0,
            best_performing_patterns=[], correlation_accuracy=0.0
        )
        
    def setup_databases(self):
        """Initialize unified signal databases"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Unified signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS unified_signals (
                signal_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                confidence_level TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                entry_price REAL NOT NULL,
                target_price REAL,
                stop_loss REAL,
                position_size REAL NOT NULL,
                time_horizon INTEGER NOT NULL,
                risk_reward_ratio REAL NOT NULL,
                supporting_evidence TEXT NOT NULL,
                validation_score REAL NOT NULL,
                market_regime_factor REAL NOT NULL,
                correlation_strength REAL NOT NULL,
                pattern_reliability REAL NOT NULL,
                backtest_performance REAL NOT NULL,
                execution_priority INTEGER NOT NULL,
                execution_status TEXT DEFAULT 'pending',
                actual_return REAL,
                signal_success BOOLEAN,
                closed_at TEXT,
                metadata TEXT NOT NULL
            )
        """)
        
        # Signal performance tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signal_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_signals INTEGER NOT NULL,
                successful_signals INTEGER NOT NULL,
                win_rate REAL NOT NULL,
                average_return REAL NOT NULL,
                sharpe_ratio REAL NOT NULL,
                best_pattern TEXT,
                market_regime TEXT,
                performance_summary TEXT NOT NULL
            )
        """)
        
        # Signal execution log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signal_execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT NOT NULL,
                execution_timestamp TEXT NOT NULL,
                execution_price REAL NOT NULL,
                execution_status TEXT NOT NULL,
                slippage REAL DEFAULT 0.0,
                commission REAL DEFAULT 0.0,
                notes TEXT,
                FOREIGN KEY (signal_id) REFERENCES unified_signals (signal_id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Unified signal databases initialized")
    
    async def generate_unified_signals(self) -> Dict[str, Any]:
        """
        Main signal generation engine - combines all analysis layers
        """
        print("🎯 Generating unified trading signals...")
        
        # 1. Load all analysis components
        correlation_data = await self.load_correlation_analysis()
        pattern_data = await self.load_pattern_analysis()
        backtest_data = await self.load_backtest_results()
        market_data = await self.load_current_market_data()
        
        # 2. Analyze current market regime
        market_regime = await self.analyze_current_market_regime(market_data)
        
        # 3. Generate candidate signals from each source
        correlation_signals = await self.extract_correlation_signals(correlation_data, market_data)
        pattern_signals = await self.extract_pattern_signals(pattern_data, market_data)
        
        # 4. Validate signals against backtest performance
        validated_signals = await self.validate_signals_with_backtest(
            correlation_signals + pattern_signals, backtest_data
        )
        
        # 5. Apply multi-layer filtering
        filtered_signals = await self.apply_multi_layer_filtering(validated_signals, market_regime)
        
        # 6. Calculate optimal position sizing
        sized_signals = await self.apply_position_sizing(filtered_signals)
        
        # 7. Rank and prioritize signals
        prioritized_signals = await self.rank_and_prioritize_signals(sized_signals)
        
        # 8. Generate final unified signals
        final_signals = await self.create_unified_signals(prioritized_signals, market_regime)
        
        # 9. Risk management final check
        risk_adjusted_signals = await self.apply_final_risk_check(final_signals)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'market_regime': market_regime,
            'candidate_signals': len(correlation_signals + pattern_signals),
            'validated_signals': len(validated_signals),
            'filtered_signals': len(filtered_signals),
            'final_signals': len(risk_adjusted_signals),
            'unified_signals': [asdict(signal) for signal in risk_adjusted_signals],
            'signal_quality_score': await self.calculate_signal_quality_score(risk_adjusted_signals),
            'execution_recommendations': await self.generate_execution_recommendations(risk_adjusted_signals),
            'performance_update': await self.update_performance_metrics()
        }
        
        # Store results
        await self.store_unified_signals(risk_adjusted_signals)
        
        print(f"✅ Unified signal generation complete:")
        print(f"   🔍 Candidate signals: {len(correlation_signals + pattern_signals)}")
        print(f"   ✅ Final signals: {len(risk_adjusted_signals)}")
        print(f"   🎯 Average confidence: {np.mean([s.confidence_score for s in risk_adjusted_signals]):.2%}")
        
        return results
    
    async def load_correlation_analysis(self) -> Dict[str, Any]:
        """Load latest correlation analysis results"""
        try:
            if not Path(self.correlation_db).exists():
                return {'patterns': [], 'signals': []}
            
            conn = sqlite3.connect(self.correlation_db)
            
            # Load high-confidence correlation patterns
            patterns_query = """
                SELECT * FROM correlation_patterns 
                WHERE correlation_strength > 0.5 AND confidence_level > 0.6
                ORDER BY correlation_strength DESC
                LIMIT 50
            """
            patterns_df = pd.read_sql_query(patterns_query, conn)
            
            # Load recent predictive signals
            signals_query = """
                SELECT * FROM predictive_signals 
                WHERE timestamp > datetime('now', '-6 hours') AND confidence > 0.6
                ORDER BY confidence DESC
            """
            signals_df = pd.read_sql_query(signals_query, conn)
            
            conn.close()
            
            return {
                'patterns': patterns_df.to_dict('records') if not patterns_df.empty else [],
                'signals': signals_df.to_dict('records') if not signals_df.empty else []
            }
            
        except Exception as e:
            print(f"⚠️ Error loading correlation analysis: {e}")
            return {'patterns': [], 'signals': []}
    
    async def load_pattern_analysis(self) -> Dict[str, Any]:
        """Load pattern recognition results"""
        try:
            if not Path(self.patterns_db).exists():
                return {'patterns': [], 'signals': []}
            
            conn = sqlite3.connect(self.patterns_db)
            
            # Load validated trading patterns
            patterns_query = """
                SELECT * FROM trading_patterns 
                WHERE confidence > 0.6 AND historical_success_rate > 0.5
                ORDER BY confidence DESC
            """
            patterns_df = pd.read_sql_query(patterns_query, conn)
            
            # Load recent trading signals
            signals_query = """
                SELECT * FROM trading_signals 
                WHERE timestamp > datetime('now', '-6 hours') 
                AND confidence > 0.6 AND execution_status = 'pending'
                ORDER BY confidence DESC
            """
            signals_df = pd.read_sql_query(signals_query, conn)
            
            conn.close()
            
            return {
                'patterns': patterns_df.to_dict('records') if not patterns_df.empty else [],
                'signals': signals_df.to_dict('records') if not signals_df.empty else []
            }
            
        except Exception as e:
            print(f"⚠️ Error loading pattern analysis: {e}")
            return {'patterns': [], 'signals': []}
    
    async def load_backtest_results(self) -> Dict[str, Any]:
        """Load backtesting validation results"""
        try:
            if not Path(self.backtest_db).exists():
                return {'results': [], 'validations': []}
            
            conn = sqlite3.connect(self.backtest_db)
            
            # Load recent backtest results
            backtest_query = """
                SELECT * FROM backtest_results 
                WHERE created_at > datetime('now', '-7 days')
                ORDER BY sharpe_ratio DESC
            """
            backtest_df = pd.read_sql_query(backtest_query, conn)
            
            # Load pattern validation results
            validation_query = """
                SELECT * FROM pattern_validation 
                WHERE validation_date > datetime('now', '-7 days')
                AND pattern_reliability > 0.5
                ORDER BY pattern_reliability DESC
            """
            validation_df = pd.read_sql_query(validation_query, conn)
            
            conn.close()
            
            return {
                'results': backtest_df.to_dict('records') if not backtest_df.empty else [],
                'validations': validation_df.to_dict('records') if not validation_df.empty else []
            }
            
        except Exception as e:
            print(f"⚠️ Error loading backtest results: {e}")
            return {'results': [], 'validations': []}
    
    async def load_current_market_data(self) -> pd.DataFrame:
        """Load current market data for signal validation"""
        try:
            # Try to load from free sources
            free_data_db = "databases/sqlite_dbs/free_sources_data.db"
            if Path(free_data_db).exists():
                conn = sqlite3.connect(free_data_db)
                
                # Get latest market data (last 2 hours)
                cutoff_time = (datetime.now() - timedelta(hours=2)).timestamp()
                
                query = """
                    SELECT timestamp, source_name, data_type, symbol, value
                    FROM free_data 
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 500
                """
                
                df = pd.read_sql_query(query, conn, params=[cutoff_time])
                conn.close()
                
                if not df.empty:
                    return self.process_market_data_for_signals(df)
            
            # Generate sample data
            return await self.generate_sample_market_data()
            
        except Exception as e:
            print(f"⚠️ Error loading market data: {e}")
            return await self.generate_sample_market_data()
    
    def process_market_data_for_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process market data for signal generation"""
        # Convert timestamp and pivot
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        pivot_df = df.pivot_table(
            index='datetime',
            columns=['source_name', 'data_type'],
            values='value',
            aggfunc='mean'
        )
        
        # Flatten column names
        pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]
        
        # Add real-time indicators
        for col in pivot_df.columns:
            if 'price' in col.lower():
                # Add momentum indicators
                pivot_df[f"{col}_momentum_5"] = pivot_df[col].pct_change(5)
                pivot_df[f"{col}_momentum_15"] = pivot_df[col].pct_change(15)
                
                # Add volatility
                pivot_df[f"{col}_volatility"] = pivot_df[col].rolling(window=20).std()
                
                # Add trend strength
                pivot_df[f"{col}_trend"] = pivot_df[col].rolling(window=10).apply(
                    lambda x: 1 if x.iloc[-1] > x.iloc[0] else -1
                )
        
        return pivot_df.fillna(method='ffill').fillna(0)
    
    async def analyze_current_market_regime(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze current market regime for signal context"""
        if market_data.empty:
            return {
                'regime_type': 'unknown',
                'volatility_level': 'unknown',
                'trend_direction': 'neutral',
                'confidence': 0.0
            }
        
        # Analyze price columns
        price_cols = [col for col in market_data.columns if 'price' in col.lower()]
        
        if not price_cols:
            return {
                'regime_type': 'no_data',
                'volatility_level': 'unknown',
                'trend_direction': 'neutral',
                'confidence': 0.0
            }
        
        # Calculate regime metrics
        volatilities = []
        trends = []
        
        for col in price_cols:
            if len(market_data[col]) > 20:
                # Volatility
                vol = market_data[col].pct_change().rolling(window=20).std().iloc[-1]
                volatilities.append(vol)
                
                # Trend
                recent_trend = (market_data[col].iloc[-1] - market_data[col].iloc[-20]) / market_data[col].iloc[-20]
                trends.append(recent_trend)
        
        if not volatilities:
            return {
                'regime_type': 'insufficient_data',
                'volatility_level': 'unknown',
                'trend_direction': 'neutral',
                'confidence': 0.0
            }
        
        avg_volatility = np.mean(volatilities)
        avg_trend = np.mean(trends)
        
        # Classify regime
        if avg_volatility > 0.05:
            volatility_level = 'high'
        elif avg_volatility > 0.02:
            volatility_level = 'medium'
        else:
            volatility_level = 'low'
        
        if avg_trend > 0.02:
            trend_direction = 'bullish'
        elif avg_trend < -0.02:
            trend_direction = 'bearish'
        else:
            trend_direction = 'neutral'
        
        # Determine regime type
        if volatility_level == 'high':
            if trend_direction != 'neutral':
                regime_type = 'trending_volatile'
            else:
                regime_type = 'chaotic'
        else:
            if trend_direction != 'neutral':
                regime_type = 'trending_stable'
            else:
                regime_type = 'range_bound'
        
        return {
            'regime_type': regime_type,
            'volatility_level': volatility_level,
            'trend_direction': trend_direction,
            'confidence': min(len(price_cols) / 3.0, 1.0),
            'avg_volatility': avg_volatility,
            'avg_trend': avg_trend
        }
    
    async def extract_correlation_signals(self, correlation_data: Dict[str, Any], 
                                        market_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract signals from correlation analysis"""
        signals = []
        
        # Process correlation patterns
        for pattern in correlation_data.get('patterns', []):
            try:
                signal = await self.convert_correlation_to_signal(pattern, market_data)
                if signal:
                    signals.append(signal)
            except Exception as e:
                continue
        
        # Process predictive signals
        for pred_signal in correlation_data.get('signals', []):
            try:
                signal = await self.convert_predictive_to_signal(pred_signal, market_data)
                if signal:
                    signals.append(signal)
            except Exception as e:
                continue
        
        print(f"   Extracted {len(signals)} signals from correlation analysis")
        return signals
    
    async def convert_correlation_to_signal(self, pattern: Dict[str, Any], 
                                          market_data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Convert correlation pattern to trading signal"""
        
        correlation_strength = pattern.get('correlation_strength', 0)
        confidence_level = pattern.get('confidence_level', 0)
        
        if correlation_strength < 0.5 or confidence_level < 0.6:
            return None
        
        # Extract symbol from pattern
        source_combination = json.loads(pattern.get('source_combination', '[]'))
        symbol = self.extract_symbol_from_sources(source_combination)
        
        if not symbol:
            return None
        
        # Get current price
        price_col = f"{symbol}_price"
        if market_data.empty or price_col not in market_data.columns:
            return None
        
        current_price = market_data[price_col].iloc[-1]
        
        # Determine signal direction based on correlation
        metadata = json.loads(pattern.get('metadata', '{}'))
        correlation_direction = metadata.get('correlation_direction', 'positive')
        
        # Simple signal logic
        signal_type = 'BUY' if correlation_direction == 'positive' else 'SELL'
        
        return {
            'source': 'correlation',
            'symbol': symbol,
            'signal_type': signal_type,
            'confidence': confidence_level,
            'current_price': current_price,
            'correlation_strength': correlation_strength,
            'pattern_id': pattern.get('pattern_id'),
            'time_lag': pattern.get('time_lag', 0),
            'metadata': metadata
        }
    
    async def convert_predictive_to_signal(self, pred_signal: Dict[str, Any], 
                                         market_data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Convert predictive signal to trading signal"""
        
        confidence = pred_signal.get('confidence', 0)
        strength = pred_signal.get('strength', 0)
        
        if confidence < 0.6 or strength < 0.5:
            return None
        
        symbol = pred_signal.get('symbol', 'BTC')
        signal_type = pred_signal.get('signal_type', 'hold')
        
        if signal_type == 'hold':
            return None
        
        # Get current price
        price_col = f"{symbol}_price"
        if market_data.empty or price_col not in market_data.columns:
            current_price = pred_signal.get('price_target', 50000)  # Default
        else:
            current_price = market_data[price_col].iloc[-1]
        
        return {
            'source': 'predictive',
            'symbol': symbol,
            'signal_type': signal_type.upper(),
            'confidence': confidence,
            'current_price': current_price,
            'strength': strength,
            'time_horizon': pred_signal.get('time_horizon', 60),
            'price_target': pred_signal.get('price_target'),
            'signal_id': pred_signal.get('signal_id'),
            'metadata': json.loads(pred_signal.get('metadata', '{}'))
        }
    
    def extract_symbol_from_sources(self, sources: List[str]) -> Optional[str]:
        """Extract trading symbol from source combination"""
        symbols = ['BTC', 'ETH', 'ADA', 'BNB', 'SOL', 'DOT', 'LINK', 'UNI']
        
        for source in sources:
            for symbol in symbols:
                if symbol in source.upper():
                    return symbol
        
        return 'BTC'  # Default fallback
    
    async def extract_pattern_signals(self, pattern_data: Dict[str, Any], 
                                    market_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract signals from pattern analysis"""
        signals = []
        
        # Process active patterns
        for pattern in pattern_data.get('active_patterns', []):
            try:
                signal = await self.convert_pattern_to_signal(pattern, market_data)
                if signal:
                    signals.append(signal)
            except Exception as e:
                continue
        
        # Process trading signals
        for trading_signal in pattern_data.get('trading_signals', []):
            try:
                signal = await self.convert_trading_signal(trading_signal, market_data)
                if signal:
                    signals.append(signal)
            except Exception as e:
                continue
        
        print(f"   Extracted {len(signals)} signals from pattern analysis")
        return signals
    
    async def convert_pattern_to_signal(self, pattern: Dict[str, Any], 
                                      market_data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Convert trading pattern to unified signal"""
        
        confidence = pattern.get('confidence', 0)
        if confidence < 0.5:
            return None
        
        symbols = pattern.get('symbols', ['BTC'])
        if not symbols:
            return None
        
        symbol = symbols[0]  # Take first symbol
        
        # Get current price
        price_col = f"{symbol}_price"
        if market_data.empty or price_col not in market_data.columns:
            current_price = 50000 if symbol == 'BTC' else 3000  # Default
        else:
            current_price = market_data[price_col].iloc[-1]
        
        # Determine signal type based on pattern type
        pattern_type = pattern.get('pattern_type', 'unknown')
        if pattern_type in ['momentum_breakout', 'volatility_expansion']:
            signal_type = 'BUY'
        elif pattern_type == 'mean_reversion':
            signal_type = 'BUY'  # Simplified
        else:
            signal_type = 'HOLD'
        
        if signal_type == 'HOLD':
            return None
        
        return {
            'source': 'pattern',
            'symbol': symbol,
            'signal_type': signal_type,
            'confidence': confidence,
            'current_price': current_price,
            'pattern_type': pattern_type,
            'pattern_id': pattern.get('pattern_id'),
            'expected_duration': pattern.get('expected_duration', 60),
            'risk_parameters': pattern.get('risk_parameters', {}),
            'metadata': pattern.get('metadata', {})
        }
    
    async def convert_trading_signal(self, trading_signal: Dict[str, Any], 
                                   market_data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Convert trading signal to unified signal"""
        
        confidence = trading_signal.get('confidence', 0)
        if confidence < 0.5:
            return None
        
        symbol = trading_signal.get('symbol', 'BTC')
        signal_type = trading_signal.get('action', 'HOLD')
        
        if signal_type == 'HOLD':
            return None
        
        current_price = trading_signal.get('entry_price', 50000)
        
        return {
            'source': 'trading_signal',
            'symbol': symbol,
            'signal_type': signal_type,
            'confidence': confidence,
            'current_price': current_price,
            'entry_price': trading_signal.get('entry_price'),
            'stop_loss': trading_signal.get('stop_loss'),
            'take_profit': trading_signal.get('take_profit'),
            'risk_score': trading_signal.get('risk_score', 0.5),
            'expected_return': trading_signal.get('expected_return', 0.02),
            'time_horizon': trading_signal.get('time_horizon', 60),
            'signal_id': trading_signal.get('signal_id'),
            'metadata': trading_signal.get('metadata', {})
        }
    
    async def extract_backtest_signals(self, backtest_data: Dict[str, Any], 
                                     market_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract signals from backtesting results"""
        signals = []
        
        # Use backtest results to validate and score signals
        for result in backtest_data.get('backtest_results', []):
            try:
                if result.get('win_rate', 0) > 0.6 and result.get('total_return_percentage', 0) > 0:
                    signal = {
                        'source': 'backtest_validation',
                        'symbol': result.get('symbol', 'BTC'),
                        'signal_type': 'BUY',  # Simplified
                        'confidence': min(result.get('win_rate', 0.5) + 0.1, 1.0),
                        'backtest_performance': result.get('total_return_percentage', 0),
                        'sharpe_ratio': result.get('sharpe_ratio', 0),
                        'max_drawdown': result.get('max_drawdown', 0.1),
                        'pattern_id': result.get('pattern_id'),
                        'metadata': result.get('metadata', {})
                    }
                    signals.append(signal)
            except Exception as e:
                continue
        
        print(f"   Extracted {len(signals)} signals from backtest validation")
        return signals
    
    async def combine_multi_source_signals(self, correlation_signals: List[Dict[str, Any]], 
                                         pattern_signals: List[Dict[str, Any]], 
                                         backtest_signals: List[Dict[str, Any]], 
                                         market_regime: Dict[str, Any]) -> List[UnifiedSignal]:
        """Combine signals from multiple sources into unified signals"""
        print("🔗 Combining multi-source signals...")
        
        # Group signals by symbol
        signal_groups = {}
        all_signals = correlation_signals + pattern_signals + backtest_signals
        
        for signal in all_signals:
            symbol = signal.get('symbol', 'BTC')
            if symbol not in signal_groups:
                signal_groups[symbol] = []
            signal_groups[symbol].append(signal)
        
        unified_signals = []
        
        for symbol, signals in signal_groups.items():
            try:
                unified_signal = await self.create_unified_signal(symbol, signals, market_regime)
                if unified_signal:
                    unified_signals.append(unified_signal)
            except Exception as e:
                print(f"⚠️ Error creating unified signal for {symbol}: {e}")
                continue
        
        # Sort by execution priority and confidence
        unified_signals.sort(key=lambda s: (s.execution_priority, s.confidence_score), reverse=True)
        
        print(f"✅ Created {len(unified_signals)} unified signals")
        return unified_signals
    
    async def create_unified_signal(self, symbol: str, signals: List[Dict[str, Any]], 
                                  market_regime: Dict[str, Any]) -> Optional[UnifiedSignal]:
        """Create a unified signal from multiple source signals"""
        
        if not signals:
            return None
        
        # Calculate combined metrics
        buy_signals = [s for s in signals if s.get('signal_type') == 'BUY']
        sell_signals = [s for s in signals if s.get('signal_type') == 'SELL']
        
        # Determine dominant signal type
        if len(buy_signals) > len(sell_signals):
            signal_type = SignalType.BUY
            relevant_signals = buy_signals
        elif len(sell_signals) > len(buy_signals):
            signal_type = SignalType.SELL
            relevant_signals = sell_signals
        else:
            return None  # No clear consensus
        
        # Calculate weighted confidence
        confidences = [s.get('confidence', 0.5) for s in relevant_signals]
        avg_confidence = np.mean(confidences) if confidences else 0.5
        
        # Boost confidence based on signal consensus
        consensus_boost = min(len(relevant_signals) * 0.1, 0.3)
        final_confidence = min(avg_confidence + consensus_boost, 1.0)
        
        # Determine confidence level
        if final_confidence >= 0.9:
            confidence_level = ConfidenceLevel.VERY_HIGH
        elif final_confidence >= 0.7:
            confidence_level = ConfidenceLevel.HIGH
        elif final_confidence >= 0.5:
            confidence_level = ConfidenceLevel.MEDIUM
        elif final_confidence >= 0.3:
            confidence_level = ConfidenceLevel.LOW
        else:
            confidence_level = ConfidenceLevel.VERY_LOW
        
        # Get current price
        current_price = signals[0].get('current_price', 50000)
        
        # Calculate position size using Kelly criterion
        position_size = self.calculate_kelly_position_size(relevant_signals)
        
        # Calculate stop loss and take profit
        stop_loss, take_profit = self.calculate_unified_exit_levels(current_price, signal_type, relevant_signals)
        
        # Calculate risk metrics
        correlation_strength = np.mean([s.get('correlation_strength', 0.5) for s in relevant_signals])
        pattern_reliability = np.mean([s.get('confidence', 0.5) for s in pattern_signals if s.get('symbol') == symbol])
        backtest_performance = np.mean([s.get('backtest_performance', 0) for s in signals if 'backtest_performance' in s])
        
        # Market regime factor
        market_regime_factor = self.calculate_market_regime_factor(market_regime, signal_type)
        
        # Execution priority
        execution_priority = self.calculate_execution_priority(final_confidence, len(relevant_signals), market_regime_factor)
        
        # Create unified signal
        unified_signal = UnifiedSignal(
            signal_id=f"unified_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            symbol=symbol,
            signal_type=signal_type,
            confidence_level=confidence_level,
            confidence_score=final_confidence,
            entry_price=current_price,
            target_price=take_profit,
            stop_loss=stop_loss,
            position_size=position_size,
            time_horizon=int(np.mean([s.get('time_horizon', 60) for s in relevant_signals])),
            risk_reward_ratio=abs((take_profit - current_price) / (current_price - stop_loss)) if stop_loss else 2.0,
            supporting_evidence={
                'correlation_signals': len([s for s in relevant_signals if s.get('source') == 'correlation']),
                'pattern_signals': len([s for s in relevant_signals if s.get('source') == 'pattern']),
                'backtest_validations': len([s for s in relevant_signals if s.get('source') == 'backtest_validation']),
                'source_signals': relevant_signals
            },
            validation_score=final_confidence,
            market_regime_factor=market_regime_factor,
            correlation_strength=correlation_strength,
            pattern_reliability=pattern_reliability,
            backtest_performance=backtest_performance,
            execution_priority=execution_priority,
            metadata={
                'creation_time': datetime.now().isoformat(),
                'signal_count': len(relevant_signals),
                'market_regime': market_regime.get('regime_type', 'unknown'),
                'source_breakdown': {s.get('source', 'unknown'): 1 for s in relevant_signals}
            }
        )
        
        return unified_signal
    
    def calculate_kelly_position_size(self, signals: List[Dict[str, Any]]) -> float:
        """Calculate optimal position size using Kelly criterion"""
        # Simplified Kelly calculation
        win_rates = [s.get('win_rate', 0.6) for s in signals if 'win_rate' in s]
        expected_returns = [s.get('expected_return', 0.02) for s in signals if 'expected_return' in s]
        
        if not win_rates or not expected_returns:
            return 0.02  # Default 2% position
        
        avg_win_rate = np.mean(win_rates)
        avg_expected_return = np.mean(expected_returns)
        
        # Kelly fraction = (bp - q) / b
        # where b = odds, p = win probability, q = loss probability
        kelly_fraction = (avg_expected_return * avg_win_rate - (1 - avg_win_rate)) / avg_expected_return
        
        # Apply conservative sizing (25% of Kelly)
        conservative_kelly = max(min(kelly_fraction * 0.25, 0.05), 0.01)
        
        return conservative_kelly
    
    def calculate_unified_exit_levels(self, entry_price: float, signal_type: SignalType, 
                                    signals: List[Dict[str, Any]]) -> Tuple[Optional[float], Optional[float]]:
        """Calculate unified stop loss and take profit levels"""
        
        # Get stop losses and take profits from signals
        stop_losses = [s.get('stop_loss') for s in signals if s.get('stop_loss')]
        take_profits = [s.get('take_profit') for s in signals if s.get('take_profit')]
        
        # Default risk management
        default_stop_pct = 0.02  # 2% stop loss
        default_reward_ratio = 2.5  # 2.5:1 reward ratio
        
        if signal_type == SignalType.BUY:
            if stop_losses:
                stop_loss = np.mean(stop_losses)
            else:
                stop_loss = entry_price * (1 - default_stop_pct)
            
            if take_profits:
                take_profit = np.mean(take_profits)
            else:
                take_profit = entry_price * (1 + default_stop_pct * default_reward_ratio)
        else:  # SELL
            if stop_losses:
                stop_loss = np.mean(stop_losses)
            else:
                stop_loss = entry_price * (1 + default_stop_pct)
            
            if take_profits:
                take_profit = np.mean(take_profits)
            else:
                take_profit = entry_price * (1 - default_stop_pct * default_reward_ratio)
        
        return stop_loss, take_profit
    
    def calculate_market_regime_factor(self, market_regime: Dict[str, Any], signal_type: SignalType) -> float:
        """Calculate market regime adjustment factor"""
        regime_type = market_regime.get('regime_type', 'unknown')
        volatility_level = market_regime.get('volatility_level', 'medium')
        trend_direction = market_regime.get('trend_direction', 'neutral')
        
        base_factor = 1.0
        
        # Adjust based on regime type
        if regime_type == 'trending_stable':
            base_factor = 1.2  # Favor trending strategies
        elif regime_type == 'range_bound':
            base_factor = 0.8  # Reduce position sizes in choppy markets
        elif regime_type == 'chaotic':
            base_factor = 0.6  # Very conservative in chaotic markets
        
        # Adjust based on signal-trend alignment
        if signal_type == SignalType.BUY and trend_direction == 'bullish':
            base_factor *= 1.1
        elif signal_type == SignalType.SELL and trend_direction == 'bearish':
            base_factor *= 1.1
        elif (signal_type == SignalType.BUY and trend_direction == 'bearish') or \
             (signal_type == SignalType.SELL and trend_direction == 'bullish'):
            base_factor *= 0.8  # Counter-trend trades get reduced weight
        
        return min(max(base_factor, 0.3), 2.0)  # Clamp between 0.3 and 2.0
    
    def calculate_execution_priority(self, confidence: float, signal_count: int, market_regime_factor: float) -> int:
        """Calculate execution priority (1-5, 5 being highest)"""
        
        base_priority = confidence * 5  # Scale confidence to 0-5
        
        # Boost based on signal consensus
        consensus_boost = min(signal_count * 0.5, 2.0)
        
        # Market regime adjustment
        regime_adjustment = (market_regime_factor - 1.0) * 2
        
        final_priority = base_priority + consensus_boost + regime_adjustment
        
        return max(1, min(int(round(final_priority)), 5))
    
    async def apply_signal_filters(self, signals: List[UnifiedSignal]) -> List[UnifiedSignal]:
        """Apply final filters to unified signals"""
        print(f"🛡️ Applying filters to {len(signals)} unified signals...")
        
        filtered_signals = []
        
        for signal in signals:
            # Filter by confidence
            if signal.confidence_score < 0.5:
                continue
            
            # Filter by risk-reward ratio
            if signal.risk_reward_ratio < 1.5:
                continue
            
            # Filter by market regime compatibility
            if signal.market_regime_factor < 0.5:
                continue
            
            # Filter by position size (avoid extremely small positions)
            if signal.position_size < 0.005:  # Less than 0.5%
                continue
            
            filtered_signals.append(signal)
        
        # Limit total number of signals
        max_signals = 8
        if len(filtered_signals) > max_signals:
            filtered_signals = filtered_signals[:max_signals]
        
        print(f"✅ {len(filtered_signals)} signals passed filters")
        return filtered_signals
    
    async def calculate_signal_quality_score(self, signals: List[UnifiedSignal]) -> float:
        """Calculate overall signal quality score"""
        if not signals:
            return 0.0
        
        # Average confidence
        avg_confidence = np.mean([s.confidence_score for s in signals])
        
        # Average backtest performance
        avg_backtest = np.mean([s.backtest_performance for s in signals])
        
        # Signal diversity (different sources)
        sources = set()
        for signal in signals:
            evidence = signal.supporting_evidence
            if evidence.get('correlation_signals', 0) > 0:
                sources.add('correlation')
            if evidence.get('pattern_signals', 0) > 0:
                sources.add('pattern')
            if evidence.get('backtest_validations', 0) > 0:
                sources.add('backtest')
        
        diversity_score = len(sources) / 3.0  # Max 3 sources
        
        # Risk-adjusted score
        avg_risk_reward = np.mean([s.risk_reward_ratio for s in signals])
        risk_adjustment = min(avg_risk_reward / 2.0, 1.0)  # Normalize to 1.0
        
        # Combined quality score
        quality_score = (avg_confidence * 0.4 + 
                        diversity_score * 0.3 + 
                        risk_adjustment * 0.2 + 
                        min(avg_backtest + 0.1, 0.1) * 0.1)
        
        return min(quality_score, 1.0)
    
    async def store_unified_signals(self, signals: List[UnifiedSignal], results: Dict[str, Any]):
        """Store unified signals in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for signal in signals:
            cursor.execute("""
                INSERT OR REPLACE INTO unified_signals
                (signal_id, timestamp, symbol, signal_type, confidence_level,
                 confidence_score, entry_price, target_price, stop_loss,
                 position_size, time_horizon, risk_reward_ratio,
                 supporting_evidence, validation_score, market_regime_factor,
                 correlation_strength, pattern_reliability, backtest_performance,
                 execution_priority, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal.signal_id,
                signal.timestamp.isoformat(),
                signal.symbol,
                signal.signal_type.value,
                signal.confidence_level.value,
                signal.confidence_score,
                signal.entry_price,
                signal.target_price,
                signal.stop_loss,
                signal.position_size,
                signal.time_horizon,
                signal.risk_reward_ratio,
                json.dumps(signal.supporting_evidence),
                signal.validation_score,
                signal.market_regime_factor,
                signal.correlation_strength,
                signal.pattern_reliability,
                signal.backtest_performance,
                signal.execution_priority,
                json.dumps(signal.metadata)
            ))
        
        # Store generation results
        cursor.execute("""
            INSERT INTO signal_generation_runs
            (timestamp, signals_generated, quality_score, market_regime, results_json)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            len(signals),
            results.get('signal_quality_score', 0),
            results.get('market_regime', {}).get('regime_type', 'unknown'),
            json.dumps(results)
        ))
        
        conn.commit()
        conn.close()
    
    async def apply_multi_layer_filtering(self, signals: List[Dict[str, Any]], 
                                         market_regime: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply multi-layer filtering to remove low-quality signals"""
        if not signals:
            return signals
        
        filtered_signals = []
        
        for signal in signals:
            # Layer 1: Confidence threshold
            confidence = signal.get('confidence', 0.0)
            if confidence < 0.5:
                continue
            
            # Layer 2: Market regime compatibility
            signal_type = signal.get('signal_type', 'BUY')
            regime_type = market_regime.get('regime_type', 'unknown')
            
            # Filter based on market regime
            if regime_type == 'trending_volatile' and signal_type in ['HOLD']:
                continue
            elif regime_type == 'range_bound' and signal_type in ['STRONG_BUY', 'STRONG_SELL']:
                continue
            
            # Layer 3: Risk-reward ratio
            risk_reward = signal.get('risk_reward_ratio', 0.0)
            if risk_reward < 1.5:  # Minimum 1.5:1 risk-reward
                continue
            
            # Layer 4: Validation score
            validation = signal.get('backtest_validation', {})
            validation_score = validation.get('validation_boost', 0.0)
            if validation_score < 0.0:  # Allow signals without validation
                pass  # Keep signal but note lack of validation
            
            # Layer 5: Time horizon compatibility
            time_horizon = signal.get('time_horizon', 0)
            if time_horizon < 15:  # Minimum 15 minutes
                continue
            
            # Layer 6: Position size reasonableness
            position_size = signal.get('position_size', 0.0)
            if position_size <= 0 or position_size > 0.1:  # Max 10% position
                continue
            
            # Signal passed all filters
            signal['filter_score'] = (
                confidence * 0.4 +
                min(risk_reward / 3.0, 1.0) * 0.3 +
                min(position_size * 10, 1.0) * 0.2 +
                (validation_score + 0.1) * 0.1  # Small boost for validation
            )
            
            filtered_signals.append(signal)
        
        print(f"✅ Multi-layer filtering: {len(filtered_signals)}/{len(signals)} signals passed all filters")
        return filtered_signals

    async def validate_signals_with_backtest(self, signals: List[Dict[str, Any]], 
                                           backtest_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate signals using backtest performance data"""
        validated_signals = []
        
        for signal in signals:
            try:
                # Find relevant backtest results for this signal
                symbol = signal.get('symbol', 'BTC')
                pattern_id = signal.get('pattern_id')
                
                # Look for backtest results
                relevant_results = []
                for result in backtest_data.get('backtest_results', []):
                    if (result.get('symbol') == symbol or 
                        result.get('pattern_id') == pattern_id):
                        relevant_results.append(result)
                
                if relevant_results:
                    # Calculate validation score based on backtest performance
                    avg_win_rate = np.mean([r.get('win_rate', 0.5) for r in relevant_results])
                    avg_sharpe = np.mean([r.get('sharpe_ratio', 0) for r in relevant_results])
                    avg_return = np.mean([r.get('total_return_percentage', 0) for r in relevant_results])
                    
                    # Boost confidence based on backtest performance
                    performance_boost = 0
                    if avg_win_rate > 0.6:
                        performance_boost += 0.1
                    if avg_sharpe > 1.0:
                        performance_boost += 0.1
                    if avg_return > 0.05:
                        performance_boost += 0.1
                    
                    # Update signal confidence
                    original_confidence = signal.get('confidence', 0.5)
                    validated_confidence = min(original_confidence + performance_boost, 1.0)
                    
                    signal['confidence'] = validated_confidence
                    signal['backtest_validation'] = {
                        'avg_win_rate': avg_win_rate,
                        'avg_sharpe_ratio': avg_sharpe,
                        'avg_return': avg_return,
                        'validation_boost': performance_boost
                    }
                    
                    validated_signals.append(signal)
                else:
                    # No backtest data available, keep original confidence but mark as unvalidated
                    signal['backtest_validation'] = {'status': 'no_data_available'}
                    validated_signals.append(signal)
                    
            except Exception as e:
                print(f"⚠️ Error validating signal: {e}")
                validated_signals.append(signal)  # Keep signal but unvalidated
                continue
        
        print(f"✅ Validated {len(validated_signals)} signals with backtest data")
        return validated_signals
    
    async def generate_sample_market_data(self) -> pd.DataFrame:
        """Generate sample market data for testing"""
        dates = pd.date_range(start=datetime.now() - timedelta(hours=2), 
                            end=datetime.now(), freq='5min')
        
        np.random.seed(42)
        sample_data = pd.DataFrame(index=dates)
        
        # Sample prices
        sample_data['BTC_price'] = 50000 + np.cumsum(np.random.randn(len(dates)) * 100)
        sample_data['ETH_price'] = 3000 + np.cumsum(np.random.randn(len(dates)) * 50)
        
        return sample_data

if __name__ == "__main__":
    async def main():
        generator = UnifiedSignalGenerator()
        results = await generator.generate_unified_signals()
        
        print("\n🎯 UNIFIED SIGNAL RESULTS:")
        print(f"Market Regime: {results['market_regime']['regime_type']}")
        print(f"Final Signals: {results['final_signals']}")
        print(f"Signal Quality: {results['signal_quality_score']:.2%}")
        
        if results['unified_signals']:
            print("\n📈 TOP SIGNALS:")
            for i, signal in enumerate(results['unified_signals'][:3], 1):
                print(f"{i}. {signal['symbol']} - {signal['signal_type']} (Confidence: {signal['confidence_score']:.2%})")
    
    asyncio.run(main()) 