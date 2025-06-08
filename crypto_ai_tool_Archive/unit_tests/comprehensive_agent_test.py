#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE AGENT TESTING FRAMEWORK
Complete testing suite for all AI agents and data sources
"""

import asyncio
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import all agents
from core_orchestration.agents.data_sentinel_agent import DataSentinelAgent
from core_orchestration.agents.root_cause_detective_agent import RootCauseDetectiveAgent
from core_orchestration.agents.onchain_oracle_agent import OnChainOracleAgent
from core_orchestration.agents.social_sentiment_agent import SocialSentimentAgent
from core_orchestration.agents.multimodal_pattern_agent import MultiModalPatternAgent

# Import data collectors
from research_center.collectors.enhanced_sources_collector import EnhancedSourcesCollector

class ComprehensiveAgentTester:
    """
    Comprehensive testing framework for all AI agents
    - Individual agent testing
    - Integration testing
    - Performance benchmarking
    - Data flow validation
    """
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
        # Initialize all agents
        self.agents = {
            "data_sentinel": DataSentinelAgent(),
            "root_cause_detective": RootCauseDetectiveAgent(),
            "onchain_oracle": OnChainOracleAgent(),
            "social_sentiment": SocialSentimentAgent(),
            "multimodal_pattern": MultiModalPatternAgent()
        }
        
        # Initialize data collector
        self.data_collector = EnhancedSourcesCollector()
        
        print("🧪 Comprehensive Agent Testing Framework Initialized")
        print(f"📊 Testing {len(self.agents)} AI agents")
        print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all comprehensive tests"""
        print("🚀 Starting comprehensive agent testing...")
        
        # Phase 1: Data Collection Testing
        print("\n📡 PHASE 1: Data Collection Testing")
        data_collection_results = await self.test_data_collection()
        
        # Phase 2: Individual Agent Testing
        print("\n🤖 PHASE 2: Individual Agent Testing")
        individual_results = await self.test_individual_agents()
        
        # Phase 3: Integration Testing
        print("\n🔗 PHASE 3: Agent Integration Testing")
        integration_results = await self.test_agent_integration()
        
        # Phase 4: Performance Benchmarking
        print("\n⚡ PHASE 4: Performance Benchmarking")
        performance_results = await self.test_performance()
        
        # Phase 5: Data Flow Validation
        print("\n🌊 PHASE 5: Data Flow Validation")
        data_flow_results = await self.test_data_flows()
        
        # Compile final results
        final_results = {
            "test_duration": time.time() - self.start_time,
            "timestamp": datetime.now().isoformat(),
            "data_collection": data_collection_results,
            "individual_agents": individual_results,
            "integration": integration_results,
            "performance": performance_results,
            "data_flows": data_flow_results,
            "overall_success_rate": self.calculate_overall_success_rate(),
            "recommendations": self.generate_recommendations()
        }
        
        # Generate test report
        await self.generate_test_report(final_results)
        
        return final_results
    
    async def test_data_collection(self) -> Dict[str, Any]:
        """Test data collection capabilities"""
        print("  🔍 Testing enhanced data collection...")
        
        results = {
            "enhanced_sources": {"status": "unknown", "sources": 0, "records": 0},
            "source_diversity": {"status": "unknown", "unique_sources": 0},
            "data_quality": {"status": "unknown", "quality_score": 0.0}
        }
        
        try:
            # Test enhanced sources collector
            collection_result = await self.data_collector.run_collection_cycle()
            
            results["enhanced_sources"] = {
                "status": "success",
                "sources": collection_result.get("sources_processed", 0),
                "records": collection_result.get("total_records", 0),
                "cycle_time": collection_result.get("cycle_time", 0)
            }
            
            # Test source diversity
            unique_sources = len(set(collection_result.get("source_names", [])))
            results["source_diversity"] = {
                "status": "success" if unique_sources >= 5 else "warning",
                "unique_sources": unique_sources,
                "target": 10
            }
            
            # Test data quality
            quality_score = collection_result.get("average_quality_score", 0.0)
            results["data_quality"] = {
                "status": "success" if quality_score >= 0.7 else "warning",
                "quality_score": quality_score,
                "threshold": 0.7
            }
            
            print(f"    ✅ Enhanced sources: {results['enhanced_sources']['sources']} sources, {results['enhanced_sources']['records']} records")
            print(f"    ✅ Source diversity: {unique_sources} unique sources")
            print(f"    ✅ Data quality: {quality_score:.2f} average score")
            
        except Exception as e:
            print(f"    ❌ Data collection error: {e}")
            for key in results:
                results[key]["status"] = "error"
                results[key]["error"] = str(e)
        
        return results
    
    async def test_individual_agents(self) -> Dict[str, Any]:
        """Test each agent individually"""
        results = {}
        
        for agent_name, agent in self.agents.items():
            print(f"  🤖 Testing {agent_name} agent...")
            
            try:
                # Run agent cycle
                if hasattr(agent, 'run_monitoring_cycle'):
                    agent_result = await agent.run_monitoring_cycle()
                elif hasattr(agent, 'run_analysis_cycle'):
                    agent_result = await agent.run_analysis_cycle()
                else:
                    agent_result = {"error": "No run method found"}
                
                # Evaluate results
                cycle_time = agent_result.get("cycle_time", 0)
                success = cycle_time > 0 and cycle_time < 30  # Reasonable cycle time
                
                results[agent_name] = {
                    "status": "success" if success else "warning",
                    "cycle_time": cycle_time,
                    "results": agent_result,
                    "performance_score": self.calculate_agent_performance_score(agent_result)
                }
                
                print(f"    ✅ {agent_name}: {cycle_time:.2f}s cycle time")
                
            except Exception as e:
                print(f"    ❌ {agent_name}: {str(e)}")
                results[agent_name] = {
                    "status": "error", 
                    "error": str(e),
                    "cycle_time": 0,
                    "performance_score": 0.0
                }
        
        return results
    
    async def test_agent_integration(self) -> Dict[str, Any]:
        """Test integration between agents"""
        print("  🔗 Testing inter-agent communication...")
        
        results = {
            "data_sharing": {"status": "unknown", "shared_databases": 0},
            "coordinated_analysis": {"status": "unknown", "coordination_score": 0.0},
            "signal_consistency": {"status": "unknown", "consistency_score": 0.0}
        }
        
        try:
            # Test data sharing (check if agents can access each other's databases)
            shared_databases = 0
            database_paths = [
                "data/enhanced_sources_data.db",
                "data/root_cause_analysis.db", 
                "data/onchain_intelligence.db",
                "data/social_intelligence.db",
                "data/multimodal_patterns.db"
            ]
            
            for db_path in database_paths:
                if Path(db_path).exists():
                    shared_databases += 1
            
            results["data_sharing"] = {
                "status": "success" if shared_databases >= 3 else "warning",
                "shared_databases": shared_databases,
                "total_expected": len(database_paths)
            }
            
            # Test coordinated analysis (run multimodal pattern agent)
            try:
                multimodal_result = await self.agents["multimodal_pattern"].run_analysis_cycle()
                coordination_score = multimodal_result.get("data_sources_analyzed", 0) / 6  # 6 expected sources
                
                results["coordinated_analysis"] = {
                    "status": "success" if coordination_score >= 0.5 else "warning",
                    "coordination_score": coordination_score,
                    "sources_analyzed": multimodal_result.get("data_sources_analyzed", 0)
                }
            except Exception as e:
                results["coordinated_analysis"] = {"status": "error", "error": str(e)}
            
            # Test signal consistency (check if agents produce consistent directional signals)
            signal_directions = []
            for agent_name, agent in self.agents.items():
                try:
                    if hasattr(agent, 'run_analysis_cycle'):
                        result = await agent.run_analysis_cycle()
                        
                        # Extract directional signals
                        if "meta_recommendation" in result:
                            if "bullish" in result["meta_recommendation"].lower():
                                signal_directions.append("bullish")
                            elif "bearish" in result["meta_recommendation"].lower():
                                signal_directions.append("bearish")
                            else:
                                signal_directions.append("neutral")
                except:
                    continue
            
            if signal_directions:
                # Calculate consistency (how many agree with majority)
                from collections import Counter
                direction_counts = Counter(signal_directions)
                majority_direction = direction_counts.most_common(1)[0][0]
                consistency_score = direction_counts[majority_direction] / len(signal_directions)
                
                results["signal_consistency"] = {
                    "status": "success" if consistency_score >= 0.6 else "warning",
                    "consistency_score": consistency_score,
                    "signal_directions": signal_directions,
                    "majority_direction": majority_direction
                }
            
            print(f"    ✅ Data sharing: {shared_databases} databases available")
            print(f"    ✅ Coordination score: {results['coordinated_analysis'].get('coordination_score', 0):.2f}")
            print(f"    ✅ Signal consistency: {results['signal_consistency'].get('consistency_score', 0):.2f}")
            
        except Exception as e:
            print(f"    ❌ Integration testing error: {e}")
            for key in results:
                results[key]["status"] = "error"
                results[key]["error"] = str(e)
        
        return results
    
    async def test_performance(self) -> Dict[str, Any]:
        """Test performance benchmarks"""
        print("  ⚡ Testing performance benchmarks...")
        
        results = {
            "response_times": {},
            "throughput": {},
            "resource_usage": {},
            "scalability": {}
        }
        
        # Test response times
        for agent_name, agent in self.agents.items():
            try:
                start_time = time.time()
                
                if hasattr(agent, 'run_monitoring_cycle'):
                    await agent.run_monitoring_cycle()
                elif hasattr(agent, 'run_analysis_cycle'):
                    await agent.run_analysis_cycle()
                
                response_time = time.time() - start_time
                
                results["response_times"][agent_name] = {
                    "time": response_time,
                    "status": "excellent" if response_time < 5 else "good" if response_time < 15 else "slow"
                }
                
            except Exception as e:
                results["response_times"][agent_name] = {"status": "error", "error": str(e)}
        
        # Test data collector throughput
        try:
            start_time = time.time()
            collection_result = await self.data_collector.run_collection_cycle()
            collection_time = time.time() - start_time
            
            records_per_second = collection_result.get("total_records", 0) / max(collection_time, 1)
            
            results["throughput"]["data_collection"] = {
                "records_per_second": records_per_second,
                "total_records": collection_result.get("total_records", 0),
                "collection_time": collection_time,
                "status": "excellent" if records_per_second > 10 else "good" if records_per_second > 5 else "slow"
            }
            
        except Exception as e:
            results["throughput"]["data_collection"] = {"status": "error", "error": str(e)}
        
        # Resource usage estimation (simplified)
        results["resource_usage"] = {
            "estimated_cpu": "low",  # Mostly I/O bound operations
            "estimated_memory": "medium",  # SQLite databases and data processing
            "estimated_network": "low",  # Free APIs with rate limits
            "cost_estimate": "€0-5/month"  # Mostly free resources
        }
        
        # Scalability assessment
        total_agents = len(self.agents)
        avg_response_time = sum(r.get("time", 30) for r in results["response_times"].values()) / max(total_agents, 1)
        
        results["scalability"] = {
            "current_agents": total_agents,
            "avg_response_time": avg_response_time,
            "estimated_max_agents": min(20, int(60 / avg_response_time)),  # Based on 1-minute cycles
            "bottlenecks": ["API rate limits", "Database I/O"] if avg_response_time > 10 else ["API rate limits"]
        }
        
        print(f"    ⚡ Average response time: {avg_response_time:.2f}s")
        print(f"    📊 Data throughput: {results['throughput'].get('data_collection', {}).get('records_per_second', 0):.1f} records/s")
        print(f"    🔧 Estimated scalability: {results['scalability']['estimated_max_agents']} agents")
        
        return results
    
    async def test_data_flows(self) -> Dict[str, Any]:
        """Test data flow integrity"""
        print("  🌊 Testing data flow integrity...")
        
        results = {
            "data_consistency": {"status": "unknown", "consistency_score": 0.0},
            "pipeline_integrity": {"status": "unknown", "pipeline_score": 0.0},
            "real_time_processing": {"status": "unknown", "latency_ms": 0}
        }
        
        try:
            # Test data consistency across databases
            consistency_checks = 0
            consistency_passes = 0
            
            # Check timestamp consistency
            database_files = [
                "data/enhanced_sources_data.db",
                "data/free_sources_data.db"
            ]
            
            for db_file in database_files:
                if Path(db_file).exists():
                    consistency_checks += 1
                    # Simple check: verify recent data exists
                    import sqlite3
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    
                    # Check for recent data (last hour)
                    recent_count = cursor.execute("""
                        SELECT COUNT(*) FROM (
                            SELECT timestamp FROM enhanced_news WHERE timestamp > ?
                            UNION ALL
                            SELECT timestamp FROM enhanced_social WHERE timestamp > ?
                            UNION ALL
                            SELECT timestamp FROM enhanced_market WHERE timestamp > ?
                        )
                    """, (time.time() - 3600, time.time() - 3600, time.time() - 3600)).fetchone()[0]
                    
                    if recent_count > 0:
                        consistency_passes += 1
                    
                    conn.close()
            
            consistency_score = consistency_passes / max(consistency_checks, 1)
            
            results["data_consistency"] = {
                "status": "success" if consistency_score >= 0.8 else "warning",
                "consistency_score": consistency_score,
                "checks_performed": consistency_checks,
                "checks_passed": consistency_passes
            }
            
            # Test pipeline integrity (data flows from collection to analysis)
            pipeline_score = 0.0
            
            # Check if data collector → agents → pattern analysis works
            try:
                # 1. Run data collection
                collection_result = await self.data_collector.run_collection_cycle()
                if collection_result.get("total_records", 0) > 0:
                    pipeline_score += 0.3
                
                # 2. Run analysis agent
                root_cause_result = await self.agents["root_cause_detective"].run_analysis_cycle()
                if root_cause_result.get("news_events_analyzed", 0) > 0:
                    pipeline_score += 0.3
                
                # 3. Run multimodal analysis
                multimodal_result = await self.agents["multimodal_pattern"].run_analysis_cycle()
                if multimodal_result.get("data_sources_analyzed", 0) > 0:
                    pipeline_score += 0.4
                
            except Exception as e:
                print(f"    ⚠️ Pipeline integrity test error: {e}")
            
            results["pipeline_integrity"] = {
                "status": "success" if pipeline_score >= 0.8 else "warning",
                "pipeline_score": pipeline_score,
                "stages_working": int(pipeline_score * 10) // 3
            }
            
            # Test real-time processing latency
            start_time = time.time()
            
            # Simulate real-time data processing
            await self.data_collector.run_collection_cycle()
            
            latency_ms = (time.time() - start_time) * 1000
            
            results["real_time_processing"] = {
                "status": "excellent" if latency_ms < 5000 else "good" if latency_ms < 15000 else "slow",
                "latency_ms": latency_ms,
                "target_ms": 10000
            }
            
            print(f"    ✅ Data consistency: {consistency_score:.2f}")
            print(f"    ✅ Pipeline integrity: {pipeline_score:.2f}")
            print(f"    ✅ Processing latency: {latency_ms:.0f}ms")
            
        except Exception as e:
            print(f"    ❌ Data flow testing error: {e}")
            for key in results:
                results[key]["status"] = "error"
                results[key]["error"] = str(e)
        
        return results
    
    def calculate_agent_performance_score(self, agent_result: Dict[str, Any]) -> float:
        """Calculate performance score for an agent"""
        score = 0.0
        
        # Cycle time score (faster is better, up to a point)
        cycle_time = agent_result.get("cycle_time", 30)
        if cycle_time < 5:
            score += 0.3
        elif cycle_time < 15:
            score += 0.2
        elif cycle_time < 30:
            score += 0.1
        
        # Data processing score
        data_processed = (
            agent_result.get("news_events_analyzed", 0) +
            agent_result.get("whale_transactions", 0) +
            agent_result.get("influencer_posts", 0) +
            agent_result.get("data_sources_analyzed", 0)
        )
        
        if data_processed > 10:
            score += 0.3
        elif data_processed > 5:
            score += 0.2
        elif data_processed > 0:
            score += 0.1
        
        # Output quality score
        if agent_result.get("high_impact_events", 0) > 0:
            score += 0.2
        if agent_result.get("whale_alerts", 0) > 0:
            score += 0.1
        if agent_result.get("social_signals", 0) > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate across all tests"""
        total_tests = 0
        successful_tests = 0
        
        # Count all test results
        for category, results in self.test_results.items():
            if isinstance(results, dict):
                for test_name, test_result in results.items():
                    if isinstance(test_result, dict) and "status" in test_result:
                        total_tests += 1
                        if test_result["status"] in ["success", "excellent", "good"]:
                            successful_tests += 1
        
        return successful_tests / max(total_tests, 1)
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check individual agent performance
        if hasattr(self, 'test_results') and 'individual_agents' in self.test_results:
            for agent_name, result in self.test_results['individual_agents'].items():
                if result.get('status') == 'error':
                    recommendations.append(f"Fix {agent_name} agent - currently failing")
                elif result.get('performance_score', 0) < 0.5:
                    recommendations.append(f"Optimize {agent_name} agent performance")
        
        # Check data collection
        if hasattr(self, 'test_results') and 'data_collection' in self.test_results:
            data_results = self.test_results['data_collection']
            if data_results.get('source_diversity', {}).get('unique_sources', 0) < 5:
                recommendations.append("Add more diverse data sources")
            if data_results.get('data_quality', {}).get('quality_score', 0) < 0.7:
                recommendations.append("Improve data quality validation")
        
        # Check integration
        if hasattr(self, 'test_results') and 'integration' in self.test_results:
            integration_results = self.test_results['integration']
            if integration_results.get('signal_consistency', {}).get('consistency_score', 0) < 0.6:
                recommendations.append("Improve signal consistency across agents")
        
        # Generic recommendations
        if not recommendations:
            recommendations = [
                "System performing well - continue monitoring",
                "Consider adding more data sources for improved coverage",
                "Monitor performance metrics regularly"
            ]
        
        return recommendations
    
    async def generate_test_report(self, results: Dict[str, Any]):
        """Generate comprehensive test report"""
        report_path = Path("reports/performance") / f"Agent_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""# 🧪 COMPREHENSIVE AGENT TEST REPORT

**Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Test Duration**: {results['test_duration']:.2f} seconds  
**Overall Success Rate**: {results.get('overall_success_rate', 0):.1%}  

## 📊 Test Summary

### 📡 Data Collection
- **Enhanced Sources**: {results['data_collection']['enhanced_sources']['sources']} sources processed
- **Records Collected**: {results['data_collection']['enhanced_sources']['records']} records
- **Source Diversity**: {results['data_collection']['source_diversity']['unique_sources']} unique sources
- **Data Quality**: {results['data_collection']['data_quality']['quality_score']:.2f}/1.0

### 🤖 Individual Agents
"""
        
        for agent_name, agent_result in results['individual_agents'].items():
            status = agent_result.get('status', 'unknown')
            cycle_time = agent_result.get('cycle_time', 0)
            performance = agent_result.get('performance_score', 0)
            
            report += f"- **{agent_name.title()}**: {status.upper()} ({cycle_time:.2f}s, {performance:.2f} score)\n"
        
        report += f"""
### 🔗 Integration Testing
- **Data Sharing**: {results['integration']['data_sharing']['shared_databases']} databases available
- **Coordination Score**: {results['integration']['coordinated_analysis'].get('coordination_score', 0):.2f}/1.0
- **Signal Consistency**: {results['integration']['signal_consistency'].get('consistency_score', 0):.2f}/1.0

### ⚡ Performance Benchmarks
- **Average Response Time**: {sum(r.get('time', 0) for r in results['performance']['response_times'].values()) / max(len(results['performance']['response_times']), 1):.2f}s
- **Data Throughput**: {results['performance']['throughput'].get('data_collection', {}).get('records_per_second', 0):.1f} records/second
- **Estimated Scalability**: {results['performance']['scalability']['estimated_max_agents']} max agents

### 🌊 Data Flow Integrity
- **Data Consistency**: {results['data_flows']['data_consistency']['consistency_score']:.2f}/1.0
- **Pipeline Integrity**: {results['data_flows']['pipeline_integrity']['pipeline_score']:.2f}/1.0
- **Processing Latency**: {results['data_flows']['real_time_processing']['latency_ms']:.0f}ms

## 💡 Recommendations

"""
        
        for i, recommendation in enumerate(results['recommendations'], 1):
            report += f"{i}. {recommendation}\n"
        
        report += f"""
## 📈 System Health Status

**Overall Assessment**: {'🟢 HEALTHY' if results.get('overall_success_rate', 0) > 0.8 else '🟡 NEEDS ATTENTION' if results.get('overall_success_rate', 0) > 0.6 else '🔴 CRITICAL ISSUES'}

**Next Test Recommended**: {datetime.now().strftime('%Y-%m-%d')} (daily testing recommended)

---
*Generated by Comprehensive Agent Testing Framework*
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Test report generated: {report_path}")

async def main():
    """Run comprehensive agent testing"""
    print("🧪 ORION PROJECT - COMPREHENSIVE AGENT TESTING")
    print("=" * 80)
    
    tester = ComprehensiveAgentTester()
    
    try:
        results = await tester.run_comprehensive_tests()
        
        print("\n" + "=" * 80)
        print("🎯 FINAL TEST RESULTS")
        print("=" * 80)
        print(f"⏱️  Total Test Duration: {results['test_duration']:.2f} seconds")
        print(f"📊 Overall Success Rate: {results.get('overall_success_rate', 0):.1%}")
        print(f"🤖 Agents Tested: {len(results['individual_agents'])}")
        print(f"📡 Data Sources: {results['data_collection']['source_diversity']['unique_sources']}")
        
        # Success/failure summary
        successful_agents = sum(1 for r in results['individual_agents'].values() if r.get('status') == 'success')
        print(f"✅ Successful Agents: {successful_agents}/{len(results['individual_agents'])}")
        
        if results.get('overall_success_rate', 0) > 0.8:
            print("🎉 SYSTEM STATUS: HEALTHY - All agents operational!")
        elif results.get('overall_success_rate', 0) > 0.6:
            print("⚠️  SYSTEM STATUS: NEEDS ATTENTION - Some agents need optimization")
        else:
            print("🚨 SYSTEM STATUS: CRITICAL ISSUES - Immediate attention required")
        
        print("\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"   {i}. {rec}")
        
        return results
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main()) 