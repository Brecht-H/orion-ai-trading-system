#!/usr/bin/env python3
"""
Crypto Trading Strategy Framework
Advanced trading strategies with AI integration for autonomous execution
"""

import requests
import json
import os
import time
import asyncio
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple

def load_notion_token():
    """Load Notion token from env file"""
    token = ''
    try:
        with open('env temp.md', 'r') as f:
            for line in f:
                if 'NOTION_TOKEN=' in line and not line.strip().startswith('#'):
                    token = line.split('=')[1].strip()
                    break
    except:
        print("❌ Could not read token from env temp.md")
        return None
    return token

class MarketDataProvider:
    """Real-time market data provider"""
    
    def __init__(self):
        self.base_url = "https://api.coinbase.com/v2"
        self.cache = {}
        self.cache_timeout = 30  # 30 seconds
    
    async def get_price(self, symbol: str) -> Optional[float]:
        """Get current price for symbol"""
        cache_key = f"price_{symbol}"
        current_time = time.time()
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if current_time - cached_time < self.cache_timeout:
                return cached_data
        
        try:
            # Fetch from API
            response = requests.get(f"{self.base_url}/exchange-rates?currency={symbol}")
            if response.status_code == 200:
                data = response.json()
                price = float(data['data']['rates']['USD'])
                
                # Cache the result
                self.cache[cache_key] = (price, current_time)
                return price
        except Exception as e:
            print(f"❌ Error fetching price for {symbol}: {e}")
        
        return None
    
    async def get_historical_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Get historical price data"""
        # For demo purposes, generate synthetic data
        # In production, you'd use a real API like CoinGecko or CoinMarketCap
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate synthetic price data with some volatility
        base_price = 45000 if symbol == 'BTC' else 3000  # BTC vs ETH
        price_data = []
        
        for i, date in enumerate(dates):
            # Add some trend and volatility
            trend = 1 + (i * 0.001)  # Small upward trend
            volatility = np.random.normal(1, 0.02)  # 2% daily volatility
            price = base_price * trend * volatility
            price_data.append(price)
        
        df = pd.DataFrame({
            'date': dates,
            'price': price_data,
            'volume': np.random.uniform(1000000, 5000000, len(dates))
        })
        
        return df

class TradingStrategy:
    """Base trading strategy class"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.performance_history = []
        self.active = False
        self.risk_level = "medium"
    
    async def analyze(self, market_data: pd.DataFrame) -> Dict:
        """Analyze market data and return trading signals"""
        raise NotImplementedError("Strategy must implement analyze method")
    
    def calculate_position_size(self, portfolio_value: float, risk_per_trade: float = 0.02) -> float:
        """Calculate position size based on risk management"""
        return portfolio_value * risk_per_trade
    
    def record_performance(self, pnl: float, trade_result: Dict):
        """Record trading performance"""
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'pnl': pnl,
            'trade_result': trade_result
        })

