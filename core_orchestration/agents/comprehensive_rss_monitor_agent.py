#!/usr/bin/env python3
"""
Comprehensive RSS Feed Monitor Agent for Orion Project
Monitors ALL RSS feeds from crypto-ai-tool and Orion configurations
Includes Twitter integration and complete news monitoring
"""

import os
import sys
import json
import sqlite3
import asyncio
import aiohttp
import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class ComprehensiveRSSMonitorAgent:
    """Comprehensive RSS feed monitoring with Twitter integration"""
    
    def __init__(self):
        self.agent_name = "Comprehensive RSS Monitor Agent"
        self.version = "1.0.0"
        self.db_path = "databases/sqlite_dbs/comprehensive_rss_data.db"
        self.setup_database()
        
        # Load environment variables
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Comprehensive RSS feeds from crypto-ai-tool and Orion
        self.crypto_feeds = {
            "Cointelegraph": "https://cointelegraph.com/rss",
            "NewsBTC": "https://www.newsbtc.com/feed/",
            "Bitcoinist": "https://bitcoinist.com/feed/",
            "CryptoSlate": "https://cryptoslate.com/feed/",
            "CryptoBriefing": "https://cryptobriefing.com/feed/",
            "The Block": "https://www.theblock.co/rss.xml",
            "CryptoPotato": "https://cryptopotato.com/feed/",
            "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "Bitcoin Magazine": "https://bitcoinmagazine.com/.rss/full/",
            "Decrypt": "https://decrypt.co/feed",
            "CoinTelegraph DeFi": "https://cointelegraph.com/rss/tag/defi",
            "CoinTelegraph Altcoins": "https://cointelegraph.com/rss/tag/altcoin",
            "CoinTelegraph Bitcoin": "https://cointelegraph.com/rss/tag/bitcoin",
            "CoinTelegraph Ethereum": "https://cointelegraph.com/rss/tag/ethereum"
        }
        
        self.financial_feeds = {
            "Reuters Finance": "https://www.reutersagency.com/feed/?best-topics=business-finance",
            "CNBC Crypto": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "Yahoo Finance BTC": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=BTC-USD&region=US&lang=en-US",
            "SeekingAlpha": "https://seekingalpha.com/market-news/all/rss.xml",
            "MarketWatch": "https://feeds.marketwatch.com/marketwatch/marketpulse/",
            "Bloomberg Crypto": "https://feeds.bloomberg.com/crypto/news.rss",
            "Forbes Crypto": "https://www.forbes.com/crypto-blockchain/feed/",
            "Business Insider Crypto": "https://markets.businessinsider.com/rss/news"
        }
        
        self.government_feeds = {
            "Federal Reserve": "https://www.federalreserve.gov/feeds/press_all.xml",
            "ECB": "https://www.ecb.europa.eu/rss/press.xml",
            "IMF": "https://www.imf.org/en/News/rss",
            "White House": "https://www.whitehouse.gov/feed/",
            "SEC": "https://www.sec.gov/rss/news/press-release.xml",
            "CFTC": "https://www.cftc.gov/rss/pressreleases.xml",
            "Treasury": "https://www.treasury.gov/resource-center/press-releases/Pages/rss.aspx"
        }
        
        self.trading_feeds = {
            "Quantocracy": "https://quantocracy.com/feed/",
            "Investopedia": "https://www.investopedia.com/rss",
            "TradingView Ideas": "https://www.tradingview.com/blog/en/rss/",
            "Alpha Architect": "https://alphaarchitect.com/feed/",
            "Quantifiable Edges": "http://quantifiableedges.com/feed/",
            "All About Alpha": "http://allaboutalpha.com/feed/"
        }
        
        self.tech_feeds = {
            "Hacker News": "https://feeds.feedwrench.com/HackerNews.rss",
            "TechCrunch": "https://techcrunch.com/feed/",
            "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
            "Wired": "https://www.wired.com/feed",
            "MIT Technology Review": "https://www.technologyreview.com/feed/"
        }
        
        # Twitter influencers to monitor
        self.twitter_influencers = [
            "elonmusk", "saylor", "VitalikButerin", "APompliano", "BTC_Archive",
            "DocumentingBTC", "BitcoinMagazine", "CoinDesk", "cointelegraph",
            "Blockstream", "Ripple", "ethereum", "chainlink", "Uniswap", "AaveAave"
        ]
        
    def setup_database(self):
        """Setup comprehensive RSS monitoring database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # RSS articles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rss_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_name TEXT,
                    feed_category TEXT,
                    title TEXT,
                    description TEXT,
                    link TEXT UNIQUE,
                    published_date TEXT,
                    sentiment_score REAL,
                    relevance_score REAL,
                    keywords TEXT,
                    timestamp TEXT
                )
            """)
            
            # Twitter data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS twitter_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    tweet_id TEXT UNIQUE,
                    content TEXT,
                    likes INTEGER,
                    retweets INTEGER,
                    timestamp TEXT,
                    sentiment_score REAL,
                    relevance_score REAL
                )
            """)
            
            # Feed monitoring status
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feed_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_name TEXT UNIQUE,
                    feed_url TEXT,
                    last_checked TEXT,
                    status TEXT,
                    articles_count INTEGER,
                    error_message TEXT
                )
            """)
            
            # Agent performance metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_time REAL,
                    articles_processed INTEGER,
                    twitter_posts INTEGER,
                    total_sources INTEGER,
                    success_rate REAL,
                    timestamp TEXT
                )
            """)
            
            conn.commit()
        
        print(f"✅ {self.agent_name} database initialized")

    async def fetch_rss_feed(self, session: aiohttp.ClientSession, name: str, url: str) -> List[Dict]:
        """Fetch articles from RSS feed"""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    articles = []
                    for entry in feed.entries[:10]:  # Limit to 10 recent articles
                        article = {
                            "feed_name": name,
                            "title": getattr(entry, 'title', 'No title'),
                            "description": getattr(entry, 'summary', 'No description'),
                            "link": getattr(entry, 'link', ''),
                            "published_date": getattr(entry, 'published', ''),
                            "timestamp": datetime.now().isoformat()
                        }
                        articles.append(article)
                    
                    # Update feed status
                    self.update_feed_status(name, url, "success", len(articles))
                    return articles
                else:
                    self.update_feed_status(name, url, "error", 0, f"HTTP {response.status}")
                    return []
                    
        except Exception as e:
            self.update_feed_status(name, url, "error", 0, str(e))
            return []

    def update_feed_status(self, name: str, url: str, status: str, count: int, error: str = None):
        """Update feed monitoring status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO feed_status 
                (feed_name, feed_url, last_checked, status, articles_count, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, url, datetime.now().isoformat(), status, count, error))
            conn.commit()

    def analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (can be enhanced with better models)"""
        positive_words = ["bullish", "moon", "pump", "gain", "profit", "rise", "up", "green", "buy"]
        negative_words = ["bearish", "dump", "crash", "loss", "drop", "fall", "down", "red", "sell"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / (positive_count + negative_count)

    def calculate_relevance(self, text: str) -> float:
        """Calculate crypto relevance score"""
        crypto_keywords = [
            "bitcoin", "btc", "ethereum", "eth", "crypto", "blockchain", "defi",
            "nft", "altcoin", "trading", "mining", "wallet", "exchange", "staking"
        ]
        
        text_lower = text.lower()
        relevance_count = sum(1 for keyword in crypto_keywords if keyword in text_lower)
        
        return min(1.0, relevance_count / 5.0)  # Normalize to 0-1

    async def collect_twitter_data(self) -> List[Dict]:
        """Collect Twitter data from influencers (mock implementation)"""
        # Mock Twitter data since we need Bearer token for real API
        twitter_data = []
        
        for username in self.twitter_influencers[:5]:  # Limit for testing
            mock_tweet = {
                "username": username,
                "tweet_id": f"mock_{username}_{datetime.now().strftime('%Y%m%d')}",
                "content": f"Mock tweet from {username} about crypto market conditions",
                "likes": 150,
                "retweets": 45,
                "timestamp": datetime.now().isoformat(),
                "sentiment_score": self.analyze_sentiment(f"crypto market {username}"),
                "relevance_score": 0.8
            }
            twitter_data.append(mock_tweet)
        
        return twitter_data

    def store_articles(self, articles: List[Dict], category: str):
        """Store RSS articles in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for article in articles:
                # Calculate sentiment and relevance
                text = f"{article['title']} {article['description']}"
                sentiment = self.analyze_sentiment(text)
                relevance = self.calculate_relevance(text)
                
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO rss_articles 
                        (feed_name, feed_category, title, description, link, published_date, 
                         sentiment_score, relevance_score, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        article["feed_name"], category, article["title"], 
                        article["description"], article["link"], article["published_date"],
                        sentiment, relevance, article["timestamp"]
                    ))
                except sqlite3.IntegrityError:
                    pass  # Skip duplicates
            
            conn.commit()

    def store_twitter_data(self, twitter_data: List[Dict]):
        """Store Twitter data in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for tweet in twitter_data:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO twitter_data 
                        (username, tweet_id, content, likes, retweets, timestamp, 
                         sentiment_score, relevance_score)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        tweet["username"], tweet["tweet_id"], tweet["content"],
                        tweet["likes"], tweet["retweets"], tweet["timestamp"],
                        tweet["sentiment_score"], tweet["relevance_score"]
                    ))
                except sqlite3.IntegrityError:
                    pass  # Skip duplicates
            
            conn.commit()

    async def run_monitoring_cycle(self) -> Dict:
        """Run complete monitoring cycle"""
        start_time = datetime.now()
        print(f"🔄 {self.agent_name} starting monitoring cycle...")
        
        all_articles = []
        twitter_data = []
        total_sources = 0
        
        # Collect RSS feeds
        async with aiohttp.ClientSession() as session:
            # Crypto feeds
            for name, url in self.crypto_feeds.items():
                articles = await self.fetch_rss_feed(session, name, url)
                if articles:
                    self.store_articles(articles, "crypto")
                    all_articles.extend(articles)
                total_sources += 1
            
            # Financial feeds
            for name, url in self.financial_feeds.items():
                articles = await self.fetch_rss_feed(session, name, url)
                if articles:
                    self.store_articles(articles, "financial")
                    all_articles.extend(articles)
                total_sources += 1
            
            # Government feeds  
            for name, url in self.government_feeds.items():
                articles = await self.fetch_rss_feed(session, name, url)
                if articles:
                    self.store_articles(articles, "government")
                    all_articles.extend(articles)
                total_sources += 1
            
            # Trading feeds
            for name, url in self.trading_feeds.items():
                articles = await self.fetch_rss_feed(session, name, url)
                if articles:
                    self.store_articles(articles, "trading")
                    all_articles.extend(articles)
                total_sources += 1
            
            # Tech feeds
            for name, url in self.tech_feeds.items():
                articles = await self.fetch_rss_feed(session, name, url)
                if articles:
                    self.store_articles(articles, "tech")
                    all_articles.extend(articles)
                total_sources += 1
        
        # Collect Twitter data
        twitter_data = await self.collect_twitter_data()
        if twitter_data:
            self.store_twitter_data(twitter_data)
        
        # Calculate metrics
        cycle_time = (datetime.now() - start_time).total_seconds()
        success_rate = len([a for a in all_articles if a]) / max(1, total_sources)
        
        # Store agent metrics
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agent_metrics 
                (cycle_time, articles_processed, twitter_posts, total_sources, success_rate, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                cycle_time, len(all_articles), len(twitter_data), 
                total_sources, success_rate, datetime.now().isoformat()
            ))
            conn.commit()
        
        results = {
            "agent": self.agent_name,
            "cycle_time": f"{cycle_time:.2f}s",
            "articles_collected": len(all_articles),
            "twitter_posts": len(twitter_data),
            "total_sources": total_sources,
            "success_rate": f"{success_rate:.2%}",
            "feeds_monitored": {
                "crypto": len(self.crypto_feeds),
                "financial": len(self.financial_feeds),
                "government": len(self.government_feeds),
                "trading": len(self.trading_feeds),
                "tech": len(self.tech_feeds)
            },
            "top_sentiment": self.get_top_sentiment_articles(),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ {self.agent_name} completed cycle in {cycle_time:.2f}s")
        print(f"📊 Articles: {len(all_articles)}, Twitter: {len(twitter_data)}, Sources: {total_sources}")
        
        return results

    def get_top_sentiment_articles(self) -> List[Dict]:
        """Get top sentiment articles from recent data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT feed_name, title, sentiment_score, relevance_score
                FROM rss_articles 
                WHERE timestamp > datetime('now', '-1 hour')
                ORDER BY ABS(sentiment_score) DESC, relevance_score DESC
                LIMIT 5
            """)
            
            results = cursor.fetchall()
            return [
                {
                    "feed": row[0],
                    "title": row[1][:60] + "..." if len(row[1]) > 60 else row[1],
                    "sentiment": f"{row[2]:.3f}",
                    "relevance": f"{row[3]:.3f}"
                }
                for row in results
            ]

    def get_status_report(self) -> Dict:
        """Get comprehensive status report"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get feed status summary
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM feed_status
                GROUP BY status
            """)
            feed_status = dict(cursor.fetchall())
            
            # Get recent articles count
            cursor.execute("""
                SELECT COUNT(*) FROM rss_articles 
                WHERE timestamp > datetime('now', '-1 hour')
            """)
            recent_articles = cursor.fetchone()[0]
            
            # Get total articles
            cursor.execute("SELECT COUNT(*) FROM rss_articles")
            total_articles = cursor.fetchone()[0]
            
            # Get Twitter data count
            cursor.execute("SELECT COUNT(*) FROM twitter_data")
            twitter_count = cursor.fetchone()[0]
            
            return {
                "agent": self.agent_name,
                "version": self.version,
                "feed_status": feed_status,
                "recent_articles": recent_articles,
                "total_articles": total_articles,
                "twitter_posts": twitter_count,
                "feeds_configured": {
                    "crypto": len(self.crypto_feeds),
                    "financial": len(self.financial_feeds),
                    "government": len(self.government_feeds),
                    "trading": len(self.trading_feeds),
                    "tech": len(self.tech_feeds)
                },
                "total_feeds": sum([
                    len(self.crypto_feeds), len(self.financial_feeds),
                    len(self.government_feeds), len(self.trading_feeds),
                    len(self.tech_feeds)
                ]),
                "twitter_influencers": len(self.twitter_influencers),
                "timestamp": datetime.now().isoformat()
            }

async def main():
    """Main function to test the comprehensive RSS monitor"""
    print("🚀 Starting Comprehensive RSS Monitor Agent Test...")
    
    agent = ComprehensiveRSSMonitorAgent()
    
    # Get initial status
    status = agent.get_status_report()
    print(f"📊 Initial Status: {status['total_feeds']} feeds configured")
    
    # Run monitoring cycle
    results = await agent.run_monitoring_cycle()
    
    print("\n📈 COMPREHENSIVE RSS MONITORING RESULTS:")
    print(f"⏱️  Cycle Time: {results['cycle_time']}")
    print(f"📰 Articles Collected: {results['articles_collected']}")
    print(f"🐦 Twitter Posts: {results['twitter_posts']}")
    print(f"📡 Sources Monitored: {results['total_sources']}")
    print(f"✅ Success Rate: {results['success_rate']}")
    
    print(f"\n📊 Feeds by Category:")
    for category, count in results['feeds_monitored'].items():
        print(f"   {category.title()}: {count} feeds")
    
    if results['top_sentiment']:
        print(f"\n🎯 Top Sentiment Articles:")
        for article in results['top_sentiment']:
            print(f"   {article['feed']}: {article['title']} (S:{article['sentiment']}, R:{article['relevance']})")
    
    # Final status
    final_status = agent.get_status_report()
    print(f"\n📊 Final Status: {final_status['total_articles']} total articles stored")
    
    return results

if __name__ == "__main__":
    asyncio.run(main()) 