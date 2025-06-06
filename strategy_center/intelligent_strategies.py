"""
FILE: strategy_center/intelligent_strategies.py
PURPOSE: Specific trading strategies enhanced with AI intelligence
CONTEXT: Part of Strategy Center - DO NOT DUPLICATE
DEPENDENCIES: Integrates with knowledge synthesis
MAINTAIN: Single source for intelligent strategies

DO NOT:
- Create duplicate strategy files
- Implement without risk management
- Skip backtesting validation
- Use without learning feedback

ONLY MODIFY:
- Strategy parameters
- Entry/exit conditions
- Risk management rules
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass
import logging
from pathlib import Path
import sys

# Add parent path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import knowledge synthesis
from knowledge_center.llm_synthesis import KnowledgeSynthesis


@dataclass
class TradeSignal:
    """Structured trade signal"""
    timestamp: datetime
    symbol: str
    strategy_name: str
    action: str  # BUY, SELL, HOLD
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    reasoning: str
    metadata: Dict[str, Any]


class IntelligentStrategyEngine:
    """
    Engine for intelligent trading strategies
    Combines classical strategies with AI enhancement
    """
    
    def __init__(self):
        self.setup_logging()
        self.knowledge_synthesis = KnowledgeSynthesis()
        
        # Strategy configurations
        self.strategies = {
            'momentum': MomentumStrategy(),
            'mean_reversion': MeanReversionStrategy(),
            'breakout': BreakoutStrategy(),
            'pattern_recognition': PatternRecognitionStrategy(),
            'sentiment_driven': SentimentDrivenStrategy()
        }
        
        # Performance tracking
        self.signal_history = []
        self.performance_metrics = {}
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - IntelligentStrategies - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    async def analyze_market(self, market_data: Dict[str, Any]) -> List[TradeSignal]:
        """
        Analyze market data using all strategies
        Enhanced with AI insights
        """
        all_signals = []
        
        # Get AI insights first
        ai_insights = await self._get_ai_insights(market_data)
        
        # Run each strategy
        for strategy_name, strategy in self.strategies.items():
            try:
                # Run strategy analysis
                signals = await strategy.analyze(market_data, ai_insights)
                
                # Enhance signals with AI confidence
                for signal in signals:
                    signal.confidence = self._adjust_confidence_with_ai(
                        signal.confidence, 
                        ai_insights
                    )
                    
                all_signals.extend(signals)
                
            except Exception as e:
                self.logger.error(f"Strategy {strategy_name} error: {e}")
                
        # Filter and rank signals
        filtered_signals = self._filter_signals(all_signals)
        
        # Store for learning
        self.signal_history.extend(filtered_signals)
        
        return filtered_signals
        
    async def _get_ai_insights(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI insights from knowledge synthesis"""
        try:
            # Synthesize current market conditions
            result = await self.knowledge_synthesis.synthesize_insights(
                {'analysis': market_data}
            )
            
            if result['success']:
                return result['knowledge']
            else:
                return {}
                
        except Exception as e:
            self.logger.error(f"AI insights error: {e}")
            return {}
            
    def _adjust_confidence_with_ai(self, base_confidence: float, 
                                  ai_insights: Dict[str, Any]) -> float:
        """Adjust confidence based on AI insights"""
        ai_confidence = ai_insights.get('confidence_level', 0.5)
        
        # Weighted average
        return (base_confidence * 0.7) + (ai_confidence * 0.3)
        
    def _filter_signals(self, signals: List[TradeSignal]) -> List[TradeSignal]:
        """Filter signals based on quality and conflicts"""
        # Remove low confidence signals
        filtered = [s for s in signals if s.confidence > 0.6]
        
        # Handle conflicts (multiple signals for same symbol)
        by_symbol = {}
        for signal in filtered:
            if signal.symbol not in by_symbol:
                by_symbol[signal.symbol] = []
            by_symbol[signal.symbol].append(signal)
            
        # Keep highest confidence signal per symbol
        final_signals = []
        for symbol, symbol_signals in by_symbol.items():
            best_signal = max(symbol_signals, key=lambda s: s.confidence)
            final_signals.append(best_signal)
            
        return final_signals


