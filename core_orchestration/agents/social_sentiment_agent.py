#!/usr/bin/env python3
"""
🐦 SOCIAL SENTIMENT AGENT
AI Agent for Twitter intelligence and social media sentiment analysis
"""

import asyncio
import json
import sqlite3
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import os
import logging
import re
from dataclasses import dataclass

@dataclass
class SocialPost:
    platform: str
    post_id: str
    author: str
    content: str
    timestamp: datetime
    engagement_score: float
    sentiment_score: float
    influence_score: float
    crypto_relevance: float

@dataclass
class InfluencerMetric:
    username: str
    platform: str
    follower_count: int
    engagement_rate: float
    crypto_relevance: float
    sentiment_trend: str
    influence_score: float

class SocialSentimentAgent:
    """
    AI Agent for social media intelligence
    - Twitter crypto influencer monitoring
    - Real-time sentiment analysis
    - Viral content detection
    - Social signal generation
    """
    
    def __init__(self):
        self.agent_id = "social_sentiment_001"
        self.db_path = "data/social_intelligence.db"
        self.setup_database()
        self.setup_logging()
        
        # Top crypto influencers to monitor
        self.crypto_influencers = {
            "twitter": [
                "elonmusk",
                "michael_saylor", 
                "VitalikButerin",
                "coinbase",
                "binance",
                "cz_binance",
                "APompliano",
                "brian_armstrong",
                "SatoshiLite",
                "novogratz",
                "ThinkingUSD",
                "WhalePanda",
                "100trillionUSD",
                "BitcoinMagazine",
                "CoinDesk"
            ]
        }
        
        # Sentiment keywords
        self.sentiment_keywords = {
            "bullish": ["moon", "bullish", "buy", "hodl", "pump", "rocket", "green", "surge"],
            "bearish": ["dump", "crash", "bearish", "sell", "red", "falling", "drop", "down"],
            "neutral": ["stable", "sideways", "flat", "consolidation", "range"]
        }
        
        # Crypto relevance keywords
        self.crypto_keywords = [
            "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
            "blockchain", "defi", "nft", "altcoin", "trading", "hodl",
            "binance", "coinbase", "exchange", "wallet", "mining"
        ]
        
    def setup_database(self):
        """Setup social intelligence database"""
        Path("data").mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Social posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                post_id TEXT UNIQUE NOT NULL,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                engagement_score REAL DEFAULT 0.0,
                sentiment_score REAL DEFAULT 0.0,
                influence_score REAL DEFAULT 0.0,
                crypto_relevance REAL DEFAULT 0.0,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0
            )
        """)
        
        # Influencer metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS influencer_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                platform TEXT NOT NULL,
                follower_count INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                crypto_relevance REAL DEFAULT 0.0,
                sentiment_trend TEXT DEFAULT 'neutral',
                influence_score REAL DEFAULT 0.0,
                last_updated REAL NOT NULL,
                posts_analyzed INTEGER DEFAULT 0
            )
        """)
        
        # Sentiment trends table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                overall_sentiment REAL DEFAULT 0.0,
                bullish_percentage REAL DEFAULT 0.0,
                bearish_percentage REAL DEFAULT 0.0,
                neutral_percentage REAL DEFAULT 0.0,
                total_posts INTEGER DEFAULT 0,
                timestamp REAL NOT NULL
            )
        """)
        
        # Viral alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viral_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                description TEXT NOT NULL,
                post_id TEXT,
                author TEXT,
                viral_score REAL DEFAULT 0.0,
                timestamp REAL NOT NULL,
                recommendation TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def setup_logging(self):
        """Setup agent logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SocialSentiment - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/social_sentiment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🐦 Social Sentiment Agent {self.agent_id} initialized")
    
    async def run_sentiment_analysis(self) -> Dict[str, Any]:
        """Alias for test compatibility"""
        return await self.run_monitoring_cycle()
    
    async def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run comprehensive social media monitoring cycle"""
        self.logger.info("🐦 Starting social sentiment monitoring cycle...")
        cycle_start = time.time()
        
        # 1. Monitor crypto influencers
        influencer_posts = await self.monitor_crypto_influencers()
        
        # 2. Analyze sentiment trends
        sentiment_trends = await self.analyze_sentiment_trends()
        
        # 3. Detect viral content
        viral_content = await self.detect_viral_content()
        
        # 4. Update influencer metrics
        influencer_metrics = await self.update_influencer_metrics()
        
        # 5. Generate social signals
        social_signals = await self.generate_social_signals(sentiment_trends, viral_content)
        
        cycle_time = time.time() - cycle_start
        
        results = {
            "cycle_time": cycle_time,
            "influencer_posts": len(influencer_posts),
            "sentiment_trends": len(sentiment_trends),
            "viral_content": len(viral_content),
            "influencer_metrics": len(influencer_metrics),
            "social_signals": len(social_signals),
            "top_influencer_posts": [
                {
                    "author": post.author,
                    "content": post.content[:100] + "...",
                    "sentiment": post.sentiment_score,
                    "influence": post.influence_score,
                    "engagement": post.engagement_score
                } for post in influencer_posts[:5]
            ],
            "viral_alerts": [
                {
                    "type": content["type"],
                    "author": content["author"],
                    "viral_score": content["viral_score"],
                    "description": content["description"]
                } for content in viral_content if content.get("viral_score", 0) > 0.8
            ]
        }
        
        self.logger.info(f"✅ Social sentiment monitoring complete ({cycle_time:.2f}s)")
        self.logger.info(f"   📱 Influencer posts: {len(influencer_posts)}")
        self.logger.info(f"   📊 Sentiment trends: {len(sentiment_trends)}")
        self.logger.info(f"   🔥 Viral content: {len(viral_content)}")
        self.logger.info(f"   📈 Social signals: {len(social_signals)}")
        
        return results
    
    async def monitor_crypto_influencers(self) -> List[SocialPost]:
        """Monitor posts from crypto influencers"""
        posts = []
        
        # Monitor Twitter influencers
        twitter_posts = await self.monitor_twitter_influencers()
        posts.extend(twitter_posts)
        
        # Store posts
        for post in posts:
            self.store_social_post(post)
        
        return posts
    
    async def monitor_twitter_influencers(self) -> List[SocialPost]:
        """Monitor Twitter crypto influencers"""
        posts = []
        
        # Note: In production, would use Twitter API v2
        # For now, generate mock data for testing
        
        mock_posts = [
            {
                "author": "elonmusk",
                "content": "Bitcoin is the future of money 🚀",
                "engagement": 50000,
                "timestamp": time.time()
            },
            {
                "author": "michael_saylor",
                "content": "MicroStrategy continues to accumulate Bitcoin. Digital property for the digital economy.",
                "engagement": 15000,
                "timestamp": time.time()
            },
            {
                "author": "VitalikButerin",
                "content": "Ethereum's latest upgrade shows significant improvements in transaction throughput.",
                "engagement": 8000,
                "timestamp": time.time()
            },
            {
                "author": "cz_binance",
                "content": "The crypto market is maturing. Institutional adoption accelerating.",
                "engagement": 12000,
                "timestamp": time.time()
            },
            {
                "author": "APompliano",
                "content": "Another day, another all-time high for crypto adoption metrics.",
                "engagement": 5000,
                "timestamp": time.time()
            }
        ]
        
        for mock_post in mock_posts:
            # Analyze post
            sentiment = self.analyze_post_sentiment(mock_post["content"])
            crypto_relevance = self.calculate_crypto_relevance(mock_post["content"])
            influence_score = self.calculate_influence_score(mock_post["author"], mock_post["engagement"])
            engagement_score = self.normalize_engagement_score(mock_post["engagement"])
            
            post = SocialPost(
                platform="twitter",
                post_id=f"tw_{mock_post['author']}_{int(mock_post['timestamp'])}",
                author=mock_post["author"],
                content=mock_post["content"],
                timestamp=datetime.fromtimestamp(mock_post["timestamp"]),
                engagement_score=engagement_score,
                sentiment_score=sentiment,
                influence_score=influence_score,
                crypto_relevance=crypto_relevance
            )
            
            posts.append(post)
        
        return posts
    
    async def analyze_sentiment_trends(self) -> List[Dict[str, Any]]:
        """Analyze overall sentiment trends"""
        trends = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent posts for trend analysis
            recent_posts = cursor.execute("""
                SELECT sentiment_score, crypto_relevance, timestamp
                FROM social_posts
                WHERE timestamp > ? AND crypto_relevance > 0.5
                ORDER BY timestamp DESC
                LIMIT 100
            """, (time.time() - 86400,)).fetchall()  # Last 24 hours
            
            conn.close()
            
            if recent_posts:
                sentiments = [post[0] for post in recent_posts]
                
                # Calculate sentiment distribution
                bullish_count = len([s for s in sentiments if s > 0.1])
                bearish_count = len([s for s in sentiments if s < -0.1])
                neutral_count = len(sentiments) - bullish_count - bearish_count
                
                total_posts = len(sentiments)
                
                trend = {
                    "platform": "twitter",
                    "timeframe": "24h",
                    "overall_sentiment": sum(sentiments) / len(sentiments),
                    "bullish_percentage": (bullish_count / total_posts) * 100,
                    "bearish_percentage": (bearish_count / total_posts) * 100,
                    "neutral_percentage": (neutral_count / total_posts) * 100,
                    "total_posts": total_posts,
                    "timestamp": time.time()
                }
                
                trends.append(trend)
                self.store_sentiment_trend(trend)
            
        except Exception as e:
            self.logger.warning(f"⚠️ Sentiment trend analysis error: {e}")
            # Generate mock trend for testing
            trends = [{
                "platform": "twitter",
                "timeframe": "24h", 
                "overall_sentiment": 0.15,
                "bullish_percentage": 45.0,
                "bearish_percentage": 25.0,
                "neutral_percentage": 30.0,
                "total_posts": 150,
                "timestamp": time.time()
            }]
        
        return trends
    
    async def detect_viral_content(self) -> List[Dict[str, Any]]:
        """Detect viral crypto content"""
        viral_content = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find high-engagement recent posts
            viral_posts = cursor.execute("""
                SELECT platform, post_id, author, content, engagement_score, 
                       sentiment_score, crypto_relevance, timestamp
                FROM social_posts
                WHERE timestamp > ? AND engagement_score > 0.8 AND crypto_relevance > 0.7
                ORDER BY engagement_score DESC
                LIMIT 10
            """, (time.time() - 3600,)).fetchall()  # Last hour
            
            conn.close()
            
            for post in viral_posts:
                platform, post_id, author, content, engagement, sentiment, relevance, timestamp = post
                
                viral_score = (engagement + relevance) / 2
                
                viral_item = {
                    "type": "viral_post",
                    "platform": platform,
                    "post_id": post_id,
                    "author": author,
                    "content": content[:200] + "...",
                    "viral_score": viral_score,
                    "sentiment": sentiment,
                    "timestamp": timestamp,
                    "description": f"Viral crypto post by @{author} ({viral_score:.2f} viral score)",
                    "recommendation": self.generate_viral_recommendation(sentiment, viral_score)
                }
                
                viral_content.append(viral_item)
                self.store_viral_alert(viral_item)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Viral content detection error: {e}")
            # Generate mock viral content for testing
            viral_content = [{
                "type": "viral_post",
                "platform": "twitter",
                "author": "elonmusk",
                "viral_score": 0.95,
                "sentiment": 0.8,
                "description": "Elon Musk's Bitcoin tweet going viral (0.95 viral score)",
                "recommendation": "Monitor for potential price impact - high influence bullish sentiment"
            }]
        
        return viral_content
    
    async def update_influencer_metrics(self) -> List[InfluencerMetric]:
        """Update metrics for crypto influencers"""
        metrics = []
        
        for influencer in self.crypto_influencers["twitter"]:
            # Calculate metrics based on recent posts
            metric = await self.calculate_influencer_metrics(influencer, "twitter")
            if metric:
                metrics.append(metric)
                self.store_influencer_metric(metric)
        
        return metrics
    
    async def calculate_influencer_metrics(self, username: str, platform: str) -> Optional[InfluencerMetric]:
        """Calculate metrics for a specific influencer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent posts from this influencer
            posts = cursor.execute("""
                SELECT engagement_score, sentiment_score, crypto_relevance
                FROM social_posts
                WHERE author = ? AND platform = ? AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 20
            """, (username, platform, time.time() - 604800)).fetchall()  # Last week
            
            conn.close()
            
            if not posts:
                return None
            
            # Calculate metrics
            avg_engagement = sum(post[0] for post in posts) / len(posts)
            avg_sentiment = sum(post[1] for post in posts) / len(posts)
            avg_relevance = sum(post[2] for post in posts) / len(posts)
            
            # Determine sentiment trend
            recent_sentiments = [post[1] for post in posts[:5]]
            sentiment_trend = "bullish" if sum(recent_sentiments) > 0.1 else "bearish" if sum(recent_sentiments) < -0.1 else "neutral"
            
            # Calculate influence score
            follower_count = self.get_follower_count(username)  # Mock data
            influence_score = (avg_engagement * 0.4 + avg_relevance * 0.3 + (follower_count / 1000000) * 0.3)
            
            return InfluencerMetric(
                username=username,
                platform=platform,
                follower_count=follower_count,
                engagement_rate=avg_engagement,
                crypto_relevance=avg_relevance,
                sentiment_trend=sentiment_trend,
                influence_score=min(influence_score, 1.0)
            )
            
        except Exception as e:
            self.logger.warning(f"⚠️ Influencer metrics calculation error for {username}: {e}")
            return None
    
    async def generate_social_signals(self, sentiment_trends: List[Dict[str, Any]], viral_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate trading signals based on social sentiment"""
        signals = []
        
        for trend in sentiment_trends:
            # Generate signal based on sentiment
            signal_strength = abs(trend["overall_sentiment"])
            
            if signal_strength > 0.3:  # Strong sentiment
                signal = {
                    "signal_type": "sentiment_signal",
                    "direction": "bullish" if trend["overall_sentiment"] > 0 else "bearish", 
                    "strength": signal_strength,
                    "confidence": min(trend["total_posts"] / 100, 1.0),  # More posts = higher confidence
                    "timeframe": trend["timeframe"],
                    "reasoning": f"{trend['bullish_percentage']:.1f}% bullish, {trend['bearish_percentage']:.1f}% bearish sentiment",
                    "recommendation": self.generate_sentiment_recommendation(trend["overall_sentiment"], signal_strength)
                }
                signals.append(signal)
        
        # Add viral content signals
        for content in viral_content:
            if content.get("viral_score", 0) > 0.8:
                signal = {
                    "signal_type": "viral_signal",
                    "direction": "bullish" if content.get("sentiment", 0) > 0 else "bearish",
                    "strength": content["viral_score"],
                    "confidence": 0.8,  # High confidence for viral content
                    "source": f"@{content['author']}",
                    "reasoning": f"Viral crypto content with {content['viral_score']:.2f} viral score",
                    "recommendation": content.get("recommendation", "Monitor for market impact")
                }
                signals.append(signal)
        
        return signals
    
    # Helper methods
    def analyze_post_sentiment(self, content: str) -> float:
        """Analyze sentiment of social media post"""
        content_lower = content.lower()
        
        bullish_score = sum(1 for word in self.sentiment_keywords["bullish"] if word in content_lower)
        bearish_score = sum(1 for word in self.sentiment_keywords["bearish"] if word in content_lower)
        
        # Normalize to -1 to 1 scale
        total_sentiment_words = bullish_score + bearish_score
        if total_sentiment_words == 0:
            return 0.0
        
        sentiment = (bullish_score - bearish_score) / total_sentiment_words
        return max(-1.0, min(1.0, sentiment))
    
    def calculate_crypto_relevance(self, content: str) -> float:
        """Calculate how relevant content is to crypto"""
        content_lower = content.lower()
        
        crypto_mentions = sum(1 for keyword in self.crypto_keywords if keyword in content_lower)
        total_words = len(content.split())
        
        # Simple relevance score
        relevance = min(crypto_mentions / max(total_words, 1) * 10, 1.0)
        return relevance
    
    def calculate_influence_score(self, author: str, engagement: int) -> float:
        """Calculate influence score based on author and engagement"""
        # Base influence based on known influencers
        base_influence = {
            "elonmusk": 1.0,
            "michael_saylor": 0.9,
            "VitalikButerin": 0.9,
            "cz_binance": 0.8,
            "APompliano": 0.7
        }
        
        author_influence = base_influence.get(author, 0.5)
        
        # Engagement modifier (normalized)
        engagement_modifier = min(engagement / 50000, 1.0)
        
        return (author_influence + engagement_modifier) / 2
    
    def normalize_engagement_score(self, engagement: int) -> float:
        """Normalize engagement to 0-1 scale"""
        # Log scale for engagement
        import math
        if engagement <= 0:
            return 0.0
        
        # Normalize based on typical crypto influencer engagement
        normalized = math.log10(engagement + 1) / 6  # log10(1M) ≈ 6
        return min(normalized, 1.0)
    
    def get_follower_count(self, username: str) -> int:
        """Get follower count for username (mock data)"""
        mock_followers = {
            "elonmusk": 150000000,
            "michael_saylor": 3000000,
            "VitalikButerin": 4500000,
            "cz_binance": 8000000,
            "APompliano": 1500000
        }
        return mock_followers.get(username, 100000)
    
    def generate_viral_recommendation(self, sentiment: float, viral_score: float) -> str:
        """Generate recommendation for viral content"""
        if viral_score > 0.9:
            if sentiment > 0.5:
                return "High-impact bullish viral content - potential price pump"
            elif sentiment < -0.5:
                return "High-impact bearish viral content - potential price dump"
            else:
                return "High-impact neutral viral content - monitor for direction"
        else:
            return "Monitor viral content for market sentiment impact"
    
    def generate_sentiment_recommendation(self, sentiment: float, strength: float) -> str:
        """Generate recommendation based on sentiment"""
        if strength > 0.5:
            if sentiment > 0.3:
                return "Strong bullish sentiment - consider long positions"
            elif sentiment < -0.3:
                return "Strong bearish sentiment - consider risk management"
        else:
            return "Moderate sentiment - monitor for trend confirmation"
    
    def store_social_post(self, post: SocialPost):
        """Store social media post in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO social_posts
            (platform, post_id, author, content, timestamp, engagement_score,
             sentiment_score, influence_score, crypto_relevance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post.platform, post.post_id, post.author, post.content,
            post.timestamp.timestamp(), post.engagement_score,
            post.sentiment_score, post.influence_score, post.crypto_relevance
        ))
        
        conn.commit()
        conn.close()
    
    def store_influencer_metric(self, metric: InfluencerMetric):
        """Store influencer metric in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO influencer_metrics
            (username, platform, follower_count, engagement_rate, crypto_relevance,
             sentiment_trend, influence_score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metric.username, metric.platform, metric.follower_count,
            metric.engagement_rate, metric.crypto_relevance,
            metric.sentiment_trend, metric.influence_score, time.time()
        ))
        
        conn.commit()
        conn.close()
    
    def store_sentiment_trend(self, trend: Dict[str, Any]):
        """Store sentiment trend in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sentiment_trends
            (platform, timeframe, overall_sentiment, bullish_percentage,
             bearish_percentage, neutral_percentage, total_posts, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trend["platform"], trend["timeframe"], trend["overall_sentiment"],
            trend["bullish_percentage"], trend["bearish_percentage"],
            trend["neutral_percentage"], trend["total_posts"], trend["timestamp"]
        ))
        
        conn.commit()
        conn.close()
    
    def store_viral_alert(self, alert: Dict[str, Any]):
        """Store viral alert in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO viral_alerts
            (platform, alert_type, description, post_id, author,
             viral_score, timestamp, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert["platform"], alert["type"], alert["description"],
            alert.get("post_id"), alert["author"], alert["viral_score"],
            alert["timestamp"], alert.get("recommendation")
        ))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    async def main():
        agent = SocialSentimentAgent()
        
        print("🐦 Social Sentiment Agent - Running monitoring cycle...")
        
        # Run monitoring cycle
        results = await agent.run_monitoring_cycle()
        
        print(f"\n🎯 SOCIAL SENTIMENT RESULTS:")
        print(f"Cycle Time: {results['cycle_time']:.2f}s")
        print(f"Influencer Posts: {results['influencer_posts']}")
        print(f"Sentiment Trends: {results['sentiment_trends']}")
        print(f"Viral Content: {results['viral_content']}")
        print(f"Social Signals: {results['social_signals']}")
        
        if results['top_influencer_posts']:
            print(f"\n📱 TOP INFLUENCER POSTS:")
            for post in results['top_influencer_posts']:
                print(f"  @{post['author']}: {post['content']}")
                print(f"    Sentiment: {post['sentiment']:.2f}, Influence: {post['influence']:.2f}")
        
        if results['viral_alerts']:
            print(f"\n🔥 VIRAL ALERTS:")
            for alert in results['viral_alerts']:
                print(f"  {alert['type']} by @{alert['author']}: {alert['description']}")
    
    asyncio.run(main()) 