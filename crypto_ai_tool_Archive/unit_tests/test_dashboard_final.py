#!/usr/bin/env python3
"""
🧪 FINAL DASHBOARD TEST
Test dashboard functions to show exact metrics
"""
import os
import sys
import sqlite3
from datetime import datetime

# Add dashboard to path
sys.path.append('dashboard')
from learning_dashboard import get_system_stats, get_system_health, get_recent_events

def test_dashboard_functions():
    """Test all dashboard functions and show metrics"""
    print("🧪 FINAL DASHBOARD FUNCTION TEST")
    print("=" * 60)
    
    try:
        # Test system stats
        print("📊 SYSTEM STATS:")
        stats = get_system_stats()
        for key, value in stats.items():
            print(f"  • {key}: {value}")
        
        print("\n🏥 SYSTEM HEALTH:")
        health = get_system_health()
        for key, value in health.items():
            print(f"  • {key}: {value}")
        
        print("\n📡 RECENT EVENTS:")
        events = get_recent_events()
        for event in events[:5]:  # Show first 5
            print(f"  • {event}")
        
        # Mac Mini specific data
        print("\n🤖 MAC MINI DATA:")
        db_path = "databases/unified/market_data.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Today's collections
            today = datetime.now().date()
            cursor.execute("SELECT COUNT(*) FROM crypto_prices WHERE date(timestamp) = ?", (today,))
            crypto_today = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM rss_articles WHERE date(created_at) = ?", (today,))
            news_today = cursor.fetchone()[0]
            
            # Pending analysis
            cursor.execute("SELECT COUNT(*) FROM rss_articles WHERE sentiment_score IS NULL")
            pending = cursor.fetchone()[0]
            
            print(f"  • Crypto collected today: {crypto_today}")
            print(f"  • News collected today: {news_today}")
            print(f"  • Pending analysis: {pending}")
            
            conn.close()
        
        print("\n✅ DASHBOARD FUNCTIONS WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

if __name__ == "__main__":
    test_dashboard_functions() 