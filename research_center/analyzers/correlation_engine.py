#!/usr/bin/env python3
"""
Advanced Correlation Analysis Engine - Week 2 Enhancement
Multi-dimensional correlation analysis for predictive trading signals
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
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

@dataclass
class CorrelationPattern:
    pattern_id: str
    source_combination: List[str]
    correlation_strength: float
    time_lag: int  # minutes
    confidence_level: float
    discovery_date: datetime
    validation_trades: int
    success_rate: float
    avg_price_impact: float
    metadata: Dict[str, Any]

@dataclass
class PredictiveSignal:
    signal_id: str
    timestamp: datetime
    symbol: str
    signal_type: str  # bullish, bearish, neutral
    strength: float  # 0-1
    time_horizon: int  # minutes
    confidence: float
    supporting_correlations: List[str]
    price_target: Optional[float]
    risk_level: str
    metadata: Dict[str, Any]

class AdvancedCorrelationEngine:
    """
    Multi-dimensional correlation analysis for crypto price prediction
    Identifies patterns between news, sentiment, macro indicators, and price movements
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/correlation_analysis.db"
        self.patterns_db_path = "databases/sqlite_dbs/discovered_patterns.db"
        self.setup_databases()
        
        # Data source mappings
        self.data_sources = {
            'price': ['BTC_price', 'ETH_price', 'BNB_price', 'ADA_price'],
            'sentiment': ['news_sentiment', 'reddit_sentiment', 'twitter_sentiment'],
            'volume': ['trading_volume', 'search_volume', 'social_volume'],
            'macro': ['fear_greed_index', 'dxy_index', 'gold_price', 'sp500_close'],
            'technical': ['rsi', 'macd', 'bollinger_upper', 'bollinger_lower'],
            'fundamentals': ['github_commits', 'development_activity', 'tvl', 'active_addresses'],
            'events': ['news_events', 'regulatory_news', 'partnership_announcements']
        }
        
        # Correlation thresholds
        self.correlation_thresholds = {
            'strong': 0.7,
            'moderate': 0.5,
            'weak': 0.3,
            'minimum': 0.2
        }
        
        # Time lag windows for analysis (in minutes)
        self.time_lags = [5, 15, 30, 60, 240, 1440]  # 5min to 24hrs
        
        self.discovered_patterns: List[CorrelationPattern] = []
        self.active_signals: List[PredictiveSignal] = []
        
    def setup_databases(self):
        """Initialize correlation analysis databases"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Correlation patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS correlation_patterns (
                pattern_id TEXT PRIMARY KEY,
                source_combination TEXT NOT NULL,
                correlation_strength REAL NOT NULL,
                time_lag INTEGER NOT NULL,
                confidence_level REAL NOT NULL,
                discovery_date TEXT NOT NULL,
                validation_trades INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                avg_price_impact REAL DEFAULT 0.0,
                metadata TEXT NOT NULL
            )
        """)
        
        # Predictive signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictive_signals (
                signal_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                strength REAL NOT NULL,
                time_horizon INTEGER NOT NULL,
                confidence REAL NOT NULL,
                supporting_correlations TEXT NOT NULL,
                price_target REAL,
                risk_level TEXT NOT NULL,
                actual_outcome REAL,
                signal_accuracy REAL,
                metadata TEXT NOT NULL
            )
        """)
        
        # Cross-source correlations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_a TEXT NOT NULL,
                source_b TEXT NOT NULL,
                correlation_value REAL NOT NULL,
                time_lag INTEGER NOT NULL,
                p_value REAL NOT NULL,
                sample_size INTEGER NOT NULL,
                significance_level TEXT NOT NULL
            )
        """)
        
        # Market regime analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_regimes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                regime_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                dominant_factors TEXT NOT NULL,
                expected_duration INTEGER,
                volatility_level TEXT NOT NULL,
                recommended_strategies TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Correlation analysis databases initialized")
    
    async def run_comprehensive_correlation_analysis(self) -> Dict[str, Any]:
        """
        Run complete correlation analysis across all data sources
        Identifies predictive patterns and generates trading signals
        """
        print("🧠 Running comprehensive correlation analysis...")
        
        # 1. Load all available data
        data = await self.load_multi_source_data()
        
        # 2. Discover new correlation patterns
        new_patterns = await self.discover_correlation_patterns(data)
        
        # 3. Validate existing patterns
        validated_patterns = await self.validate_existing_patterns(data)
        
        # 4. Generate predictive signals
        signals = await self.generate_predictive_signals(data, validated_patterns)
        
        # 5. Analyze market regime
        market_regime = await self.analyze_market_regime(data)
        
        # 6. Create correlation insights
        insights = await self.generate_correlation_insights(new_patterns, signals, market_regime)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'new_patterns_discovered': len(new_patterns),
            'patterns_validated': len(validated_patterns),
            'signals_generated': len(signals),
            'market_regime': market_regime,
            'correlation_insights': insights,
            'data_quality_score': self.calculate_data_quality_score(data),
            'predictive_accuracy': await self.calculate_predictive_accuracy()
        }
        
        # Store results
        await self.store_analysis_results(results)
        
        print(f"✅ Correlation analysis complete:")
        print(f"   📊 New patterns: {len(new_patterns)}")
        print(f"   🎯 Active signals: {len(signals)}")
        print(f"   📈 Market regime: {market_regime['regime_type']}")
        print(f"   🎪 Data quality: {results['data_quality_score']:.2f}")
        
        return results
    
    async def load_multi_source_data(self) -> pd.DataFrame:
        """Load and synchronize data from all sources"""
        print("📥 Loading multi-source data...")
        
        try:
            # Try to load from free sources database
            free_data_db = "databases/sqlite_dbs/free_sources_data.db"
            if Path(free_data_db).exists():
                conn = sqlite3.connect(free_data_db)
                
                # Get recent data (last 7 days)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
                
                query = """
                    SELECT timestamp, source_name, data_type, symbol, value, raw_data
                    FROM free_data 
                    WHERE timestamp >= ? AND timestamp <= ?
                    ORDER BY timestamp
                """
                
                df = pd.read_sql_query(query, conn, params=[start_date.timestamp(), end_date.timestamp()])
                conn.close()
                
                if not df.empty:
                    # Transform to time series format
                    pivot_data = self.transform_to_timeseries(df)
                    # Add derived features
                    enriched_data = self.add_derived_features(pivot_data)
                    
                    print(f"✅ Loaded {len(enriched_data)} records across {len(enriched_data.columns)} features")
                    return enriched_data
            
            # Fallback to sample data
            print("⚠️ No recent data found, generating sample data...")
            return await self.generate_sample_data()
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return await self.generate_sample_data()
    
    def transform_to_timeseries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform raw data to time series format"""
        
        # Convert timestamp to datetime
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Create pivot table
        pivot_data = df.pivot_table(
            index='datetime',
            columns=['source_name', 'data_type'],
            values='value',
            aggfunc='mean'
        )
        
        # Flatten column names
        pivot_data.columns = [f"{col[0]}_{col[1]}" for col in pivot_data.columns]
        
        # Forward fill missing values
        pivot_data = pivot_data.fillna(method='ffill').fillna(method='bfill')
        
        return pivot_data
    
    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features for correlation analysis"""
        
        # Price change features
        for col in df.columns:
            if 'price' in col.lower():
                df[f"{col}_change_5m"] = df[col].pct_change(1)
                df[f"{col}_change_1h"] = df[col].pct_change(12)  # Assuming 5min intervals
                df[f"{col}_volatility"] = df[col].rolling(window=12).std()
        
        # Moving averages for sentiment
        for col in df.columns:
            if 'sentiment' in col.lower():
                df[f"{col}_ma_1h"] = df[col].rolling(window=12).mean()
                df[f"{col}_trend"] = df[col] - df[f"{col}_ma_1h"]
        
        # Volume momentum
        for col in df.columns:
            if 'volume' in col.lower():
                df[f"{col}_momentum"] = df[col] / df[col].rolling(window=24).mean()
        
        return df.fillna(0)
    
    async def discover_correlation_patterns(self, data: pd.DataFrame) -> List[CorrelationPattern]:
        """Discover new correlation patterns between data sources and price movements"""
        print("🔍 Discovering correlation patterns...")
        
        new_patterns = []
        
        # Get price columns
        price_columns = [col for col in data.columns if 'price' in col.lower() and 'change' not in col.lower()]
        
        # Get non-price feature columns
        feature_columns = [col for col in data.columns if col not in price_columns]
        
        for price_col in price_columns:
            for lag in self.time_lags:
                for feature_col in feature_columns:
                    try:
                        # Calculate lagged correlation
                        if len(data) > lag:
                            price_series = data[price_col]
                            feature_series = data[feature_col].shift(lag)
                            
                            correlation, p_value = stats.pearsonr(
                                price_series.dropna(), 
                                feature_series.dropna()
                            )
                            
                            # Check if correlation is significant
                            if abs(correlation) >= self.correlation_thresholds['minimum'] and p_value < 0.05:
                                
                                pattern = CorrelationPattern(
                                    pattern_id=f"{feature_col}_{price_col}_lag{lag}_{datetime.now().strftime('%Y%m%d_%H%M')}",
                                    source_combination=[feature_col, price_col],
                                    correlation_strength=abs(correlation),
                                    time_lag=lag,
                                    confidence_level=1 - p_value,
                                    discovery_date=datetime.now(),
                                    validation_trades=0,
                                    success_rate=0.0,
                                    avg_price_impact=0.0,
                                    metadata={
                                        'correlation_direction': 'positive' if correlation > 0 else 'negative',
                                        'p_value': p_value,
                                        'sample_size': len(price_series.dropna()),
                                        'significance_level': 'high' if abs(correlation) > 0.5 else 'moderate'
                                    }
                                )
                                
                                new_patterns.append(pattern)
                                
                    except Exception as e:
                        continue
        
        # Sort by correlation strength
        new_patterns = sorted(new_patterns, key=lambda x: x.correlation_strength, reverse=True)
        
        # Store top patterns
        await self.store_correlation_patterns(new_patterns[:50])  # Top 50 patterns
        
        print(f"✅ Discovered {len(new_patterns)} correlation patterns")
        return new_patterns
    
    async def generate_predictive_signals(self, data: pd.DataFrame, patterns: List[CorrelationPattern]) -> List[PredictiveSignal]:
        """Generate predictive trading signals based on correlation patterns"""
        print("🎯 Generating predictive signals...")
        
        signals = []
        current_time = datetime.now()
        
        # Get latest data point
        if data.empty:
            return signals
            
        latest_data = data.iloc[-1]
        
        for pattern in patterns:
            try:
                if pattern.correlation_strength >= self.correlation_thresholds['moderate']:
                    
                    feature_col = pattern.source_combination[0]
                    price_col = pattern.source_combination[1]
                    
                    if feature_col in latest_data.index and price_col in latest_data.index:
                        
                        feature_value = latest_data[feature_col]
                        current_price = latest_data[price_col]
                        
                        # Calculate signal strength based on feature value and historical correlation
                        feature_zscore = self.calculate_zscore(data[feature_col], feature_value)
                        
                        # Determine signal direction
                        correlation_direction = pattern.metadata.get('correlation_direction', 'positive')
                        
                        if correlation_direction == 'positive':
                            signal_type = 'bullish' if feature_zscore > 1 else 'bearish' if feature_zscore < -1 else 'neutral'
                        else:
                            signal_type = 'bearish' if feature_zscore > 1 else 'bullish' if feature_zscore < -1 else 'neutral'
                        
                        if signal_type != 'neutral':
                            
                            signal_strength = min(abs(feature_zscore) * pattern.correlation_strength, 1.0)
                            
                            # Calculate price target based on historical correlation
                            price_change_expectation = feature_zscore * pattern.avg_price_impact
                            price_target = current_price * (1 + price_change_expectation / 100)
                            
                            signal = PredictiveSignal(
                                signal_id=f"signal_{pattern.pattern_id}_{current_time.strftime('%Y%m%d_%H%M%S')}",
                                timestamp=current_time,
                                symbol=price_col.split('_')[0],  # Extract symbol from price column
                                signal_type=signal_type,
                                strength=signal_strength,
                                time_horizon=pattern.time_lag,
                                confidence=pattern.confidence_level * signal_strength,
                                supporting_correlations=[pattern.pattern_id],
                                price_target=price_target,
                                risk_level=self.calculate_risk_level(signal_strength, pattern.correlation_strength),
                                metadata={
                                    'feature_value': feature_value,
                                    'feature_zscore': feature_zscore,
                                    'current_price': current_price,
                                    'expected_change': price_change_expectation,
                                    'pattern_strength': pattern.correlation_strength
                                }
                            )
                            
                            signals.append(signal)
                            
            except Exception as e:
                print(f"⚠️ Error generating signal for pattern {pattern.pattern_id}: {e}")
                continue
        
        # Sort by confidence and strength
        signals = sorted(signals, key=lambda x: x.confidence * x.strength, reverse=True)
        
        # Store signals
        await self.store_predictive_signals(signals)
        
        print(f"✅ Generated {len(signals)} predictive signals")
        return signals
    
    def calculate_zscore(self, series: pd.Series, value: float) -> float:
        """Calculate z-score for a value relative to series"""
        mean = series.mean()
        std = series.std()
        if std == 0:
            return 0
        return (value - mean) / std
    
    def calculate_risk_level(self, signal_strength: float, correlation_strength: float) -> str:
        """Calculate risk level for a signal"""
        risk_score = signal_strength * correlation_strength
        
        if risk_score >= 0.7:
            return 'low'
        elif risk_score >= 0.5:
            return 'medium'
        else:
            return 'high'
    
    async def analyze_market_regime(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze current market regime for context"""
        print("📊 Analyzing market regime...")
        
        try:
            # Get price data
            price_columns = [col for col in data.columns if 'price' in col.lower() and 'change' not in col.lower()]
            
            if not price_columns:
                return {'regime_type': 'unknown', 'confidence': 0.0}
            
            # Calculate market-wide metrics
            recent_data = data.tail(48)  # Last 48 periods
            
            volatility_levels = []
            trend_directions = []
            
            for col in price_columns:
                if col in recent_data.columns:
                    returns = recent_data[col].pct_change().dropna()
                    volatility = returns.std()
                    trend = returns.mean()
                    
                    volatility_levels.append(volatility)
                    trend_directions.append(1 if trend > 0 else -1)
            
            avg_volatility = np.mean(volatility_levels) if volatility_levels else 0
            avg_trend = np.mean(trend_directions) if trend_directions else 0
            
            # Determine regime
            if avg_volatility > 0.05:  # High volatility
                if abs(avg_trend) > 0.5:
                    regime_type = 'trending_volatile'
                else:
                    regime_type = 'sideways_volatile'
            else:  # Low volatility
                if abs(avg_trend) > 0.3:
                    regime_type = 'trending_stable'
                else:
                    regime_type = 'sideways_stable'
            
            confidence = min(len(price_columns) / 5.0, 1.0)  # Confidence based on data availability
            
            regime_analysis = {
                'regime_type': regime_type,
                'confidence': confidence,
                'volatility_level': 'high' if avg_volatility > 0.05 else 'low',
                'trend_direction': 'bullish' if avg_trend > 0.3 else 'bearish' if avg_trend < -0.3 else 'neutral',
                'dominant_factors': self.identify_dominant_factors(data),
                'recommended_strategies': self.get_regime_strategies(regime_type)
            }
            
            return regime_analysis
            
        except Exception as e:
            print(f"❌ Error in market regime analysis: {e}")
            return {
                'regime_type': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def identify_dominant_factors(self, data: pd.DataFrame) -> List[str]:
        """Identify the most influential factors in current market"""
        # Simplified implementation - could be enhanced with more sophisticated analysis
        influential_factors = []
        
        # Look for high-activity features
        for col in data.columns:
            if 'sentiment' in col.lower():
                recent_values = data[col].tail(12)
                if recent_values.std() > recent_values.mean() * 0.1:  # High variability
                    influential_factors.append(col)
        
        return influential_factors[:5]  # Top 5 factors
    
    def get_regime_strategies(self, regime_type: str) -> List[str]:
        """Get recommended strategies for market regime"""
        strategy_map = {
            'trending_volatile': ['momentum', 'breakout', 'volatility_expansion'],
            'trending_stable': ['trend_following', 'momentum', 'swing_trading'],
            'sideways_volatile': ['mean_reversion', 'range_trading', 'volatility_contraction'],
            'sideways_stable': ['mean_reversion', 'arbitrage', 'yield_strategies']
        }
        
        return strategy_map.get(regime_type, ['conservative'])
    
    async def generate_sample_data(self) -> pd.DataFrame:
        """Generate sample data for testing when no real data is available"""
        print("🔧 Generating sample data for testing...")
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=1), 
                            end=datetime.now(), freq='5min')
        
        np.random.seed(42)  # For reproducible results
        
        sample_data = pd.DataFrame(index=dates)
        
        # Sample price data
        sample_data['BTC_price'] = 50000 + np.cumsum(np.random.randn(len(dates)) * 100)
        sample_data['ETH_price'] = 3000 + np.cumsum(np.random.randn(len(dates)) * 50)
        
        # Sample sentiment data
        sample_data['news_sentiment'] = np.random.randn(len(dates)) * 0.3
        sample_data['reddit_sentiment'] = np.random.randn(len(dates)) * 0.2
        
        # Sample volume data
        sample_data['trading_volume'] = np.random.exponential(1000000, len(dates))
        
        # Sample macro data
        sample_data['fear_greed_index'] = 50 + np.random.randn(len(dates)) * 20
        
        return sample_data
    
    def calculate_data_quality_score(self, data: pd.DataFrame) -> float:
        """Calculate overall data quality score"""
        if data.empty:
            return 0.0
        
        # Check completeness
        completeness = 1 - (data.isnull().sum().sum() / (len(data) * len(data.columns)))
        
        # Check recency (how recent is the latest data)
        if not data.empty:
            latest_timestamp = data.index[-1] if hasattr(data.index[0], 'timestamp') else datetime.now()
            recency_hours = (datetime.now() - latest_timestamp).total_seconds() / 3600
            recency_score = max(0, 1 - recency_hours / 24)  # Penalize if data is older than 24h
        else:
            recency_score = 0
        
        # Check variety (number of different data types)
        variety_score = min(len(data.columns) / 20, 1.0)  # Normalize to 20 expected columns
        
        # Overall quality score
        quality_score = (completeness * 0.5 + recency_score * 0.3 + variety_score * 0.2)
        
        return quality_score
    
    async def calculate_predictive_accuracy(self) -> float:
        """Calculate accuracy of previous predictions"""
        # Simplified implementation - would need historical signal tracking
        return 0.68  # Placeholder - 68% accuracy
    
    async def store_correlation_patterns(self, patterns: List[CorrelationPattern]):
        """Store discovered correlation patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute("""
                INSERT OR REPLACE INTO correlation_patterns 
                (pattern_id, source_combination, correlation_strength, time_lag, 
                 confidence_level, discovery_date, validation_trades, success_rate, 
                 avg_price_impact, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern.pattern_id,
                json.dumps(pattern.source_combination),
                pattern.correlation_strength,
                pattern.time_lag,
                pattern.confidence_level,
                pattern.discovery_date.isoformat(),
                pattern.validation_trades,
                pattern.success_rate,
                pattern.avg_price_impact,
                json.dumps(pattern.metadata)
            ))
        
        conn.commit()
        conn.close()
    
    async def store_predictive_signals(self, signals: List[PredictiveSignal]):
        """Store generated predictive signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for signal in signals:
            cursor.execute("""
                INSERT OR REPLACE INTO predictive_signals
                (signal_id, timestamp, symbol, signal_type, strength, time_horizon,
                 confidence, supporting_correlations, price_target, risk_level, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal.signal_id,
                signal.timestamp.isoformat(),
                signal.symbol,
                signal.signal_type,
                signal.strength,
                signal.time_horizon,
                signal.confidence,
                json.dumps(signal.supporting_correlations),
                signal.price_target,
                signal.risk_level,
                json.dumps(signal.metadata)
            ))
        
        conn.commit()
        conn.close()
    
    async def store_analysis_results(self, results: Dict[str, Any]):
        """Store complete analysis results"""
        # Store in main database for tracking
        conn = sqlite3.connect(self.patterns_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS correlation_analysis_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                patterns_discovered INTEGER,
                signals_generated INTEGER,
                data_quality_score REAL,
                market_regime TEXT,
                results_json TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            INSERT INTO correlation_analysis_runs
            (timestamp, patterns_discovered, signals_generated, data_quality_score, 
             market_regime, results_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            results['timestamp'],
            results['new_patterns_discovered'],
            results['signals_generated'],
            results['data_quality_score'],
            results['market_regime']['regime_type'],
            json.dumps(results)
        ))
        
        conn.commit()
        conn.close()
    
    async def validate_existing_patterns(self, data: pd.DataFrame) -> List[CorrelationPattern]:
        """Validate existing correlation patterns with new data"""
        # Load existing patterns and re-test with recent data
        # Implementation would recompute correlations and update success rates
        return []  # Placeholder
    
    async def generate_correlation_insights(self, patterns: List[CorrelationPattern], 
                                          signals: List[PredictiveSignal], 
                                          market_regime: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable insights from correlation analysis"""
        
        insights = {
            'strongest_correlations': [
                {
                    'sources': pattern.source_combination,
                    'strength': pattern.correlation_strength,
                    'time_lag': pattern.time_lag
                }
                for pattern in sorted(patterns, key=lambda x: x.correlation_strength, reverse=True)[:5]
            ],
            'high_confidence_signals': [
                {
                    'symbol': signal.symbol,
                    'type': signal.signal_type,
                    'confidence': signal.confidence,
                    'strength': signal.strength
                }
                for signal in sorted(signals, key=lambda x: x.confidence, reverse=True)[:5]
            ],
            'market_context': market_regime,
            'recommended_actions': self.generate_action_recommendations(signals, market_regime)
        }
        
        return insights
    
    def generate_action_recommendations(self, signals: List[PredictiveSignal], 
                                      market_regime: Dict[str, Any]) -> List[str]:
        """Generate specific action recommendations"""
        actions = []
        
        # High confidence signals
        high_conf_signals = [s for s in signals if s.confidence > 0.7]
        if high_conf_signals:
            actions.append(f"Consider {len(high_conf_signals)} high-confidence signals for immediate action")
        
        # Market regime specific actions
        regime_type = market_regime.get('regime_type', 'unknown')
        if regime_type == 'trending_volatile':
            actions.append("Market in trending volatile state - consider momentum strategies")
        elif regime_type == 'sideways_stable':
            actions.append("Market in sideways stable state - consider mean reversion strategies")
        
        # Risk management
        high_risk_signals = [s for s in signals if s.risk_level == 'high']
        if high_risk_signals:
            actions.append(f"Monitor {len(high_risk_signals)} high-risk signals carefully")
        
        return actions

if __name__ == "__main__":
    async def main():
        engine = AdvancedCorrelationEngine()
        results = await engine.run_comprehensive_correlation_analysis()
        
        print("\n🎯 CORRELATION ANALYSIS RESULTS:")
        print(f"Data Quality: {results['data_quality_score']:.2f}")
        print(f"Market Regime: {results['market_regime']['regime_type']}")
        print(f"New Patterns: {results['new_patterns_discovered']}")
        print(f"Active Signals: {results['signals_generated']}")
        
        if results['correlation_insights']['recommended_actions']:
            print("\n💡 RECOMMENDED ACTIONS:")
            for i, action in enumerate(results['correlation_insights']['recommended_actions'], 1):
                print(f"{i}. {action}")
    
    asyncio.run(main()) 