class MomentumStrategy:
    """
    Momentum trading strategy
    Trades in direction of strong price movements
    """
    
    def __init__(self):
        self.name = "Momentum Trader"
        self.lookback_period = 20
        self.momentum_threshold = 0.02  # 2% minimum momentum
        
    async def analyze(self, market_data: Dict[str, Any], 
                     ai_insights: Dict[str, Any]) -> List[TradeSignal]:
        """Analyze for momentum opportunities"""
        signals = []
        
        prices = market_data.get('prices', {})
        
        for symbol, price_data in prices.items():
            # Calculate momentum
            momentum = self._calculate_momentum(price_data)
            
            if abs(momentum) > self.momentum_threshold:
                # Check AI sentiment alignment
                ai_sentiment = ai_insights.get('market_sentiment', 'neutral')
                
                if momentum > 0 and ai_sentiment in ['bullish', 'neutral']:
                    # Bullish momentum signal
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='BUY',
                        confidence=min(0.9, 0.5 + abs(momentum) * 10),
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 0.98,  # 2% stop
                        take_profit=price_data['price'] * 1.05,  # 5% target
                        position_size=0.02,  # 2% of portfolio
                        reasoning=f"Strong bullish momentum: {momentum:.2%}",
                        metadata={'momentum': momentum, 'ai_sentiment': ai_sentiment}
                    )
                    signals.append(signal)
                    
                elif momentum < 0 and ai_sentiment in ['bearish', 'neutral']:
                    # Bearish momentum (short signal)
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='SELL',
                        confidence=min(0.9, 0.5 + abs(momentum) * 10),
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 1.02,  # 2% stop
                        take_profit=price_data['price'] * 0.95,  # 5% target
                        position_size=0.02,
                        reasoning=f"Strong bearish momentum: {momentum:.2%}",
                        metadata={'momentum': momentum, 'ai_sentiment': ai_sentiment}
                    )
                    signals.append(signal)
                    
        return signals
        
    def _calculate_momentum(self, price_data: Dict) -> float:
        """Calculate price momentum"""
        current = price_data.get('price', 0)
        change_24h = price_data.get('change_24h', 0)
        
        # Simple momentum based on 24h change
        return change_24h / 100


class MeanReversionStrategy:
    """
    Mean reversion strategy
    Trades expecting prices to revert to average
    """
    
    def __init__(self):
        self.name = "Mean Reversion"
        self.deviation_threshold = 2.0  # Standard deviations
        self.lookback_period = 50
        
    async def analyze(self, market_data: Dict[str, Any], 
                     ai_insights: Dict[str, Any]) -> List[TradeSignal]:
        """Analyze for mean reversion opportunities"""
        signals = []
        
        prices = market_data.get('prices', {})
        indicators = market_data.get('indicators', {})
        
        for symbol, price_data in prices.items():
            # Check if price is extended
            deviation = self._calculate_deviation(price_data, indicators)
            
            if abs(deviation) > self.deviation_threshold:
                # Check for reversal confirmation in AI insights
                patterns = ai_insights.get('patterns_identified', [])
                reversal_likely = any('reversal' in p.lower() for p in patterns)
                
                if deviation > self.deviation_threshold:
                    # Overbought - potential short
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='SELL',
                        confidence=0.7 if reversal_likely else 0.5,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 1.03,  # 3% stop
                        take_profit=price_data['price'] * 0.97,  # 3% target
                        position_size=0.015,
                        reasoning=f"Overbought: {deviation:.1f} std devs above mean",
                        metadata={'deviation': deviation, 'reversal_signal': reversal_likely}
                    )
                    signals.append(signal)
                    
                elif deviation < -self.deviation_threshold:
                    # Oversold - potential long
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='BUY',
                        confidence=0.7 if reversal_likely else 0.5,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 0.97,
                        take_profit=price_data['price'] * 1.03,
                        position_size=0.015,
                        reasoning=f"Oversold: {abs(deviation):.1f} std devs below mean",
                        metadata={'deviation': deviation, 'reversal_signal': reversal_likely}
                    )
                    signals.append(signal)
                    
        return signals
        
    def _calculate_deviation(self, price_data: Dict, indicators: Dict) -> float:
        """Calculate standard deviation from mean"""
        # Simplified calculation using RSI as proxy
        rsi = indicators.get(f"{price_data.get('symbol', 'UNKNOWN').lower()}_rsi", 50)
        
        # Convert RSI to standard deviations
        # RSI 70 = +2 std, RSI 30 = -2 std
        if rsi > 50:
            deviation = (rsi - 50) / 10  # 70 -> 2.0
        else:
            deviation = (rsi - 50) / 10  # 30 -> -2.0
            
        return deviation


