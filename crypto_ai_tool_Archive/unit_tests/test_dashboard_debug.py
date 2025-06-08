#!/usr/bin/env python3
"""
Dashboard Debug - Test API functions directly
"""
import sys
import os
sys.path.append('dashboard')
from learning_dashboard import LearningDashboard
import json

def test_mac_mini_stats():
    print("🧪 TESTING MAC MINI STATS")
    print("="*30)
    
    try:
        stats = LearningDashboard.get_mac_mini_stats()
        print("✅ Mac Mini Stats:")
        print(json.dumps(stats, indent=2))
        return True
    except Exception as e:
        print(f"❌ Error getting Mac Mini stats: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_learning_stats():
    print("\n🧪 TESTING LEARNING STATS")
    print("="*30)
    
    try:
        stats = LearningDashboard.get_learning_stats()
        print("✅ Learning Stats:")
        print(json.dumps(stats, indent=2))
        return True
    except Exception as e:
        print(f"❌ Error getting learning stats: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_timeline():
    print("\n🧪 TESTING EVENT TIMELINE")
    print("="*30)
    
    try:
        events = LearningDashboard.get_event_timeline()
        print(f"✅ Found {len(events)} events")
        if events:
            print("Latest events:")
            for event in events[:3]:
                print(f"  - {event['type']} from {event['source']} at {event['timestamp']}")
        return True
    except Exception as e:
        print(f"❌ Error getting events: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_databases():
    print("\n🧪 CHECKING DATABASE FILES")
    print("="*30)
    
    databases = {
        'Mac Mini DB': 'databases/unified/market_data.db',
        'Research DB': 'databases/sqlite_dbs/research_learnings.db',
        'Knowledge DB': 'databases/sqlite_dbs/knowledge_base.db',
        'Events DB': 'databases/sqlite_dbs/event_store.db',
        'Free Data DB': 'data/free_sources_data.db'
    }
    
    for name, path in databases.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024  # KB
            print(f"✅ {name}: {size:.1f} KB")
        else:
            print(f"❌ {name}: MISSING ({path})")

if __name__ == "__main__":
    print("🔍 DASHBOARD DEBUG TEST")
    print("="*50)
    
    check_databases()
    
    success_count = 0
    success_count += test_mac_mini_stats()
    success_count += test_learning_stats() 
    success_count += test_event_timeline()
    
    print(f"\n📊 RESULTS: {success_count}/3 tests passed")
    
    if success_count == 3:
        print("✅ All dashboard functions working - issue might be Flask server")
    else:
        print("❌ Dashboard functions have issues - need to fix before starting server") 