#!/usr/bin/env python3
"""
Unified Signal Aggregator - ORION PHASE 2
Combines RSS, Twitter, OnChain, and Sentiment signals into actionable trading intelligence
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from pathlib import Path
import logging

@dataclass
class UnifiedSignal:
    signal_id: str
    timestamp: float
    signal_type: str  # "RSS", "TWITTER", "ONCHAIN", "SENTIMENT", "CORRELATION"
    symbol: str  # BTC, ETH, etc.
    direction: str  # "BULLISH", "BEARISH", "NEUTRAL"
    confidence: float  # 0.0 - 1.0
    strength: float  # 0.0 - 1.0
    source: str
    content: str
    impact_prediction: float  # Expected price impact
    time_horizon: str  # "SHORT", "MEDIUM", "LONG"
    correlations: List[str]  # Related signals
    metadata: Dict[str, Any]

@dataclass
class MarketSignal:
    symbol: str
    overall_direction: str
    confidence_score: float
    signal_count: int
    bullish_signals: int
    bearish_signals: int
    dominant_sources: List[str]
    predicted_impact: float
    risk_score: float
    timestamp: float

class SignalAggregator:
    """
    Master Signal Aggregation System
    Combines all data sources into unified trading intelligence
    """
    
    def __init__(self):
        self.db_path = "databases/sqlite_dbs/enhanced_signals.db"
        self.logger = self.setup_logging()
        self.setup_database()
        
        # Signal weights by source reliability
        self.source_weights = {
            "RSS_REUTERS": 0.95,
            "RSS_SEC": 1.0,
            "RSS_FEDERALRESERVE": 0.9,
            "RSS_COINDESK": 0.85,
            "RSS_COINTELEGRAPH": 0.8,
            "TWITTER_ELONMUSK": 0.9,
            "TWITTER_SAYLOR": 0.85,
            "TWITTER_VITALIK": 0.8,
            "ONCHAIN_WHALE": 0.9,
            "ONCHAIN_EXCHANGE": 0.85,
            "SENTIMENT_REDDIT": 0.7,
            "SENTIMENT_SOCIAL": 0.65
        }
        
        # Correlation patterns for signal amplification
        self.correlation_patterns = {
            "REGULATORY_NEGATIVE": ["SEC", "CFTC", "regulatory", "ban", "restriction"],
            "INSTITUTIONAL_POSITIVE": ["MicroStrategy", "Tesla", "institutional", "adoption"],
            "WHALE_MOVEMENT": ["whale", "large transfer", "exchange inflow", "exchange outflow"],
            "TECHNICAL_BREAKOUT": ["breakout", "resistance", "support", "volume"]
        }
        
        self.logger.info("🎯 Signal Aggregator initialized - Phase 2 Enhanced Intelligence")
    
    def setup_database(self):
        """Setup unified signals database"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enhanced_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT UNIQUE NOT NULL,
                timestamp REAL NOT NULL,
                signal_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                confidence REAL NOT NULL,
                strength REAL NOT NULL,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                impact_prediction REAL NOT NULL,
                time_horizon TEXT NOT NULL,
                correlations TEXT,
                metadata TEXT,
                processed BOOLEAN DEFAULT 0
            )
        """)
        
        # Market signals table (aggregated by symbol)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp REAL NOT NULL,
                overall_direction TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                signal_count INTEGER NOT NULL,
                bullish_signals INTEGER NOT NULL,
                bearish_signals INTEGER NOT NULL,
                dominant_sources TEXT NOT NULL,
                predicted_impact REAL NOT NULL,
                risk_score REAL NOT NULL,
                metadata TEXT
            )
        """)
        
        # Signal correlations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signal_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                primary_signal_id TEXT NOT NULL,
                correlated_signal_id TEXT NOT NULL,
                correlation_strength REAL NOT NULL,
                correlation_type TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def setup_logging(self):
        """Setup signal aggregator logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SignalAggregator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/signal_aggregator.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def collect_all_signals(self) -> Dict[str, Any]:
        """Collect and aggregate signals from all sources"""
        self.logger.info("🔄 Starting comprehensive signal collection...")
        start_time = time.time()
        
        # 1. Collect signals from each source
        rss_signals = self.collect_rss_signals()
        twitter_signals = self.collect_twitter_signals()
        onchain_signals = self.collect_onchain_signals()
        sentiment_signals = self.collect_sentiment_signals()
        
        # 2. Process and unify signals
        all_signals = rss_signals + twitter_signals + onchain_signals + sentiment_signals
        unified_signals = self.process_unified_signals(all_signals)
        
        # 3. Generate market signals by symbol
        market_signals = self.generate_market_signals(unified_signals)
        
        # 4. Identify correlations
        correlations = self.identify_signal_correlations(unified_signals)
        
        execution_time = time.time() - start_time
        
        summary = {
            "total_signals": len(unified_signals),
            "market_signals": len(market_signals),
            "correlations_found": len(correlations),
            "execution_time": execution_time,
            "signal_breakdown": {
                "RSS": len(rss_signals),
                "Twitter": len(twitter_signals),
                "OnChain": len(onchain_signals),
                "Sentiment": len(sentiment_signals)
            },
            "top_market_signals": [
                {
                    "symbol": signal.symbol,
                    "direction": signal.overall_direction,
                    "confidence": signal.confidence_score,
                    "impact": signal.predicted_impact
                } for signal in market_signals[:5]
            ]
        }
        
        self.logger.info(f"✅ Signal aggregation complete ({execution_time:.2f}s)")
        self.logger.info(f"   📊 Total signals: {len(unified_signals)}")
        self.logger.info(f"   🎯 Market signals: {len(market_signals)}")
        self.logger.info(f"   🔗 Correlations: {len(correlations)}")
        
        return summary
    
    def collect_rss_signals(self) -> List[UnifiedSignal]:
        """Extract signals from RSS monitoring data"""
        signals = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/comprehensive_rss_data.db")
            cursor = conn.cursor()
            
            # Get recent RSS articles with sentiment
            recent_articles = cursor.execute("""
                SELECT title, description, sentiment_score, relevance_score, feed_name, timestamp
                FROM rss_articles 
                WHERE timestamp > ?
                ORDER BY relevance_score DESC
                LIMIT 50
            """, (datetime.now() - timedelta(days=1),)).fetchall()
            
            conn.close()
            
            for article in recent_articles:
                title, description, sentiment, relevance, source, timestamp = article
                
                # Extract symbol mentions
                symbols = self.extract_crypto_symbols(title + " " + description)
                
                for symbol in symbols:
                    # Determine direction from sentiment and keywords
                    direction = self.determine_direction_from_content(title + " " + description, sentiment)
                    
                    # Calculate confidence based on source and relevance
                    source_weight = self.source_weights.get(f"RSS_{source.upper()}", 0.7)
                    confidence = min(abs(sentiment) * source_weight * relevance, 1.0)
                    
                    signal = UnifiedSignal(
                        signal_id=f"RSS_{symbol}_{hash(title)}",
                        timestamp=time.time(),
                        signal_type="RSS",
                        symbol=symbol,
                        direction=direction,
                        confidence=confidence,
                        strength=abs(sentiment),
                        source=f"RSS_{source}",
                        content=title[:200],
                        impact_prediction=relevance,
                        time_horizon=self.determine_time_horizon(description),
                        correlations=[],
                        metadata={"full_content": description[:500]}
                    )
                    signals.append(signal)
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error collecting RSS signals: {e}")
        
        return signals
    
    def collect_twitter_signals(self) -> List[UnifiedSignal]:
        """Extract signals from Twitter intelligence data"""
        signals = []
        
        try:
            conn = sqlite3.connect("databases/sqlite_dbs/twitter_intelligence.db")
            cursor = conn.cursor()
            
            # Get recent tweets with market signals
            recent_tweets = cursor.execute("""
                SELECT username, content, sentiment_score, influence_score, timestamp, market_impact
                FROM twitter_posts 
                WHERE timestamp > ?
                ORDER BY influence_score DESC
                LIMIT 30
            """, (datetime.now() - timedelta(days=1),)).fetchall()
            
            conn.close()
            
            for tweet in recent_tweets:
                username, content, sentiment, influence, timestamp, market_signal = tweet
                
                # Extract symbols
                symbols = self.extract_crypto_symbols(content)
                
                for symbol in symbols:
                    direction = self.determine_direction_from_content(content, sentiment)
                    
                    # Twitter influence weight
                    source_weight = self.source_weights.get(f"TWITTER_{username.upper()}", 0.6)
                    confidence = min(abs(sentiment) * source_weight * influence, 1.0)
                    
                    signal = UnifiedSignal(
                        signal_id=f"TWITTER_{symbol}_{username}_{int(timestamp)}",
                        timestamp=timestamp,
                        signal_type="TWITTER",
                        symbol=symbol,
                        direction=direction,
                        confidence=confidence,
                        strength=influence,
                        source=f"TWITTER_{username}",
                        content=content[:200],
                        impact_prediction=market_signal if market_signal else 0.0,
                        time_horizon="SHORT",
                        correlations=[],
                        metadata={"influence_score": influence}
                    )
                    signals.append(signal)
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error collecting Twitter signals: {e}")
        
        return signals
    
    def collect_onchain_signals(self) -> List[UnifiedSignal]:
        """Extract signals from OnChain oracle data"""
        signals = []
        
        try:
            # Get whale movements and exchange flows
            whale_movements = self.get_whale_movements()
            exchange_flows = self.get_exchange_flows()
            
            # Process whale movements
            for movement in whale_movements:
                direction = "BEARISH" if movement['type'] == 'exchange_inflow' else "BULLISH"
                
                signal = UnifiedSignal(
                    signal_id=f"ONCHAIN_WHALE_{movement['symbol']}_{int(movement['timestamp'])}",
                    timestamp=movement['timestamp'],
                    signal_type="ONCHAIN",
                    symbol=movement['symbol'],
                    direction=direction,
                    confidence=0.8,
                    strength=min(movement['amount'] / 1000, 1.0),  # Normalize by 1000 BTC
                    source="ONCHAIN_WHALE",
                    content=f"Whale movement: {movement['amount']} {movement['symbol']}",
                    impact_prediction=movement.get('impact_score', 0.5),
                    time_horizon="MEDIUM",
                    correlations=[],
                    metadata=movement
                )
                signals.append(signal)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error collecting OnChain signals: {e}")
        
        return signals
    
    def collect_sentiment_signals(self) -> List[UnifiedSignal]:
        """Extract signals from social sentiment analysis"""
        signals = []
        
        try:
            # Mock sentiment data - in production this would come from social sentiment agent
            sentiment_data = [
                {"symbol": "BTC", "sentiment": 0.7, "volume": 1000, "source": "REDDIT"},
                {"symbol": "ETH", "sentiment": -0.3, "volume": 800, "source": "SOCIAL"},
                {"symbol": "SOL", "sentiment": 0.5, "volume": 500, "source": "REDDIT"}
            ]
            
            for data in sentiment_data:
                direction = "BULLISH" if data['sentiment'] > 0 else "BEARISH"
                
                signal = UnifiedSignal(
                    signal_id=f"SENTIMENT_{data['symbol']}_{int(time.time())}",
                    timestamp=time.time(),
                    signal_type="SENTIMENT",
                    symbol=data['symbol'],
                    direction=direction,
                    confidence=abs(data['sentiment']),
                    strength=min(data['volume'] / 1000, 1.0),
                    source=f"SENTIMENT_{data['source']}",
                    content=f"Social sentiment analysis: {data['sentiment']:.2f}",
                    impact_prediction=abs(data['sentiment']) * 0.5,
                    time_horizon="SHORT",
                    correlations=[],
                    metadata=data
                )
                signals.append(signal)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error collecting sentiment signals: {e}")
        
        return signals
    
    def process_unified_signals(self, signals: List[UnifiedSignal]) -> List[UnifiedSignal]:
        """Process and store unified signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        processed_signals = []
        
        for signal in signals:
            try:
                # Store signal in database
                cursor.execute("""
                    INSERT OR REPLACE INTO enhanced_signals 
                    (signal_id, timestamp, signal_type, symbol, direction, confidence, 
                     strength, source, content, impact_prediction, time_horizon, 
                     correlations, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    signal.signal_id, signal.timestamp, signal.signal_type,
                    signal.symbol, signal.direction, signal.confidence,
                    signal.strength, signal.source, signal.content,
                    signal.impact_prediction, signal.time_horizon,
                    json.dumps(signal.correlations), json.dumps(signal.metadata)
                ))
                
                processed_signals.append(signal)
                
            except Exception as e:
                self.logger.warning(f"⚠️ Error processing signal {signal.signal_id}: {e}")
        
        conn.commit()
        conn.close()
        
        return processed_signals
    
    def generate_market_signals(self, signals: List[UnifiedSignal]) -> List[MarketSignal]:
        """Generate aggregated market signals by symbol"""
        symbol_groups = {}
        
        # Group signals by symbol
        for signal in signals:
            if signal.symbol not in symbol_groups:
                symbol_groups[signal.symbol] = []
            symbol_groups[signal.symbol].append(signal)
        
        market_signals = []
        
        for symbol, symbol_signals in symbol_groups.items():
            if len(symbol_signals) < 2:  # Need at least 2 signals for aggregation
                continue
            
            # Calculate aggregated metrics
            bullish_signals = len([s for s in symbol_signals if s.direction == "BULLISH"])
            bearish_signals = len([s for s in symbol_signals if s.direction == "BEARISH"])
            total_signals = len(symbol_signals)
            
            # Determine overall direction
            if bullish_signals > bearish_signals:
                overall_direction = "BULLISH"
            elif bearish_signals > bullish_signals:
                overall_direction = "BEARISH"
            else:
                overall_direction = "NEUTRAL"
            
            # Calculate confidence score (weighted by signal confidence and source reliability)
            total_confidence = sum(s.confidence * self.source_weights.get(s.source, 0.5) for s in symbol_signals)
            confidence_score = total_confidence / total_signals
            
            # Calculate predicted impact
            predicted_impact = np.mean([s.impact_prediction for s in symbol_signals])
            
            # Calculate risk score (higher when signals conflict)
            signal_variance = np.var([1 if s.direction == "BULLISH" else -1 for s in symbol_signals])
            risk_score = min(signal_variance * 2, 1.0)
            
            # Get dominant sources
            source_counts = {}
            for signal in symbol_signals:
                source_type = signal.signal_type
                source_counts[source_type] = source_counts.get(source_type, 0) + 1
            dominant_sources = sorted(source_counts.keys(), key=lambda x: source_counts[x], reverse=True)
            
            market_signal = MarketSignal(
                symbol=symbol,
                overall_direction=overall_direction,
                confidence_score=confidence_score,
                signal_count=total_signals,
                bullish_signals=bullish_signals,
                bearish_signals=bearish_signals,
                dominant_sources=dominant_sources,
                predicted_impact=predicted_impact,
                risk_score=risk_score,
                timestamp=time.time()
            )
            
            market_signals.append(market_signal)
            
            # Store in database
            self.store_market_signal(market_signal)
        
        # Sort by confidence and impact
        market_signals.sort(key=lambda x: x.confidence_score * x.predicted_impact, reverse=True)
        
        return market_signals
    
    def identify_signal_correlations(self, signals: List[UnifiedSignal]) -> List[Dict[str, Any]]:
        """Identify correlations between signals"""
        correlations = []
        
        for i, signal1 in enumerate(signals):
            for j, signal2 in enumerate(signals[i+1:], i+1):
                # Check for correlation patterns
                correlation_strength = self.calculate_correlation_strength(signal1, signal2)
                
                if correlation_strength > 0.5:  # Threshold for significant correlation
                    correlation = {
                        "primary_signal": signal1.signal_id,
                        "correlated_signal": signal2.signal_id,
                        "strength": correlation_strength,
                        "type": self.determine_correlation_type(signal1, signal2),
                        "timestamp": time.time()
                    }
                    correlations.append(correlation)
                    
                    # Store in database
                    self.store_signal_correlation(correlation)
        
        return correlations
    
    def calculate_correlation_strength(self, signal1: UnifiedSignal, signal2: UnifiedSignal) -> float:
        """Calculate correlation strength between two signals"""
        strength = 0.0
        
        # Same symbol correlation
        if signal1.symbol == signal2.symbol:
            strength += 0.3
        
        # Same direction correlation
        if signal1.direction == signal2.direction:
            strength += 0.2
        
        # Time proximity correlation (within 1 hour)
        time_diff = abs(signal1.timestamp - signal2.timestamp)
        if time_diff < 3600:  # 1 hour
            strength += 0.3 * (1 - time_diff / 3600)
        
        # Content similarity correlation
        content_similarity = self.calculate_content_similarity(signal1.content, signal2.content)
        strength += content_similarity * 0.2
        
        return min(strength, 1.0)
    
    def calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate content similarity between two signals"""
        # Simple keyword-based similarity
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def determine_correlation_type(self, signal1: UnifiedSignal, signal2: UnifiedSignal) -> str:
        """Determine the type of correlation between signals"""
        if signal1.signal_type == signal2.signal_type:
            return "SAME_SOURCE"
        elif signal1.symbol == signal2.symbol:
            return "SAME_ASSET"
        elif signal1.direction == signal2.direction:
            return "DIRECTIONAL"
        else:
            return "TEMPORAL"
    
    def extract_crypto_symbols(self, text: str) -> List[str]:
        """Extract cryptocurrency symbols from text"""
        symbols = []
        text_upper = text.upper()
        
        # Common crypto symbols and their variations
        crypto_patterns = {
            "BTC": ["BITCOIN", "BTC", "$BTC"],
            "ETH": ["ETHEREUM", "ETH", "$ETH"],
            "SOL": ["SOLANA", "SOL", "$SOL"],
            "ADA": ["CARDANO", "ADA", "$ADA"],
            "DOT": ["POLKADOT", "DOT", "$DOT"],
            "LINK": ["CHAINLINK", "LINK", "$LINK"],
            "MATIC": ["POLYGON", "MATIC", "$MATIC"],
            "AVAX": ["AVALANCHE", "AVAX", "$AVAX"]
        }
        
        for symbol, patterns in crypto_patterns.items():
            for pattern in patterns:
                if pattern in text_upper:
                    symbols.append(symbol)
                    break
        
        return list(set(symbols)) if symbols else ["BTC"]  # Default to BTC if no symbol found
    
    def determine_direction_from_content(self, content: str, sentiment: float) -> str:
        """Determine signal direction from content and sentiment"""
        content_lower = content.lower()
        
        # Bullish keywords
        bullish_keywords = ["bullish", "buy", "pump", "moon", "rally", "breakout", "adoption", "institutional"]
        bearish_keywords = ["bearish", "sell", "dump", "crash", "correction", "ban", "regulation", "fear"]
        
        bullish_score = sum(1 for keyword in bullish_keywords if keyword in content_lower)
        bearish_score = sum(1 for keyword in bearish_keywords if keyword in content_lower)
        
        # Combine keyword analysis with sentiment
        if sentiment > 0.1 or bullish_score > bearish_score:
            return "BULLISH"
        elif sentiment < -0.1 or bearish_score > bullish_score:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def determine_time_horizon(self, content: str) -> str:
        """Determine time horizon from content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["immediate", "now", "today", "urgent"]):
            return "SHORT"
        elif any(word in content_lower for word in ["week", "month", "quarterly", "medium"]):
            return "MEDIUM"
        elif any(word in content_lower for word in ["year", "long", "decade", "future"]):
            return "LONG"
        else:
            return "MEDIUM"  # Default
    
    def get_whale_movements(self) -> List[Dict[str, Any]]:
        """Get recent whale movements (mock data for now)"""
        return [
            {
                "symbol": "BTC",
                "amount": 500,
                "type": "exchange_outflow",
                "timestamp": time.time() - 3600,
                "impact_score": 0.7
            },
            {
                "symbol": "ETH", 
                "amount": 10000,
                "type": "exchange_inflow",
                "timestamp": time.time() - 7200,
                "impact_score": 0.6
            }
        ]
    
    def get_exchange_flows(self) -> List[Dict[str, Any]]:
        """Get recent exchange flows (mock data for now)"""
        return [
            {
                "exchange": "Coinbase",
                "symbol": "BTC",
                "flow_type": "outflow",
                "amount": 200,
                "timestamp": time.time() - 1800
            }
        ]
    
    def store_market_signal(self, signal: MarketSignal):
        """Store market signal in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO market_signals 
            (symbol, timestamp, overall_direction, confidence_score, signal_count,
             bullish_signals, bearish_signals, dominant_sources, predicted_impact,
             risk_score, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            signal.symbol, signal.timestamp, signal.overall_direction,
            signal.confidence_score, signal.signal_count, signal.bullish_signals,
            signal.bearish_signals, json.dumps(signal.dominant_sources),
            signal.predicted_impact, signal.risk_score, json.dumps(asdict(signal))
        ))
        
        conn.commit()
        conn.close()
    
    def store_signal_correlation(self, correlation: Dict[str, Any]):
        """Store signal correlation in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO signal_correlations 
            (primary_signal_id, correlated_signal_id, correlation_strength, 
             correlation_type, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            correlation["primary_signal"], correlation["correlated_signal"],
            correlation["strength"], correlation["type"], correlation["timestamp"]
        ))
        
        conn.commit()
        conn.close()

# Test function
async def main():
    """Test the Signal Aggregator"""
    print("🎯 Testing Signal Aggregator - Phase 2 Enhanced Intelligence...")
    
    aggregator = SignalAggregator()
    results = aggregator.collect_all_signals()
    
    print(f"✅ Signal Aggregation Complete:")
    print(f"   📊 Total signals: {results['total_signals']}")
    print(f"   🎯 Market signals: {results['market_signals']}")
    print(f"   🔗 Correlations: {results['correlations_found']}")
    print(f"   ⏱️ Execution time: {results['execution_time']:.2f}s")
    
    print("\n🔥 Top Market Signals:")
    for signal in results['top_market_signals']:
        print(f"   {signal['symbol']}: {signal['direction']} (confidence: {signal['confidence']:.2f})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())