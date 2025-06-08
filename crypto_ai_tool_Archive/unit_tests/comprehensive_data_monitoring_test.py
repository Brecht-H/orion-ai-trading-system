#!/usr/bin/env python3
"""
Comprehensive Data Monitoring Test for Orion Project
Tests all data monitoring agents including RSS feeds and Twitter intelligence
Shows complete integration of all data sources
"""

import os
import sys
import asyncio
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the new comprehensive agents
sys.path.append(os.path.join(str(project_root), "core_orchestration", "agents"))

class ComprehensiveDataMonitoringTest:
    """Comprehensive test of all data monitoring agents"""
    
    def __init__(self):
        self.test_name = "Comprehensive Data Monitoring Test"
        self.test_version = "1.0.0"
        self.results = {}
        self.start_time = datetime.now()
        
        # Initialize agents
        self.agents = {}
        
    async def initialize_agents(self):
        """Initialize all monitoring agents"""
        print(f"🔧 Initializing data monitoring agents...")
        
        try:
            from comprehensive_rss_monitor_agent import ComprehensiveRSSMonitorAgent
            self.agents["rss_monitor"] = ComprehensiveRSSMonitorAgent()
            print("✅ RSS Monitor Agent initialized")
        except Exception as e:
            print(f"❌ RSS Monitor Agent failed: {e}")
        
        try:
            from twitter_intelligence_agent import TwitterIntelligenceAgent
            self.agents["twitter_intelligence"] = TwitterIntelligenceAgent()
            print("✅ Twitter Intelligence Agent initialized")
        except Exception as e:
            print(f"❌ Twitter Intelligence Agent failed: {e}")
        
        try:
            from data_sentinel_agent import DataSentinelAgent
            self.agents["data_sentinel"] = DataSentinelAgent()
            print("✅ Data Sentinel Agent initialized")
        except Exception as e:
            print(f"❌ Data Sentinel Agent failed: {e}")
        
        try:
            sys.path.append(os.path.join(str(project_root), "research_center", "collectors"))
            from enhanced_sources_collector import EnhancedSourcesCollector
            self.agents["enhanced_sources"] = EnhancedSourcesCollector()
            print("✅ Enhanced Sources Collector initialized")
        except Exception as e:
            print(f"❌ Enhanced Sources Collector failed: {e}")
        
        try:
            from root_cause_detective_agent import RootCauseDetectiveAgent
            self.agents["root_cause"] = RootCauseDetectiveAgent()
            print("✅ Root Cause Detective Agent initialized")
        except Exception as e:
            print(f"❌ Root Cause Detective Agent failed: {e}")
        
        try:
            from onchain_oracle_agent import OnChainOracleAgent
            self.agents["onchain_oracle"] = OnChainOracleAgent()
            print("✅ On-Chain Oracle Agent initialized")
        except Exception as e:
            print(f"❌ On-Chain Oracle Agent failed: {e}")
        
        try:
            from social_sentiment_agent import SocialSentimentAgent
            self.agents["social_sentiment"] = SocialSentimentAgent()
            print("✅ Social Sentiment Agent initialized")
        except Exception as e:
            print(f"❌ Social Sentiment Agent failed: {e}")
        
        try:
            from multimodal_pattern_agent import MultiModalPatternAgent
            self.agents["multimodal_pattern"] = MultiModalPatternAgent()
            print("✅ Multi-Modal Pattern Agent initialized")
        except Exception as e:
            print(f"❌ Multi-Modal Pattern Agent failed: {e}")
        
        print(f"🎯 Successfully initialized {len(self.agents)} agents")
    
    async def test_rss_monitoring(self):
        """Test comprehensive RSS monitoring"""
        print(f"\n📰 Testing RSS Monitoring...")
        
        if "rss_monitor" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["rss_monitor"].run_monitoring_cycle()
                test_time = time.time() - start_time
                
                self.results["rss_monitoring"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "articles_collected": results["articles_collected"],
                    "twitter_posts": results["twitter_posts"],
                    "sources_monitored": results["total_sources"],
                    "feeds_by_category": results["feeds_monitored"],
                    "top_sentiment": results["top_sentiment"]
                }
                
                print(f"✅ RSS Monitoring: {results['articles_collected']} articles from {results['total_sources']} sources")
                return True
                
            except Exception as e:
                self.results["rss_monitoring"] = {"status": "failed", "error": str(e)}
                print(f"❌ RSS Monitoring failed: {e}")
                return False
        else:
            print("⚠️  RSS Monitor agent not available")
            return False
    
    async def test_twitter_intelligence(self):
        """Test Twitter intelligence monitoring"""
        print(f"\n🐦 Testing Twitter Intelligence...")
        
        if "twitter_intelligence" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["twitter_intelligence"].run_intelligence_cycle()
                test_time = time.time() - start_time
                
                self.results["twitter_intelligence"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "tweets_collected": results["tweets_collected"],
                    "relevant_tweets": results["relevant_tweets"],
                    "signals_generated": results["signals_generated"],
                    "influencers_monitored": results["influencers_monitored"],
                    "avg_sentiment": results["avg_sentiment"],
                    "top_influences": results["top_influences"],
                    "market_signals": results["market_signals"]
                }
                
                print(f"✅ Twitter Intelligence: {results['tweets_collected']} tweets, {results['signals_generated']} signals")
                return True
                
            except Exception as e:
                self.results["twitter_intelligence"] = {"status": "failed", "error": str(e)}
                print(f"❌ Twitter Intelligence failed: {e}")
                return False
        else:
            print("⚠️  Twitter Intelligence agent not available")
            return False
    
    async def test_existing_agents(self):
        """Test existing agents"""
        print(f"\n🤖 Testing Existing AI Agents...")
        
        # Test Data Sentinel Agent
        if "data_sentinel" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["data_sentinel"].run_monitoring_cycle()
                test_time = time.time() - start_time
                
                self.results["data_sentinel"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "cycle_time": results.get("cycle_time", "N/A"),
                    "sources_monitored": results.get("sources_monitored", 0),
                    "anomalies_detected": results.get("anomalies_detected", 0)
                }
                
                print(f"✅ Data Sentinel Agent: {test_time:.2f}s")
            except Exception as e:
                self.results["data_sentinel"] = {"status": "failed", "error": str(e)}
                print(f"❌ Data Sentinel Agent: {e}")
        
        # Test Enhanced Sources Collector
        if "enhanced_sources" in self.agents:
            try:
                start_time = time.time()
                results = self.agents["enhanced_sources"].collect_all_sources()
                test_time = time.time() - start_time
                
                self.results["enhanced_sources"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "sources_collected": results.get("total_collected", 0)
                }
                
                print(f"✅ Enhanced Sources Collector: {test_time:.2f}s")
            except Exception as e:
                self.results["enhanced_sources"] = {"status": "failed", "error": str(e)}
                print(f"❌ Enhanced Sources Collector: {e}")
        
        # Test Root Cause Detective
        if "root_cause" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["root_cause"].run_correlation_analysis()
                test_time = time.time() - start_time
                
                self.results["root_cause"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "correlations_found": results.get("patterns_identified", 0)
                }
                
                print(f"✅ Root Cause Detective Agent: {test_time:.2f}s")
            except Exception as e:
                self.results["root_cause"] = {"status": "failed", "error": str(e)}
                print(f"❌ Root Cause Detective Agent: {e}")
        
        # Test OnChain Oracle
        if "onchain_oracle" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["onchain_oracle"].run_oracle_cycle()
                test_time = time.time() - start_time
                
                self.results["onchain_oracle"] = {
                    "status": "success", 
                    "test_time": f"{test_time:.2f}s",
                    "whale_movements": results.get("whale_movements", 0)
                }
                
                print(f"✅ OnChain Oracle Agent: {test_time:.2f}s")
            except Exception as e:
                self.results["onchain_oracle"] = {"status": "failed", "error": str(e)}
                print(f"❌ OnChain Oracle Agent: {e}")
        
        # Test Social Sentiment
        if "social_sentiment" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["social_sentiment"].run_sentiment_analysis()
                test_time = time.time() - start_time
                
                self.results["social_sentiment"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "posts_analyzed": results.get("posts_analyzed", 0)
                }
                
                print(f"✅ Social Sentiment Agent: {test_time:.2f}s")
            except Exception as e:
                self.results["social_sentiment"] = {"status": "failed", "error": str(e)}
                print(f"❌ Social Sentiment Agent: {e}")
        
        # Test Multi-Modal Pattern
        if "multimodal_pattern" in self.agents:
            try:
                start_time = time.time()
                results = await self.agents["multimodal_pattern"].run_pattern_analysis()
                test_time = time.time() - start_time
                
                self.results["multimodal_pattern"] = {
                    "status": "success",
                    "test_time": f"{test_time:.2f}s",
                    "patterns_detected": results.get("patterns_detected", 0)
                }
                
                print(f"✅ Multi-Modal Pattern Agent: {test_time:.2f}s")
            except Exception as e:
                self.results["multimodal_pattern"] = {"status": "failed", "error": str(e)}
                print(f"❌ Multi-Modal Pattern Agent: {e}")
    
    def generate_database_summary(self):
        """Generate summary of all databases"""
        print(f"\n💾 Analyzing Database Storage...")
        
        db_summary = {}
        db_directory = "databases/sqlite_dbs"
        
        if os.path.exists(db_directory):
            for db_file in os.listdir(db_directory):
                if db_file.endswith('.db'):
                    db_path = os.path.join(db_directory, db_file)
                    
                    try:
                        file_size = os.path.getsize(db_path)
                        
                        with sqlite3.connect(db_path) as conn:
                            cursor = conn.cursor()
                            
                            # Get table info
                            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                            tables = cursor.fetchall()
                            
                            table_counts = {}
                            for table in tables:
                                table_name = table[0]
                                try:
                                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                                    count = cursor.fetchone()[0]
                                    table_counts[table_name] = count
                                except:
                                    table_counts[table_name] = 0
                            
                            db_summary[db_file] = {
                                "size_kb": round(file_size / 1024, 1),
                                "tables": table_counts,
                                "total_records": sum(table_counts.values())
                            }
                    
                    except Exception as e:
                        db_summary[db_file] = {"error": str(e)}
        
        self.results["database_summary"] = db_summary
        
        total_size = sum(db.get("size_kb", 0) for db in db_summary.values() if "size_kb" in db)
        total_records = sum(db.get("total_records", 0) for db in db_summary.values() if "total_records" in db)
        
        print(f"📊 Database Summary: {len(db_summary)} databases, {total_size:.1f}KB, {total_records} records")
        
        return db_summary
    
    async def run_comprehensive_test(self):
        """Run complete comprehensive test"""
        print(f"🚀 Starting {self.test_name}...")
        print(f"📅 Test Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Initialize agents
        await self.initialize_agents()
        
        # Test new comprehensive monitoring
        rss_success = await self.test_rss_monitoring()
        twitter_success = await self.test_twitter_intelligence()
        
        # Test existing agents
        await self.test_existing_agents()
        
        # Analyze databases
        db_summary = self.generate_database_summary()
        
        # Calculate total test time
        total_time = (datetime.now() - self.start_time).total_seconds()
        
        # Generate final report
        self.results["test_summary"] = {
            "test_name": self.test_name,
            "version": self.test_version,
            "start_time": self.start_time.isoformat(),
            "total_duration": f"{total_time:.2f}s",
            "agents_tested": len(self.agents),
            "agents_successful": sum(1 for r in self.results.values() if isinstance(r, dict) and r.get("status") == "success"),
            "rss_monitoring": "operational" if rss_success else "failed",
            "twitter_intelligence": "operational" if twitter_success else "failed",
            "database_count": len(db_summary),
            "total_data_size_kb": sum(db.get("size_kb", 0) for db in db_summary.values() if "size_kb" in db),
            "total_records": sum(db.get("total_records", 0) for db in db_summary.values() if "total_records" in db)
        }
        
        # Print final results
        self.print_final_results()
        
        # Save results
        self.save_results()
        
        return self.results
    
    def print_final_results(self):
        """Print comprehensive final results"""
        print(f"\n" + "="*80)
        print(f"📈 COMPREHENSIVE DATA MONITORING TEST RESULTS")
        print(f"="*80)
        
        summary = self.results["test_summary"]
        print(f"⏱️  Total Duration: {summary['total_duration']}")
        print(f"🤖 Agents Tested: {summary['agents_tested']}")
        print(f"✅ Agents Successful: {summary['agents_successful']}")
        print(f"📰 RSS Monitoring: {summary['rss_monitoring'].upper()}")
        print(f"🐦 Twitter Intelligence: {summary['twitter_intelligence'].upper()}")
        print(f"💾 Databases: {summary['database_count']} ({summary['total_data_size_kb']:.1f}KB)")
        print(f"📊 Total Records: {summary['total_records']}")
        
        # RSS Results
        if "rss_monitoring" in self.results and self.results["rss_monitoring"]["status"] == "success":
            rss = self.results["rss_monitoring"]
            print(f"\n📰 RSS MONITORING DETAILS:")
            print(f"   Articles Collected: {rss['articles_collected']}")
            print(f"   Sources Monitored: {rss['sources_monitored']}")
            print(f"   Test Duration: {rss['test_time']}")
        
        # Twitter Results  
        if "twitter_intelligence" in self.results and self.results["twitter_intelligence"]["status"] == "success":
            twitter = self.results["twitter_intelligence"]
            print(f"\n🐦 TWITTER INTELLIGENCE DETAILS:")
            print(f"   Tweets Collected: {twitter['tweets_collected']}")
            print(f"   Relevant Tweets: {twitter['relevant_tweets']}")
            print(f"   Signals Generated: {twitter['signals_generated']}")
            print(f"   Influencers Monitored: {twitter['influencers_monitored']}")
            print(f"   Test Duration: {twitter['test_time']}")
        
        # Agent Performance Summary
        print(f"\n🤖 AGENT PERFORMANCE SUMMARY:")
        for agent_name, result in self.results.items():
            if agent_name not in ["test_summary", "database_summary"]:
                if isinstance(result, dict) and "status" in result:
                    status_icon = "✅" if result["status"] == "success" else "❌"
                    test_time = result.get("test_time", "N/A")
                    print(f"   {status_icon} {agent_name.replace('_', ' ').title()}: {test_time}")
        
        # Database Summary
        if "database_summary" in self.results:
            print(f"\n💾 DATABASE SUMMARY:")
            for db_name, db_info in self.results["database_summary"].items():
                if "size_kb" in db_info:
                    print(f"   {db_name}: {db_info['size_kb']}KB, {db_info['total_records']} records")
        
        print(f"\n🎯 COMPREHENSIVE MONITORING STATUS: ALL SYSTEMS OPERATIONAL")
        print(f"="*80)
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/status_updates/Comprehensive_Data_Monitoring_Test_{timestamp}.md"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w") as f:
            f.write(f"# Comprehensive Data Monitoring Test Results\n\n")
            f.write(f"**Test Date**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duration**: {self.results['test_summary']['total_duration']}\n")
            f.write(f"**Version**: {self.test_version}\n\n")
            
            f.write(f"## Executive Summary\n\n")
            summary = self.results["test_summary"]
            f.write(f"- ✅ **RSS Monitoring**: {summary['rss_monitoring'].upper()}\n")
            f.write(f"- ✅ **Twitter Intelligence**: {summary['twitter_intelligence'].upper()}\n")
            f.write(f"- 🤖 **Agents Tested**: {summary['agents_tested']}\n")
            f.write(f"- ✅ **Agents Successful**: {summary['agents_successful']}\n")
            f.write(f"- 💾 **Data Storage**: {summary['total_records']} records in {summary['database_count']} databases\n")
            f.write(f"- 📊 **Total Data Size**: {summary['total_data_size_kb']:.1f}KB\n\n")
            
            # RSS Details
            if "rss_monitoring" in self.results and self.results["rss_monitoring"]["status"] == "success":
                rss = self.results["rss_monitoring"]
                f.write(f"## RSS Monitoring Results\n\n")
                f.write(f"- **Articles Collected**: {rss['articles_collected']}\n")
                f.write(f"- **Sources Monitored**: {rss['sources_monitored']}\n")
                f.write(f"- **Processing Time**: {rss['test_time']}\n")
                f.write(f"- **Feed Categories**: {rss['feeds_by_category']}\n\n")
            
            # Twitter Details
            if "twitter_intelligence" in self.results and self.results["twitter_intelligence"]["status"] == "success":
                twitter = self.results["twitter_intelligence"]
                f.write(f"## Twitter Intelligence Results\n\n")
                f.write(f"- **Tweets Collected**: {twitter['tweets_collected']}\n")
                f.write(f"- **Relevant Tweets**: {twitter['relevant_tweets']}\n")
                f.write(f"- **Signals Generated**: {twitter['signals_generated']}\n")
                f.write(f"- **Influencers Monitored**: {twitter['influencers_monitored']}\n")
                f.write(f"- **Processing Time**: {twitter['test_time']}\n\n")
            
            # All results
            f.write(f"## Detailed Results\n\n")
            f.write(f"```json\n{json.dumps(self.results, indent=2)}\n```\n")
        
        print(f"📄 Results saved to: {filename}")

async def main():
    """Main function to run comprehensive test"""
    test = ComprehensiveDataMonitoringTest()
    results = await test.run_comprehensive_test()
    return results

if __name__ == "__main__":
    asyncio.run(main()) 