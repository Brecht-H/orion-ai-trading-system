#!/usr/bin/env python3
"""
Week 2 Enhancements Testing Suite
Comprehensive testing of correlation analysis, pattern recognition, backtesting, and signal generation
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import sqlite3
import pandas as pd
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

class Week2EnhancementsTester:
    """
    Comprehensive testing suite for Week 2 enhancements
    """
    
    def __init__(self):
        self.project_root = project_root
        self.test_results = {
            'correlation_analysis': {'status': 'pending', 'details': {}},
            'pattern_recognition': {'status': 'pending', 'details': {}},
            'backtesting': {'status': 'pending', 'details': {}},
            'signal_generation': {'status': 'pending', 'details': {}},
            'orchestration': {'status': 'pending', 'details': {}},
            'data_integration': {'status': 'pending', 'details': {}}
        }
        
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive testing of all Week 2 enhancements
        """
        print("🧪 Starting Week 2 Enhancements Testing Suite")
        print("=" * 60)
        
        # Test 1: Correlation Analysis
        await self.test_correlation_analysis()
        
        # Test 2: Pattern Recognition
        await self.test_pattern_recognition()
        
        # Test 3: Backtesting Framework
        await self.test_backtesting_framework()
        
        # Test 4: Unified Signal Generation
        await self.test_signal_generation()
        
        # Test 5: Data Integration
        await self.test_data_integration()
        
        # Test 6: Enhanced Orchestration
        await self.test_enhanced_orchestration()
        
        # Generate test report
        report = await self.generate_test_report()
        
        return report
    
    async def test_correlation_analysis(self):
        """Test correlation analysis functionality"""
        print("\n🔍 Testing Correlation Analysis...")
        
        try:
            # Test if correlation engine can be imported
            try:
                from research_center.analyzers.correlation_engine import AdvancedCorrelationEngine
                print("   ✅ Correlation engine import successful")
                import_success = True
            except ImportError as e:
                print(f"   ❌ Correlation engine import failed: {e}")
                import_success = False
            
            if import_success:
                # Test correlation engine initialization
                try:
                    engine = AdvancedCorrelationEngine()
                    print("   ✅ Correlation engine initialization successful")
                    init_success = True
                except Exception as e:
                    print(f"   ❌ Correlation engine initialization failed: {e}")
                    init_success = False
                
                if init_success:
                    # Test correlation analysis execution
                    try:
                        results = await engine.run_comprehensive_correlation_analysis()
                        
                        # Validate results structure
                        required_keys = ['timestamp', 'new_patterns_discovered', 'signals_generated', 
                                       'market_regime', 'data_quality_score']
                        
                        validation_success = all(key in results for key in required_keys)
                        
                        if validation_success:
                            print("   ✅ Correlation analysis execution successful")
                            print(f"      Patterns discovered: {results.get('new_patterns_discovered', 0)}")
                            print(f"      Signals generated: {results.get('signals_generated', 0)}")
                            print(f"      Data quality: {results.get('data_quality_score', 0):.2f}")
                            
                            self.test_results['correlation_analysis'] = {
                                'status': 'passed',
                                'details': {
                                    'patterns_discovered': results.get('new_patterns_discovered', 0),
                                    'signals_generated': results.get('signals_generated', 0),
                                    'data_quality_score': results.get('data_quality_score', 0),
                                    'market_regime': results.get('market_regime', {}).get('regime_type', 'unknown')
                                }
                            }
                        else:
                            print("   ❌ Correlation analysis results validation failed")
                            self.test_results['correlation_analysis']['status'] = 'failed'
                            
                    except Exception as e:
                        print(f"   ❌ Correlation analysis execution failed: {e}")
                        self.test_results['correlation_analysis']['status'] = 'failed'
                        self.test_results['correlation_analysis']['details']['error'] = str(e)
                else:
                    self.test_results['correlation_analysis']['status'] = 'failed'
            else:
                self.test_results['correlation_analysis']['status'] = 'failed'
                
        except Exception as e:
            print(f"   ❌ Correlation analysis test failed: {e}")
            self.test_results['correlation_analysis']['status'] = 'error'
            self.test_results['correlation_analysis']['details']['error'] = str(e)
    
    async def test_pattern_recognition(self):
        """Test pattern recognition functionality"""
        print("\n🎯 Testing Pattern Recognition...")
        
        try:
            # Test pattern recognition import
            try:
                from strategy_center.pattern_recognition.trading_patterns import AdvancedPatternRecognition
                print("   ✅ Pattern recognition import successful")
                import_success = True
            except ImportError as e:
                print(f"   ❌ Pattern recognition import failed: {e}")
                import_success = False
            
            if import_success:
                # Test pattern recognition initialization
                try:
                    recognizer = AdvancedPatternRecognition()
                    print("   ✅ Pattern recognition initialization successful")
                    init_success = True
                except Exception as e:
                    print(f"   ❌ Pattern recognition initialization failed: {e}")
                    init_success = False
                
                if init_success:
                    # Test pattern recognition execution
                    try:
                        results = await recognizer.run_pattern_recognition()
                        
                        # Validate results
                        required_keys = ['patterns_discovered', 'patterns_validated', 'signals_generated']
                        validation_success = all(key in results for key in required_keys)
                        
                        if validation_success:
                            print("   ✅ Pattern recognition execution successful")
                            print(f"      Patterns discovered: {results.get('patterns_discovered', 0)}")
                            print(f"      Patterns validated: {results.get('patterns_validated', 0)}")
                            print(f"      Signals generated: {results.get('signals_generated', 0)}")
                            
                            self.test_results['pattern_recognition'] = {
                                'status': 'passed',
                                'details': {
                                    'patterns_discovered': results.get('patterns_discovered', 0),
                                    'patterns_validated': results.get('patterns_validated', 0),
                                    'signals_generated': results.get('signals_generated', 0)
                                }
                            }
                        else:
                            print("   ❌ Pattern recognition results validation failed")
                            self.test_results['pattern_recognition']['status'] = 'failed'
                            
                    except Exception as e:
                        print(f"   ❌ Pattern recognition execution failed: {e}")
                        self.test_results['pattern_recognition']['status'] = 'failed'
                        self.test_results['pattern_recognition']['details']['error'] = str(e)
                else:
                    self.test_results['pattern_recognition']['status'] = 'failed'
            else:
                self.test_results['pattern_recognition']['status'] = 'failed'
                
        except Exception as e:
            print(f"   ❌ Pattern recognition test failed: {e}")
            self.test_results['pattern_recognition']['status'] = 'error'
            self.test_results['pattern_recognition']['details']['error'] = str(e)
    
    async def test_backtesting_framework(self):
        """Test backtesting framework functionality"""
        print("\n📊 Testing Backtesting Framework...")
        
        try:
            # Test backtesting import
            try:
                from strategy_center.backtesting.pattern_backtester import AdvancedPatternBacktester
                print("   ✅ Backtesting framework import successful")
                import_success = True
            except ImportError as e:
                print(f"   ❌ Backtesting framework import failed: {e}")
                import_success = False
            
            if import_success:
                # Test backtesting initialization
                try:
                    backtester = AdvancedPatternBacktester()
                    print("   ✅ Backtesting framework initialization successful")
                    init_success = True
                except Exception as e:
                    print(f"   ❌ Backtesting framework initialization failed: {e}")
                    init_success = False
                
                if init_success:
                    # Test backtesting execution (with shorter timeframe for testing)
                    try:
                        results = await backtester.run_comprehensive_backtesting(lookback_days=3)
                        
                        # Validate results
                        required_keys = ['patterns_tested', 'pattern_validation_results']
                        validation_success = all(key in results for key in required_keys)
                        
                        if validation_success:
                            print("   ✅ Backtesting execution successful")
                            print(f"      Patterns tested: {results.get('patterns_tested', 0)}")
                            print(f"      Validation results: {len(results.get('pattern_validation_results', []))}")
                            
                            self.test_results['backtesting'] = {
                                'status': 'passed',
                                'details': {
                                    'patterns_tested': results.get('patterns_tested', 0),
                                    'validation_results_count': len(results.get('pattern_validation_results', [])),
                                    'validation_period_days': results.get('validation_period_days', 0)
                                }
                            }
                        else:
                            print("   ❌ Backtesting results validation failed")
                            self.test_results['backtesting']['status'] = 'failed'
                            
                    except Exception as e:
                        print(f"   ❌ Backtesting execution failed: {e}")
                        self.test_results['backtesting']['status'] = 'failed'
                        self.test_results['backtesting']['details']['error'] = str(e)
                else:
                    self.test_results['backtesting']['status'] = 'failed'
            else:
                self.test_results['backtesting']['status'] = 'failed'
                
        except Exception as e:
            print(f"   ❌ Backtesting test failed: {e}")
            self.test_results['backtesting']['status'] = 'error'
            self.test_results['backtesting']['details']['error'] = str(e)
    
    async def test_signal_generation(self):
        """Test unified signal generation functionality"""
        print("\n🎯 Testing Unified Signal Generation...")
        
        try:
            # Test signal generation import
            try:
                from strategy_center.signal_integration.unified_signal_generator import UnifiedSignalGenerator
                print("   ✅ Signal generation import successful")
                import_success = True
            except ImportError as e:
                print(f"   ❌ Signal generation import failed: {e}")
                import_success = False
            
            if import_success:
                # Test signal generation initialization
                try:
                    generator = UnifiedSignalGenerator()
                    print("   ✅ Signal generation initialization successful")
                    init_success = True
                except Exception as e:
                    print(f"   ❌ Signal generation initialization failed: {e}")
                    init_success = False
                
                if init_success:
                    # Test signal generation execution
                    try:
                        results = await generator.generate_unified_signals()
                        
                        # Validate results
                        required_keys = ['final_signals', 'signal_quality_score', 'market_regime']
                        validation_success = all(key in results for key in required_keys)
                        
                        if validation_success:
                            print("   ✅ Signal generation execution successful")
                            print(f"      Final signals: {results.get('final_signals', 0)}")
                            print(f"      Signal quality: {results.get('signal_quality_score', 0):.2%}")
                            print(f"      Market regime: {results.get('market_regime', {}).get('regime_type', 'unknown')}")
                            
                            self.test_results['signal_generation'] = {
                                'status': 'passed',
                                'details': {
                                    'final_signals': results.get('final_signals', 0),
                                    'signal_quality_score': results.get('signal_quality_score', 0),
                                    'market_regime': results.get('market_regime', {}).get('regime_type', 'unknown'),
                                    'unified_signals_count': len(results.get('unified_signals', []))
                                }
                            }
                        else:
                            print("   ❌ Signal generation results validation failed")
                            self.test_results['signal_generation']['status'] = 'failed'
                            
                    except Exception as e:
                        print(f"   ❌ Signal generation execution failed: {e}")
                        self.test_results['signal_generation']['status'] = 'failed'
                        self.test_results['signal_generation']['details']['error'] = str(e)
                else:
                    self.test_results['signal_generation']['status'] = 'failed'
            else:
                self.test_results['signal_generation']['status'] = 'failed'
                
        except Exception as e:
            print(f"   ❌ Signal generation test failed: {e}")
            self.test_results['signal_generation']['status'] = 'error'
            self.test_results['signal_generation']['details']['error'] = str(e)
    
    async def test_data_integration(self):
        """Test data integration across all components"""
        print("\n📊 Testing Data Integration...")
        
        try:
            # Check if databases exist and are accessible
            db_paths = [
                "databases/sqlite_dbs/correlation_analysis.db",
                "databases/sqlite_dbs/trading_patterns.db", 
                "databases/sqlite_dbs/backtest_results.db",
                "databases/sqlite_dbs/unified_signals.db"
            ]
            
            accessible_dbs = 0
            for db_path in db_paths:
                try:
                    if Path(db_path).exists():
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = cursor.fetchall()
                        conn.close()
                        accessible_dbs += 1
                        print(f"   ✅ Database accessible: {db_path} ({len(tables)} tables)")
                    else:
                        print(f"   ⚠️ Database not found: {db_path}")
                except Exception as e:
                    print(f"   ❌ Database error {db_path}: {e}")
            
            # Test free sources data
            try:
                free_data_db = "databases/sqlite_dbs/free_sources_data.db"
                if Path(free_data_db).exists():
                    conn = sqlite3.connect(free_data_db)
                    
                    # Check for recent data
                    query = "SELECT COUNT(*) FROM free_data WHERE timestamp > ?"
                    cutoff = (datetime.now() - pd.Timedelta(days=1)).timestamp()
                    cursor = conn.cursor()
                    cursor.execute(query, (cutoff,))
                    recent_records = cursor.fetchone()[0]
                    conn.close()
                    
                    print(f"   ✅ Free sources data: {recent_records} recent records")
                    accessible_dbs += 1
                else:
                    print("   ⚠️ Free sources database not found")
            except Exception as e:
                print(f"   ❌ Free sources data error: {e}")
            
            # Calculate integration score
            total_expected_dbs = len(db_paths) + 1  # +1 for free sources
            integration_score = accessible_dbs / total_expected_dbs
            
            if integration_score >= 0.8:
                print(f"   ✅ Data integration successful ({integration_score:.1%})")
                self.test_results['data_integration'] = {
                    'status': 'passed',
                    'details': {
                        'accessible_databases': accessible_dbs,
                        'total_databases': total_expected_dbs,
                        'integration_score': integration_score
                    }
                }
            else:
                print(f"   ⚠️ Data integration partial ({integration_score:.1%})")
                self.test_results['data_integration'] = {
                    'status': 'partial',
                    'details': {
                        'accessible_databases': accessible_dbs,
                        'total_databases': total_expected_dbs,
                        'integration_score': integration_score
                    }
                }
                
        except Exception as e:
            print(f"   ❌ Data integration test failed: {e}")
            self.test_results['data_integration']['status'] = 'error'
            self.test_results['data_integration']['details']['error'] = str(e)
    
    async def test_enhanced_orchestration(self):
        """Test enhanced orchestration functionality"""
        print("\n🎭 Testing Enhanced Orchestration...")
        
        try:
            # Test orchestration import
            try:
                from core_orchestration.data_pipeline.enhanced_orchestrator import EnhancedTradingOrchestrator
                print("   ✅ Enhanced orchestration import successful")
                import_success = True
            except ImportError as e:
                print(f"   ❌ Enhanced orchestration import failed: {e}")
                import_success = False
            
            if import_success:
                # Test orchestration initialization
                try:
                    orchestrator = EnhancedTradingOrchestrator()
                    print("   ✅ Enhanced orchestration initialization successful")
                    init_success = True
                except Exception as e:
                    print(f"   ❌ Enhanced orchestration initialization failed: {e}")
                    init_success = False
                
                if init_success:
                    # Test orchestration execution
                    try:
                        results = await orchestrator.run_enhanced_trading_cycle()
                        
                        # Validate results
                        required_attributes = ['timestamp', 'execution_time_seconds', 'components_executed',
                                             'market_regime', 'overall_confidence']
                        
                        validation_success = all(hasattr(results, attr) for attr in required_attributes)
                        
                        if validation_success:
                            print("   ✅ Enhanced orchestration execution successful")
                            print(f"      Execution time: {results.execution_time_seconds:.2f}s")
                            print(f"      Components executed: {len(results.components_executed)}")
                            print(f"      Market regime: {results.market_regime}")
                            print(f"      Overall confidence: {results.overall_confidence:.2%}")
                            
                            self.test_results['orchestration'] = {
                                'status': 'passed',
                                'details': {
                                    'execution_time_seconds': results.execution_time_seconds,
                                    'components_executed': len(results.components_executed),
                                    'correlation_patterns_discovered': results.correlation_patterns_discovered,
                                    'unified_signals_generated': results.unified_signals_generated,
                                    'market_regime': results.market_regime,
                                    'overall_confidence': results.overall_confidence
                                }
                            }
                        else:
                            print("   ❌ Enhanced orchestration results validation failed")
                            self.test_results['orchestration']['status'] = 'failed'
                            
                    except Exception as e:
                        print(f"   ❌ Enhanced orchestration execution failed: {e}")
                        self.test_results['orchestration']['status'] = 'failed'
                        self.test_results['orchestration']['details']['error'] = str(e)
                else:
                    self.test_results['orchestration']['status'] = 'failed'
            else:
                self.test_results['orchestration']['status'] = 'failed'
                
        except Exception as e:
            print(f"   ❌ Enhanced orchestration test failed: {e}")
            self.test_results['orchestration']['status'] = 'error'
            self.test_results['orchestration']['details']['error'] = str(e)
    
    async def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        print("\n📋 Generating Test Report...")
        
        # Calculate overall success rate
        total_tests = len(self.test_results)
        passed_tests = len([test for test in self.test_results.values() if test['status'] == 'passed'])
        partial_tests = len([test for test in self.test_results.values() if test['status'] == 'partial'])
        failed_tests = len([test for test in self.test_results.values() if test['status'] == 'failed'])
        error_tests = len([test for test in self.test_results.values() if test['status'] == 'error'])
        
        success_rate = (passed_tests + partial_tests * 0.5) / total_tests if total_tests > 0 else 0
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'partial_tests': partial_tests,
                'failed_tests': failed_tests,
                'error_tests': error_tests,
                'success_rate': success_rate
            },
            'test_results': self.test_results,
            'recommendations': self.generate_recommendations(),
            'overall_assessment': self.generate_overall_assessment(success_rate)
        }
        
        # Save report to file
        report_file = f"tests/week2_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path(report_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Test report saved to: {report_file}")
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        for test_name, result in self.test_results.items():
            if result['status'] == 'failed':
                recommendations.append(f"Fix issues with {test_name.replace('_', ' ').title()}")
            elif result['status'] == 'error':
                recommendations.append(f"Investigate critical errors in {test_name.replace('_', ' ').title()}")
            elif result['status'] == 'partial':
                recommendations.append(f"Improve {test_name.replace('_', ' ').title()} implementation")
        
        if not recommendations:
            recommendations.append("All systems functioning well - consider performance optimization")
        
        return recommendations
    
    def generate_overall_assessment(self, success_rate: float) -> str:
        """Generate overall assessment based on test results"""
        if success_rate >= 0.9:
            return "Excellent - Week 2 enhancements are working exceptionally well"
        elif success_rate >= 0.7:
            return "Good - Week 2 enhancements are mostly functional with minor issues"
        elif success_rate >= 0.5:
            return "Fair - Week 2 enhancements have significant issues that need attention"
        else:
            return "Poor - Week 2 enhancements require major fixes before production use"

async def main():
    """Main test execution function"""
    tester = Week2EnhancementsTester()
    
    print("🚀 Week 2 Enhancements Testing Suite")
    print("Testing advanced correlation analysis, pattern recognition, backtesting, and signal generation")
    print("=" * 80)
    
    # Run comprehensive tests
    report = await tester.run_comprehensive_tests()
    
    # Display summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    summary = report['test_summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed_tests']} ✅")
    print(f"Partial: {summary['partial_tests']} ⚠️")
    print(f"Failed: {summary['failed_tests']} ❌")
    print(f"Errors: {summary['error_tests']} 🚨")
    print(f"Success Rate: {summary['success_rate']:.1%}")
    
    print(f"\n🔍 OVERALL ASSESSMENT:")
    print(f"{report['overall_assessment']}")
    
    if report['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")
    
    print(f"\n📁 Detailed report saved to test file")
    
    return report

if __name__ == "__main__":
    asyncio.run(main()) 