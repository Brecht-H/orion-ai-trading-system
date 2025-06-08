#!/usr/bin/env python3
"""
Force HuggingFace Test - Bypass Ollama Detection
"""
import sys
sys.path.append('research_center')
import asyncio
import json
from datetime import datetime
import os

# Import after path setup
from llm_analyzer import ResearchIntelligence

class ForceHuggingFaceAnalyzer(ResearchIntelligence):
    """Force HuggingFace usage by overriding detection"""
    
    def __init__(self):
        # Initialize parent but override HF settings
        super().__init__()
        
        # Force HuggingFace usage
        self.use_huggingface = True
        self.hf_api_key = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HUGGINGFACE_API_KEY')
        
        if not self.hf_api_key:
            raise ValueError("No HuggingFace API key found!")
            
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
        print("🌐 FORCED: Using HuggingFace API")

async def test_forced_huggingface():
    print("🧪 FORCED HUGGINGFACE TEST")
    print("="*40)
    
    try:
        # Use forced HuggingFace analyzer
        analyzer = ForceHuggingFaceAnalyzer()
        
        test_data = {
            'prices': {
                'BTC': {'price': 43000, 'change_24h': 2.5},
                'ETH': {'price': 2600, 'change_24h': 3.1}
            }
        }
        
        print("📊 Test Data:")
        print(json.dumps(test_data, indent=2))
        
        print("\n🔬 Running HuggingFace Analysis...")
        start_time = datetime.now()
        
        result = await analyzer.analyze_market_data(test_data)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ HuggingFace Analysis Complete in {duration:.2f}s")
        print("📋 Result:")
        print(json.dumps(result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"\n❌ HuggingFace Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_forced_huggingface())
    if success:
        print("\n🎉 HUGGINGFACE INTEGRATION WORKING!")
    else:
        print("\n💥 HUGGINGFACE INTEGRATION FAILED!") 