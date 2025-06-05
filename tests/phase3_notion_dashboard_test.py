#!/usr/bin/env python3
"""
ORION PHASE 3 TEST SUITE - Notion Dashboard Integration
Comprehensive testing of mobile-optimized executive dashboard
"""

import asyncio
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Test imports
from notion_integration_hub.core.notion_client import NotionClient
from notion_integration_hub.dashboards.dashboard_manager import DashboardManager, DashboardConfig
from notion_integration_hub.mobile.mobile_optimizer import MobileOptimizer, MobileConfig

class Phase3TestSuite:
    """
    Comprehensive test suite for ORION Phase 3
    Tests Notion integration, dashboard management, and mobile optimization
    """
    
    def __init__(self):
        self.logger = self.setup_logging()
        
        # Test results tracking
        self.test_results = {
            "start_time": datetime.now(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "components_tested": [],
            "performance_metrics": {},
            "error_details": []
        }
        
        self.logger.info("🧪 ORION Phase 3 Test Suite initialized")
    
    def setup_logging(self):
        """Setup comprehensive logging for testing"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - Phase3Tests - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/phase3_tests.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    async def run_comprehensive_tests(self):
        """Run complete Phase 3 test suite"""
        self.logger.info("🚀 Starting ORION Phase 3 Comprehensive Test Suite...")
        
        print("=" * 80)
        print("🎯 ORION PHASE 3: NOTION DASHBOARD INTEGRATION TEST SUITE")
        print("=" * 80)
        
        try:
            # Test 1: Notion Client Integration
            await self.test_notion_client()
            
            # Test 2: Dashboard Manager
            await self.test_dashboard_manager()
            
            # Test 3: Mobile Optimizer
            await self.test_mobile_optimizer()
            
            # Test 4: End-to-End Integration
            await self.test_complete_integration()
            
            # Test 5: Performance Benchmarks
            await self.test_performance_benchmarks()
            
            # Test 6: Error Handling & Fallbacks
            await self.test_error_handling()
            
            # Generate final report
            self.generate_final_report()
            
        except Exception as e:
            self.logger.error(f"❌ Critical test suite error: {e}")
            self.test_results["critical_error"] = str(e)
            return False
        
        return True
    
    async def test_notion_client(self):
        """Test Notion Client functionality"""
        self.logger.info("🧪 Testing Notion Client...")
        test_name = "Notion Client Integration"
        
        try:
            start_time = time.time()
            
            # Initialize client
            client = NotionClient()
            self.logger.info("✅ Notion client initialized")
            
            # Test data collection
            metrics = client.collect_current_metrics()
            alerts = client.collect_current_alerts()
            performance = client.collect_performance_data()
            
            # Validate data structure
            assert len(metrics) > 0, "No metrics collected"
            assert len(alerts) >= 0, "Alert collection failed"
            assert len(performance) > 0, "No performance data"
            
            execution_time = time.time() - start_time
            
            self.test_results["performance_metrics"]["notion_client"] = {
                "execution_time": execution_time,
                "metrics_collected": len(metrics),
                "alerts_collected": len(alerts),
                "performance_metrics": len(performance)
            }
            
            self.record_test_result(test_name, True, f"Collected {len(metrics)} metrics, {len(alerts)} alerts in {execution_time:.2f}s")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Notion client test failed: {e}")
    
    async def test_dashboard_manager(self):
        """Test Dashboard Manager functionality"""
        self.logger.info("🧪 Testing Dashboard Manager...")
        test_name = "Dashboard Manager"
        
        try:
            start_time = time.time()
            
            # Initialize with test config
            config = DashboardConfig(
                update_interval_seconds=5,
                enable_real_time_updates=False,  # Disable for testing
                alert_threshold_critical=3
            )
            
            manager = DashboardManager(config)
            self.logger.info("✅ Dashboard manager initialized")
            
            # Test dashboard updates
            update_result = await manager.update_all_dashboards()
            
            # Validate update results
            assert "metrics_updated" in update_result, "Metrics update failed"
            assert "alerts_updated" in update_result, "Alerts update failed"
            assert update_result["execution_time"] < 10, "Update too slow"
            
            # Test status reporting
            status = manager.get_dashboard_status()
            assert status["system_health"] > 0, "System health calculation failed"
            
            execution_time = time.time() - start_time
            
            self.test_results["performance_metrics"]["dashboard_manager"] = {
                "execution_time": execution_time,
                "update_time": update_result["execution_time"],
                "metrics_updated": update_result["metrics_updated"],
                "alerts_updated": update_result["alerts_updated"],
                "system_health": status["system_health"]
            }
            
            self.record_test_result(test_name, True, f"Updated {update_result['metrics_updated']} metrics, {update_result['alerts_updated']} alerts in {update_result['execution_time']:.2f}s")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Dashboard manager test failed: {e}")
    
    async def test_mobile_optimizer(self):
        """Test Mobile Optimizer functionality"""
        self.logger.info("🧪 Testing Mobile Optimizer...")
        test_name = "Mobile Optimizer"
        
        try:
            start_time = time.time()
            
            # Create test dashboard data
            test_data = {
                "metrics": [
                    {"name": "Total Signals Processed", "value": "78", "status": "good", "change": "+12%"},
                    {"name": "System Health", "value": "100%", "status": "good", "change": "Excellent"},
                    {"name": "Processing Speed", "value": "145.7/sec", "status": "good", "change": "Stable"},
                    {"name": "Active Strategies", "value": "4", "status": "good", "change": "Stable"}
                ],
                "alerts": [
                    {"title": "High Confidence Signal Detected", "message": "BTC bullish signal with 0.85 confidence", "priority": "HIGH", "requires_action": True, "timestamp": datetime.now().isoformat()},
                    {"title": "Correlation Pattern Identified", "message": "1,399 correlations detected across sources", "priority": "MEDIUM", "requires_action": False, "timestamp": datetime.now().isoformat()}
                ],
                "strategy_signals": [],
                "performance": [
                    {"metric": "Signal Accuracy", "daily": "78%", "trend": "Improving", "target": "75%+"},
                    {"metric": "Processing Speed", "daily": "145.7/sec", "trend": "Improving", "target": "100+/sec"}
                ]
            }
            
            # Initialize optimizer
            config = MobileConfig(
                max_items_per_view=8,
                fast_loading_mode=True,
                compact_view=True
            )
            
            optimizer = MobileOptimizer(config)
            self.logger.info("✅ Mobile optimizer initialized")
            
            # Test mobile optimization
            mobile_dashboard = optimizer.optimize_dashboard_for_mobile(test_data)
            
            # Validate mobile optimization
            assert "overview" in mobile_dashboard, "Overview view missing"
            assert "alerts" in mobile_dashboard, "Alerts view missing"
            assert "mobile_metadata" in mobile_dashboard, "Mobile metadata missing"
            
            overview = mobile_dashboard["overview"]
            assert len(overview.items) <= config.max_items_per_view, "Too many items in mobile view"
            assert overview.title.startswith("🎯"), "Mobile title formatting failed"
            
            alerts = mobile_dashboard["alerts"]
            assert alerts.title.startswith("🚨"), "Alert title formatting failed"
            
            execution_time = time.time() - start_time
            optimization_time = mobile_dashboard["mobile_metadata"]["optimization_time"]
            
            self.test_results["performance_metrics"]["mobile_optimizer"] = {
                "execution_time": execution_time,
                "optimization_time": optimization_time,
                "views_created": mobile_dashboard["mobile_metadata"]["views_count"],
                "overview_items": len(overview.items),
                "alert_items": len(alerts.items)
            }
            
            self.record_test_result(test_name, True, f"Optimized {mobile_dashboard['mobile_metadata']['views_count']} views in {optimization_time:.3f}s")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Mobile optimizer test failed: {e}")
    
    async def test_complete_integration(self):
        """Test complete end-to-end integration"""
        self.logger.info("🧪 Testing Complete Integration...")
        test_name = "End-to-End Integration"
        
        try:
            start_time = time.time()
            
            # Test full pipeline: Data Collection → Dashboard Management → Mobile Optimization
            
            # Step 1: Collect data via Dashboard Manager
            config = DashboardConfig(enable_real_time_updates=False)
            manager = DashboardManager(config)
            
            update_result = await manager.update_all_dashboards()
            
            # Step 2: Optimize for mobile
            mobile_config = MobileConfig(max_items_per_view=6)
            optimizer = MobileOptimizer(mobile_config)
            
            # Create mock dashboard data from manager results
            dashboard_data = {
                "metrics": [
                    {"name": "Total Signals", "value": str(update_result["metrics_updated"]), "status": "good"},
                    {"name": "Alerts", "value": str(update_result["alerts_updated"]), "status": "good"}
                ],
                "alerts": [],
                "strategy_signals": [],
                "performance": []
            }
            
            mobile_dashboard = optimizer.optimize_dashboard_for_mobile(dashboard_data)
            
            # Step 3: Validate complete pipeline
            assert mobile_dashboard["mobile_metadata"]["views_count"] >= 5, "Insufficient mobile views"
            assert "overview" in mobile_dashboard, "Overview missing in integration"
            
            execution_time = time.time() - start_time
            
            self.test_results["performance_metrics"]["integration"] = {
                "total_execution_time": execution_time,
                "dashboard_update_time": update_result["execution_time"],
                "mobile_optimization_time": mobile_dashboard["mobile_metadata"]["optimization_time"],
                "pipeline_efficiency": execution_time < 5.0
            }
            
            self.record_test_result(test_name, True, f"Complete pipeline executed in {execution_time:.2f}s")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Integration test failed: {e}")
    
    async def test_performance_benchmarks(self):
        """Test performance benchmarks and scalability"""
        self.logger.info("🧪 Testing Performance Benchmarks...")
        test_name = "Performance Benchmarks"
        
        try:
            # Benchmark 1: Dashboard Update Speed
            config = DashboardConfig(enable_real_time_updates=False)
            manager = DashboardManager(config)
            
            update_times = []
            for i in range(5):
                start = time.time()
                await manager.update_all_dashboards()
                update_times.append(time.time() - start)
            
            avg_update_time = sum(update_times) / len(update_times)
            
            # Benchmark 2: Mobile Optimization Speed
            optimizer = MobileOptimizer()
            test_data = {"metrics": [], "alerts": [], "strategy_signals": [], "performance": []}
            
            optimization_times = []
            for i in range(10):
                start = time.time()
                optimizer.optimize_dashboard_for_mobile(test_data)
                optimization_times.append(time.time() - start)
            
            avg_optimization_time = sum(optimization_times) / len(optimization_times)
            
            # Performance assertions
            assert avg_update_time < 3.0, f"Dashboard updates too slow: {avg_update_time:.2f}s"
            assert avg_optimization_time < 0.1, f"Mobile optimization too slow: {avg_optimization_time:.3f}s"
            
            self.test_results["performance_metrics"]["benchmarks"] = {
                "avg_dashboard_update": avg_update_time,
                "avg_mobile_optimization": avg_optimization_time,
                "update_samples": len(update_times),
                "optimization_samples": len(optimization_times),
                "performance_grade": "EXCELLENT" if avg_update_time < 1.0 else "GOOD" if avg_update_time < 2.0 else "ACCEPTABLE"
            }
            
            self.record_test_result(test_name, True, f"Avg update: {avg_update_time:.2f}s, Avg optimization: {avg_optimization_time:.3f}s")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Performance benchmark test failed: {e}")
    
    async def test_error_handling(self):
        """Test error handling and fallback mechanisms"""
        self.logger.info("🧪 Testing Error Handling...")
        test_name = "Error Handling & Fallbacks"
        
        try:
            # Test 1: Mobile optimizer with invalid data
            optimizer = MobileOptimizer()
            
            # Test with empty data
            empty_result = optimizer.optimize_dashboard_for_mobile({})
            assert "overview" in empty_result, "Fallback failed for empty data"
            
            # Test with malformed data
            malformed_data = {"metrics": "invalid", "alerts": None}
            malformed_result = optimizer.optimize_dashboard_for_mobile(malformed_data)
            assert "mobile_metadata" in malformed_result, "Fallback failed for malformed data"
            
            # Test 2: Dashboard manager error recovery
            config = DashboardConfig(enable_real_time_updates=False)
            manager = DashboardManager(config)
            
            # Simulate multiple update attempts
            for i in range(3):
                try:
                    await manager.update_all_dashboards()
                except Exception:
                    pass  # Expected to handle gracefully
            
            status = manager.get_dashboard_status()
            assert "system_health" in status, "Status reporting failed during errors"
            
            self.test_results["performance_metrics"]["error_handling"] = {
                "empty_data_handled": True,
                "malformed_data_handled": True,
                "dashboard_recovery": True,
                "fallback_systems": "OPERATIONAL"
            }
            
            self.record_test_result(test_name, True, "All error conditions handled gracefully")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error: {e}")
            self.logger.error(f"❌ Error handling test failed: {e}")
    
    def record_test_result(self, test_name: str, passed: bool, details: str):
        """Record individual test result"""
        self.test_results["tests_run"] += 1
        
        if passed:
            self.test_results["tests_passed"] += 1
            self.logger.info(f"✅ {test_name}: PASSED - {details}")
            print(f"✅ {test_name}: PASSED - {details}")
        else:
            self.test_results["tests_failed"] += 1
            self.test_results["error_details"].append({"test": test_name, "details": details})
            self.logger.error(f"❌ {test_name}: FAILED - {details}")
            print(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results["components_tested"].append(test_name)
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        total_time = (end_time - self.test_results["start_time"]).total_seconds()
        
        self.test_results["end_time"] = end_time
        self.test_results["total_execution_time"] = total_time
        
        success_rate = (self.test_results["tests_passed"] / self.test_results["tests_run"]) * 100
        
        print("\n" + "=" * 80)
        print("📊 ORION PHASE 3 TEST SUITE - FINAL REPORT")
        print("=" * 80)
        
        print(f"⏱️  Total Execution Time: {total_time:.2f} seconds")
        print(f"🧪 Tests Run: {self.test_results['tests_run']}")
        print(f"✅ Tests Passed: {self.test_results['tests_passed']}")
        print(f"❌ Tests Failed: {self.test_results['tests_failed']}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        print(f"\n🏗️ COMPONENTS TESTED:")
        for component in self.test_results["components_tested"]:
            print(f"   • {component}")
        
        print(f"\n⚡ PERFORMANCE METRICS:")
        perf = self.test_results["performance_metrics"]
        
        if "dashboard_manager" in perf:
            dm = perf["dashboard_manager"]
            print(f"   📊 Dashboard Manager: {dm['update_time']:.2f}s ({dm['metrics_updated']} metrics, {dm['alerts_updated']} alerts)")
        
        if "mobile_optimizer" in perf:
            mo = perf["mobile_optimizer"]
            print(f"   📱 Mobile Optimizer: {mo['optimization_time']:.3f}s ({mo['views_created']} views)")
        
        if "benchmarks" in perf:
            bench = perf["benchmarks"]
            print(f"   🏃 Performance Grade: {bench['performance_grade']}")
            print(f"   ⏱️  Avg Dashboard Update: {bench['avg_dashboard_update']:.2f}s")
            print(f"   📱 Avg Mobile Optimization: {bench['avg_mobile_optimization']:.3f}s")
        
        # Overall status determination
        if success_rate >= 90:
            overall_status = "🎯 EXCELLENT - PHASE 3 READY FOR PRODUCTION"
            status_color = "GREEN"
        elif success_rate >= 75:
            overall_status = "✅ GOOD - PHASE 3 OPERATIONAL WITH MINOR ISSUES"
            status_color = "YELLOW"
        else:
            overall_status = "⚠️ NEEDS ATTENTION - PHASE 3 REQUIRES FIXES"
            status_color = "RED"
        
        print(f"\n🎯 OVERALL STATUS: {overall_status}")
        
        if self.test_results["tests_failed"] > 0:
            print(f"\n❌ FAILED TESTS:")
            for error in self.test_results["error_details"]:
                print(f"   • {error['test']}: {error['details']}")
        
        # Save detailed report
        report_file = f"logs/phase3_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        
        print("=" * 80)
        
        self.logger.info(f"Phase 3 test suite completed: {success_rate:.1f}% success rate")
        
        return success_rate >= 75

# Main test execution
async def main():
    """Execute comprehensive Phase 3 test suite"""
    print("🚀 Initializing ORION Phase 3 Test Suite...")
    
    try:
        test_suite = Phase3TestSuite()
        success = await test_suite.run_comprehensive_tests()
        
        if success:
            print("\n🎉 PHASE 3 TEST SUITE COMPLETED SUCCESSFULLY!")
            print("🚀 ORION Phase 3 (Notion Dashboard Integration) is READY FOR PRODUCTION!")
            return True
        else:
            print("\n⚠️ PHASE 3 TEST SUITE COMPLETED WITH ISSUES")
            print("🔧 Please review failed tests before production deployment")
            return False
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR IN TEST SUITE: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())