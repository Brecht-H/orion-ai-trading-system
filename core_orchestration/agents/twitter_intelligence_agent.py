#!/usr/bin/env python3
"""
Twitter Intelligence Agent for Orion Project
Advanced Twitter monitoring with crypto influencer analysis
Uses actual Twitter API with comprehensive market intelligence extraction
"""

import os
import sys
import json
import sqlite3
import asyncio
import aiohttp
import requests
import tweepy
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TwitterIntelligenceAgent:
    """Advanced Twitter intelligence with market analysis"""
    
    def __init__(self):
        self.agent_name = "Twitter Intelligence Agent"
        self.version = "1.0.0"
        self.db_path = "databases/sqlite_dbs/twitter_intelligence.db"
        self.setup_database()
        
        # Load Twitter API credentials
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Initialize Twitter API (v2)
        self.twitter_client = None
        if self.bearer_token:
            self.twitter_client = tweepy.Client(bearer_token=self.bearer_token)
        elif self.api_key and self.api_secret:
            # Fallback to v1.1 API if no bearer token
            auth = tweepy.AppAuthHandler(self.api_key, self.api_secret)
            self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Crypto influencers with their Twitter handles and specializations
        self.crypto_influencers = {
            "elonmusk": {
                "name": "Elon Musk",
                "followers": "150M+",
                "influence_score": 10,
                "specialization": ["bitcoin", "dogecoin", "general_crypto"],
                "market_impact": "extreme"
            },
            "saylor": {
                "name": "Michael Saylor",
                "followers": "3M+", 
                "influence_score": 9,
                "specialization": ["bitcoin", "corporate_adoption"],
                "market_impact": "high"
            },
            "VitalikButerin": {
                "name": "Vitalik Buterin",
                "followers": "5M+",
                "influence_score": 9,
                "specialization": ["ethereum", "defi", "technical"],
                "market_impact": "high"
            },
            "APompliano": {
                "name": "Anthony Pompliano",
                "followers": "1.5M+",
                "influence_score": 8,
                "specialization": ["bitcoin", "investment", "macro"],
                "market_impact": "medium-high"
            },
            "BTC_Archive": {
                "name": "Bitcoin Archive",
                "followers": "2M+",
                "influence_score": 7,
                "specialization": ["bitcoin", "history", "education"],
                "market_impact": "medium"
            },
            "DocumentingBTC": {
                "name": "Documenting Bitcoin",
                "followers": "800K+",
                "influence_score": 7,
                "specialization": ["bitcoin", "adoption", "news"],
                "market_impact": "medium"
            },
            "BitcoinMagazine": {
                "name": "Bitcoin Magazine",
                "followers": "1M+",
                "influence_score": 7,
                "specialization": ["bitcoin", "news", "technical"],
                "market_impact": "medium"
            },
            "CoinDesk": {
                "name": "CoinDesk",
                "followers": "1.2M+",
                "influence_score": 7,
                "specialization": ["general_crypto", "news", "market"],
                "market_impact": "medium"
            },
            "cointelegraph": {
                "name": "Cointelegraph",
                "followers": "2M+",
                "influence_score": 7,
                "specialization": ["general_crypto", "news", "analysis"],
                "market_impact": "medium"
            },
            "Blockstream": {
                "name": "Blockstream",
                "followers": "500K+",
                "influence_score": 6,
                "specialization": ["bitcoin", "lightning", "technical"],
                "market_impact": "low-medium"
            },
            "Ripple": {
                "name": "Ripple",
                "followers": "3M+",
                "influence_score": 6,
                "specialization": ["xrp", "payments", "corporate"],
                "market_impact": "medium"
            },
            "ethereum": {
                "name": "Ethereum",
                "followers": "3M+",
                "influence_score": 8,
                "specialization": ["ethereum", "defi", "technical"],
                "market_impact": "high"
            },
            "chainlink": {
                "name": "Chainlink",
                "followers": "1M+",
                "influence_score": 6,
                "specialization": ["chainlink", "oracles", "defi"],
                "market_impact": "medium"
            },
            "Uniswap": {
                "name": "Uniswap",
                "followers": "800K+",
                "influence_score": 6,
                "specialization": ["defi", "dex", "ethereum"],
                "market_impact": "medium"
            },
            "AaveAave": {
                "name": "Aave",
                "followers": "600K+",
                "influence_score": 6,
                "specialization": ["defi", "lending", "ethereum"],
                "market_impact": "medium"
            }
        }
        
        # Crypto keywords for relevance scoring
        self.crypto_keywords = [
            "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
            "blockchain", "defi", "nft", "altcoin", "hodl", "pump", "dump",
            "bull", "bear", "moon", "satoshi", "mining", "wallet", "exchange",
            "trading", "price", "market", "adoption", "regulation", "sec"
        ]
        
        # Market sentiment indicators
        self.bullish_indicators = [
            "bullish", "moon", "pump", "rally", "breakout", "ath", "green",
            "buy", "accumulate", "hodl", "diamond hands", "laser eyes"
        ]
        
        self.bearish_indicators = [
            "bearish", "dump", "crash", "correction", "red", "sell", "fear",
            "panic", "fud", "bottom", "capitulation", "weak hands"
        ]
    
    def setup_database(self):
        """Setup Twitter intelligence database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Twitter posts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS twitter_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tweet_id TEXT UNIQUE,
                    username TEXT,
                    user_full_name TEXT,
                    content TEXT,
                    created_at TEXT,
                    likes INTEGER,
                    retweets INTEGER,
                    replies INTEGER,
                    influence_score INTEGER,
                    market_impact TEXT,
                    sentiment_score REAL,
                    relevance_score REAL,
                    crypto_mentions TEXT,
                    hashtags TEXT,
                    urls TEXT,
                    timestamp TEXT
                )
            """)
            
            # Influencer tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS influencer_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    full_name TEXT,
                    followers_count INTEGER,
                    influence_score INTEGER,
                    specialization TEXT,
                    market_impact TEXT,
                    last_tweet_id TEXT,
                    posts_today INTEGER,
                    avg_sentiment REAL,
                    last_updated TEXT
                )
            """)
            
            # Market signals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_type TEXT,
                    signal_strength REAL,
                    source_username TEXT,
                    source_tweet_id TEXT,
                    description TEXT,
                    confidence_score REAL,
                    timestamp TEXT
                )
            """)
            
            # Agent performance metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS twitter_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_time REAL,
                    posts_analyzed INTEGER,
                    signals_generated INTEGER,
                    influencers_monitored INTEGER,
                    api_calls_made INTEGER,
                    timestamp TEXT
                )
            """)
            
            conn.commit()
        
        print(f"✅ {self.agent_name} database initialized")
    
    def extract_crypto_mentions(self, text: str) -> List[str]:
        """Extract crypto-related mentions from text"""
        text_lower = text.lower()
        mentions = []
        
        for keyword in self.crypto_keywords:
            if keyword in text_lower:
                mentions.append(keyword)
        
        # Extract ticker symbols ($BTC, $ETH, etc.)
        ticker_pattern = r'\$([A-Z]{2,5})'
        tickers = re.findall(ticker_pattern, text.upper())
        mentions.extend([f"${ticker}" for ticker in tickers])
        
        return list(set(mentions))
    
    def calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score based on crypto-specific indicators"""
        text_lower = text.lower()
        
        bullish_count = sum(1 for indicator in self.bullish_indicators if indicator in text_lower)
        bearish_count = sum(1 for indicator in self.bearish_indicators if indicator in text_lower)
        
        if bullish_count + bearish_count == 0:
            return 0.0
        
        return (bullish_count - bearish_count) / (bullish_count + bearish_count)
    
    def calculate_relevance_score(self, text: str) -> float:
        """Calculate crypto relevance score"""
        crypto_mentions = self.extract_crypto_mentions(text)
        
        # Base score from crypto keywords
        base_score = min(1.0, len(crypto_mentions) / 3.0)
        
        # Boost for specific high-value terms
        high_value_terms = ["bitcoin", "ethereum", "btc", "eth", "regulation", "adoption"]
        boost = sum(0.1 for term in high_value_terms if term in text.lower())
        
        return min(1.0, base_score + boost)
    
    def generate_market_signals(self, posts: List[Dict]) -> List[Dict]:
        """Generate market signals from Twitter analysis"""
        signals = []
        
        # Aggregate sentiment by timeframe
        recent_posts = [p for p in posts if p['sentiment_score'] != 0]
        
        if len(recent_posts) >= 3:
            avg_sentiment = sum(p['sentiment_score'] for p in recent_posts) / len(recent_posts)
            
            # Strong sentiment signal
            if abs(avg_sentiment) > 0.5:
                signal_type = "bullish_sentiment" if avg_sentiment > 0 else "bearish_sentiment"
                signal_strength = abs(avg_sentiment)
                
                signals.append({
                    "signal_type": signal_type,
                    "signal_strength": signal_strength,
                    "description": f"Strong {signal_type.split('_')[0]} sentiment across {len(recent_posts)} influencer posts",
                    "confidence_score": min(0.9, signal_strength + 0.2),
                    "source_count": len(recent_posts)
                })
        
        # High-influence user signals
        for post in posts:
            if post['influence_score'] >= 8 and post['relevance_score'] > 0.7:
                signals.append({
                    "signal_type": "high_influence_post",
                    "signal_strength": post['influence_score'] / 10.0,
                    "source_username": post['username'],
                    "source_tweet_id": post['tweet_id'],
                    "description": f"High-influence post from {post['user_full_name']}",
                    "confidence_score": 0.8,
                    "content_snippet": post['content'][:100] + "..."
                })
        
        return signals
    
    async def collect_user_tweets(self, username: str, max_tweets: int = 10) -> List[Dict]:
        """Collect recent tweets from a specific user"""
        tweets = []
        
        try:
            if self.twitter_client:
                # Use Twitter API v2
                user = self.twitter_client.get_user(username=username)
                if user.data:
                    user_tweets = self.twitter_client.get_users_tweets(
                        id=user.data.id,
                        max_results=max_tweets,
                        tweet_fields=['created_at', 'public_metrics', 'context_annotations']
                    )
                    
                    if user_tweets.data:
                        for tweet in user_tweets.data:
                            tweet_data = {
                                "tweet_id": tweet.id,
                                "username": username,
                                "user_full_name": self.crypto_influencers.get(username, {}).get("name", username),
                                "content": tweet.text,
                                "created_at": tweet.created_at.isoformat() if tweet.created_at else "",
                                "likes": tweet.public_metrics.get('like_count', 0) if tweet.public_metrics else 0,
                                "retweets": tweet.public_metrics.get('retweet_count', 0) if tweet.public_metrics else 0,
                                "replies": tweet.public_metrics.get('reply_count', 0) if tweet.public_metrics else 0,
                                "influence_score": self.crypto_influencers.get(username, {}).get("influence_score", 5),
                                "market_impact": self.crypto_influencers.get(username, {}).get("market_impact", "low"),
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            # Calculate sentiment and relevance
                            tweet_data["sentiment_score"] = self.calculate_sentiment_score(tweet.text)
                            tweet_data["relevance_score"] = self.calculate_relevance_score(tweet.text)
                            tweet_data["crypto_mentions"] = json.dumps(self.extract_crypto_mentions(tweet.text))
                            
                            # Extract hashtags and URLs
                            hashtags = re.findall(r'#(\w+)', tweet.text)
                            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.text)
                            
                            tweet_data["hashtags"] = json.dumps(hashtags)
                            tweet_data["urls"] = json.dumps(urls)
                            
                            tweets.append(tweet_data)
            
            else:
                # Mock data if no API access
                mock_tweet = {
                    "tweet_id": f"mock_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "username": username,
                    "user_full_name": self.crypto_influencers.get(username, {}).get("name", username),
                    "content": f"Mock crypto tweet from {username} about current market conditions #crypto #bitcoin",
                    "created_at": datetime.now().isoformat(),
                    "likes": 150,
                    "retweets": 45,
                    "replies": 12,
                    "influence_score": self.crypto_influencers.get(username, {}).get("influence_score", 5),
                    "market_impact": self.crypto_influencers.get(username, {}).get("market_impact", "low"),
                    "sentiment_score": 0.3,
                    "relevance_score": 0.8,
                    "crypto_mentions": json.dumps(["crypto", "bitcoin"]),
                    "hashtags": json.dumps(["crypto", "bitcoin"]),
                    "urls": json.dumps([]),
                    "timestamp": datetime.now().isoformat()
                }
                tweets.append(mock_tweet)
                
        except Exception as e:
            print(f"❌ Error collecting tweets for {username}: {e}")
        
        return tweets
    
    def store_tweets(self, tweets: List[Dict]):
        """Store tweets in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for tweet in tweets:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO twitter_posts 
                        (tweet_id, username, user_full_name, content, created_at, likes, retweets, replies,
                         influence_score, market_impact, sentiment_score, relevance_score, crypto_mentions,
                         hashtags, urls, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        tweet["tweet_id"], tweet["username"], tweet["user_full_name"],
                        tweet["content"], tweet["created_at"], tweet["likes"], tweet["retweets"],
                        tweet["replies"], tweet["influence_score"], tweet["market_impact"],
                        tweet["sentiment_score"], tweet["relevance_score"], tweet["crypto_mentions"],
                        tweet["hashtags"], tweet["urls"], tweet["timestamp"]
                    ))
                except sqlite3.IntegrityError:
                    pass  # Skip duplicates
            
            conn.commit()
    
    def store_market_signals(self, signals: List[Dict]):
        """Store market signals in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for signal in signals:
                cursor.execute("""
                    INSERT INTO market_signals 
                    (signal_type, signal_strength, source_username, source_tweet_id, 
                     description, confidence_score, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    signal["signal_type"], signal["signal_strength"],
                    signal.get("source_username"), signal.get("source_tweet_id"),
                    signal["description"], signal["confidence_score"],
                    datetime.now().isoformat()
                ))
            
            conn.commit()
    
    async def run_intelligence_cycle(self) -> Dict:
        """Run complete Twitter intelligence cycle"""
        start_time = datetime.now()
        print(f"🔄 {self.agent_name} starting intelligence cycle...")
        
        all_tweets = []
        api_calls = 0
        
        # Collect tweets from all influencers
        for username in self.crypto_influencers.keys():
            print(f"📱 Collecting tweets from @{username}...")
            tweets = await self.collect_user_tweets(username, max_tweets=5)
            all_tweets.extend(tweets)
            api_calls += 1
            
            # Rate limiting
            await asyncio.sleep(1)
        
        # Store tweets
        if all_tweets:
            self.store_tweets(all_tweets)
        
        # Generate market signals
        signals = self.generate_market_signals(all_tweets)
        if signals:
            self.store_market_signals(signals)
        
        # Calculate metrics
        cycle_time = (datetime.now() - start_time).total_seconds()
        
        # Store agent metrics
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO twitter_metrics 
                (cycle_time, posts_analyzed, signals_generated, influencers_monitored, api_calls_made, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                cycle_time, len(all_tweets), len(signals), 
                len(self.crypto_influencers), api_calls, datetime.now().isoformat()
            ))
            conn.commit()
        
        # Calculate sentiment aggregates
        relevant_tweets = [t for t in all_tweets if t['relevance_score'] > 0.5]
        avg_sentiment = sum(t['sentiment_score'] for t in relevant_tweets) / max(1, len(relevant_tweets))
        
        results = {
            "agent": self.agent_name,
            "cycle_time": f"{cycle_time:.2f}s",
            "tweets_collected": len(all_tweets),
            "relevant_tweets": len(relevant_tweets),
            "signals_generated": len(signals),
            "influencers_monitored": len(self.crypto_influencers),
            "api_calls_made": api_calls,
            "avg_sentiment": f"{avg_sentiment:.3f}",
            "top_influences": self.get_top_influence_posts(all_tweets),
            "market_signals": [
                {
                    "type": s["signal_type"],
                    "strength": f"{s['signal_strength']:.2f}",
                    "confidence": f"{s['confidence_score']:.2f}",
                    "description": s["description"][:60] + "..."
                }
                for s in signals[:3]
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ {self.agent_name} completed cycle in {cycle_time:.2f}s")
        print(f"📊 Tweets: {len(all_tweets)}, Signals: {len(signals)}, Sentiment: {avg_sentiment:.3f}")
        
        return results
    
    def get_top_influence_posts(self, tweets: List[Dict], limit: int = 3) -> List[Dict]:
        """Get top influence posts from recent tweets"""
        sorted_tweets = sorted(tweets, key=lambda x: x['influence_score'] * x['relevance_score'], reverse=True)
        
        return [
            {
                "username": tweet["username"],
                "influence": tweet["influence_score"],
                "sentiment": f"{tweet['sentiment_score']:.2f}",
                "relevance": f"{tweet['relevance_score']:.2f}",
                "engagement": tweet["likes"] + tweet["retweets"],
                "content": tweet["content"][:80] + "..." if len(tweet["content"]) > 80 else tweet["content"]
            }
            for tweet in sorted_tweets[:limit]
        ]

async def main():
    """Main function to test Twitter intelligence agent"""
    print("🚀 Starting Twitter Intelligence Agent Test...")
    
    agent = TwitterIntelligenceAgent()
    
    # Check API status
    if agent.twitter_client:
        print("✅ Twitter API v2 connected")
    elif hasattr(agent, 'twitter_api'):
        print("✅ Twitter API v1.1 connected")
    else:
        print("⚠️  Using mock data (no Twitter API credentials)")
    
    print(f"👥 Monitoring {len(agent.crypto_influencers)} crypto influencers")
    
    # Run intelligence cycle
    results = await agent.run_intelligence_cycle()
    
    print("\n📈 TWITTER INTELLIGENCE RESULTS:")
    print(f"⏱️  Cycle Time: {results['cycle_time']}")
    print(f"📱 Tweets Collected: {results['tweets_collected']}")
    print(f"🎯 Relevant Tweets: {results['relevant_tweets']}")
    print(f"🚨 Signals Generated: {results['signals_generated']}")
    print(f"📊 Average Sentiment: {results['avg_sentiment']}")
    
    if results['top_influences']:
        print(f"\n🌟 Top Influence Posts:")
        for post in results['top_influences']:
            print(f"   @{post['username']} (I:{post['influence']}, S:{post['sentiment']}): {post['content']}")
    
    if results['market_signals']:
        print(f"\n🚨 Market Signals:")
        for signal in results['market_signals']:
            print(f"   {signal['type']} (S:{signal['strength']}, C:{signal['confidence']}): {signal['description']}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main()) 