class BreakoutStrategy:
    """
    Breakout trading strategy
    Trades on price breaking key levels
    """
    
    def __init__(self):
        self.name = "Breakout Hunter"
        self.volume_multiplier = 1.5  # Volume must be 1.5x average
        self.breakout_threshold = 0.01  # 1% beyond level
        
    async def analyze(self, market_data: Dict[str, Any], 
                     ai_insights: Dict[str, Any]) -> List[TradeSignal]:
        """Analyze for breakout opportunities"""
        signals = []
        
        prices = market_data.get('prices', {})
        
        for symbol, price_data in prices.items():
            # Check for breakout conditions
            breakout_type = self._detect_breakout(price_data)
            
            if breakout_type:
                # Verify with AI insights
                opportunities = ai_insights.get('opportunities', [])
                breakout_confirmed = any('breakout' in o.lower() for o in opportunities)
                
                if breakout_type == 'resistance':
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='BUY',
                        confidence=0.8 if breakout_confirmed else 0.6,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 0.98,
                        take_profit=price_data['price'] * 1.08,  # 8% target
                        position_size=0.025,
                        reasoning="Resistance breakout with volume",
                        metadata={'breakout_type': 'resistance', 'ai_confirmed': breakout_confirmed}
                    )
                    signals.append(signal)
                    
                elif breakout_type == 'support':
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='SELL',
                        confidence=0.8 if breakout_confirmed else 0.6,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 1.02,
                        take_profit=price_data['price'] * 0.92,
                        position_size=0.025,
                        reasoning="Support breakdown with volume",
                        metadata={'breakout_type': 'support', 'ai_confirmed': breakout_confirmed}
                    )
                    signals.append(signal)
                    
        return signals
        
    def _detect_breakout(self, price_data: Dict) -> Optional[str]:
        """Detect breakout patterns"""
        price = price_data.get('price', 0)
        high_24h = price_data.get('high_24h', price)
        low_24h = price_data.get('low_24h', price)
        volume = price_data.get('volume_24h', 0)
        
        # Simple breakout detection
        if price > high_24h * (1 + self.breakout_threshold):
            return 'resistance'
        elif price < low_24h * (1 - self.breakout_threshold):
            return 'support'
            
        return None


class PatternRecognitionStrategy:
    """
    Pattern recognition strategy
    Uses AI to identify chart patterns
    """
    
    def __init__(self):
        self.name = "Pattern Scanner"
        self.min_pattern_confidence = 0.7
        
    async def analyze(self, market_data: Dict[str, Any], 
                     ai_insights: Dict[str, Any]) -> List[TradeSignal]:
        """Analyze for pattern-based opportunities"""
        signals = []
        
        # Get patterns from AI insights
        patterns = ai_insights.get('patterns_identified', [])
        
        if not patterns:
            return signals
            
        prices = market_data.get('prices', {})
        
        for pattern in patterns:
            # Parse pattern for tradeable setup
            trade_setup = self._parse_pattern(pattern, prices)
            
            if trade_setup:
                signal = TradeSignal(
                    timestamp=datetime.now(),
                    symbol=trade_setup['symbol'],
                    strategy_name=self.name,
                    action=trade_setup['action'],
                    confidence=trade_setup['confidence'],
                    entry_price=trade_setup['entry'],
                    stop_loss=trade_setup['stop_loss'],
                    take_profit=trade_setup['take_profit'],
                    position_size=0.02,
                    reasoning=f"Pattern detected: {pattern}",
                    metadata={'pattern': pattern}
                )
                signals.append(signal)
                
        return signals
        
    def _parse_pattern(self, pattern: str, prices: Dict) -> Optional[Dict]:
        """Parse pattern description into trade setup"""
        pattern_lower = pattern.lower()
        
        # Map patterns to trade setups
        if 'bullish' in pattern_lower or 'support' in pattern_lower:
            # Find best symbol for bullish trade
            for symbol, price_data in prices.items():
                if symbol in pattern:
                    return {
                        'symbol': symbol,
                        'action': 'BUY',
                        'confidence': self.min_pattern_confidence,
                        'entry': price_data['price'],
                        'stop_loss': price_data['price'] * 0.97,
                        'take_profit': price_data['price'] * 1.05
                    }
                    
        elif 'bearish' in pattern_lower or 'resistance' in pattern_lower:
            # Find best symbol for bearish trade
            for symbol, price_data in prices.items():
                if symbol in pattern:
                    return {
                        'symbol': symbol,
                        'action': 'SELL',
                        'confidence': self.min_pattern_confidence,
                        'entry': price_data['price'],
                        'stop_loss': price_data['price'] * 1.03,
                        'take_profit': price_data['price'] * 0.95
                    }
                    
        return None


