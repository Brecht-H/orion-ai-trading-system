#!/usr/bin/env python3
"""
🧠 MULTI-MODAL PATTERN AGENT
AI Agent for coordinated analysis across all data modalities
"""

import asyncio
import json
import sqlite3
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import os
import logging
from dataclasses import dataclass

@dataclass
class PatternSignal:
    pattern_type: str
    data_sources: List[str]
    confidence: float
    strength: float
    direction: str  # bullish, bearish, neutral
    timeframe: str
    correlation_score: float
    reasoning: str

@dataclass
class CrossModalCorrelation:
    source_a: str
    source_b: str
    correlation_coefficient: float
    lag_minutes: int
    confidence: float
    sample_size: int

class MultiModalPatternAgent:
    """
    AI Agent for multi-modal pattern recognition
    - Cross-modal correlation analysis
    - Pattern convergence detection
    - Coordinated signal generation
    - Meta-analysis across all data sources
    """
    
    def __init__(self):
        self.agent_id = "multimodal_pattern_001"
        self.db_path = "data/multimodal_patterns.db"
        self.setup_database()
        self.setup_logging()
        
        # Data source weights
        self.source_weights = {
            "price_data": 0.25,
            "news_sentiment": 0.20,
            "social_sentiment": 0.15,
            "whale_movements": 0.20,
            "technical_indicators": 0.15,
            "onchain_metrics": 0.05
        }
        
        # Pattern types
        self.pattern_types = [
            "convergence_bullish",
            "convergence_bearish",
            "divergence_warning",
            "momentum_shift",
            "sentiment_reversal",
            "whale_accumulation",
            "institutional_flow"
        ]
        
        # Data source databases
        self.data_sources = {
            "enhanced_sources": "data/enhanced_sources_data.db",
            "root_cause": "data/root_cause_analysis.db",
            "onchain_intelligence": "data/onchain_intelligence.db",
            "social_intelligence": "data/social_intelligence.db",
            "free_sources": "data/free_sources_data.db"
        }
        
    def setup_database(self):
        """Setup multi-modal pattern database"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Pattern signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                data_sources TEXT NOT NULL,
                confidence REAL NOT NULL,
                strength REAL NOT NULL,
                direction TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                correlation_score REAL DEFAULT 0.0,
                reasoning TEXT NOT NULL,
                timestamp REAL NOT NULL,
                market_impact_prediction REAL DEFAULT 0.0
            )
        """)
        
        # Cross-modal correlations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_modal_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_a TEXT NOT NULL,
                source_b TEXT NOT NULL,
                correlation_coefficient REAL NOT NULL,
                lag_minutes INTEGER DEFAULT 0,
                confidence REAL NOT NULL,
                sample_size INTEGER NOT NULL,
                last_updated REAL NOT NULL,
                significance_level REAL DEFAULT 0.05
            )
        """)
        
        # Pattern convergence events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS convergence_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                participating_sources TEXT NOT NULL,
                convergence_strength REAL NOT NULL,
                consensus_direction TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp REAL NOT NULL,
                duration_minutes INTEGER DEFAULT 0,
                market_impact REAL DEFAULT 0.0
            )
        """)
        
        # Meta analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meta_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL,
                sources_analyzed TEXT NOT NULL,
                overall_score REAL NOT NULL,
                direction TEXT NOT NULL,
                confidence REAL NOT NULL,
                key_factors TEXT NOT NULL,
                timestamp REAL NOT NULL,
                recommendation TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_logging(self):
        """Setup agent logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - MultiModalPattern - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/multimodal_pattern.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🧠 Multi-Modal Pattern Agent {self.agent_id} initialized")
    
    async def run_pattern_analysis(self) -> Dict[str, Any]:
        """Alias for test compatibility"""
        return await self.run_analysis_cycle()
    
    async def run_analysis_cycle(self) -> Dict[str, Any]:
        """Run comprehensive multi-modal pattern analysis"""
        self.logger.info("🧠 Starting multi-modal pattern analysis cycle...")
        cycle_start = time.time()
        
        # 1. Collect data from all sources
        multi_modal_data = await self.collect_multimodal_data()
        
        # 2. Analyze cross-modal correlations
        correlations = await self.analyze_cross_modal_correlations(multi_modal_data)
        
        # 3. Detect pattern convergence
        convergence_patterns = await self.detect_pattern_convergence(multi_modal_data)
        
        # 4. Generate coordinated signals
        coordinated_signals = await self.generate_coordinated_signals(convergence_patterns)
        
        # 5. Perform meta-analysis
        meta_analysis = await self.perform_meta_analysis(multi_modal_data, correlations)
        
        cycle_time = time.time() - cycle_start
        
        results = {
            "cycle_time": cycle_time,
            "data_sources_analyzed": len(multi_modal_data),
            "cross_modal_correlations": len(correlations),
            "convergence_patterns": len(convergence_patterns),
            "coordinated_signals": len(coordinated_signals),
            "meta_analysis_score": meta_analysis.get("overall_score", 0.0),
            "strongest_correlations": [
                {
                    "sources": f"{corr.source_a} ↔ {corr.source_b}",
                    "correlation": corr.correlation_coefficient,
                    "confidence": corr.confidence,
                    "lag": corr.lag_minutes
                } for corr in correlations[:3]
            ],
            "top_patterns": [
                {
                    "type": pattern.pattern_type,
                    "sources": pattern.data_sources,
                    "confidence": pattern.confidence,
                    "direction": pattern.direction,
                    "strength": pattern.strength
                } for pattern in convergence_patterns[:3]
            ],
            "meta_recommendation": meta_analysis.get("recommendation", "No clear signal")
        }
        
        self.logger.info(f"✅ Multi-modal pattern analysis complete ({cycle_time:.2f}s)")
        self.logger.info(f"   📊 Data sources: {len(multi_modal_data)}")
        self.logger.info(f"   🔗 Correlations: {len(correlations)}")
        self.logger.info(f"   🎯 Patterns: {len(convergence_patterns)}")
        self.logger.info(f"   🧠 Meta score: {meta_analysis.get('overall_score', 0.0):.2f}")
        
        return results
    
    async def collect_multimodal_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Collect data from all available sources"""
        multimodal_data = {}
        
        # Collect from enhanced news sources
        multimodal_data["news_sentiment"] = await self.get_news_sentiment_data()
        
        # Collect from social media sources
        multimodal_data["social_sentiment"] = await self.get_social_sentiment_data()
        
        # Collect from on-chain sources
        multimodal_data["whale_movements"] = await self.get_whale_movement_data()
        multimodal_data["onchain_metrics"] = await self.get_onchain_metrics_data()
        
        # Collect from market data sources
        multimodal_data["price_data"] = await self.get_price_data()
        multimodal_data["technical_indicators"] = await self.get_technical_indicators()
        
        return multimodal_data
    
    async def get_news_sentiment_data(self) -> List[Dict[str, Any]]:
        """Get recent news sentiment data"""
        data = []
        
        try:
            if Path(self.data_sources["enhanced_sources"]).exists():
                conn = sqlite3.connect(self.data_sources["enhanced_sources"])
                cursor = conn.cursor()
                
                news_data = cursor.execute("""
                    SELECT sentiment_score, impact_prediction, timestamp
                    FROM enhanced_news
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 50
                """, (time.time() - 3600,)).fetchall()  # Last hour
                
                conn.close()
                
                for row in news_data:
                    sentiment, impact, timestamp = row
                    data.append({
                        "type": "news_sentiment",
                        "value": sentiment,
                        "weight": impact,
                        "timestamp": timestamp
                    })
                    
        except Exception as e:
            self.logger.warning(f"⚠️ News sentiment data error: {e}")
            # Generate mock data
            data = [
                {"type": "news_sentiment", "value": 0.3, "weight": 0.7, "timestamp": time.time()},
                {"type": "news_sentiment", "value": 0.1, "weight": 0.5, "timestamp": time.time() - 300},
                {"type": "news_sentiment", "value": -0.2, "weight": 0.6, "timestamp": time.time() - 600}
            ]
        
        return data
    
    async def get_social_sentiment_data(self) -> List[Dict[str, Any]]:
        """Get recent social sentiment data"""
        data = []
        
        try:
            if Path(self.data_sources["social_intelligence"]).exists():
                conn = sqlite3.connect(self.data_sources["social_intelligence"])
                cursor = conn.cursor()
                
                social_data = cursor.execute("""
                    SELECT sentiment_score, influence_score, timestamp
                    FROM social_posts
                    WHERE timestamp > ? AND crypto_relevance > 0.5
                    ORDER BY timestamp DESC
                    LIMIT 30
                """, (time.time() - 3600,)).fetchall()
                
                conn.close()
                
                for row in social_data:
                    sentiment, influence, timestamp = row
                    data.append({
                        "type": "social_sentiment",
                        "value": sentiment,
                        "weight": influence,
                        "timestamp": timestamp
                    })
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Social sentiment data error: {e}")
            # Generate mock data
            data = [
                {"type": "social_sentiment", "value": 0.5, "weight": 0.9, "timestamp": time.time()},
                {"type": "social_sentiment", "value": 0.2, "weight": 0.7, "timestamp": time.time() - 200},
                {"type": "social_sentiment", "value": 0.4, "weight": 0.8, "timestamp": time.time() - 400}
            ]
        
        return data
    
    async def get_whale_movement_data(self) -> List[Dict[str, Any]]:
        """Get recent whale movement data"""
        data = []
        
        try:
            if Path(self.data_sources["onchain_intelligence"]).exists():
                conn = sqlite3.connect(self.data_sources["onchain_intelligence"])
                cursor = conn.cursor()
                
                whale_data = cursor.execute("""
                    SELECT transaction_type, significance_score, amount, timestamp
                    FROM whale_transactions
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 20
                """, (time.time() - 3600,)).fetchall()
                
                conn.close()
                
                for row in whale_data:
                    tx_type, significance, amount, timestamp = row
                    
                    # Convert transaction type to sentiment
                    sentiment = 0.5 if tx_type == "exchange_withdrawal" else -0.5 if tx_type == "exchange_deposit" else 0.0
                    
                    data.append({
                        "type": "whale_movement",
                        "value": sentiment,
                        "weight": significance,
                        "amount": amount,
                        "timestamp": timestamp
                    })
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Whale movement data error: {e}")
            # Generate mock data
            data = [
                {"type": "whale_movement", "value": -0.5, "weight": 0.9, "amount": 2500, "timestamp": time.time()},
                {"type": "whale_movement", "value": 0.5, "weight": 0.8, "amount": 1800, "timestamp": time.time() - 600}
            ]
        
        return data
    
    async def get_onchain_metrics_data(self) -> List[Dict[str, Any]]:
        """Get recent on-chain metrics data"""
        data = []
        
        try:
            if Path(self.data_sources["onchain_intelligence"]).exists():
                conn = sqlite3.connect(self.data_sources["onchain_intelligence"])
                cursor = conn.cursor()
                
                metrics_data = cursor.execute("""
                    SELECT metric_type, value, change_percentage, timestamp
                    FROM onchain_metrics
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """, (time.time() - 3600,)).fetchall()
                
                conn.close()
                
                for row in metrics_data:
                    metric_type, value, change_pct, timestamp = row
                    
                    data.append({
                        "type": "onchain_metric",
                        "metric": metric_type,
                        "value": value,
                        "change": change_pct,
                        "timestamp": timestamp
                    })
                    
        except Exception as e:
            self.logger.warning(f"⚠️ On-chain metrics data error: {e}")
            # Generate mock data
            data = [
                {"type": "onchain_metric", "metric": "hash_rate", "value": 500000000, "change": 2.1, "timestamp": time.time()},
                {"type": "onchain_metric", "metric": "active_addresses", "value": 450000, "change": 1.5, "timestamp": time.time()}
            ]
        
        return data
    
    async def get_price_data(self) -> List[Dict[str, Any]]:
        """Get recent price data"""
        data = []
        
        try:
            if Path(self.data_sources["free_sources"]).exists():
                conn = sqlite3.connect(self.data_sources["free_sources"])
                cursor = conn.cursor()
                
                price_data = cursor.execute("""
                    SELECT symbol, current_price, price_change_percentage_24h, timestamp
                    FROM cryptocurrency_data
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 20
                """, (time.time() - 3600,)).fetchall()
                
                conn.close()
                
                for row in price_data:
                    symbol, price, change_pct, timestamp = row
                    
                    data.append({
                        "type": "price_data",
                        "symbol": symbol,
                        "price": price,
                        "change": change_pct,
                        "timestamp": timestamp
                    })
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Price data error: {e}")
            # Generate mock data
            data = [
                {"type": "price_data", "symbol": "bitcoin", "price": 45000, "change": 3.2, "timestamp": time.time()},
                {"type": "price_data", "symbol": "ethereum", "price": 3200, "change": 2.8, "timestamp": time.time()}
            ]
        
        return data
    
    async def get_technical_indicators(self) -> List[Dict[str, Any]]:
        """Get recent technical indicator data"""
        # Mock technical indicators for now
        data = [
            {"type": "technical", "indicator": "rsi", "value": 65.5, "signal": "neutral", "timestamp": time.time()},
            {"type": "technical", "indicator": "macd", "value": 0.8, "signal": "bullish", "timestamp": time.time()},
            {"type": "technical", "indicator": "bb_position", "value": 0.7, "signal": "neutral", "timestamp": time.time()}
        ]
        
        return data
    
    async def analyze_cross_modal_correlations(self, multimodal_data: Dict[str, List[Dict[str, Any]]]) -> List[CrossModalCorrelation]:
        """Analyze correlations between different data modalities"""
        correlations = []
        
        # Get data sources with sufficient data
        valid_sources = {k: v for k, v in multimodal_data.items() if len(v) >= 3}
        
        # Calculate correlations between all pairs
        source_names = list(valid_sources.keys())
        for i, source_a in enumerate(source_names):
            for source_b in source_names[i+1:]:
                correlation = await self.calculate_correlation(
                    valid_sources[source_a], 
                    valid_sources[source_b],
                    source_a,
                    source_b
                )
                
                if correlation:
                    correlations.append(correlation)
                    self.store_correlation(correlation)
        
        return correlations
    
    async def calculate_correlation(self, data_a: List[Dict[str, Any]], data_b: List[Dict[str, Any]], 
                                  source_a: str, source_b: str) -> Optional[CrossModalCorrelation]:
        """Calculate correlation between two data sources"""
        try:
            # Extract values and timestamps
            values_a = []
            values_b = []
            
            # Align data by timestamp (simplified)
            for item_a in data_a:
                timestamp_a = item_a.get("timestamp", 0)
                
                # Find closest timestamp in data_b
                closest_item_b = min(data_b, key=lambda x: abs(x.get("timestamp", 0) - timestamp_a))
                timestamp_b = closest_item_b.get("timestamp", 0)
                
                # Only include if timestamps are within 5 minutes
                if abs(timestamp_a - timestamp_b) <= 300:
                    value_a = item_a.get("value", item_a.get("change", 0))
                    value_b = closest_item_b.get("value", closest_item_b.get("change", 0))
                    
                    if value_a is not None and value_b is not None:
                        values_a.append(float(value_a))
                        values_b.append(float(value_b))
            
            if len(values_a) < 3:
                return None
            
            # Calculate correlation coefficient
            correlation_coeff = np.corrcoef(values_a, values_b)[0, 1]
            
            if np.isnan(correlation_coeff):
                return None
            
            # Calculate confidence based on sample size and correlation strength
            sample_size = len(values_a)
            confidence = min(abs(correlation_coeff) * (sample_size / 10), 1.0)
            
            return CrossModalCorrelation(
                source_a=source_a,
                source_b=source_b,
                correlation_coefficient=correlation_coeff,
                lag_minutes=0,  # Simplified - would calculate optimal lag
                confidence=confidence,
                sample_size=sample_size
            )
            
        except Exception as e:
            self.logger.warning(f"⚠️ Correlation calculation error: {e}")
            return None
    
    async def detect_pattern_convergence(self, multimodal_data: Dict[str, List[Dict[str, Any]]]) -> List[PatternSignal]:
        """Detect convergence patterns across data modalities"""
        patterns = []
        
        # Analyze sentiment convergence
        sentiment_pattern = await self.analyze_sentiment_convergence(multimodal_data)
        if sentiment_pattern:
            patterns.append(sentiment_pattern)
        
        # Analyze momentum convergence
        momentum_pattern = await self.analyze_momentum_convergence(multimodal_data)
        if momentum_pattern:
            patterns.append(momentum_pattern)
        
        # Analyze whale/institutional convergence
        institutional_pattern = await self.analyze_institutional_convergence(multimodal_data)
        if institutional_pattern:
            patterns.append(institutional_pattern)
        
        # Store patterns
        for pattern in patterns:
            self.store_pattern_signal(pattern)
        
        return patterns
    
    async def analyze_sentiment_convergence(self, multimodal_data: Dict[str, List[Dict[str, Any]]]) -> Optional[PatternSignal]:
        """Analyze convergence of sentiment across news and social media"""
        try:
            news_data = multimodal_data.get("news_sentiment", [])
            social_data = multimodal_data.get("social_sentiment", [])
            
            if len(news_data) < 2 or len(social_data) < 2:
                return None
            
            # Calculate average sentiments
            news_sentiment = sum(item["value"] for item in news_data) / len(news_data)
            social_sentiment = sum(item["value"] for item in social_data) / len(social_data)
            
            # Check for convergence
            sentiment_diff = abs(news_sentiment - social_sentiment)
            avg_sentiment = (news_sentiment + social_sentiment) / 2
            
            if sentiment_diff < 0.3 and abs(avg_sentiment) > 0.2:  # Convergence threshold
                direction = "bullish" if avg_sentiment > 0 else "bearish"
                confidence = (1 - sentiment_diff) * min(len(news_data) + len(social_data), 20) / 20
                strength = abs(avg_sentiment)
                
                return PatternSignal(
                    pattern_type="sentiment_convergence",
                    data_sources=["news_sentiment", "social_sentiment"],
                    confidence=confidence,
                    strength=strength,
                    direction=direction,
                    timeframe="1h",
                    correlation_score=1 - sentiment_diff,
                    reasoning=f"News sentiment ({news_sentiment:.2f}) and social sentiment ({social_sentiment:.2f}) converging on {direction} direction"
                )
                
        except Exception as e:
            self.logger.warning(f"⚠️ Sentiment convergence analysis error: {e}")
        
        return None
    
    async def analyze_momentum_convergence(self, multimodal_data: Dict[str, List[Dict[str, Any]]]) -> Optional[PatternSignal]:
        """Analyze momentum convergence across price and on-chain data"""
        try:
            price_data = multimodal_data.get("price_data", [])
            onchain_data = multimodal_data.get("onchain_metrics", [])
            
            if len(price_data) < 2 or len(onchain_data) < 2:
                return None
            
            # Calculate momentum indicators
            price_momentum = sum(item.get("change", 0) for item in price_data) / len(price_data)
            onchain_momentum = sum(item.get("change", 0) for item in onchain_data) / len(onchain_data)
            
            # Check for momentum alignment
            if (price_momentum > 0 and onchain_momentum > 0) or (price_momentum < 0 and onchain_momentum < 0):
                direction = "bullish" if price_momentum > 0 else "bearish"
                strength = (abs(price_momentum) + abs(onchain_momentum)) / 2
                confidence = min(strength / 5.0, 1.0)  # Normalize to 0-1
                
                return PatternSignal(
                    pattern_type="momentum_convergence",
                    data_sources=["price_data", "onchain_metrics"],
                    confidence=confidence,
                    strength=strength,
                    direction=direction,
                    timeframe="1h",
                    correlation_score=0.8,
                    reasoning=f"Price momentum ({price_momentum:.2f}%) and on-chain momentum ({onchain_momentum:.2f}%) aligned {direction}"
                )
                
        except Exception as e:
            self.logger.warning(f"⚠️ Momentum convergence analysis error: {e}")
        
        return None
    
    async def analyze_institutional_convergence(self, multimodal_data: Dict[str, List[Dict[str, Any]]]) -> Optional[PatternSignal]:
        """Analyze institutional/whale activity convergence"""
        try:
            whale_data = multimodal_data.get("whale_movements", [])
            news_data = multimodal_data.get("news_sentiment", [])
            
            if len(whale_data) < 1 or len(news_data) < 1:
                return None
            
            # Check for whale accumulation with positive news
            whale_sentiment = sum(item["value"] for item in whale_data) / len(whale_data)
            news_sentiment = sum(item["value"] for item in news_data) / len(news_data)
            
            # High whale significance + positive sentiment = institutional interest
            avg_whale_significance = sum(item.get("weight", 0) for item in whale_data) / len(whale_data)
            
            if avg_whale_significance > 0.7 and whale_sentiment > 0 and news_sentiment > 0:
                return PatternSignal(
                    pattern_type="institutional_accumulation",
                    data_sources=["whale_movements", "news_sentiment"],
                    confidence=avg_whale_significance,
                    strength=(whale_sentiment + news_sentiment) / 2,
                    direction="bullish",
                    timeframe="1h",
                    correlation_score=0.9,
                    reasoning=f"High significance whale accumulation ({avg_whale_significance:.2f}) with positive news sentiment"
                )
                
        except Exception as e:
            self.logger.warning(f"⚠️ Institutional convergence analysis error: {e}")
        
        return None
    
    async def generate_coordinated_signals(self, patterns: List[PatternSignal]) -> List[Dict[str, Any]]:
        """Generate coordinated trading signals from patterns"""
        signals = []
        
        if not patterns:
            return signals
        
        # Group patterns by direction
        bullish_patterns = [p for p in patterns if p.direction == "bullish"]
        bearish_patterns = [p for p in patterns if p.direction == "bearish"]
        
        # Generate bullish signal if multiple bullish patterns
        if len(bullish_patterns) >= 2:
            combined_confidence = sum(p.confidence for p in bullish_patterns) / len(bullish_patterns)
            combined_strength = sum(p.strength for p in bullish_patterns) / len(bullish_patterns)
            
            signal = {
                "signal_type": "coordinated_bullish",
                "direction": "bullish",
                "confidence": combined_confidence,
                "strength": combined_strength,
                "supporting_patterns": [p.pattern_type for p in bullish_patterns],
                "data_sources": list(set(sum([p.data_sources for p in bullish_patterns], []))),
                "reasoning": f"Multiple bullish patterns converging: {', '.join([p.pattern_type for p in bullish_patterns])}",
                "recommendation": "Consider long position - multiple indicators aligned"
            }
            signals.append(signal)
        
        # Generate bearish signal if multiple bearish patterns
        if len(bearish_patterns) >= 2:
            combined_confidence = sum(p.confidence for p in bearish_patterns) / len(bearish_patterns)
            combined_strength = sum(p.strength for p in bearish_patterns) / len(bearish_patterns)
            
            signal = {
                "signal_type": "coordinated_bearish",
                "direction": "bearish",
                "confidence": combined_confidence,
                "strength": combined_strength,
                "supporting_patterns": [p.pattern_type for p in bearish_patterns],
                "data_sources": list(set(sum([p.data_sources for p in bearish_patterns], []))),
                "reasoning": f"Multiple bearish patterns converging: {', '.join([p.pattern_type for p in bearish_patterns])}",
                "recommendation": "Consider risk management - multiple bearish indicators"
            }
            signals.append(signal)
        
        return signals
    
    async def perform_meta_analysis(self, multimodal_data: Dict[str, List[Dict[str, Any]]], 
                                  correlations: List[CrossModalCorrelation]) -> Dict[str, Any]:
        """Perform meta-analysis across all data sources"""
        try:
            # Calculate weighted sentiment across all sources
            total_weighted_sentiment = 0.0
            total_weight = 0.0
            
            for source, data in multimodal_data.items():
                if not data:
                    continue
                
                source_weight = self.source_weights.get(source, 0.1)
                
                # Calculate source sentiment
                if source in ["news_sentiment", "social_sentiment"]:
                    source_sentiment = sum(item.get("value", 0) for item in data) / len(data)
                elif source == "whale_movements":
                    source_sentiment = sum(item.get("value", 0) for item in data) / len(data)
                elif source == "price_data":
                    source_sentiment = sum(item.get("change", 0) for item in data) / len(data) / 10  # Normalize price changes
                elif source == "onchain_metrics":
                    source_sentiment = sum(item.get("change", 0) for item in data) / len(data) / 10
                else:
                    source_sentiment = 0.0
                
                total_weighted_sentiment += source_sentiment * source_weight
                total_weight += source_weight
            
            overall_score = total_weighted_sentiment / max(total_weight, 0.1)
            
            # Determine direction and confidence
            direction = "bullish" if overall_score > 0.1 else "bearish" if overall_score < -0.1 else "neutral"
            confidence = min(abs(overall_score) * len(multimodal_data), 1.0)
            
            # Generate recommendation
            if confidence > 0.7:
                if direction == "bullish":
                    recommendation = "Strong bullish consensus across multiple data sources - consider aggressive long position"
                elif direction == "bearish":
                    recommendation = "Strong bearish consensus across multiple data sources - implement risk management"
                else:
                    recommendation = "Mixed signals - maintain current positions and monitor"
            elif confidence > 0.4:
                recommendation = f"Moderate {direction} signal - cautious position sizing recommended"
            else:
                recommendation = "Insufficient consensus - avoid new positions until clearer signals emerge"
            
            meta_analysis = {
                "analysis_type": "comprehensive_meta_analysis",
                "sources_analyzed": list(multimodal_data.keys()),
                "overall_score": overall_score,
                "direction": direction,
                "confidence": confidence,
                "key_factors": [source for source, data in multimodal_data.items() if len(data) > 0],
                "strongest_correlations": len([c for c in correlations if abs(c.correlation_coefficient) > 0.5]),
                "recommendation": recommendation,
                "timestamp": time.time()
            }
            
            # Store meta-analysis
            self.store_meta_analysis(meta_analysis)
            
            return meta_analysis
            
        except Exception as e:
            self.logger.warning(f"⚠️ Meta-analysis error: {e}")
            return {
                "overall_score": 0.0,
                "direction": "neutral",
                "confidence": 0.0,
                "recommendation": "Analysis error - manual review required"
            }
    
    # Storage methods
    def store_pattern_signal(self, pattern: PatternSignal):
        """Store pattern signal in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pattern_signals
            (pattern_type, data_sources, confidence, strength, direction,
             timeframe, correlation_score, reasoning, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pattern.pattern_type, json.dumps(pattern.data_sources),
            pattern.confidence, pattern.strength, pattern.direction,
            pattern.timeframe, pattern.correlation_score, pattern.reasoning,
            time.time()
        ))
        
        conn.commit()
        conn.close()
    
    def store_correlation(self, correlation: CrossModalCorrelation):
        """Store cross-modal correlation in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO cross_modal_correlations
            (source_a, source_b, correlation_coefficient, lag_minutes,
             confidence, sample_size, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            correlation.source_a, correlation.source_b,
            correlation.correlation_coefficient, correlation.lag_minutes,
            correlation.confidence, correlation.sample_size, time.time()
        ))
        
        conn.commit()
        conn.close()
    
    def store_meta_analysis(self, analysis: Dict[str, Any]):
        """Store meta-analysis results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO meta_analysis
            (analysis_type, sources_analyzed, overall_score, direction,
             confidence, key_factors, timestamp, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis["analysis_type"], json.dumps(analysis["sources_analyzed"]),
            analysis["overall_score"], analysis["direction"],
            analysis["confidence"], json.dumps(analysis["key_factors"]),
            analysis["timestamp"], analysis["recommendation"]
        ))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    async def main():
        agent = MultiModalPatternAgent()
        
        print("🧠 Multi-Modal Pattern Agent - Running analysis cycle...")
        
        # Run analysis cycle
        results = await agent.run_analysis_cycle()
        
        print(f"\n🎯 MULTI-MODAL ANALYSIS RESULTS:")
        print(f"Cycle Time: {results['cycle_time']:.2f}s")
        print(f"Data Sources: {results['data_sources_analyzed']}")
        print(f"Cross-Modal Correlations: {results['cross_modal_correlations']}")
        print(f"Convergence Patterns: {results['convergence_patterns']}")
        print(f"Coordinated Signals: {results['coordinated_signals']}")
        print(f"Meta-Analysis Score: {results['meta_analysis_score']:.2f}")
        
        if results['strongest_correlations']:
            print(f"\n🔗 STRONGEST CORRELATIONS:")
            for corr in results['strongest_correlations']:
                print(f"  {corr['sources']}: {corr['correlation']:.3f} ({corr['confidence']:.2f} confidence)")
        
        if results['top_patterns']:
            print(f"\n🎯 TOP PATTERNS:")
            for pattern in results['top_patterns']:
                print(f"  {pattern['type']}: {pattern['direction']} ({pattern['confidence']:.2f} confidence)")
                print(f"    Sources: {', '.join(pattern['sources'])}")
        
        print(f"\n💡 META RECOMMENDATION:")
        print(f"  {results['meta_recommendation']}")
    
    asyncio.run(main()) 