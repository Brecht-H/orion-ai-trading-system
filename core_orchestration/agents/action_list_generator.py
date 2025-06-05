#!/usr/bin/env python3
"""
🎯 COMPREHENSIVE ACTION LIST GENERATOR
Scans all Orion modules and generates prioritized, filterable action lists for Notion
GOAL: Create executive-ready action items with full context and prioritization
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
import re

@dataclass
class ActionItem:
    """Structured action item for CEO execution"""
    id: str
    title: str
    description: str
    category: str
    priority: str  # Critical, High, Medium, Low
    effort: str    # Minutes, Hours, Days
    cost: str      # Free, <$25, <$100, >$100
    roi_potential: str  # High, Medium, Low
    dependencies: List[str]
    module_source: str
    deadline: str
    implementation_notes: str
    api_details: str = ""
    testing_required: bool = False

class OrionActionListGenerator:
    """
    🎯 ORION ACTION LIST GENERATOR
    
    CAPABILITIES:
    - Scan all modules for action items
    - Prioritize by impact and urgency
    - Generate Notion-ready database entries
    - Provide filtering and categorization
    - Track dependencies and deadlines
    """
    
    def __init__(self):
        self.generator_id = "action_list_generator_001"
        self.setup_logging()
        self.action_items = []
        self.categories = [
            "API_INTEGRATIONS", "SECURITY", "OPTIMIZATION", "MONITORING",
            "STRATEGY_DEVELOPMENT", "KNOWLEDGE_EXPANSION", "RISK_MANAGEMENT",
            "TRADING_EXECUTION", "INFRASTRUCTURE", "DOCUMENTATION"
        ]
        
    def setup_logging(self):
        """Setup action list logging"""
        Path("logs/action_lists").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ActionGenerator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/action_lists/action_generation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🎯 Action List Generator {self.generator_id} initialized")
    
    def generate_comprehensive_action_list(self):
        """Generate complete action list from all modules"""
        self.logger.info("🔍 Scanning all Orion modules for action items...")
        
        # Scan different sources
        self.scan_api_integration_needs()
        self.scan_security_requirements()
        self.scan_optimization_opportunities()
        self.scan_strategy_development_needs()
        self.scan_knowledge_center_expansion()
        self.scan_infrastructure_improvements()
        self.scan_monitoring_setup()
        self.scan_documentation_needs()
        self.scan_trading_execution_setup()
        
        # Prioritize and organize
        self.prioritize_actions()
        
        # Generate outputs
        notion_database = self.generate_notion_database()
        csv_export = self.generate_csv_export()
        executive_summary = self.generate_executive_summary()
        
        return {
            'notion_database': notion_database,
            'csv_export': csv_export,
            'executive_summary': executive_summary,
            'total_actions': len(self.action_items),
            'by_priority': self.count_by_priority(),
            'by_category': self.count_by_category()
        }
    
    def scan_api_integration_needs(self):
        """Scan for API integration requirements"""
        
        # Exchange APIs
        exchange_apis = [
            {
                'title': 'Setup Bybit Testnet API',
                'description': 'Configure Bybit testnet API for paper trading and strategy testing',
                'priority': 'High',
                'effort': '30 minutes',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'Testnet: https://testnet.bybit.com, No KYC required',
                'implementation_notes': 'Already have API keys in .env, need endpoint configuration',
                'testing_required': True
            },
            {
                'title': 'Setup Bybit Live API',
                'description': 'Configure Bybit live API for real trading execution',
                'priority': 'Medium',
                'effort': '1 hour',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'Live: https://api.bybit.com, KYC required',
                'implementation_notes': 'Requires KYC verification and live account setup',
                'dependencies': ['Bybit Testnet API'],
                'testing_required': True
            },
            {
                'title': 'Add Binance API Integration',
                'description': 'Add Binance exchange for broader market access and liquidity',
                'priority': 'Medium',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'REST + WebSocket APIs, testnet available',
                'implementation_notes': 'Higher liquidity than Bybit, good for larger trades'
            },
            {
                'title': 'Add Coinbase Pro API',
                'description': 'Integrate Coinbase Pro for US market access and fiat onramps',
                'priority': 'Low',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'api_details': 'REST API, sandbox available',
                'implementation_notes': 'Good for US compliance and fiat integration'
            }
        ]
        
        for api in exchange_apis:
            self.add_action_item(
                category="API_INTEGRATIONS",
                module_source="Trading Execution Center",
                deadline="1 week" if api['priority'] == 'High' else "2 weeks",
                **api
            )
        
        # News Source APIs
        news_apis = [
            {
                'title': 'Expand CoinTelegraph API',
                'description': 'Add full CoinTelegraph RSS and API integration for crypto news',
                'priority': 'High',
                'effort': '45 minutes',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'RSS feeds + potential API access',
                'implementation_notes': 'Major crypto news source, high signal value'
            },
            {
                'title': 'Add The Block API',
                'description': 'Integrate The Block for institutional crypto news and data',
                'priority': 'High',
                'effort': '30 minutes',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'RSS feeds, potential premium API',
                'implementation_notes': 'Institutional focus, regulatory news'
            },
            {
                'title': 'Add DeFiPulse API',
                'description': 'Integrate DeFiPulse for DeFi TVL and protocol data',
                'priority': 'Medium',
                'effort': '1 hour',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'api_details': 'Free API with good DeFi metrics',
                'implementation_notes': 'Valuable for DeFi trend analysis'
            },
            {
                'title': 'Add CryptoCompare API',
                'description': 'Integrate CryptoCompare for comprehensive market data',
                'priority': 'Medium',
                'effort': '1 hour',
                'cost': 'Free tier available',
                'roi_potential': 'High',
                'api_details': 'Free tier: 100k calls/month',
                'implementation_notes': 'Comprehensive historical and real-time data'
            }
        ]
        
        for api in news_apis:
            self.add_action_item(
                category="API_INTEGRATIONS",
                module_source="Research Center",
                deadline="1 week",
                **api
            )
        
        # Free LLM APIs
        llm_apis = [
            {
                'title': 'Maximize Groq Free Tier',
                'description': 'Optimize Groq API usage to maximize 14k daily free requests',
                'priority': 'High',
                'effort': '30 minutes',
                'cost': 'Free',
                'roi_potential': 'High',
                'api_details': 'Free: 14,000 requests/day, very fast inference',
                'implementation_notes': 'Already configured, optimize usage patterns',
                'testing_required': True
            },
            {
                'title': 'Setup Replicate Free Tier',
                'description': 'Add Replicate for additional free LLM access',
                'priority': 'Medium',
                'effort': '45 minutes',
                'cost': 'Free tier available',
                'roi_potential': 'Medium',
                'api_details': 'Free tier with various models available',
                'implementation_notes': 'Good backup for Groq limits'
            },
            {
                'title': 'Add Perplexity API',
                'description': 'Integrate Perplexity for real-time web search + LLM',
                'priority': 'Medium',
                'effort': '1 hour',
                'cost': 'Free tier: $5 credit',
                'roi_potential': 'High',
                'api_details': 'Combines search with LLM, real-time data',
                'implementation_notes': 'Excellent for current market analysis'
            }
        ]
        
        for api in llm_apis:
            self.add_action_item(
                category="API_INTEGRATIONS",
                module_source="LLM Orchestrator",
                deadline="3 days",
                **api
            )
    
    def scan_security_requirements(self):
        """Scan for security implementation needs"""
        
        security_items = [
            {
                'title': 'Implement API Key Rotation',
                'description': 'Setup automated API key rotation for enhanced security',
                'priority': 'Critical',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Prevent API key abuse, automate rotation schedule',
                'deadline': '3 days'
            },
            {
                'title': 'Setup SSH Key Authentication',
                'description': 'Replace password authentication with SSH keys',
                'priority': 'High',
                'effort': '30 minutes',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'More secure than passwords, prevent brute force',
                'deadline': '1 week'
            },
            {
                'title': 'Enable 2FA on All Accounts',
                'description': 'Enable two-factor authentication on all service accounts',
                'priority': 'High',
                'effort': '1 hour',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Exchange accounts, API services, GitHub, etc.',
                'deadline': '1 week'
            },
            {
                'title': 'Setup Security Monitoring',
                'description': 'Implement automated security monitoring and alerts',
                'priority': 'Medium',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Monitor file access, API usage, login attempts',
                'deadline': '2 weeks'
            }
        ]
        
        for item in security_items:
            self.add_action_item(
                category="SECURITY",
                module_source="Security Analysis Agent",
                **item
            )
    
    def scan_optimization_opportunities(self):
        """Scan for system optimization opportunities"""
        
        optimization_items = [
            {
                'title': 'Implement Weekly Optimization Automation',
                'description': 'Setup automated weekly system optimization runs',
                'priority': 'Medium',
                'effort': '1 hour',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Automate the optimization script via cron',
                'deadline': '1 week'
            },
            {
                'title': 'Setup Performance Monitoring Dashboard',
                'description': 'Create real-time performance monitoring in Notion',
                'priority': 'Medium',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Track memory, CPU, API usage, costs',
                'deadline': '2 weeks'
            },
            {
                'title': 'Optimize Database Queries',
                'description': 'Review and optimize SQLite database queries for performance',
                'priority': 'Low',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Add indexes, optimize slow queries',
                'deadline': '1 month'
            }
        ]
        
        for item in optimization_items:
            self.add_action_item(
                category="OPTIMIZATION",
                module_source="System Optimization Agent",
                **item
            )
    
    def scan_strategy_development_needs(self):
        """Scan for strategy development requirements"""
        
        strategy_items = [
            {
                'title': 'Backtest All Strategies on Real Data',
                'description': 'Run comprehensive backtesting on all 4 strategies with recent data',
                'priority': 'High',
                'effort': '4 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Validate strategy performance, optimize parameters',
                'deadline': '1 week',
                'testing_required': True
            },
            {
                'title': 'Implement Paper Trading',
                'description': 'Setup paper trading for all strategies before live deployment',
                'priority': 'High',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Test strategies without real money risk',
                'deadline': '1 week',
                'dependencies': ['Bybit Testnet API'],
                'testing_required': True
            },
            {
                'title': 'Create Strategy Performance Dashboard',
                'description': 'Build Notion dashboard for strategy performance tracking',
                'priority': 'Medium',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Track win rate, Sharpe ratio, drawdown for each strategy',
                'deadline': '2 weeks'
            }
        ]
        
        for item in strategy_items:
            self.add_action_item(
                category="STRATEGY_DEVELOPMENT",
                module_source="Strategy Center",
                **item
            )
    
    def scan_knowledge_center_expansion(self):
        """Scan for knowledge center expansion needs"""
        
        knowledge_items = [
            {
                'title': 'Expand Newsletter Subscriptions',
                'description': 'Subscribe to 10 additional high-value crypto newsletters',
                'priority': 'High',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Morning Brew Crypto, Bankless, Decrypt, etc.',
                'deadline': '1 week'
            },
            {
                'title': 'Setup YouTube Content Ingestion',
                'description': 'Automate ingestion from top crypto YouTube channels',
                'priority': 'Medium',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Coin Bureau, Benjamin Cowen, InvestAnswers',
                'deadline': '2 weeks'
            },
            {
                'title': 'Add Podcast Transcription',
                'description': 'Setup automatic podcast transcription and analysis',
                'priority': 'Low',
                'effort': '4 hours',
                'cost': '<$25/month',
                'roi_potential': 'Medium',
                'implementation_notes': 'Unchained, Bankless, What Bitcoin Did',
                'deadline': '1 month'
            }
        ]
        
        for item in knowledge_items:
            self.add_action_item(
                category="KNOWLEDGE_EXPANSION",
                module_source="Knowledge Center",
                **item
            )
    
    def scan_infrastructure_improvements(self):
        """Scan for infrastructure improvement needs"""
        
        infrastructure_items = [
            {
                'title': 'Setup Automated Backups',
                'description': 'Implement automated backup system for databases and configs',
                'priority': 'High',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Daily backups to external storage, cloud backup',
                'deadline': '1 week'
            },
            {
                'title': 'Implement Error Logging',
                'description': 'Setup comprehensive error logging and alerting system',
                'priority': 'Medium',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Centralized logging, error notifications to Notion',
                'deadline': '2 weeks'
            },
            {
                'title': 'Setup CI/CD Pipeline',
                'description': 'Create continuous integration/deployment pipeline',
                'priority': 'Low',
                'effort': '6 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'GitHub Actions for automated testing and deployment',
                'deadline': '1 month'
            }
        ]
        
        for item in infrastructure_items:
            self.add_action_item(
                category="INFRASTRUCTURE",
                module_source="Core Orchestration",
                **item
            )
    
    def scan_monitoring_setup(self):
        """Scan for monitoring setup needs"""
        
        monitoring_items = [
            {
                'title': 'Setup Portfolio Value Tracking',
                'description': 'Real-time portfolio value monitoring and alerts',
                'priority': 'High',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Track total value, daily P&L, risk metrics',
                'deadline': '1 week'
            },
            {
                'title': 'Implement Risk Alerts',
                'description': 'Setup automated risk threshold alerts to Notion',
                'priority': 'High',
                'effort': '1 hour',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Alert on high drawdown, concentration risk, etc.',
                'deadline': '1 week'
            },
            {
                'title': 'Create Executive Status Report',
                'description': 'Automated daily executive status report generation',
                'priority': 'Medium',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Daily summary of performance, risks, opportunities',
                'deadline': '2 weeks'
            }
        ]
        
        for item in monitoring_items:
            self.add_action_item(
                category="MONITORING",
                module_source="Risk Management Center",
                **item
            )
    
    def scan_documentation_needs(self):
        """Scan for documentation requirements"""
        
        doc_items = [
            {
                'title': 'Create API Documentation',
                'description': 'Document all API integrations and usage patterns',
                'priority': 'Medium',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Essential for maintenance and troubleshooting',
                'deadline': '2 weeks'
            },
            {
                'title': 'Create Trading Strategy Manual',
                'description': 'Document all trading strategies with parameters and logic',
                'priority': 'Medium',
                'effort': '4 hours',
                'cost': 'Free',
                'roi_potential': 'Medium',
                'implementation_notes': 'Critical for strategy optimization and debugging',
                'deadline': '2 weeks'
            }
        ]
        
        for item in doc_items:
            self.add_action_item(
                category="DOCUMENTATION",
                module_source="Documentation",
                **item
            )
    
    def scan_trading_execution_setup(self):
        """Scan for trading execution setup needs"""
        
        trading_items = [
            {
                'title': 'Setup Position Sizing Calculator',
                'description': 'Implement dynamic position sizing based on volatility and risk',
                'priority': 'High',
                'effort': '2 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': '2% risk per trade, adjusted for volatility',
                'deadline': '1 week'
            },
            {
                'title': 'Implement Stop Loss Management',
                'description': 'Automated stop loss placement and trailing functionality',
                'priority': 'High',
                'effort': '3 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Dynamic stops based on ATR, trailing stops',
                'deadline': '1 week'
            },
            {
                'title': 'Setup Order Execution Engine',
                'description': 'Build robust order execution with retry logic and error handling',
                'priority': 'Critical',
                'effort': '6 hours',
                'cost': 'Free',
                'roi_potential': 'High',
                'implementation_notes': 'Handle network issues, partial fills, rejections',
                'deadline': '3 days'
            }
        ]
        
        for item in trading_items:
            self.add_action_item(
                category="TRADING_EXECUTION",
                module_source="Trading Execution Center",
                **item
            )
    
    def add_action_item(self, **kwargs):
        """Add action item with auto-generated ID"""
        action_id = f"ACT_{len(self.action_items):03d}_{kwargs['category'][:3]}"
        
        # Extract dependencies to avoid duplicate keyword argument
        dependencies = kwargs.pop('dependencies', [])
        
        action = ActionItem(
            id=action_id,
            dependencies=dependencies,
            **kwargs
        )
        
        self.action_items.append(action)
        self.logger.info(f"✅ Added action: {action.title}")
    
    def prioritize_actions(self):
        """Prioritize actions by impact and urgency"""
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        
        self.action_items.sort(key=lambda x: (
            priority_order.get(x.priority, 4),
            x.cost != 'Free',  # Free items first
            x.effort  # Shorter efforts first
        ))
        
        self.logger.info(f"📊 Prioritized {len(self.action_items)} action items")
    
    def generate_notion_database(self):
        """Generate Notion database-ready JSON"""
        notion_items = []
        
        for action in self.action_items:
            notion_item = {
                "Action ID": action.id,
                "Title": action.title,
                "Description": action.description,
                "Category": action.category,
                "Priority": action.priority,
                "Effort": action.effort,
                "Cost": action.cost,
                "ROI Potential": action.roi_potential,
                "Module Source": action.module_source,
                "Deadline": action.deadline,
                "Implementation Notes": action.implementation_notes,
                "API Details": action.api_details,
                "Dependencies": ", ".join(action.dependencies),
                "Testing Required": action.testing_required,
                "Status": "Not Started",
                "Assigned To": "CEO",
                "Created Date": datetime.now().strftime("%Y-%m-%d"),
                "Estimated ROI": self.calculate_estimated_roi(action),
                "Quick Win": "Yes" if action.effort in ["30 minutes", "45 minutes"] and action.cost == "Free" else "No"
            }
            notion_items.append(notion_item)
        
        return notion_items
    
    def calculate_estimated_roi(self, action):
        """Calculate estimated ROI for action item"""
        if action.roi_potential == "High" and action.cost == "Free":
            return "Very High"
        elif action.roi_potential == "High":
            return "High"
        elif action.roi_potential == "Medium" and action.cost == "Free":
            return "High"
        else:
            return action.roi_potential
    
    def generate_csv_export(self):
        """Generate CSV export for easy filtering"""
        csv_data = []
        headers = ["Action ID", "Title", "Category", "Priority", "Effort", "Cost", 
                  "ROI Potential", "Deadline", "Quick Win", "API Details", "Implementation Notes"]
        
        csv_data.append(headers)
        
        for action in self.action_items:
            row = [
                action.id,
                action.title,
                action.category,
                action.priority,
                action.effort,
                action.cost,
                action.roi_potential,
                action.deadline,
                "Yes" if action.effort in ["30 minutes", "45 minutes"] and action.cost == "Free" else "No",
                action.api_details,
                action.implementation_notes
            ]
            csv_data.append(row)
        
        return csv_data
    
    def generate_executive_summary(self):
        """Generate executive summary of action items"""
        total = len(self.action_items)
        by_priority = self.count_by_priority()
        by_category = self.count_by_category()
        
        quick_wins = len([a for a in self.action_items 
                         if a.effort in ["30 minutes", "45 minutes"] and a.cost == "Free"])
        
        high_impact_free = len([a for a in self.action_items 
                               if a.roi_potential == "High" and a.cost == "Free"])
        
        critical_deadline = len([a for a in self.action_items 
                                if a.priority == "Critical"])
        
        summary = {
            'total_actions': total,
            'critical_items': by_priority.get('Critical', 0),
            'high_priority': by_priority.get('High', 0),
            'quick_wins_available': quick_wins,
            'high_impact_free': high_impact_free,
            'items_needing_immediate_attention': critical_deadline,
            'categories': by_category,
            'estimated_total_implementation_time': self.estimate_total_time(),
            'recommended_first_week': self.get_first_week_recommendations(),
            'api_integrations_needed': by_category.get('API_INTEGRATIONS', 0)
        }
        
        return summary
    
    def count_by_priority(self):
        """Count actions by priority"""
        counts = {}
        for action in self.action_items:
            counts[action.priority] = counts.get(action.priority, 0) + 1
        return counts
    
    def count_by_category(self):
        """Count actions by category"""
        counts = {}
        for action in self.action_items:
            counts[action.category] = counts.get(action.category, 0) + 1
        return counts
    
    def estimate_total_time(self):
        """Estimate total implementation time"""
        time_mapping = {
            "30 minutes": 0.5,
            "45 minutes": 0.75,
            "1 hour": 1,
            "2 hours": 2,
            "3 hours": 3,
            "4 hours": 4,
            "6 hours": 6
        }
        
        total_hours = 0
        for action in self.action_items:
            total_hours += time_mapping.get(action.effort, 2)  # Default 2 hours
        
        return f"{total_hours:.1f} hours ({total_hours/8:.1f} working days)"
    
    def get_first_week_recommendations(self):
        """Get recommended actions for first week"""
        first_week = []
        for action in self.action_items:
            if action.priority in ["Critical", "High"] and action.cost == "Free":
                first_week.append({
                    'id': action.id,
                    'title': action.title,
                    'effort': action.effort,
                    'category': action.category
                })
                if len(first_week) >= 10:  # Limit to top 10
                    break
        
        return first_week
    
    def save_results(self, results):
        """Save all results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save Notion database JSON
        notion_file = f"action_lists/notion_database_{timestamp}.json"
        Path(notion_file).parent.mkdir(exist_ok=True)
        with open(notion_file, 'w') as f:
            json.dump(results['notion_database'], f, indent=2)
        
        # Save CSV
        csv_file = f"action_lists/action_list_{timestamp}.csv"
        with open(csv_file, 'w') as f:
            for row in results['csv_export']:
                f.write(','.join([f'"{cell}"' for cell in row]) + '\n')
        
        # Save executive summary
        summary_file = f"action_lists/executive_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(results['executive_summary'], f, indent=2)
        
        self.logger.info(f"💾 Results saved: {notion_file}, {csv_file}, {summary_file}")
        
        return {
            'notion_file': notion_file,
            'csv_file': csv_file,
            'summary_file': summary_file
        }