class SentimentDrivenStrategy:
    """
    Sentiment-driven strategy
    Trades based on market sentiment analysis
    """
    
    def __init__(self):
        self.name = "Sentiment Trader"
        self.sentiment_threshold = 70  # Fear & Greed threshold
        
    async def analyze(self, market_data: Dict[str, Any], 
                     ai_insights: Dict[str, Any]) -> List[TradeSignal]:
        """Analyze sentiment for trading opportunities"""
        signals = []
        
        sentiment_data = market_data.get('sentiment', {})
        fear_greed = sentiment_data.get('fear_greed_index', 50)
        
        # Get AI sentiment analysis
        ai_sentiment = ai_insights.get('market_sentiment', 'neutral')
        risk_factors = ai_insights.get('risk_factors', [])
        
        # Extreme fear = buying opportunity
        if fear_greed < 30 and ai_sentiment != 'bearish':
            # Select best assets to buy
            prices = market_data.get('prices', {})
            
            for symbol, price_data in prices.items():
                if price_data.get('change_24h', 0) < -5:  # Down 5%+
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='BUY',
                        confidence=0.7,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 0.95,
                        take_profit=price_data['price'] * 1.10,
                        position_size=0.02,
                        reasoning=f"Extreme fear ({fear_greed}) + oversold",
                        metadata={'fear_greed': fear_greed, 'ai_sentiment': ai_sentiment}
                    )
                    signals.append(signal)
                    
        # Extreme greed = selling opportunity
        elif fear_greed > 80 and ai_sentiment != 'bullish':
            prices = market_data.get('prices', {})
            
            for symbol, price_data in prices.items():
                if price_data.get('change_24h', 0) > 10:  # Up 10%+
                    signal = TradeSignal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        strategy_name=self.name,
                        action='SELL',
                        confidence=0.7,
                        entry_price=price_data['price'],
                        stop_loss=price_data['price'] * 1.05,
                        take_profit=price_data['price'] * 0.90,
                        position_size=0.02,
                        reasoning=f"Extreme greed ({fear_greed}) + overbought",
                        metadata={'fear_greed': fear_greed, 'ai_sentiment': ai_sentiment}
                    )
                    signals.append(signal)
                    
        return signals


# Integration with main system
async def run_strategy_analysis(market_data: Dict[str, Any]) -> List[TradeSignal]:
    """Run complete strategy analysis"""
    engine = IntelligentStrategyEngine()
    
    # Analyze market with all strategies
    signals = await engine.analyze_market(market_data)
    
    # Log results
    print(f"\n📊 Strategy Analysis Complete")
    print(f"   Generated {len(signals)} trade signals")
    
    for signal in signals:
        print(f"\n   📈 {signal.strategy_name}: {signal.action} {signal.symbol}")
        print(f"      Confidence: {signal.confidence:.1%}")
        print(f"      Entry: ${signal.entry_price:.2f}")
        print(f"      Stop: ${signal.stop_loss:.2f} | Target: ${signal.take_profit:.2f}")
        print(f"      Reason: {signal.reasoning}")
        
    return signals


# Example usage
if __name__ == "__main__":
    # Test data
    test_market_data = {
        'prices': {
            'BTC': {'price': 52000, 'change_24h': 5.2, 'volume_24h': 25000000000, 'high_24h': 52500, 'low_24h': 49000},
            'ETH': {'price': 3200, 'change_24h': -2.1, 'volume_24h': 15000000000, 'high_24h': 3300, 'low_24h': 3150},
            'SOL': {'price': 95, 'change_24h': 12.5, 'volume_24h': 2500000000, 'high_24h': 96, 'low_24h': 84}
        },
        'sentiment': {
            'fear_greed_index': 72,
            'social_sentiment': 'positive'
        },
        'indicators': {
            'btc_rsi': 68,
            'eth_rsi': 42,
            'sol_rsi': 78
        }
    }
    
    # Run analysis
    asyncio.run(run_strategy_analysis(test_market_data))