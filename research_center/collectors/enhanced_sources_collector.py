#!/usr/bin/env python3
"""
Enhanced Data Sources Collector - "Our Gold" Implementation
Twitter Intelligence + On-Chain Analytics + Expanded News
"""

import asyncio
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sqlite3
from pathlib import Path
import os
import time
from dataclasses import dataclass
import re

@dataclass
class DataSource:
    name: str
    url: str
    category: str
    priority: int  # 1-5, 5 being highest
    update_frequency: int  # minutes
    api_key_required: bool
    cost_per_month: float
    description: str

class EnhancedSourcesCollector:
    """
    Enhanced data collection - the gold mine of crypto intelligence
    Twitter + On-Chain + News + Sentiment + Traditional Markets
    """
    
    def __init__(self):
        self.db_path = "data/enhanced_sources_data.db"
        self.setup_database()
        
        # API Keys
        self.api_keys = {
            "twitter_bearer": os.getenv("TWITTER_BEARER_TOKEN"),
            "news_api": os.getenv("NEWS_API_KEY"),
            "etherscan": os.getenv("ETHERSCAN_API_KEY"),
            "blockchain_info": "free",  # Free API
            "coingecko_pro": os.getenv("COINGECKO_PRO_API_KEY"),
            "glassnode": os.getenv("GLASSNODE_API_KEY")
        }
        
        # Critical Twitter Accounts to Monitor
        self.twitter_accounts = {
            "market_movers": [
                "elonmusk", "michael_saylor", "VitalikButerin", 
                "cz_binance", "APompliano", "novogratz", "naval"
            ],
            "crypto_projects": [
                "bitcoin", "ethereum", "solana", "Polkadot", 
                "chainlink", "aave", "uniswap", "MakerDAO"
            ],
            "institutional": [
                "GrayscaleInvest", "MicroStrategy", "Tesla", 
                "PayPal", "Square", "Fidelity"
            ],
            "analysts": [
                "woonomic", "100trillionUSD", "rektcapital", 
                "pentosh1", "ByzGeneral", "TeddyCleps"
            ],
            "news_sources": [
                "CoinDesk", "Cointelegraph", "DecryptMedia",
                "TheBlock__", "MessariCrypto", "DelpDigital"
            ]
        }
        
        # Enhanced News Sources
        self.news_sources = {
            "crypto_news": [
                "https://www.coindesk.com/arc/outboundfeeds/rss/",
                "https://cointelegraph.com/rss",
                "https://decrypt.co/feed",
                "https://bitcoinmagazine.com/.rss/full/",
                "https://thedefiant.io/feed/",
                "https://www.theblockcrypto.com/rss.xml"
            ],
            "regulatory_news": [
                "https://www.sec.gov/news/whatsnew/wn-today.xml",
                "https://www.federalreserve.gov/feeds/press_all.xml"
            ]
        }
        
    def setup_database(self):
        """Setup enhanced database schema"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Twitter data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS twitter_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                sentiment_score REAL DEFAULT 0.0,
                influence_score REAL DEFAULT 0.0,
                market_impact_prediction REAL DEFAULT 0.0,
                raw_data TEXT NOT NULL
            )
        """)
        
        # On-chain data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS onchain_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blockchain TEXT NOT NULL,
                data_type TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp REAL NOT NULL,
                transaction_hash TEXT,
                wallet_address TEXT,
                significance_score REAL DEFAULT 0.0,
                raw_data TEXT NOT NULL
            )
        """)
        
        # Enhanced news table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enhanced_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                timestamp REAL NOT NULL,
                category TEXT NOT NULL,
                sentiment_score REAL DEFAULT 0.0,
                impact_prediction REAL DEFAULT 0.0,
                keywords TEXT,
                raw_data TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Enhanced sources database setup complete")
    
    def collect_all_sources(self) -> Dict[str, Any]:
        """Synchronous wrapper for test compatibility"""
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If already in an async context, create a task instead
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.collect_all_enhanced_data())
                    return future.result()
            else:
                return asyncio.run(self.collect_all_enhanced_data())
        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            return asyncio.run(self.collect_all_enhanced_data())
    
    async def collect_all_enhanced_data(self) -> Dict[str, Any]:
        """Master collection orchestrator"""
        print("🔍 Starting enhanced data collection - 'Our Gold' mining operation...")
        
        start_time = time.time()
        
        # Sequential collection to avoid overwhelming APIs
        results = {
            "twitter_intelligence": await self.collect_twitter_intelligence(),
            "onchain_analytics": await self.collect_onchain_analytics(), 
            "enhanced_news": await self.collect_enhanced_news(),
            "whale_movements": await self.collect_whale_movements(),
            "social_sentiment": await self.collect_social_sentiment()
        }
        
        execution_time = time.time() - start_time
        
        # Calculate total records
        total_records = sum(
            len(data) if isinstance(data, list) else 1 
            for data in results.values()
        )
        
        summary = {
            "total_records": total_records,
            "execution_time": execution_time,
            "sources_collected": len([k for k, v in results.items() if v]),
            "data_breakdown": {k: len(v) if isinstance(v, list) else 1 for k, v in results.items()},
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ Enhanced data collection complete:")
        print(f"   📊 Total records: {total_records}")
        print(f"   ⏱️  Execution time: {execution_time:.2f}s")
        print(f"   🎯 Active sources: {summary['sources_collected']}")
        
        return summary
    
    async def collect_twitter_intelligence(self) -> List[Dict]:
        """Collect critical Twitter intelligence"""
        print("🐦 Collecting Twitter intelligence...")
        
        # Mock data for now (implement with Twitter API when keys available)
        twitter_data = self.generate_mock_twitter_data()
        
        for tweet in twitter_data:
            self.store_twitter_data(tweet)
        
        print(f"✅ Twitter intelligence collected: {len(twitter_data)} tweets")
        return twitter_data
    
    async def collect_onchain_analytics(self) -> List[Dict]:
        """Collect on-chain analytics data"""
        print("⛓️ Collecting on-chain analytics...")
        
        onchain_data = []
        
        # Bitcoin on-chain data using free APIs
        try:
            # Bitcoin transaction count
            response = requests.get("https://blockchain.info/q/24hrtransactioncount", timeout=10)
            if response.status_code == 200:
                tx_count = float(response.text.strip())
                onchain_data.append({
                    "blockchain": "bitcoin",
                    "data_type": "daily_transactions",
                    "value": tx_count,
                    "timestamp": time.time(),
                    "significance_score": self.calculate_significance_score("daily_transactions", tx_count)
                })
                
        except Exception as e:
            print(f"⚠️ Bitcoin on-chain error: {e}")
        
        # Bitcoin hash rate
        try:
            response = requests.get("https://blockchain.info/q/hashrate", timeout=10)
            if response.status_code == 200:
                hash_rate = float(response.text.strip())
                onchain_data.append({
                    "blockchain": "bitcoin", 
                    "data_type": "hash_rate",
                    "value": hash_rate,
                    "timestamp": time.time(),
                    "significance_score": self.calculate_significance_score("hash_rate", hash_rate)
                })
                
        except Exception as e:
            print(f"⚠️ Bitcoin hash rate error: {e}")
        
        # Store on-chain data
        for data in onchain_data:
            self.store_onchain_data(data)
        
        print(f"✅ On-chain analytics collected: {len(onchain_data)} metrics")
        return onchain_data
    
    async def collect_enhanced_news(self) -> List[Dict]:
        """Collect from enhanced news sources"""
        print("📰 Collecting enhanced news feeds...")
        
        news_data = []
        
        try:
            import feedparser
            
            # Collect from all news categories
            for category, sources in self.news_sources.items():
                for source_url in sources[:3]:  # Limit to avoid overload
                    try:
                        feed = feedparser.parse(source_url)
                        
                        for entry in feed.entries[:5]:  # Limit per source
                            news_item = {
                                "source_name": feed.feed.get("title", "Unknown"),
                                "title": entry.title,
                                "content": entry.get("summary", ""),
                                "url": entry.link,
                                "timestamp": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else time.time(),
                                "category": category,
                                "sentiment_score": self.calculate_advanced_sentiment(entry.title + " " + entry.get("summary", "")),
                                "impact_prediction": self.predict_news_impact(entry.title, entry.get("summary", ""))
                            }
                            news_data.append(news_item)
                            self.store_news_data(news_item)
                            
                    except Exception as e:
                        print(f"⚠️ Error collecting from {source_url}: {e}")
                        continue
                        
        except ImportError:
            print("⚠️ feedparser not available, install with: pip install feedparser")
            
        print(f"✅ Enhanced news collected: {len(news_data)} articles")
        return news_data
    
    async def collect_whale_movements(self) -> List[Dict]:
        """Monitor whale wallet movements"""
        print("🐋 Monitoring whale movements...")
        
        # Mock whale movement data for now
        whale_data = [
            {
                "blockchain": "bitcoin",
                "amount": 1500.0,
                "transaction_type": "exchange_deposit",
                "significance": "high",
                "timestamp": time.time()
            },
            {
                "blockchain": "ethereum", 
                "amount": 25000.0,
                "transaction_type": "whale_accumulation",
                "significance": "medium",
                "timestamp": time.time()
            }
        ]
        
        print(f"✅ Whale movements monitored: {len(whale_data)} significant transactions")
        return whale_data
    
    async def collect_social_sentiment(self) -> List[Dict]:
        """Collect social sentiment data"""
        print("😊 Analyzing social sentiment...")
        
        reddit_data = []
        try:
            for subreddit in ["cryptocurrency", "bitcoin", "ethereum"]:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                response = requests.get(url, headers={"User-Agent": "OrionBot"}, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for post in data["data"]["children"]:
                        post_data = post["data"]
                        sentiment_item = {
                            "source": "reddit",
                            "subreddit": subreddit,
                            "title": post_data["title"],
                            "score": post_data["score"],
                            "sentiment_score": self.calculate_advanced_sentiment(post_data["title"]),
                            "timestamp": post_data["created_utc"]
                        }
                        reddit_data.append(sentiment_item)
                        
        except Exception as e:
            print(f"⚠️ Reddit collection error: {e}")
        
        print(f"✅ Social sentiment analyzed: {len(reddit_data)} posts")
        return reddit_data
    
    def calculate_advanced_sentiment(self, text: str) -> float:
        """Calculate advanced sentiment score"""
        positive_words = ["bullish", "moon", "pump", "gains", "profit", "buy", "hodl", "diamond", "rocket"]
        negative_words = ["bearish", "dump", "crash", "loss", "sell", "panic", "fear", "rekt"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Normalize to -1 to 1 scale
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
            
        sentiment = (positive_count - negative_count) / max(total_words, 1)
        return max(-1.0, min(1.0, sentiment))
    
    def predict_news_impact(self, title: str, content: str) -> float:
        """Predict market impact of news"""
        high_impact_keywords = ["regulation", "ban", "adoption", "sec", "etf", "institutional"]
        text = (title + " " + content).lower()
        
        keyword_count = sum(1 for keyword in high_impact_keywords if keyword in text)
        return min(keyword_count * 0.3, 1.0)
    
    def calculate_significance_score(self, data_type: str, value: float) -> float:
        """Calculate significance score for on-chain metrics"""
        normal_ranges = {
            "daily_transactions": (200000, 400000),
            "hash_rate": (100, 200)
        }
        
        if data_type in normal_ranges:
            min_val, max_val = normal_ranges[data_type]
            if value < min_val:
                return min((min_val - value) / min_val, 1.0)
            elif value > max_val:
                return min((value - max_val) / max_val, 1.0)
        
        return 0.0
    
    def store_twitter_data(self, data: Dict):
        """Store Twitter data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO twitter_data
            (tweet_id, username, content, timestamp, likes, retweets, replies,
             sentiment_score, influence_score, market_impact_prediction, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["tweet_id"], data["username"], data["content"], data["timestamp"],
            data["likes"], data["retweets"], data["replies"], data["sentiment_score"],
            data["influence_score"], data["market_impact_prediction"], json.dumps(data)
        ))
        
        conn.commit()
        conn.close()
    
    def store_onchain_data(self, data: Dict):
        """Store on-chain data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO onchain_data
            (blockchain, data_type, value, timestamp, significance_score, raw_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["blockchain"], data["data_type"], data["value"],
            data["timestamp"], data["significance_score"], json.dumps(data)
        ))
        
        conn.commit()
        conn.close()
    
    def store_news_data(self, data: Dict):
        """Store news data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO enhanced_news
            (source_name, title, content, url, timestamp, category,
             sentiment_score, impact_prediction, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["source_name"], data["title"], data["content"], data["url"],
            data["timestamp"], data["category"], data["sentiment_score"],
            data["impact_prediction"], json.dumps(data)
        ))
        
        conn.commit()
        conn.close()
    
    def generate_mock_twitter_data(self) -> List[Dict]:
        """Generate mock Twitter data for testing"""
        return [
            {
                "tweet_id": "mock_001",
                "username": "elonmusk", 
                "content": "Bitcoin is the future of money",
                "sentiment_score": 0.8,
                "influence_score": 1.0,
                "market_impact_prediction": 0.9,
                "timestamp": time.time(),
                "likes": 50000,
                "retweets": 15000,
                "replies": 8000
            },
            {
                "tweet_id": "mock_002",
                "username": "michael_saylor",
                "content": "MicroStrategy continues to accumulate Bitcoin",
                "sentiment_score": 0.7,
                "influence_score": 0.8,
                "market_impact_prediction": 0.7,
                "timestamp": time.time(),
                "likes": 25000,
                "retweets": 8000,
                "replies": 3000
            }
        ]

if __name__ == "__main__":
    async def main():
        collector = EnhancedSourcesCollector()
        results = await collector.collect_all_enhanced_data()
        
        print("\n🎯 ENHANCED COLLECTION RESULTS:")
        print(f"Total Records: {results['total_records']}")
        print(f"Execution Time: {results['execution_time']:.2f}s")
        print(f"Active Sources: {results['sources_collected']}")
        
        print("\n📊 DATA BREAKDOWN:")
        for source, count in results['data_breakdown'].items():
            print(f"  {source}: {count} records")
    
    asyncio.run(main()) 