#!/usr/bin/env python3
"""
News RSS Feed Integration with Mac Mini LLM Sentiment Analysis
Using the comprehensive feed list provided by CEO
"""
import feedparser
import requests
from datetime import datetime
from typing import Dict, List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from protocols.orion_unified_protocol_enhanced import EnhancedOrionUnifiedProtocolV3

class NewsSentimentAnalyzer:
    """RSS news feed integration with Mac Mini sentiment analysis"""
    
    def __init__(self):
        self.protocol = EnhancedOrionUnifiedProtocolV3()
        
        # CEO's comprehensive RSS feed list
        self.crypto_feeds = {
            "Cointelegraph": "https://cointelegraph.com/rss",
            "NewsBTC": "https://www.newsbtc.com/feed/",
            "Bitcoinist": "https://bitcoinist.com/feed/",
            "CryptoSlate": "https://cryptoslate.com/feed/",
            "CryptoBriefing": "https://cryptobriefing.com/feed/",
            "The Block": "https://www.theblock.co/rss.xml",
            "CryptoPotato": "https://cryptopotato.com/feed/"
        }
        
        self.financial_feeds = {
            "Reuters": "https://www.reutersagency.com/feed/?best-topics=business-finance",
            "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "Yahoo Finance BTC": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=BTC-USD&region=US&lang=en-US",
            "SeekingAlpha": "https://seekingalpha.com/market-news/all/rss.xml"
        }
        
        self.government_feeds = {
            "Federal Reserve": "https://www.federalreserve.gov/feeds.htm",
            "ECB": "https://www.ecb.europa.eu/rss/rss.xml",
            "IMF": "https://www.imf.org/en/News/rss",
            "White House": "https://www.whitehouse.gov/feed/"
        }
    
    def fetch_feed_articles(self, feed_url: str, max_articles: int = 5) -> List[Dict]:
        """Fetch articles from RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:max_articles]:
                article = {
                    "title": getattr(entry, 'title', 'No title'),
                    "description": getattr(entry, 'summary', 'No description'),
                    "link": getattr(entry, 'link', ''),
                    "published": getattr(entry, 'published', ''),
                    "source": feed.feed.title if hasattr(feed, 'feed') else 'Unknown'
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"❌ Error fetching {feed_url}: {e}")
            return []
    
    def analyze_sentiment_with_mac_mini(self, text: str) -> Dict:
        """Analyze sentiment using Mac Mini LLM"""
        try:
            response = requests.post(
                "http://192.168.68.103:5001/sentiment",
                json={"text": text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Log API usage
                self.protocol.log_api_usage("mac_mini", "/sentiment", 0.0, 10)
                
                return {
                    "success": True,
                    "sentiment": result["sentiment"],
                    "confidence": result["confidence"],
                    "model": result["model"]
                }
            else:
                return {"success": False, "error": f"API error {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_all_feeds(self, max_per_feed: int = 3) -> Dict:
        """Process all RSS feeds and analyze sentiment"""
        print("📰 Processing all RSS feeds...")
        
        all_articles = []
        sentiment_scores = []
        
        # Process crypto feeds
        for name, url in self.crypto_feeds.items():
            print(f"📊 Processing {name}...")
            articles = self.fetch_feed_articles(url, max_per_feed)
            
            for article in articles:
                # Analyze sentiment of title + description
                text = f"{article['title']} {article['description']}"
                sentiment = self.analyze_sentiment_with_mac_mini(text)
                
                if sentiment["success"]:
                    article["sentiment"] = sentiment["sentiment"]
                    article["confidence"] = sentiment["confidence"]
                    article["feed_category"] = "crypto"
                    
                    # Convert sentiment to numeric score
                    score = sentiment["confidence"] if sentiment["sentiment"] == "positive" else -sentiment["confidence"]
                    sentiment_scores.append(score)
                    
                all_articles.append(article)
        
        # Calculate overall sentiment
        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return {
            "articles": all_articles,
            "article_count": len(all_articles),
            "sentiment_scores": sentiment_scores,
            "overall_sentiment": overall_sentiment,
            "timestamp": datetime.now().isoformat()
        }

def test_news_integration():
    """Test news RSS integration with Mac Mini"""
    print("🧪 Testing News RSS Integration...")
    
    analyzer = NewsSentimentAnalyzer()
    
    # Test Mac Mini connection
    try:
        response = requests.get("http://192.168.68.103:5001/health", timeout=3)
        if response.status_code == 200:
            print("✅ Mac Mini LLM: Connected")
            
            # Process feeds
            news_data = analyzer.process_all_feeds(max_per_feed=2)
            
            print(f"✅ Articles Processed: {news_data['article_count']}")
            print(f"✅ Overall Sentiment: {news_data['overall_sentiment']:.3f}")
            print(f"✅ Sentiment Range: {min(news_data['sentiment_scores']):.3f} to {max(news_data['sentiment_scores']):.3f}")
            
            # Show sample analysis
            if news_data['articles']:
                sample = news_data['articles'][0]
                print(f"\n📰 Sample Analysis:")
                print(f"   Title: {sample['title'][:60]}...")
                print(f"   Sentiment: {sample.get('sentiment', 'unknown')} ({sample.get('confidence', 0):.2%})")
            
            return news_data
        else:
            print("❌ Mac Mini LLM: Not responding")
            return None
            
    except Exception as e:
        print(f"❌ News integration error: {e}")
        return None

if __name__ == "__main__":
    test_news_integration()