def main():
    """Generate comprehensive action list"""
    generator = OrionActionListGenerator()
    results = generator.generate_comprehensive_action_list()
    file_paths = generator.save_results(results)
    
    # Display results
    print("\n" + "="*80)
    print("🎯 ORION COMPREHENSIVE ACTION LIST - GENERATED")
    print("="*80)
    
    summary = results['executive_summary']
    print(f"\n📊 EXECUTIVE SUMMARY:")
    print(f"   Total Actions: {summary['total_actions']}")
    print(f"   Critical Items: {summary['critical_items']}")
    print(f"   High Priority: {summary['high_priority']}")
    print(f"   Quick Wins (≤45 min, Free): {summary['quick_wins_available']}")
    print(f"   High Impact Free Items: {summary['high_impact_free']}")
    print(f"   Estimated Total Time: {summary['estimated_total_implementation_time']}")
    
    print(f"\n🎯 FIRST WEEK RECOMMENDATIONS:")
    for i, item in enumerate(summary['recommended_first_week'][:5], 1):
        print(f"   {i}. {item['title']} ({item['effort']}) - {item['category']}")
    
    print(f"\n📂 FILES GENERATED:")
    print(f"   Notion Database: {file_paths['notion_file']}")
    print(f"   CSV Export: {file_paths['csv_file']}")
    print(f"   Executive Summary: {file_paths['summary_file']}")
    
    print(f"\n✅ Ready for Notion import and CEO action!")
    print("="*80)
    
    return results

if __name__ == "__main__":
    main() 