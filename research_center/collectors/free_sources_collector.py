#!/usr/bin/env python3
"""
Free Data Sources Collector
Comprehensive collection from all available free sources for MVP
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
from dataclasses import dataclass
import yfinance as yf
import feedparser
import re

@dataclass
class FreeDataSource:
    name: str
    url: str
    api_key_required: bool
    rate_limit: int  # requests per minute
    data_type: str
    description: str

class FreeSourcesCollector:
    """Collects data from all available free sources"""
    
    def __init__(self):
        self.db_path = "data/free_sources_data.db"
        self.setup_database()
        
        # Free data sources (geen API key nodig)
        self.free_sources = {
            "crypto_prices": [
                {
                    "name": "CoinGecko Free",
                    "url": "https://api.coingecko.com/api/v3/simple/price",
                    "rate_limit": 50,  # per minute
                    "description": "Real-time crypto prices"
                },
                {
                    "name": "CryptoCompare Free", 
                    "url": "https://min-api.cryptocompare.com/data/pricemulti",
                    "rate_limit": 100,
                    "description": "Crypto prices and volume"
                },
                {
                    "name": "Binance Public API",
                    "url": "https://api.binance.com/api/v3/ticker/24hr",
                    "rate_limit": 1200,
                    "description": "24hr ticker statistics"
                }
            ],
            "news_rss": [
                {
                    "name": "CoinDesk RSS",
                    "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
                    "description": "Crypto news feed"
                },
                {
                    "name": "CoinTelegraph RSS", 
                    "url": "https://cointelegraph.com/rss",
                    "description": "Crypto news and analysis"
                },
                {
                    "name": "Decrypt RSS",
                    "url": "https://decrypt.co/feed",
                    "description": "Crypto and blockchain news"
                },
                {
                    "name": "Bitcoin Magazine RSS",
                    "url": "https://bitcoinmagazine.com/.rss/full/",
                    "description": "Bitcoin focused news"
                }
            ],
            "fear_greed": [
                {
                    "name": "Alternative.me Fear & Greed",
                    "url": "https://api.alternative.me/fng/",
                    "description": "Crypto Fear & Greed Index"
                }
            ],
            "github_activity": [
                {
                    "name": "GitHub Bitcoin Core",
                    "url": "https://api.github.com/repos/bitcoin/bitcoin/commits",
                    "description": "Bitcoin development activity"
                },
                {
                    "name": "GitHub Ethereum",
                    "url": "https://api.github.com/repos/ethereum/go-ethereum/commits", 
                    "description": "Ethereum development activity"
                }
            ],
            "economic_data": [
                {
                    "name": "FRED Economic Data",
                    "url": "https://api.stlouisfed.org/fred/series/observations",
                    "description": "US Economic indicators (free with API key)"
                }
            ],
            "social_metrics": [
                {
                    "name": "Reddit Crypto Posts",
                    "url": "https://www.reddit.com/r/cryptocurrency.json",
                    "description": "Reddit crypto discussions"
                },
                {
                    "name": "Reddit Bitcoin Posts", 
                    "url": "https://www.reddit.com/r/bitcoin.json",
                    "description": "Reddit Bitcoin discussions"
                }
            ]
        }
        
        # API keys from environment (optional)
        self.api_keys = {
            "coingecko": os.getenv("COINGECKO_API_KEY"),
            "twitter": os.getenv("TWITTER_API_KEY"), 
            "news": os.getenv("NEWS_API_KEY"),
            "fred": os.getenv("FRED_API_KEY")
        }
        
    def setup_database(self):
        """Setup database for free sources data"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS free_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                source_name TEXT NOT NULL,
                data_type TEXT NOT NULL,
                symbol TEXT,
                value TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                source_name TEXT NOT NULL,
                records_collected INTEGER NOT NULL,
                last_collection REAL NOT NULL,
                errors_count INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Free sources database setup complete")
    
    async def collect_all_free_data(self) -> Dict[str, Any]:
        """Collect from all free sources"""
        print("🚀 Starting free data collection...")
        
        results = {
            "crypto_prices": await self.collect_crypto_prices(),
            "news_feeds": await self.collect_news_feeds(),
            "fear_greed": await self.collect_fear_greed(),
            "github_activity": await self.collect_github_activity(),
            "reddit_sentiment": await self.collect_reddit_data(),
            "traditional_markets": await self.collect_traditional_markets()
        }
        
        # Store collection stats
        total_records = sum(len(data) if isinstance(data, list) else 1 for data in results.values())
        self.update_collection_stats("all_sources", total_records)
        
        print(f"✅ Free data collection complete: {total_records} records")
        return results
    
    async def collect_crypto_prices(self) -> List[Dict]:
        """Collect crypto prices from free APIs"""
        print("💰 Collecting crypto prices...")
        
        collected_data = []
        
        # 1. CoinGecko Free (50 requests/minute)
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin,ethereum,binancecoin,cardano,solana,polkadot,polygon,chainlink,avalanche-2,uniswap",
                "vs_currencies": "usd,eur", 
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
                "include_market_cap": "true"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for coin_id, price_data in data.items():
                    record = {
                        "source": "coingecko_free",
                        "symbol": coin_id.upper(),
                        "price_usd": price_data.get("usd", 0),
                        "price_eur": price_data.get("eur", 0),
                        "change_24h": price_data.get("usd_24h_change", 0),
                        "volume_24h": price_data.get("usd_24h_vol", 0),
                        "market_cap": price_data.get("usd_market_cap", 0),
                        "timestamp": datetime.now().timestamp()
                    }
                    collected_data.append(record)
                    self.store_free_data("coingecko_free", "crypto_price", coin_id.upper(), json.dumps(record))
                    
        except Exception as e:
            print(f"❌ CoinGecko error: {e}")
        
        # 2. Binance Public API (geen API key)
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Filter voor belangrijke crypto's
                important_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
                
                for ticker in data:
                    if ticker["symbol"] in important_symbols:
                        symbol = ticker["symbol"].replace("USDT", "")
                        record = {
                            "source": "binance_public",
                            "symbol": symbol,
                            "price": float(ticker["lastPrice"]),
                            "change_24h": float(ticker["priceChangePercent"]),
                            "volume_24h": float(ticker["volume"]),
                            "high_24h": float(ticker["highPrice"]),
                            "low_24h": float(ticker["lowPrice"]),
                            "timestamp": datetime.now().timestamp()
                        }
                        collected_data.append(record)
                        self.store_free_data("binance_public", "crypto_price", symbol, json.dumps(record))
                        
        except Exception as e:
            print(f"❌ Binance error: {e}")
        
        print(f"✅ Collected {len(collected_data)} crypto price records")
        return collected_data
    
    async def collect_news_feeds(self) -> List[Dict]:
        """Collect news from RSS feeds"""
        print("📰 Collecting news feeds...")
        
        collected_data = []
        
        for source in self.free_sources["news_rss"]:
            try:
                feed = feedparser.parse(source["url"])
                
                for entry in feed.entries[:5]:  # Top 5 recent articles
                    # Simple sentiment scoring based on keywords
                    title = entry.title.lower()
                    sentiment_score = self.calculate_simple_sentiment(title)
                    
                    record = {
                        "source": source["name"],
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published if hasattr(entry, 'published') else str(datetime.now()),
                        "sentiment_score": sentiment_score,
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "timestamp": datetime.now().timestamp()
                    }
                    collected_data.append(record)
                    self.store_free_data(source["name"], "news", "CRYPTO", json.dumps(record))
                    
            except Exception as e:
                print(f"❌ RSS Feed error for {source['name']}: {e}")
        
        print(f"✅ Collected {len(collected_data)} news records")
        return collected_data
    
    async def collect_fear_greed(self) -> Dict:
        """Collect Fear & Greed Index"""
        print("😨 Collecting Fear & Greed Index...")
        
        try:
            url = "https://api.alternative.me/fng/"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if "data" in data and len(data["data"]) > 0:
                    latest = data["data"][0]
                    record = {
                        "source": "alternative_me",
                        "fear_greed_index": int(latest["value"]),
                        "classification": latest["value_classification"],
                        "timestamp": datetime.now().timestamp()
                    }
                    
                    self.store_free_data("fear_greed", "sentiment", "CRYPTO", json.dumps(record))
                    print(f"✅ Fear & Greed Index: {record['fear_greed_index']} ({record['classification']})")
                    return record
                    
        except Exception as e:
            print(f"❌ Fear & Greed error: {e}")
        
        return {}
    
    async def collect_github_activity(self) -> List[Dict]:
        """Collect GitHub development activity"""
        print("💻 Collecting GitHub activity...")
        
        collected_data = []
        
        github_repos = [
            ("bitcoin", "bitcoin", "BTC"),
            ("ethereum", "go-ethereum", "ETH")
        ]
        
        for org, repo, symbol in github_repos:
            try:
                url = f"https://api.github.com/repos/{org}/{repo}/commits"
                params = {"per_page": 10, "since": (datetime.now() - timedelta(days=7)).isoformat()}
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    commits = response.json()
                    
                    record = {
                        "source": "github",
                        "symbol": symbol,
                        "repo": f"{org}/{repo}",
                        "commits_last_week": len(commits),
                        "last_commit_date": commits[0]["commit"]["author"]["date"] if commits else None,
                        "timestamp": datetime.now().timestamp()
                    }
                    collected_data.append(record)
                    self.store_free_data("github", "development", symbol, json.dumps(record))
                    
            except Exception as e:
                print(f"❌ GitHub error for {org}/{repo}: {e}")
        
        print(f"✅ Collected {len(collected_data)} GitHub records")
        return collected_data
    
    async def collect_reddit_data(self) -> List[Dict]:
        """Collect Reddit sentiment data"""
        print("📱 Collecting Reddit data...")
        
        collected_data = []
        
        reddit_feeds = [
            ("https://www.reddit.com/r/cryptocurrency.json", "r/cryptocurrency"),
            ("https://www.reddit.com/r/bitcoin.json", "r/bitcoin"),
            ("https://www.reddit.com/r/ethereum.json", "r/ethereum")
        ]
        
        for url, subreddit in reddit_feeds:
            try:
                headers = {"User-Agent": "CryptoAI Bot 1.0"}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    sentiment_scores = []
                    for post in posts[:10]:  # Top 10 posts
                        post_data = post.get("data", {})
                        title = post_data.get("title", "").lower()
                        sentiment = self.calculate_simple_sentiment(title)
                        sentiment_scores.append(sentiment)
                    
                    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
                    
                    record = {
                        "source": "reddit",
                        "subreddit": subreddit,
                        "avg_sentiment": avg_sentiment,
                        "posts_analyzed": len(sentiment_scores),
                        "timestamp": datetime.now().timestamp()
                    }
                    collected_data.append(record)
                    self.store_free_data("reddit", "sentiment", subreddit, json.dumps(record))
                    
            except Exception as e:
                print(f"❌ Reddit error for {subreddit}: {e}")
        
        print(f"✅ Collected {len(collected_data)} Reddit records")
        return collected_data
    
    async def collect_traditional_markets(self) -> List[Dict]:
        """Collect traditional market data using yfinance"""
        print("📈 Collecting traditional markets...")
        
        collected_data = []
        
        symbols = ["^GSPC", "^IXIC", "^VIX", "GC=F", "CL=F", "^TNX", "DX=F"]  # S&P, NASDAQ, VIX, Gold, Oil, 10Y Treasury, DXY
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    previous = hist.iloc[-2] if len(hist) > 1 else hist.iloc[-1]
                    
                    change_pct = ((latest["Close"] - previous["Close"]) / previous["Close"]) * 100
                    
                    record = {
                        "source": "yfinance",
                        "symbol": symbol,
                        "price": latest["Close"],
                        "change_24h": change_pct,
                        "volume": latest["Volume"],
                        "high": latest["High"],
                        "low": latest["Low"],
                        "timestamp": datetime.now().timestamp()
                    }
                    collected_data.append(record)
                    self.store_free_data("yfinance", "traditional_market", symbol, json.dumps(record))
                    
            except Exception as e:
                print(f"❌ yfinance error for {symbol}: {e}")
        
        print(f"✅ Collected {len(collected_data)} traditional market records")
        return collected_data
    
    def calculate_simple_sentiment(self, text: str) -> float:
        """Simple sentiment analysis based on keywords"""
        positive_words = ["bullish", "moon", "pump", "gain", "rise", "surge", "breakthrough", "adoption", "positive", "up", "rally", "bull", "green"]
        negative_words = ["bearish", "dump", "crash", "fall", "drop", "decline", "fear", "sell", "red", "bear", "correction", "dip"]
        
        text = text.lower()
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / (positive_count + negative_count)
        return sentiment  # Returns -1 to 1
    
    def store_free_data(self, source_name: str, data_type: str, symbol: str, data: str):
        """Store collected data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO free_data 
            (timestamp, source_name, data_type, symbol, value, raw_data, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().timestamp(),
            source_name,
            data_type,
            symbol,
            data,  # value = data for now
            data,  # raw_data
            datetime.now().strftime('%Y-%m-%d')
        ))
        
        conn.commit()
        conn.close()
    
    def update_collection_stats(self, source_name: str, records_count: int):
        """Update collection statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT OR REPLACE INTO collection_stats 
            (date, source_name, records_collected, last_collection)
            VALUES (?, ?, ?, ?)
        """, (today, source_name, records_count, datetime.now().timestamp()))
        
        conn.commit()
        conn.close()
    
    def get_collection_summary(self) -> Dict[str, Any]:
        """Get summary of data collection"""
        conn = sqlite3.connect(self.db_path)
        
        # Total records per source
        query = """
            SELECT source_name, COUNT(*) as total_records, MAX(timestamp) as last_collection
            FROM free_data 
            WHERE date = ?
            GROUP BY source_name
        """
        
        today = datetime.now().strftime('%Y-%m-%d')
        df = pd.read_sql_query(query, conn, params=[today])
        
        conn.close()
        
        summary = {
            "collection_date": today,
            "total_sources": len(df),
            "total_records": df["total_records"].sum() if not df.empty else 0,
            "sources": df.to_dict("records") if not df.empty else []
        }
        
        return summary

if __name__ == "__main__":
    async def main():
        collector = FreeSourcesCollector()
        
        print("🚀 Testing Free Sources Collector...")
        results = await collector.collect_all_free_data()
        
        print(f"\n📊 COLLECTION SUMMARY:")
        summary = collector.get_collection_summary()
        print(f"   Total Sources: {summary['total_sources']}")
        print(f"   Total Records: {summary['total_records']}")
        
        for source in summary['sources']:
            print(f"   - {source['source_name']}: {source['total_records']} records")
        
        print("\n✅ Free data collection test complete!")
    
    asyncio.run(main()) 