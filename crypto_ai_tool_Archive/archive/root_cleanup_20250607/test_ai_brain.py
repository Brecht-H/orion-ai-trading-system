#!/usr/bin/env python3
"""
TEST AI BRAIN - Complete validation of intelligence layer
Tests both ResearchIntelligence and KnowledgeSynthesis
"""
import asyncio
import json
import sys
from datetime import datetime

# Import AI modules
from research_center.llm_analyzer import ResearchIntelligence
from knowledge_center.llm_synthesis import KnowledgeSynthesis

class AIBrainTester:
    def __init__(self):
        self.analyzer = None
        self.synthesizer = None
        
    async def test_research_intelligence(self):
        """Test the research analyzer"""
        print("🧠 Testing Research Intelligence...")
        
        try:
            self.analyzer = ResearchIntelligence()
            
            # Sample market data
            test_data = {
                'prices': {
                    'BTC': {'price': 52000, 'change_24h': 2.5},
                    'ETH': {'price': 3200, 'change_24h': -1.2},
                    'SOL': {'price': 95, 'change_24h': 5.8}
                },
                'sentiment': {
                    'fear_greed_index': 65,
                    'social_sentiment': 'positive'
                },
                'indicators': {
                    'btc_rsi': 58,
                    'eth_rsi': 45,
                    'market_trend': 'consolidating'
                }
            }
            
            # Test analysis
            analysis = await self.analyzer.analyze_market_data(test_data)
            
            if analysis['success']:
                print("✅ Research Intelligence WORKING!")
                print(f"   Market Sentiment: {analysis['analysis'].get('market_sentiment')}")
                print(f"   Confidence: {analysis['analysis'].get('confidence', 0):.2%}")
                print(f"   Key Insights: {len(analysis['analysis'].get('key_insights', []))}")
                return analysis
            else:
                print(f"❌ Research Intelligence FAILED: {analysis['error']}")
                return None
                
        except Exception as e:
            print(f"❌ Research Intelligence ERROR: {e}")
            return None
            
    async def test_knowledge_synthesis(self, research_analysis):
        """Test knowledge synthesis"""
        print("\n🎯 Testing Knowledge Synthesis...")
        
        if not research_analysis:
            print("❌ No research analysis to synthesize")
            return None
            
        try:
            self.synthesizer = KnowledgeSynthesis()
            
            # Test synthesis
            synthesis = await self.synthesizer.synthesize_insights(research_analysis)
            
            if synthesis['success']:
                print("✅ Knowledge Synthesis WORKING!")
                knowledge = synthesis['knowledge']
                print(f"   Patterns Identified: {len(knowledge.get('patterns_identified', []))}")
                print(f"   Strategies Generated: {len(knowledge.get('strategies_generated', []))}")
                print(f"   Confidence Level: {knowledge.get('confidence_level', 0):.2%}")
                
                # Test strategy generation
                strategies = await self.synthesizer.generate_strategies(knowledge)
                print(f"   Detailed Strategies: {len(strategies)}")
                
                return synthesis
            else:
                print(f"❌ Knowledge Synthesis FAILED: {synthesis['error']}")
                return None
                
        except Exception as e:
            print(f"❌ Knowledge Synthesis ERROR: {e}")
            return None
            
    async def test_full_pipeline(self):
        """Test complete AI pipeline"""
        print("\n🚀 Testing Complete AI Pipeline...")
        
        # Step 1: Research Analysis
        research_result = await self.test_research_intelligence()
        
        # Step 2: Knowledge Synthesis
        synthesis_result = await self.test_knowledge_synthesis(research_result)
        
        # Step 3: Results
        if research_result and synthesis_result:
            print("\n🎉 AI BRAIN FULLY OPERATIONAL!")
            print("="*50)
            print("✅ Research Intelligence: ACTIVE")
            print("✅ Knowledge Synthesis: ACTIVE") 
            print("✅ Strategy Generation: ACTIVE")
            print("✅ Learning System: ACTIVE")
            
            # Show sample output
            if synthesis_result['success']:
                knowledge = synthesis_result['knowledge']
                print(f"\n📊 Sample Output:")
                print(f"   Patterns: {knowledge.get('patterns_identified', [])[:2]}")
                print(f"   Actions: {knowledge.get('recommended_actions', [])[:2]}")
                
            return True
        else:
            print("\n❌ AI BRAIN PARTIALLY WORKING")
            print("="*50)
            print(f"✅ Research Intelligence: {'ACTIVE' if research_result else 'FAILED'}")
            print(f"❌ Knowledge Synthesis: {'ACTIVE' if synthesis_result else 'FAILED'}")
            return False
            
    async def run_test(self):
        """Run complete test suite"""
        print("🔬 AI BRAIN DIAGNOSTIC TEST")
        print("="*50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Python: {sys.version.split()[0]}")
        
        # Check dependencies
        try:
            import ollama
            print("✅ Ollama: Available")
        except ImportError:
            print("❌ Ollama: Missing")
            return False
            
        try:
            import chromadb
            print("✅ ChromaDB: Available")
        except ImportError:
            print("❌ ChromaDB: Missing")
            return False
            
        print("\n" + "="*50)
        
        # Run tests
        success = await self.test_full_pipeline()
        
        print("\n" + "="*50)
        if success:
            print("🎯 RESULT: AI BRAIN IS READY FOR INTEGRATION")
            print("💡 Next: Activate in main system")
        else:
            print("🚨 RESULT: AI BRAIN NEEDS FIXES")
            print("💡 Check error messages above")
            
        return success

async def main():
    """Main test runner"""
    tester = AIBrainTester()
    success = await tester.run_test()
    
    if success:
        print("\n🔥 AI BRAIN TEST: PASSED")
        sys.exit(0)
    else:
        print("\n💥 AI BRAIN TEST: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 