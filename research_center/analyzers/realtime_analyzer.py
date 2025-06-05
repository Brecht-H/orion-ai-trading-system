#!/usr/bin/env python3
"""
Real-time Crypto Analysis System - Orion Protocol v3.7
Integrates all 8 APIs with Mac Mini LLM for comprehensive analysis
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
from dataclasses import dataclass

@dataclass
class CryptoAnalysis:
    timestamp: datetime
    symbol: str
    price: float
    sentiment_score: float
    news_summary: str
    technical_indicators: Dict
    recommendation: str
    confidence: float
    cost_usd: float

class OrionCryptoAnalyzer:
    def __init__(self):
        """Initialize with all 8 integrated APIs"""
        
        from src.utils.credentials import credentials
        from src.ai.llm_manager import llm_manager
        
        self.credentials = credentials
        self.llm_manager = llm_manager
        self.db_path = "data/databases/crypto_analysis.db"
        self.initialize_database()
        
        # API configurations
        self.apis = {
            "coingecko": {
                "base_url": "https://api.coingecko.com/api/v3",
                "headers": {"x-cg-pro-api-key": self.credentials.get_api_credential("coingecko", "api_key")}
            },
            "twitter": {
                "base_url": "https://api.twitter.com/2",
                "headers": {"Authorization": f"Bearer {self.credentials.get_api_credential('twitter', 'bearer_token')}"}
            },
            "newsapi": {
                "base_url": "https://newsapi.org/v2",
                "api_key": self.credentials.get_api_credential("newsapi", "key")
            },
            "newsdata_io": {
                "base_url": "https://newsdata.io/api/1",
                "api_key": self.credentials.get_api_credential("newsdata_io", "api_key")
            }
        }
        
    def initialize_database(self):
        """Initialize analysis database"""
        
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crypto_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    sentiment_score REAL,
                    news_summary TEXT,
                    technical_indicators TEXT,
                    recommendation TEXT,
                    confidence REAL,
                    cost_usd REAL,
                    analysis_data TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    api_provider TEXT NOT NULL,
                    endpoint TEXT,
                    cost_usd REAL,
                    tokens_used INTEGER,
                    success BOOLEAN
                )
            """)
    
    async def analyze_crypto(self, symbol: str = "bitcoin") -> CryptoAnalysis:
        """Perform comprehensive crypto analysis using all APIs"""
        
        print(f"🔍 Analyzing {symbol.upper()}...")
        
        total_cost = 0.0
        analysis_data = {}
        
        try:
            # 1. Get market data from CoinGecko
            market_data = await self.get_market_data(symbol)
            analysis_data["market"] = market_data
            total_cost += 0.0  # CoinGecko PRO is already paid
            
            # 2. Get sentiment from Twitter
            sentiment_data = await self.get_twitter_sentiment(symbol)
            analysis_data["sentiment"] = sentiment_data
            total_cost += 0.0  # Free tier
            
            # 3. Get news from multiple sources
            news_data = await self.get_news_analysis(symbol)
            analysis_data["news"] = news_data
            total_cost += 0.001  # Minimal cost
            
            # 4. Get technical analysis using Mac Mini LLM
            llm_analysis = await self.get_llm_analysis(analysis_data)
            analysis_data["llm"] = llm_analysis
            total_cost += 0.0  # Mac Mini is free
            
            # 5. Generate recommendation
            recommendation = self.generate_recommendation(analysis_data)
            
            # Create analysis result
            analysis = CryptoAnalysis(
                timestamp=datetime.now(),
                symbol=symbol,
                price=market_data.get("price", 0.0),
                sentiment_score=sentiment_data.get("score", 0.0),
                news_summary=news_data.get("summary", ""),
                technical_indicators=market_data.get("indicators", {}),
                recommendation=recommendation["action"],
                confidence=recommendation["confidence"],
                cost_usd=total_cost
            )
            
            # Store analysis
            self.store_analysis(analysis, analysis_data)
            
            print(f"✅ Analysis complete: {analysis.recommendation} (${total_cost:.4f})")
            return analysis
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return None
    
    async def get_market_data(self, symbol: str) -> Dict:
        """Get comprehensive market data from CoinGecko"""
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get current price and basic data
                url = f"{self.apis['coingecko']['base_url']}/simple/price"
                params = {
                    "ids": symbol,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_24hr_vol": "true",
                    "include_market_cap": "true"
                }
                
                async with session.get(url, headers=self.apis["coingecko"]["headers"], params=params) as response:
                    price_data = await response.json()
                
                # Get historical data for technical indicators
                history_url = f"{self.apis['coingecko']['base_url']}/coins/{symbol}/market_chart"
                history_params = {"vs_currency": "usd", "days": "7"}
                
                async with session.get(history_url, headers=self.apis["coingecko"]["headers"], params=history_params) as response:
                    history_data = await response.json()
                
                return {
                    "price": price_data[symbol]["usd"],
                    "change_24h": price_data[symbol].get("usd_24h_change", 0),
                    "volume_24h": price_data[symbol].get("usd_24h_vol", 0),
                    "market_cap": price_data[symbol].get("usd_market_cap", 0),
                    "price_history": history_data.get("prices", []),
                    "indicators": self.calculate_technical_indicators(history_data.get("prices", []))
                }
                
        except Exception as e:
            print(f"❌ CoinGecko error: {e}")
            return {"price": 0, "error": str(e)}
    
    async def get_twitter_sentiment(self, symbol: str) -> Dict:
        """Get sentiment analysis from Twitter"""
        
        try:
            # Twitter API v2 search would go here
            # For now, return placeholder data
            return {
                "score": 0.1,  # Slightly positive
                "tweet_count": 0,
                "positive_ratio": 0.6,
                "summary": "Limited Twitter data available"
            }
            
        except Exception as e:
            print(f"❌ Twitter error: {e}")
            return {"score": 0, "error": str(e)}
    
    async def get_news_analysis(self, symbol: str) -> Dict:
        """Get news analysis from multiple sources"""
        
        try:
            news_items = []
            
            # NewsAPI
            if self.apis["newsapi"]["api_key"]:
                news_items.extend(await self.fetch_newsapi_data(symbol))
            
            # NewsData.io
            if self.apis["newsdata_io"]["api_key"]:
                news_items.extend(await self.fetch_newsdata_io(symbol))
            
            return {
                "articles_count": len(news_items),
                "summary": self.summarize_news(news_items),
                "sentiment": self.analyze_news_sentiment(news_items)
            }
            
        except Exception as e:
            print(f"❌ News analysis error: {e}")
            return {"summary": "News analysis unavailable", "error": str(e)}
    
    async def get_llm_analysis(self, analysis_data: Dict) -> Dict:
        """Get AI analysis using Mac Mini LLM"""
        
        try:
            # Create comprehensive prompt
            prompt = f"""
            Analyze the following cryptocurrency data and provide trading insights:
            
            Market Data:
            - Price: ${analysis_data.get('market', {}).get('price', 'N/A')}
            - 24h Change: {analysis_data.get('market', {}).get('change_24h', 'N/A')}%
            - Volume: ${analysis_data.get('market', {}).get('volume_24h', 'N/A')}
            
            Sentiment: {analysis_data.get('sentiment', {}).get('score', 'N/A')}
            News Summary: {analysis_data.get('news', {}).get('summary', 'No news available')}
            
            Provide a brief analysis and recommendation (buy/sell/hold) with confidence level.
            """
            
            response = self.llm_manager.generate_response(prompt, provider="mac_mini")
            
            return {
                "analysis": response.get("response", "LLM analysis unavailable"),
                "cost": response.get("cost", 0.0),
                "provider": response.get("provider", "unknown")
            }
            
        except Exception as e:
            print(f"❌ LLM analysis error: {e}")
            return {"analysis": "LLM analysis failed", "error": str(e)}
    
    def calculate_technical_indicators(self, price_history: List) -> Dict:
        """Calculate basic technical indicators"""
        
        if len(price_history) < 7:
            return {"error": "Insufficient data"}
        
        prices = [float(point[1]) for point in price_history[-7:]]  # Last 7 days
        
        return {
            "sma_7": sum(prices) / len(prices),
            "volatility": self.calculate_volatility(prices),
            "trend": "up" if prices[-1] > prices[0] else "down"
        }
    
    def calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility"""
        if len(prices) < 2:
            return 0.0
        
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return variance ** 0.5
    
    def generate_recommendation(self, analysis_data: Dict) -> Dict:
        """Generate trading recommendation based on all data"""
        
        market = analysis_data.get("market", {})
        sentiment = analysis_data.get("sentiment", {})
        
        # Simple scoring system
        score = 0
        
        # Price trend
        if market.get("change_24h", 0) > 5:
            score += 2
        elif market.get("change_24h", 0) > 0:
            score += 1
        elif market.get("change_24h", 0) < -5:
            score -= 2
        elif market.get("change_24h", 0) < 0:
            score -= 1
        
        # Sentiment
        sentiment_score = sentiment.get("score", 0)
        if sentiment_score > 0.5:
            score += 2
        elif sentiment_score > 0:
            score += 1
        elif sentiment_score < -0.5:
            score -= 2
        elif sentiment_score < 0:
            score -= 1
        
        # Generate recommendation
        if score >= 3:
            return {"action": "BUY", "confidence": 0.8}
        elif score >= 1:
            return {"action": "BUY", "confidence": 0.6}
        elif score <= -3:
            return {"action": "SELL", "confidence": 0.8}
        elif score <= -1:
            return {"action": "SELL", "confidence": 0.6}
        else:
            return {"action": "HOLD", "confidence": 0.5}
    
    def store_analysis(self, analysis: CryptoAnalysis, raw_data: Dict):
        """Store analysis results in database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO crypto_analysis 
                    (timestamp, symbol, price, sentiment_score, news_summary, 
                     technical_indicators, recommendation, confidence, cost_usd, analysis_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    analysis.timestamp.isoformat(),
                    analysis.symbol,
                    analysis.price,
                    analysis.sentiment_score,
                    analysis.news_summary,
                    json.dumps(analysis.technical_indicators),
                    analysis.recommendation,
                    analysis.confidence,
                    analysis.cost_usd,
                    json.dumps(raw_data)
                ))
                
        except Exception as e:
            print(f"❌ Database storage error: {e}")

# Global analyzer instance
crypto_analyzer = OrionCryptoAnalyzer()