class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy"""
    
    def __init__(self):
        super().__init__(
            "AI Momentum Trader",
            "Identifies momentum breakouts using AI pattern recognition"
        )
        self.risk_level = "medium-high"
        self.lookback_period = 20
        self.momentum_threshold = 0.05  # 5% momentum threshold
    
    async def analyze(self, market_data: pd.DataFrame) -> Dict:
        """Analyze momentum patterns"""
        if len(market_data) < self.lookback_period:
            return {"signal": "hold", "confidence": 0, "reason": "insufficient_data"}
        
        # Calculate momentum indicators
        current_price = market_data['price'].iloc[-1]
        sma_20 = market_data['price'].rolling(window=20).mean().iloc[-1]
        
        # Price momentum
        price_change = (current_price - market_data['price'].iloc[-20]) / market_data['price'].iloc[-20]
        
        # Volume momentum  
        avg_volume = market_data['volume'].rolling(window=10).mean().iloc[-1]
        current_volume = market_data['volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume
        
        # Generate signal
        signal = "hold"
        confidence = 0.5
        reason = "neutral_momentum"
        
        if price_change > self.momentum_threshold and current_price > sma_20 and volume_ratio > 1.5:
            signal = "buy"
            confidence = min(0.9, 0.6 + (price_change * 2) + (volume_ratio * 0.1))
            reason = f"strong_upward_momentum_{price_change:.2%}"
        elif price_change < -self.momentum_threshold and current_price < sma_20 and volume_ratio > 1.5:
            signal = "sell"
            confidence = min(0.9, 0.6 + (abs(price_change) * 2) + (volume_ratio * 0.1))
            reason = f"strong_downward_momentum_{price_change:.2%}"
        
        return {
            "signal": signal,
            "confidence": confidence,
            "reason": reason,
            "price_momentum": price_change,
            "volume_ratio": volume_ratio,
            "current_price": current_price,
            "sma_20": sma_20
        }

class MeanReversionStrategy(TradingStrategy):
    """Mean reversion trading strategy"""
    
    def __init__(self):
        super().__init__(
            "AI Mean Reversion",
            "Exploits overbought/oversold conditions using AI analysis"
        )
        self.risk_level = "medium"
        self.lookback_period = 14
        self.overbought_threshold = 0.8
        self.oversold_threshold = 0.2
    
    async def analyze(self, market_data: pd.DataFrame) -> Dict:
        """Analyze mean reversion patterns"""
        if len(market_data) < self.lookback_period:
            return {"signal": "hold", "confidence": 0, "reason": "insufficient_data"}
        
        # Calculate RSI-like indicator
        price_changes = market_data['price'].diff()
        gains = price_changes.where(price_changes > 0, 0)
        losses = -price_changes.where(price_changes < 0, 0)
        
        avg_gains = gains.rolling(window=self.lookback_period).mean()
        avg_losses = losses.rolling(window=self.lookback_period).mean()
        
        rs = avg_gains / avg_losses
        rsi = 1 - (1 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # Calculate Bollinger Bands
        sma = market_data['price'].rolling(window=20).mean()
        std = market_data['price'].rolling(window=20).std()
        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)
        
        current_price = market_data['price'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        
        # Generate signal
        signal = "hold"
        confidence = 0.5
        reason = "neutral_conditions"
        
        if current_rsi < self.oversold_threshold and current_price < current_lower:
            signal = "buy"
            confidence = 0.7 + (0.3 * (self.oversold_threshold - current_rsi))
            reason = f"oversold_rsi_{current_rsi:.2f}_below_lower_band"
        elif current_rsi > self.overbought_threshold and current_price > current_upper:
            signal = "sell"
            confidence = 0.7 + (0.3 * (current_rsi - self.overbought_threshold))
            reason = f"overbought_rsi_{current_rsi:.2f}_above_upper_band"
        
        return {
            "signal": signal,
            "confidence": confidence,
            "reason": reason,
            "rsi": current_rsi,
            "bollinger_position": (current_price - current_lower) / (current_upper - current_lower),
            "current_price": current_price
        }

class AITradingOrchestrator:
    """Main trading orchestrator that coordinates strategies with AI system"""
    
    def __init__(self):
        self.market_data = MarketDataProvider()
        self.strategies = {
            "momentum": MomentumStrategy(),
            "mean_reversion": MeanReversionStrategy()
        }
        self.portfolio = {
            "btc": 0.5,  # 50% Bitcoin
            "eth": 0.3,  # 30% Ethereum
            "cash": 0.2  # 20% Cash
        }
        self.portfolio_value = 100000  # $100K starting portfolio
        self.notion_headers = None
        self.setup_notion()
    
    def setup_notion(self):
        """Setup Notion API headers"""
        token = load_notion_token()
        if token:
            self.notion_headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            }
    
    async def analyze_market(self, symbol: str) -> Dict:
        """Run comprehensive market analysis"""
        print(f"🔍 Analyzing market for {symbol}...")
        
        # Get historical data
        historical_data = await self.market_data.get_historical_data(symbol)
        
        # Run all strategies
        strategy_results = {}
        for strategy_name, strategy in self.strategies.items():
            result = await strategy.analyze(historical_data)
            strategy_results[strategy_name] = result
        
        # Combine signals using AI consensus
        consensus = self.calculate_consensus(strategy_results)
        
        # Save analysis
        analysis_file = f"ai_outputs/market_analysis_{symbol}_{int(time.time())}.json"
        os.makedirs("ai_outputs", exist_ok=True)
        
        analysis_data = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "strategy_results": strategy_results,
            "consensus": consensus,
            "market_data_summary": {
                "current_price": historical_data['price'].iloc[-1],
                "24h_change": (historical_data['price'].iloc[-1] - historical_data['price'].iloc[-2]) / historical_data['price'].iloc[-2],
                "volume": historical_data['volume'].iloc[-1]
            }
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        return analysis_data
    
    def calculate_consensus(self, strategy_results: Dict) -> Dict:
        """Calculate AI consensus from multiple strategies"""
        
        # Collect all signals and confidences
        buy_confidence = 0
        sell_confidence = 0
        hold_confidence = 0
        
        strategy_count = len(strategy_results)
        
        for strategy_name, result in strategy_results.items():
            signal = result.get("signal", "hold")
            confidence = result.get("confidence", 0.5)
            
            if signal == "buy":
                buy_confidence += confidence
            elif signal == "sell":
                sell_confidence += confidence
            else:
                hold_confidence += confidence
        
        # Normalize confidences
        total_confidence = buy_confidence + sell_confidence + hold_confidence
        if total_confidence > 0:
            buy_confidence /= total_confidence
            sell_confidence /= total_confidence
            hold_confidence /= total_confidence
        
        # Determine consensus
        if buy_confidence > 0.6:
            consensus_signal = "buy"
            consensus_confidence = buy_confidence
        elif sell_confidence > 0.6:
            consensus_signal = "sell" 
            consensus_confidence = sell_confidence
        else:
            consensus_signal = "hold"
            consensus_confidence = hold_confidence
        
        return {
            "signal": consensus_signal,
            "confidence": consensus_confidence,
            "buy_confidence": buy_confidence,
            "sell_confidence": sell_confidence,
            "hold_confidence": hold_confidence,
            "strategy_agreement": max(buy_confidence, sell_confidence, hold_confidence),
            "recommendation": self.get_recommendation(consensus_signal, consensus_confidence)
        }
    
    def get_recommendation(self, signal: str, confidence: float) -> str:
        """Get human-readable recommendation"""
        if confidence > 0.8:
            strength = "Strong"
        elif confidence > 0.6:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        if signal == "buy":
            return f"{strength} Buy Signal - Consider increasing position"
        elif signal == "sell":
            return f"{strength} Sell Signal - Consider reducing position"
        else:
            return f"{strength} Hold Signal - Maintain current position"
    
    async def create_trading_opportunity(self, analysis: Dict):
        """Create trading opportunity in Notion dashboard"""
        
        if not self.notion_headers:
            return
        
        symbol = analysis["symbol"]
        consensus = analysis["consensus"]
        
        opportunity_data = {
            "🎯 Trading Opportunity": {"title": [{"text": {"content": f"🚀 {symbol.upper()} - {consensus['recommendation']}"}}]},
            "📊 Signal": {"select": {"name": f"📈 {consensus['signal'].upper()}" if consensus['signal'] == 'buy' else f"📉 {consensus['signal'].upper()}" if consensus['signal'] == 'sell' else "⏸️ HOLD"}},
            "🎯 Confidence": {"number": consensus['confidence']},
            "💰 Symbol": {"rich_text": [{"text": {"content": symbol.upper()}}]},
            "📈 Current Price": {"number": analysis['market_data_summary']['current_price']},
            "📊 24h Change": {"number": analysis['market_data_summary']['24h_change']},
            "🤖 AI Recommendation": {"rich_text": [{"text": {"content": consensus['recommendation']}}]},
            "📅 Analysis Date": {"date": {"start": datetime.now().isoformat()}},
            "📱 Mobile Ready": {"checkbox": True},
            "🚀 Auto-Execute": {"checkbox": consensus['confidence'] > 0.75}  # Auto-execute high confidence signals
        }
        
        # Find trading dashboard
        try:
            response = requests.post(
                'https://api.notion.com/v1/search',
                headers=self.notion_headers,
                data=json.dumps({
                    "query": "Trading Opportunities",
                    "filter": {"property": "object", "value": "database"}
                })
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    database_id = results[0]['id']
                    
                    # Create opportunity entry
                    create_response = requests.post(
                        'https://api.notion.com/v1/pages',
                        headers=self.notion_headers,
                        data=json.dumps({
                            "parent": {"database_id": database_id},
                            "properties": opportunity_data
                        })
                    )
                    
                    if create_response.status_code == 200:
                        print(f"✅ Trading opportunity created for {symbol}")
                    else:
                        print(f"⚠️ Failed to create opportunity: {create_response.text}")
        
        except Exception as e:
            print(f"❌ Error creating trading opportunity: {e}")
    
    async def run_trading_analysis(self, symbols: List[str] = ["BTC", "ETH"]):
        """Run comprehensive trading analysis for multiple symbols"""
        
        print("🚀 CRYPTO TRADING STRATEGY ANALYSIS")
        print("="*60)
        print(f"🕐 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        opportunities = []
        
        for symbol in symbols:
            analysis = await self.analyze_market(symbol)
            opportunities.append(analysis)
            
            # Create Notion opportunity if signal is strong
            if analysis['consensus']['confidence'] > 0.6:
                await self.create_trading_opportunity(analysis)
            
            print(f"\n📊 {symbol} Analysis:")
            print(f"   Signal: {analysis['consensus']['signal'].upper()}")
            print(f"   Confidence: {analysis['consensus']['confidence']:.1%}")
            print(f"   Recommendation: {analysis['consensus']['recommendation']}")
        
        # Save comprehensive report
        report_file = f"trading_strategies/analysis_report_{int(time.time())}.json"
        os.makedirs("trading_strategies", exist_ok=True)
        
        report_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "symbols_analyzed": symbols,
            "opportunities": opportunities,
            "portfolio_summary": self.portfolio,
            "portfolio_value": self.portfolio_value
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📊 Analysis complete! Report saved: {report_file}")
        return opportunities

async def main():
    """Main trading strategy execution"""
    
    # Initialize trading orchestrator
    orchestrator = AITradingOrchestrator()
    
    # Run analysis
    opportunities = await orchestrator.run_trading_analysis(["BTC", "ETH"])
    
    print(f"\n🎯 TRADING OPPORTUNITIES SUMMARY:")
    for opportunity in opportunities:
        symbol = opportunity['symbol']
        consensus = opportunity['consensus']
        print(f"   {symbol}: {consensus['signal'].upper()} ({consensus['confidence']:.1%} confidence)")
    
    print(f"\n📱 Check your Notion mobile app for trading opportunities!")
    print(f"🚀 High-confidence signals (>75%) are marked for auto-execution")

if __name__ == "__main__":
    asyncio.run(main()) 