#!/usr/bin/env python3
"""
Complete HuggingFace Test - End to End
"""
import sys
sys.path.append('research_center')
from llm_analyzer import ResearchIntelligence
import asyncio
import json
from datetime import datetime

async def test_complete_hf_system():
    print("🧪 COMPLETE HUGGINGFACE SYSTEM TEST")
    print("="*50)
    
    # Initialize analyzer
    analyzer = ResearchIntelligence()
    print(f"💡 Using HuggingFace: {analyzer.use_huggingface}")
    print(f"🖥️  Ollama Available: {hasattr(analyzer, 'client')}")
    print(f"🔑 HF API Key: {'✅ Present' if analyzer.hf_api_key else '❌ Missing'}")
    
    # Test data similar to Mac Mini collection
    test_data = {
        'prices': {
            'BTC': {'price': 43000, 'change_24h': 2.5},
            'ETH': {'price': 2600, 'change_24h': 3.1},
            'SOL': {'price': 105, 'change_24h': -1.2}
        },
        'articles': [
            {'title': 'Bitcoin ETF Approval News', 'sentiment': 'positive'},
            {'title': 'Ethereum Network Upgrade', 'sentiment': 'neutral'}
        ]
    }
    
    print("\n📊 Test Data:")
    print(json.dumps(test_data, indent=2))
    
    print("\n🔬 Running Analysis...")
    start_time = datetime.now()
    
    try:
        result = await analyzer.analyze_market_data(test_data)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Analysis Complete in {duration:.2f}s")
        print("📋 Analysis Result:")
        print(json.dumps(result, indent=2))
        
        # Test learning capability
        if result.get('success', True):
            print("\n🧠 Testing Learning...")
            learning_result = await analyzer.learn_from_analysis(
                result, 
                {'outcome': 'test_successful', 'profit': 0}
            )
            print("📚 Learning Result:")
            print(json.dumps(learning_result, indent=2))
        
        print("\n📈 Daily Insights...")
        insights = await analyzer.get_daily_insights()
        print(json.dumps(insights, indent=2))
        
    except Exception as e:
        print(f"\n❌ Analysis Failed: {e}")
        return False
    
    print("\n✅ COMPLETE TEST SUCCESSFUL")
    print(f"⏱️  Total Duration: {(datetime.now() - start_time).total_seconds():.2f}s")
    return True

if __name__ == "__main__":
    asyncio.run(test_complete_hf_system()) 