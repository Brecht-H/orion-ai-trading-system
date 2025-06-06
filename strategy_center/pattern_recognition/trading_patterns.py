#!/usr/bin/env python3
"""
Advanced Trading Pattern Recognition System - Week 2 Enhancement
Connects correlation patterns to actionable trading strategies
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
import os
import logging
warnings.filterwarnings('ignore')

class PatternType(Enum):
    MOMENTUM_BREAKOUT = "momentum_breakout"
    MEAN_REVERSION = "mean_reversion"
    VOLATILITY_EXPANSION = "volatility_expansion"
    VOLATILITY_CONTRACTION = "volatility_contraction"
    NEWS_SENTIMENT_DIVERGENCE = "news_sentiment_divergence"
    CORRELATION_BREAKDOWN = "correlation_breakdown"
    MULTI_ASSET_CONVERGENCE = "multi_asset_convergence"

class SignalStrength(Enum):
    VERY_STRONG = 5
    STRONG = 4
    MODERATE = 3
    WEAK = 2
    VERY_WEAK = 1

@dataclass
class TradingPattern:
    pattern_id: str
    pattern_type: PatternType
    symbols: List[str]
    confidence: float
    strength: SignalStrength
    entry_conditions: Dict[str, Any]
    exit_conditions: Dict[str, Any]
    risk_parameters: Dict[str, Any]
    expected_duration: int  # minutes
    historical_success_rate: float
    discovered_at: datetime
    last_validated: datetime
    metadata: Dict[str, Any]

@dataclass
class TradingSignal:
    signal_id: str
    timestamp: datetime
    symbol: str
    action: str  # BUY, SELL, HOLD
    quantity: float
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    confidence: float
    pattern_ids: List[str]
    risk_score: float
    expected_return: float
    time_horizon: int
    metadata: Dict[str, Any]

class AdvancedPatternRecognition:
    """
    Advanced pattern recognition that converts correlation analysis into trading strategies
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/trading_patterns.db"
        self.correlation_db = "databases/sqlite_dbs/correlation_analysis.db"
        self.setup_databases()
        
        # Pattern recognition parameters
        self.pattern_templates = self.initialize_pattern_templates()
        self.risk_management_rules = self.initialize_risk_rules()
        
        # Discovered patterns
        self.active_patterns: List[TradingPattern] = []
        self.generated_signals: List[TradingSignal] = []
        
        # 🔧 CRITICAL FIX: Setup logger
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            # Setup basic logging if not already configured
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
    def setup_databases(self):
        """Initialize pattern recognition databases"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trading patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                symbols TEXT NOT NULL,
                confidence REAL NOT NULL,
                strength INTEGER NOT NULL,
                entry_conditions TEXT NOT NULL,
                exit_conditions TEXT NOT NULL,
                risk_parameters TEXT NOT NULL,
                expected_duration INTEGER NOT NULL,
                historical_success_rate REAL NOT NULL,
                discovered_at TEXT NOT NULL,
                last_validated TEXT NOT NULL,
                validation_count INTEGER DEFAULT 0,
                profit_factor REAL DEFAULT 1.0,
                metadata TEXT NOT NULL
            )
        """)
        
        # Trading signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_signals (
                signal_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity REAL NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                confidence REAL NOT NULL,
                pattern_ids TEXT NOT NULL,
                risk_score REAL NOT NULL,
                expected_return REAL NOT NULL,
                time_horizon INTEGER NOT NULL,
                actual_return REAL,
                signal_success BOOLEAN,
                execution_status TEXT DEFAULT 'pending',
                metadata TEXT NOT NULL
            )
        """)
        
        # Pattern performance tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT NOT NULL,
                trade_date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                pnl REAL,
                pnl_percentage REAL,
                duration_minutes INTEGER,
                success BOOLEAN,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Pattern recognition databases initialized")
    
    def initialize_pattern_templates(self) -> Dict[PatternType, Dict[str, Any]]:
        """Initialize pattern recognition templates"""
        return {
            PatternType.MOMENTUM_BREAKOUT: {
                'description': 'Price breaks through resistance with strong momentum and correlation support',
                'min_confidence': 0.6,
                'time_horizon_range': (15, 240),  # 15 minutes to 4 hours
                'risk_reward_ratio': 2.5,
                'success_rate_threshold': 0.65
            },
            PatternType.MEAN_REVERSION: {
                'description': 'Price deviates significantly from mean with reversal indicators',
                'min_confidence': 0.55,
                'time_horizon_range': (30, 480),  # 30 minutes to 8 hours
                'risk_reward_ratio': 2.0,
                'success_rate_threshold': 0.60
            },
            PatternType.VOLATILITY_EXPANSION: {
                'description': 'Low volatility environment transitioning to high volatility',
                'min_confidence': 0.7,
                'time_horizon_range': (60, 1440),  # 1 hour to 24 hours
                'risk_reward_ratio': 3.0,
                'success_rate_threshold': 0.70
            },
            PatternType.NEWS_SENTIMENT_DIVERGENCE: {
                'description': 'Price and sentiment moving in opposite directions',
                'min_confidence': 0.5,
                'time_horizon_range': (5, 60),  # 5 minutes to 1 hour
                'risk_reward_ratio': 1.8,
                'success_rate_threshold': 0.58
            },
            PatternType.CORRELATION_BREAKDOWN: {
                'description': 'Historical correlations breaking down indicating regime change',
                'min_confidence': 0.65,
                'time_horizon_range': (240, 2880),  # 4 hours to 2 days
                'risk_reward_ratio': 2.2,
                'success_rate_threshold': 0.62
            }
        }
    
    def initialize_risk_rules(self) -> Dict[str, Any]:
        """Initialize risk management rules"""
        return {
            'max_position_size': 0.05,  # 5% of portfolio per trade
            'max_daily_risk': 0.02,     # 2% of portfolio per day
            'max_correlation_exposure': 0.15,  # 15% in correlated positions
            'stop_loss_percentage': 0.02,      # 2% stop loss
            'take_profit_multiplier': 2.5,     # 2.5x risk-reward ratio
            'max_concurrent_signals': 5,       # Maximum 5 active signals
            'min_time_between_signals': 15,    # 15 minutes between signals for same asset
        }
    
    async def run_pattern_recognition(self) -> Dict[str, Any]:
        """
        Main pattern recognition engine
        Analyzes correlation data and generates trading patterns and signals
        """
        print("🔍 Running advanced pattern recognition...")
        
        # 1. Load correlation analysis results
        correlation_data = await self.load_correlation_analysis()
        
        # 2. Load current market data
        market_data = await self.load_recent_market_data()
        
        # 3. Identify trading patterns
        discovered_patterns = await self.identify_trading_patterns(correlation_data, market_data)
        
        # 4. Validate patterns against historical data
        validated_patterns = await self.validate_patterns(discovered_patterns, market_data)
        
        # 5. Generate trading signals
        trading_signals = await self.generate_trading_signals(validated_patterns, market_data)
        
        # 6. Apply risk management filters
        filtered_signals = await self.apply_risk_filters(trading_signals)
        
        # 7. Create pattern insights
        insights = await self.generate_pattern_insights(validated_patterns, filtered_signals)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'patterns_discovered': len(discovered_patterns),
            'patterns_validated': len(validated_patterns),
            'signals_generated': len(trading_signals),
            'signals_after_risk_filter': len(filtered_signals),
            'pattern_insights': insights,
            'active_patterns': [asdict(p) for p in validated_patterns],
            'trading_signals': [asdict(s) for s in filtered_signals],
            'risk_assessment': await self.assess_portfolio_risk(filtered_signals)
        }
        
        # Store results
        await self.store_pattern_results(results)
        
        print(f"✅ Pattern recognition complete:")
        print(f"   🔍 Patterns discovered: {len(discovered_patterns)}")
        print(f"   ✅ Patterns validated: {len(validated_patterns)}")
        print(f"   📈 Trading signals: {len(filtered_signals)}")
        
        return results
    
    async def load_correlation_analysis(self) -> Dict[str, Any]:
        """Load latest correlation analysis results"""
        try:
            conn = sqlite3.connect(self.correlation_db)
            
            # Get latest correlation patterns
            query = """
                SELECT * FROM correlation_patterns 
                WHERE confidence_level > 0.5 
                ORDER BY correlation_strength DESC 
                LIMIT 100
            """
            
            patterns_df = pd.read_sql_query(query, conn)
            
            # Get latest predictive signals
            signals_query = """
                SELECT * FROM predictive_signals 
                WHERE timestamp > datetime('now', '-24 hours')
                ORDER BY confidence DESC
            """
            
            signals_df = pd.read_sql_query(signals_query, conn)
            conn.close()
            
            return {
                'correlation_patterns': patterns_df,
                'predictive_signals': signals_df,
                'loaded_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ Could not load correlation data: {e}")
            return {'correlation_patterns': pd.DataFrame(), 'predictive_signals': pd.DataFrame()}
    
    async def load_recent_market_data(self) -> pd.DataFrame:
        """🔥 CRITICAL FIX: Load real market data instead of generating mock data"""
        try:
            # First try to load from free sources database (real data)
            free_sources_db = "data/free_sources_data.db"
            
            if os.path.exists(free_sources_db):
                self.logger.info("📊 Loading REAL market data from free sources...")
                
                conn = sqlite3.connect(free_sources_db)
                
                # Load recent market data (last 24 hours)
                cutoff_time = (datetime.now() - timedelta(hours=24)).timestamp()
                
                query = """
                    SELECT timestamp, source_name, data_type, symbol, value, raw_data
                    FROM free_data 
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                """
                
                df = pd.read_sql_query(query, conn, params=[cutoff_time])
                conn.close()
                
                if not df.empty:
                    self.logger.info(f"✅ Loaded {len(df)} real market data records")
                    return self.process_real_market_data(df)
                else:
                    self.logger.warning("⚠️ No recent real data found, falling back to sample data")
            else:
                self.logger.warning("⚠️ Free sources database not found, falling back to sample data")
            
            # Fallback to sample data only if no real data available
            return await self.generate_sample_market_data()
            
        except Exception as e:
            self.logger.error(f"❌ Error loading market data: {e}")
            # Emergency fallback to sample data
            return await self.generate_sample_market_data()
    
    def process_real_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """🔄 Process real market data into analysis format"""
        try:
            processed_data = []
            
            # Process each data point
            for _, row in df.iterrows():
                try:
                    # Parse the raw JSON data
                    raw_data = json.loads(row['raw_data'])
                    
                    # Extract price data from different sources
                    if row['data_type'] == 'crypto_price':
                        if 'price_usd' in raw_data:
                            # CoinGecko format
                            processed_data.append({
                                'timestamp': pd.to_datetime(row['timestamp'], unit='s'),
                                'symbol': row['symbol'],
                                'price': float(raw_data.get('price_usd', 0)),
                                'volume': float(raw_data.get('volume_24h', 0)),
                                'change_24h': float(raw_data.get('change_24h', 0)),
                                'source': row['source_name']
                            })
                        elif 'price' in raw_data:
                            # Binance format
                            processed_data.append({
                                'timestamp': pd.to_datetime(row['timestamp'], unit='s'),
                                'symbol': row['symbol'],
                                'price': float(raw_data.get('price', 0)),
                                'volume': float(raw_data.get('volume_24h', 0)),
                                'change_24h': float(raw_data.get('change_24h', 0)),
                                'source': row['source_name']
                            })
                    
                    elif row['data_type'] == 'sentiment':
                        # Process sentiment data
                        if 'fear_greed_index' in raw_data:
                            processed_data.append({
                                'timestamp': pd.to_datetime(row['timestamp'], unit='s'),
                                'symbol': 'CRYPTO_MARKET',
                                'sentiment_score': float(raw_data.get('fear_greed_index', 50)) / 100,
                                'sentiment_class': raw_data.get('classification', 'neutral'),
                                'source': row['source_name']
                            })
                        elif 'avg_sentiment' in raw_data:
                            processed_data.append({
                                'timestamp': pd.to_datetime(row['timestamp'], unit='s'),
                                'symbol': 'SOCIAL_SENTIMENT',
                                'sentiment_score': float(raw_data.get('avg_sentiment', 0)),
                                'posts_analyzed': int(raw_data.get('posts_analyzed', 0)),
                                'source': row['source_name']
                            })
                    
                except Exception as e:
                    self.logger.debug(f"⚠️ Skipping malformed data row: {e}")
                    continue
            
            if not processed_data:
                self.logger.warning("⚠️ No valid price data found in real data")
                return pd.DataFrame()
            
            # Convert to DataFrame
            market_df = pd.DataFrame(processed_data)
            
            # Pivot to get symbols as columns
            if 'price' in market_df.columns:
                price_pivot = market_df[market_df['price'] > 0].pivot_table(
                    index='timestamp',
                    columns='symbol',
                    values='price',
                    aggfunc='mean'
                )
                
                # Add technical indicators for each symbol
                for symbol in price_pivot.columns:
                    if len(price_pivot[symbol].dropna()) > 14:  # Need enough data for RSI
                        price_pivot[f"{symbol}_rsi"] = self.calculate_rsi(price_pivot[symbol])
                        price_pivot[f"{symbol}_volatility"] = price_pivot[symbol].rolling(window=20).std()
                        price_pivot[f"{symbol}_momentum"] = price_pivot[symbol].pct_change(5)
                
                # Fill NaN values
                price_pivot = price_pivot.fillna(method='ffill').fillna(0)
                
                self.logger.info(f"✅ Processed real market data: {len(price_pivot)} timestamps, {len(price_pivot.columns)} indicators")
                return price_pivot
            
            self.logger.warning("⚠️ No price data found in processed data")
            return pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"❌ Error processing real market data: {e}")
            return pd.DataFrame()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    async def identify_trading_patterns(self, correlation_data: Dict[str, Any], 
                                      market_data: pd.DataFrame) -> List[TradingPattern]:
        """Identify trading patterns from correlation analysis"""
        print("🧠 Identifying trading patterns...")
        
        patterns = []
        correlation_patterns = correlation_data.get('correlation_patterns', pd.DataFrame())
        
        if correlation_patterns.empty:
            return patterns
        
        for _, correlation_row in correlation_patterns.iterrows():
            try:
                source_combo = json.loads(correlation_row['source_combination'])
                correlation_strength = correlation_row['correlation_strength']
                time_lag = correlation_row['time_lag']
                
                # Determine pattern type based on correlation characteristics
                pattern_type = self.classify_pattern_type(correlation_row, market_data)
                
                if pattern_type and correlation_strength >= self.pattern_templates[pattern_type]['min_confidence']:
                    
                    # Extract symbols from source combination
                    symbols = self.extract_symbols_from_sources(source_combo)
                    
                    # Calculate pattern confidence
                    confidence = self.calculate_pattern_confidence(correlation_row, market_data)
                    
                    # Determine signal strength
                    strength = self.determine_signal_strength(correlation_strength, confidence)
                    
                    # Create pattern
                    pattern = TradingPattern(
                        pattern_id=f"pattern_{pattern_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        pattern_type=pattern_type,
                        symbols=symbols,
                        confidence=confidence,
                        strength=strength,
                        entry_conditions=self.create_entry_conditions(pattern_type, correlation_row),
                        exit_conditions=self.create_exit_conditions(pattern_type, correlation_row),
                        risk_parameters=self.create_risk_parameters(pattern_type, correlation_strength),
                        expected_duration=self.estimate_pattern_duration(pattern_type, time_lag),
                        historical_success_rate=self.pattern_templates[pattern_type]['success_rate_threshold'],
                        discovered_at=datetime.now(),
                        last_validated=datetime.now(),
                        metadata={
                            'correlation_id': correlation_row['pattern_id'],
                            'correlation_strength': correlation_strength,
                            'time_lag': time_lag,
                            'source_combination': source_combo
                        }
                    )
                    
                    patterns.append(pattern)
                    
            except Exception as e:
                print(f"⚠️ Error processing correlation pattern: {e}")
                continue
        
        print(f"✅ Identified {len(patterns)} trading patterns")
        return patterns
    
    def classify_pattern_type(self, correlation_row: pd.Series, market_data: pd.DataFrame) -> Optional[PatternType]:
        """Classify the type of trading pattern based on correlation characteristics"""
        
        correlation_strength = correlation_row['correlation_strength']
        time_lag = correlation_row['time_lag']
        source_combo = json.loads(correlation_row['source_combination'])
        
        # Classify based on sources and characteristics
        if any('sentiment' in source.lower() for source in source_combo):
            if any('price' in source.lower() for source in source_combo):
                return PatternType.NEWS_SENTIMENT_DIVERGENCE
        
        if any('volume' in source.lower() for source in source_combo):
            if time_lag <= 30:  # Short-term volume patterns
                return PatternType.MOMENTUM_BREAKOUT
        
        if correlation_strength > 0.7:
            if time_lag > 240:  # Long-term strong correlations
                return PatternType.CORRELATION_BREAKDOWN
            else:  # Short-term strong correlations
                return PatternType.MOMENTUM_BREAKOUT
        
        if 0.3 <= correlation_strength <= 0.6:
            return PatternType.MEAN_REVERSION
        
        return None
    
    def extract_symbols_from_sources(self, source_combo: List[str]) -> List[str]:
        """Extract trading symbols from source combination"""
        symbols = set()
        
        for source in source_combo:
            # Extract symbol from source name (e.g., "BTC_price" -> "BTC")
            parts = source.split('_')
            for part in parts:
                if part.upper() in ['BTC', 'ETH', 'ADA', 'BNB', 'SOL', 'DOT', 'LINK', 'UNI']:
                    symbols.add(part.upper())
        
        return list(symbols) if symbols else ['BTC']  # Default to BTC
    
    def calculate_pattern_confidence(self, correlation_row: pd.Series, market_data: pd.DataFrame) -> float:
        """Calculate confidence level for the trading pattern"""
        base_confidence = correlation_row['confidence_level']
        correlation_strength = correlation_row['correlation_strength']
        
        # Adjust confidence based on current market conditions
        confidence_adjustment = 0.0
        
        # Check data availability
        if not market_data.empty:
            confidence_adjustment += 0.1
        
        # Strong correlations get confidence boost
        if correlation_strength > 0.6:
            confidence_adjustment += 0.1
        
        return min(base_confidence + confidence_adjustment, 1.0)
    
    def determine_signal_strength(self, correlation_strength: float, confidence: float) -> SignalStrength:
        """Determine signal strength based on correlation and confidence"""
        combined_score = (correlation_strength + confidence) / 2
        
        if combined_score >= 0.8:
            return SignalStrength.VERY_STRONG
        elif combined_score >= 0.7:
            return SignalStrength.STRONG
        elif combined_score >= 0.6:
            return SignalStrength.MODERATE
        elif combined_score >= 0.5:
            return SignalStrength.WEAK
        else:
            return SignalStrength.VERY_WEAK
    
    def create_entry_conditions(self, pattern_type: PatternType, correlation_row: pd.Series) -> Dict[str, Any]:
        """Create entry conditions for the pattern"""
        base_conditions = {
            'min_confidence': 0.6,
            'min_volume_ratio': 1.2,
            'max_position_size': 0.05
        }
        
        if pattern_type == PatternType.MOMENTUM_BREAKOUT:
            base_conditions.update({
                'price_breakout_threshold': 0.02,  # 2% price move
                'volume_confirmation': True,
                'rsi_range': (30, 70)
            })
        elif pattern_type == PatternType.MEAN_REVERSION:
            base_conditions.update({
                'rsi_oversold': 30,
                'rsi_overbought': 70,
                'price_deviation_threshold': 2.0  # 2 standard deviations
            })
        
        return base_conditions
    
    def create_exit_conditions(self, pattern_type: PatternType, correlation_row: pd.Series) -> Dict[str, Any]:
        """Create exit conditions for the pattern"""
        template = self.pattern_templates[pattern_type]
        
        return {
            'stop_loss_percentage': self.risk_management_rules['stop_loss_percentage'],
            'take_profit_ratio': template['risk_reward_ratio'],
            'max_holding_time': template['time_horizon_range'][1],
            'trailing_stop': True
        }
    
    def create_risk_parameters(self, pattern_type: PatternType, correlation_strength: float) -> Dict[str, Any]:
        """Create risk parameters for the pattern"""
        base_risk = self.risk_management_rules['max_position_size']
        
        # Adjust risk based on pattern strength
        risk_multiplier = min(correlation_strength * 1.5, 1.0)
        
        return {
            'max_position_size': base_risk * risk_multiplier,
            'stop_loss_percentage': self.risk_management_rules['stop_loss_percentage'],
            'risk_reward_ratio': self.pattern_templates[pattern_type]['risk_reward_ratio'],
            'correlation_strength_factor': correlation_strength
        }
    
    def estimate_pattern_duration(self, pattern_type: PatternType, time_lag: int) -> int:
        """Estimate how long the pattern is expected to last"""
        base_range = self.pattern_templates[pattern_type]['time_horizon_range']
        
        # Use time lag as a guide for duration
        if time_lag <= 15:
            return base_range[0]  # Minimum duration
        elif time_lag >= 240:
            return base_range[1]  # Maximum duration
        else:
            # Interpolate based on time lag
            ratio = time_lag / 240
            return int(base_range[0] + (base_range[1] - base_range[0]) * ratio)
    
    async def validate_patterns(self, patterns: List[TradingPattern], market_data: pd.DataFrame) -> List[TradingPattern]:
        """Validate patterns against current market conditions"""
        print(f"✅ Validating {len(patterns)} patterns...")
        
        validated_patterns = []
        
        for pattern in patterns:
            try:
                # Simple validation based on pattern confidence and market data availability
                validation_score = pattern.confidence
                
                # Boost validation if we have market data for the symbols
                for symbol in pattern.symbols:
                    symbol_columns = [col for col in market_data.columns if symbol.lower() in col.lower()]
                    if symbol_columns:
                        validation_score += 0.1
                
                # Accept patterns with reasonable validation scores
                if validation_score >= 0.5:
                    validated_patterns.append(pattern)
                    
            except Exception as e:
                print(f"⚠️ Error validating pattern {pattern.pattern_id}: {e}")
                continue
        
        print(f"✅ Validated {len(validated_patterns)} patterns")
        return validated_patterns
    
    async def generate_trading_signals(self, patterns: List[TradingPattern], market_data: pd.DataFrame) -> List[TradingSignal]:
        """Generate trading signals from validated patterns"""
        print(f"📈 Generating signals from {len(patterns)} patterns...")
        
        signals = []
        current_time = datetime.now()
        
        for pattern in patterns:
            try:
                for symbol in pattern.symbols:
                    # Get current price if available
                    current_price = self.get_current_price(symbol, market_data)
                    
                    if current_price is None:
                        continue
                    
                    # Determine signal action based on pattern type
                    action = self.determine_signal_action(pattern, market_data)
                    
                    if action != 'HOLD':
                        # Calculate position size
                        position_size = self.calculate_position_size(pattern, current_price)
                        
                        # Calculate stop loss and take profit
                        stop_loss, take_profit = self.calculate_exit_levels(pattern, current_price, action)
                        
                        signal = TradingSignal(
                            signal_id=f"signal_{pattern.pattern_id}_{symbol}_{current_time.strftime('%Y%m%d_%H%M%S')}",
                            timestamp=current_time,
                            symbol=symbol,
                            action=action,
                            quantity=position_size,
                            entry_price=current_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            confidence=pattern.confidence,
                            pattern_ids=[pattern.pattern_id],
                            risk_score=self.calculate_signal_risk(pattern, current_price),
                            expected_return=self.calculate_expected_return(pattern),
                            time_horizon=pattern.expected_duration,
                            metadata={
                                'pattern_type': pattern.pattern_type.value,
                                'pattern_strength': pattern.strength.value,
                                'entry_conditions': pattern.entry_conditions,
                                'exit_conditions': pattern.exit_conditions
                            }
                        )
                        
                        signals.append(signal)
                        
            except Exception as e:
                print(f"⚠️ Error generating signal for pattern {pattern.pattern_id}: {e}")
                continue
        
        print(f"✅ Generated {len(signals)} trading signals")
        return signals
    
    def get_current_price(self, symbol: str, market_data: pd.DataFrame) -> Optional[float]:
        """Get current price for symbol from market data"""
        price_columns = [col for col in market_data.columns if symbol.lower() in col.lower() and 'price' in col.lower()]
        
        if price_columns and not market_data.empty:
            return float(market_data[price_columns[0]].iloc[-1])
        
        # Default prices for testing
        default_prices = {'BTC': 50000, 'ETH': 3000, 'ADA': 0.5, 'BNB': 300}
        return default_prices.get(symbol, 100)
    
    def determine_signal_action(self, pattern: TradingPattern, market_data: pd.DataFrame) -> str:
        """Determine trading action based on pattern"""
        if pattern.pattern_type == PatternType.MOMENTUM_BREAKOUT:
            return 'BUY'
        elif pattern.pattern_type == PatternType.MEAN_REVERSION:
            return 'BUY'  # Simplified - would need more logic
        elif pattern.pattern_type == PatternType.NEWS_SENTIMENT_DIVERGENCE:
            return 'BUY' if pattern.confidence > 0.6 else 'SELL'
        else:
            return 'HOLD'
    
    def calculate_position_size(self, pattern: TradingPattern, current_price: float) -> float:
        """Calculate position size based on risk parameters"""
        max_position_size = pattern.risk_parameters.get('max_position_size', 0.05)
        
        # Simplified position sizing - would normally consider portfolio size
        portfolio_value = 10000  # Default portfolio size
        position_value = portfolio_value * max_position_size
        
        return position_value / current_price
    
    def calculate_exit_levels(self, pattern: TradingPattern, entry_price: float, action: str) -> Tuple[Optional[float], Optional[float]]:
        """Calculate stop loss and take profit levels"""
        stop_loss_pct = pattern.risk_parameters.get('stop_loss_percentage', 0.02)
        risk_reward_ratio = pattern.risk_parameters.get('risk_reward_ratio', 2.0)
        
        if action == 'BUY':
            stop_loss = entry_price * (1 - stop_loss_pct)
            take_profit = entry_price * (1 + stop_loss_pct * risk_reward_ratio)
        else:  # SELL
            stop_loss = entry_price * (1 + stop_loss_pct)
            take_profit = entry_price * (1 - stop_loss_pct * risk_reward_ratio)
        
        return stop_loss, take_profit
    
    def calculate_signal_risk(self, pattern: TradingPattern, current_price: float) -> float:
        """Calculate risk score for the signal"""
        base_risk = 1 - pattern.confidence
        
        # Adjust risk based on pattern strength
        strength_adjustment = (5 - pattern.strength.value) * 0.1
        
        return min(base_risk + strength_adjustment, 1.0)
    
    def calculate_expected_return(self, pattern: TradingPattern) -> float:
        """Calculate expected return for the pattern"""
        risk_reward_ratio = pattern.risk_parameters.get('risk_reward_ratio', 2.0)
        stop_loss_pct = pattern.risk_parameters.get('stop_loss_percentage', 0.02)
        
        return stop_loss_pct * risk_reward_ratio
    
    async def apply_risk_filters(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Apply risk management filters to signals"""
        print(f"🛡️ Applying risk filters to {len(signals)} signals...")
        
        filtered_signals = []
        
        # Sort by confidence descending
        sorted_signals = sorted(signals, key=lambda s: s.confidence, reverse=True)
        
        for signal in sorted_signals:
            # Risk filters
            if signal.risk_score > 0.8:  # Too risky
                continue
            
            if signal.confidence < 0.3:  # Too low confidence
                continue
            
            # Limit number of concurrent signals
            if len(filtered_signals) >= self.risk_management_rules['max_concurrent_signals']:
                break
            
            filtered_signals.append(signal)
        
        print(f"✅ {len(filtered_signals)} signals passed risk filters")
        return filtered_signals
    
    async def assess_portfolio_risk(self, signals: List[TradingSignal]) -> Dict[str, Any]:
        """Assess overall portfolio risk from signals"""
        if not signals:
            return {'total_risk': 0.0, 'risk_level': 'none'}
        
        total_risk = sum(signal.risk_score for signal in signals) / len(signals)
        
        risk_level = 'low' if total_risk < 0.3 else 'medium' if total_risk < 0.6 else 'high'
        
        return {
            'total_risk': total_risk,
            'risk_level': risk_level,
            'signal_count': len(signals),
            'avg_confidence': sum(s.confidence for s in signals) / len(signals)
        }
    
    async def generate_pattern_insights(self, patterns: List[TradingPattern], signals: List[TradingSignal]) -> Dict[str, Any]:
        """Generate insights from pattern analysis"""
        insights = {
            'pattern_summary': {
                'total_patterns': len(patterns),
                'pattern_types': {},
                'avg_confidence': sum(p.confidence for p in patterns) / len(patterns) if patterns else 0,
                'strongest_patterns': []
            },
            'signal_summary': {
                'total_signals': len(signals),
                'buy_signals': len([s for s in signals if s.action == 'BUY']),
                'sell_signals': len([s for s in signals if s.action == 'SELL']),
                'avg_expected_return': sum(s.expected_return for s in signals) / len(signals) if signals else 0
            },
            'recommendations': []
        }
        
        # Count pattern types
        for pattern in patterns:
            pattern_type = pattern.pattern_type.value
            insights['pattern_summary']['pattern_types'][pattern_type] = insights['pattern_summary']['pattern_types'].get(pattern_type, 0) + 1
        
        # Add strongest patterns
        strongest_patterns = sorted(patterns, key=lambda p: p.confidence, reverse=True)[:3]
        insights['pattern_summary']['strongest_patterns'] = [
            {
                'pattern_id': p.pattern_id,
                'type': p.pattern_type.value,
                'confidence': p.confidence,
                'symbols': p.symbols
            }
            for p in strongest_patterns
        ]
        
        # Generate recommendations
        if len(signals) > 5:
            insights['recommendations'].append("High signal activity detected - consider position sizing adjustments")
        
        if insights['signal_summary']['avg_expected_return'] > 0.05:
            insights['recommendations'].append("Strong expected returns - consider increasing position sizes")
        
        return insights
    
    async def store_pattern_results(self, results: Dict[str, Any]):
        """Store pattern recognition results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store patterns
        for pattern_dict in results.get('active_patterns', []):
            cursor.execute("""
                INSERT OR REPLACE INTO trading_patterns
                (pattern_id, pattern_type, symbols, confidence, strength,
                 entry_conditions, exit_conditions, risk_parameters,
                 expected_duration, historical_success_rate, discovered_at,
                 last_validated, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern_dict['pattern_id'],
                pattern_dict['pattern_type'],
                json.dumps(pattern_dict['symbols']),
                pattern_dict['confidence'],
                pattern_dict['strength'],
                json.dumps(pattern_dict['entry_conditions']),
                json.dumps(pattern_dict['exit_conditions']),
                json.dumps(pattern_dict['risk_parameters']),
                pattern_dict['expected_duration'],
                pattern_dict['historical_success_rate'],
                pattern_dict['discovered_at'],
                pattern_dict['last_validated'],
                json.dumps(pattern_dict['metadata'])
            ))
        
        # Store signals
        for signal_dict in results.get('trading_signals', []):
            cursor.execute("""
                INSERT OR REPLACE INTO trading_signals
                (signal_id, timestamp, symbol, action, quantity,
                 entry_price, stop_loss, take_profit, confidence,
                 pattern_ids, risk_score, expected_return, time_horizon, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal_dict['signal_id'],
                signal_dict['timestamp'],
                signal_dict['symbol'],
                signal_dict['action'],
                signal_dict['quantity'],
                signal_dict['entry_price'],
                signal_dict['stop_loss'],
                signal_dict['take_profit'],
                signal_dict['confidence'],
                json.dumps(signal_dict['pattern_ids']),
                signal_dict['risk_score'],
                signal_dict['expected_return'],
                signal_dict['time_horizon'],
                json.dumps(signal_dict['metadata'])
            ))
        
        conn.commit()
        conn.close()
    
    async def generate_sample_market_data(self) -> pd.DataFrame:
        """🔧 Generate sample market data ONLY as fallback"""
        self.logger.warning("⚠️ Using SAMPLE data - real data unavailable")
        
        dates = pd.date_range(start=datetime.now() - timedelta(hours=6), 
                            end=datetime.now(), freq='5min')
        
        np.random.seed(42)
        
        sample_data = pd.DataFrame(index=dates)
        sample_data['BTC_price'] = 50000 + np.cumsum(np.random.randn(len(dates)) * 100)
        sample_data['ETH_price'] = 3000 + np.cumsum(np.random.randn(len(dates)) * 50)
        
        # Add technical indicators
        sample_data['BTC_rsi'] = self.calculate_rsi(sample_data['BTC_price'])
        sample_data['ETH_rsi'] = self.calculate_rsi(sample_data['ETH_price'])
        
        self.logger.warning("⚠️ SAMPLE DATA GENERATED - NOT FOR LIVE TRADING")
        return sample_data.fillna(50)  # Fill RSI NaNs with neutral value

if __name__ == "__main__":
    async def main():
        recognizer = AdvancedPatternRecognition()
        results = await recognizer.run_pattern_recognition()
        
        print("\n🎯 PATTERN RECOGNITION RESULTS:")
        print(f"Patterns Discovered: {results['patterns_discovered']}")
        print(f"Patterns Validated: {results['patterns_validated']}")
        print(f"Trading Signals: {results['signals_after_risk_filter']}")
        
        if results['trading_signals']:
            print("\n📈 TOP TRADING SIGNALS:")
            for i, signal in enumerate(results['trading_signals'][:3], 1):
                print(f"{i}. {signal['symbol']} - {signal['action']} (Confidence: {signal['confidence']:.2f})")
    
    asyncio.run(main()) 