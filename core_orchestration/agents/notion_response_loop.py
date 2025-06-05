#!/usr/bin/env python3
"""
🤖 NOTION AUTOMATED RESPONSE LOOP
Monitors Notion action list for updates and provides intelligent LLM responses
GOAL: Complete automation - CEO updates Notion, system responds intelligently
"""

import os
import json
import requests
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Any
import asyncio
from threading import Thread
import signal
import sys

class NotionResponseLoop:
    """
    🤖 NOTION AUTOMATED RESPONSE LOOP
    
    CAPABILITIES:
    - Monitor Notion database for changes
    - Detect status updates, comments, priority changes
    - Generate intelligent LLM responses
    - Provide next steps and recommendations
    - Update system state based on progress
    - Alert on critical items and blockers
    """
    
    def __init__(self):
        self.loop_id = "notion_response_loop_001"
        self.setup_logging()
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = "208cba76-1065-8185-bad8-f0f1aeb99ecf"  # From integration
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # State tracking
        self.last_check = datetime.now()
        self.known_items = {}
        self.running = False
        self.setup_local_database()
        
        # 🎯 CEO Action Flow Integration
        self.ceo_flow = None
        self.load_ceo_action_flow()
        
    def setup_logging(self):
        """Setup response loop logging"""
        Path("logs/notion_response_loop").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ResponseLoop - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/notion_response_loop/response_loop.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🤖 Notion Response Loop {self.loop_id} initialized")
    
    def setup_local_database(self):
        """Setup local SQLite database for state tracking"""
        Path("databases/sqlite_dbs").mkdir(parents=True, exist_ok=True)
        self.db_path = "databases/sqlite_dbs/notion_response_loop.db"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS action_states (
            action_id TEXT PRIMARY KEY,
            last_status TEXT,
            last_priority TEXT,
            last_updated TEXT,
            completion_date TEXT,
            response_count INTEGER DEFAULT 0,
            roi_achieved REAL DEFAULT 0
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id TEXT,
            response_type TEXT,
            response_content TEXT,
            created_at TEXT,
            FOREIGN KEY (action_id) REFERENCES action_states (action_id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            date TEXT PRIMARY KEY,
            actions_completed INTEGER DEFAULT 0,
            total_roi_achieved REAL DEFAULT 0,
            critical_items_remaining INTEGER DEFAULT 0,
            quick_wins_completed INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("📊 Local tracking database initialized")
    
    def load_ceo_action_flow(self):
        """Load the CEO Action Flow system"""
        try:
            from core_orchestration.agents.ceo_action_flow import CEOActionFlow
            self.ceo_flow = CEOActionFlow()
            self.logger.info("🎯 CEO Action Flow integrated successfully")
        except Exception as e:
            self.logger.error(f"⚠️ CEO Action Flow not available: {e}")
    
    def detect_action_id(self, title):
        """Detect action ID from title"""
        if not title:
            return None
            
        title_upper = title.upper()
        
        # Common action patterns
        action_patterns = [
            'ACT_011_SEC', 'ACT_034_TRA', 'ACT_045_OPT', 'ACT_067_MON',
            'ACT_089_INT', 'ACT_012_BAC', 'ACT_023_API', 'ACT_056_DAT',
            'ACT_078_REP', 'ACT_090_DEP'
        ]
        
        for pattern in action_patterns:
            if pattern in title_upper:
                return pattern
        
        # Check for generic ACT_ pattern
        import re
        match = re.search(r'ACT_\d{3}_[A-Z]{3}', title_upper)
        if match:
            return match.group(0)
        
        return None
    
    def create_ceo_response(self, action_id, status, ceo_result):
        """Create CEO-style response from CEO Action Flow result"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        response = {
            "type": "ceo_action_flow",
            "action_id": action_id,
            "status": status,
            "timestamp": timestamp,
            "ceo_result": ceo_result
        }
        
        if status.lower() == 'complete':
            if ceo_result.get('status') == 'implementation_complete':
                response["message"] = f"🎯 {action_id} IMPLEMENTATION COMPLETE ✅"
                response["details"] = f"Successfully implemented at {timestamp}"
                response["results"] = ceo_result.get('results', [])
            else:
                response["message"] = f"⚠️ {action_id} IMPLEMENTATION PENDING"
                response["details"] = f"Waiting for prerequisites: {', '.join(ceo_result.get('missing', []))}"
        
        elif status.lower() == 'wait':
            response["message"] = f"⏸️ {action_id} READY FOR IMPLEMENTATION"
            response["details"] = f"Prepared and waiting: {ceo_result.get('message', 'Ready when you are')}"
        
        elif status.lower() == 'blocked':
            response["message"] = f"🚫 {action_id} BLOCKER ANALYSIS"
            response["details"] = f"Blockers identified: {', '.join(ceo_result.get('blockers', []))}"
            response["unblock_options"] = ceo_result.get('unblock_options', [])
        
        else:
            response["message"] = f"📊 {action_id} STATUS UPDATE"
            response["details"] = f"Status: {status} | {ceo_result.get('message', 'Monitoring')}"
        
        return response
    
    def start_monitoring_loop(self):
        """Start the automated monitoring loop"""
        self.logger.info("🚀 Starting automated Notion monitoring loop...")
        self.running = True
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Initial sync
        self.sync_initial_state()
        
        # Main monitoring loop
        check_interval = 30  # Check every 30 seconds
        
        while self.running:
            try:
                self.check_for_updates()
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Received interrupt signal")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
        
        self.logger.info("🏁 Monitoring loop stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def sync_initial_state(self):
        """Sync initial state of all action items"""
        self.logger.info("🔄 Syncing initial state from Notion...")
        
        try:
            # Query all pages in the database
            query_params = {
                "filter": {
                    "property": "Status",
                    "select": {
                        "does_not_equal": "Completed"
                    }
                }
            }
            
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json=query_params
            )
            
            if response.status_code == 200:
                pages = response.json().get('results', [])
                self.logger.info(f"📊 Found {len(pages)} active action items")
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for page in pages:
                    action_id = self.extract_action_id(page)
                    status = self.extract_property_value(page, 'Status')
                    priority = self.extract_property_value(page, 'Priority')
                    
                    # Store initial state
                    cursor.execute('''
                    INSERT OR REPLACE INTO action_states 
                    (action_id, last_status, last_priority, last_updated)
                    VALUES (?, ?, ?, ?)
                    ''', (action_id, status, priority, datetime.now().isoformat()))
                    
                    self.known_items[action_id] = {
                        'status': status,
                        'priority': priority,
                        'last_updated': datetime.now()
                    }
                
                conn.commit()
                conn.close()
                
                self.logger.info(f"✅ Initial state synced for {len(self.known_items)} items")
                
            else:
                self.logger.error(f"❌ Failed to sync initial state: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"❌ Error syncing initial state: {e}")
    
    def check_for_updates(self):
        """Check for updates since last check"""
        try:
            # Query database for pages modified since last check
            query_params = {
                "filter": {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": self.last_check.isoformat()
                    }
                },
                "sorts": [
                    {
                        "timestamp": "last_edited_time",
                        "direction": "descending"
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json=query_params
            )
            
            if response.status_code == 200:
                updated_pages = response.json().get('results', [])
                
                if updated_pages:
                    self.logger.info(f"🔄 Found {len(updated_pages)} updated items")
                    
                    for page in updated_pages:
                        self.process_page_update(page)
                
                self.last_check = datetime.now()
                
            else:
                self.logger.error(f"❌ Failed to check updates: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"❌ Error checking updates: {e}")
    
    def process_page_update(self, page):
        """Process an individual page update"""
        try:
            action_id = self.extract_action_id(page)
            current_status = self.extract_property_value(page, 'Status')
            current_priority = self.extract_property_value(page, 'Priority')
            title = self.extract_property_value(page, 'Title')
            
            # Get previous state
            previous_state = self.known_items.get(action_id, {})
            previous_status = previous_state.get('status')
            previous_priority = previous_state.get('priority')
            
            self.logger.info(f"🔄 Processing update for {action_id}: {previous_status} → {current_status}")
            
            # Detect what changed
            changes = self.detect_changes(action_id, page, previous_state)
            
            if changes:
                # 🎯 CEO ACTION FLOW INTEGRATION
                ceo_action_id = self.detect_action_id(title)
                
                if ceo_action_id and self.ceo_flow:
                    # Process through CEO Action Flow
                    self.logger.info(f"🎯 Processing {ceo_action_id} through CEO Action Flow")
                    
                    # Create item data for CEO flow
                    item_data = {
                        'title': title,
                        'status': current_status,
                        'id': page.get('id'),
                        'changes': changes,
                        'previous_status': previous_status
                    }
                    
                    try:
                        ceo_result = self.ceo_flow.process_action_status_change(
                            ceo_action_id, current_status, item_data
                        )
                        
                        # Create CEO-style response
                        ceo_response = self.create_ceo_response(ceo_action_id, current_status, ceo_result)
                        
                        # Store and display CEO response
                        self.store_response(action_id, changes, ceo_response)
                        self.display_response(action_id, title, changes, ceo_response)
                        
                        self.logger.info(f"✅ {ceo_action_id} processed by CEO Action Flow")
                        
                    except Exception as e:
                        self.logger.error(f"❌ CEO Action Flow error for {ceo_action_id}: {e}")
                        # Fallback to standard response
                        response = self.generate_intelligent_response(action_id, changes, page)
                        self.store_response(action_id, changes, response)
                        self.display_response(action_id, title, changes, response)
                else:
                    # Standard intelligent response for non-action items
                    response = self.generate_intelligent_response(action_id, changes, page)
                    self.store_response(action_id, changes, response)
                    self.display_response(action_id, title, changes, response)
                
                # Update local state
                self.update_local_state(action_id, page)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing update for page: {e}")
    
    def detect_changes(self, action_id, page, previous_state):
        """Detect what changed in the action item"""
        changes = {}
        
        current_status = self.extract_property_value(page, 'Status')
        current_priority = self.extract_property_value(page, 'Priority')
        
        if previous_state.get('status') != current_status:
            changes['status'] = {
                'from': previous_state.get('status'),
                'to': current_status
            }
        
        if previous_state.get('priority') != current_priority:
            changes['priority'] = {
                'from': previous_state.get('priority'),
                'to': current_priority
            }
        
        # Check for completion
        if current_status == "Completed" and previous_state.get('status') != "Completed":
            changes['completed'] = True
        
        # Check for blockers
        if current_status == "Blocked":
            changes['blocked'] = True
        
        # Check for progress start
        if current_status == "In Progress" and previous_state.get('status') == "Not Started":
            changes['started'] = True
        
        return changes
    
    def generate_intelligent_response(self, action_id, changes, page):
        """Generate intelligent LLM response based on changes"""
        try:
            # Extract action details
            title = self.extract_property_value(page, 'Title')
            category = self.extract_property_value(page, 'Category')
            effort = self.extract_property_value(page, 'Effort')
            cost = self.extract_property_value(page, 'Cost')
            roi_potential = self.extract_property_value(page, 'ROI Potential')
            implementation_notes = self.extract_property_value(page, 'Implementation Notes')
            dependencies = self.extract_property_value(page, 'Dependencies')
            
            # Build context for LLM
            context = {
                'action_id': action_id,
                'title': title,
                'category': category,
                'effort': effort,
                'cost': cost,
                'roi_potential': roi_potential,
                'implementation_notes': implementation_notes,
                'dependencies': dependencies,
                'changes': changes
            }
            
            # Generate response based on change type
            if changes.get('completed'):
                response = self.generate_completion_response(context)
            elif changes.get('blocked'):
                response = self.generate_blocker_response(context)
            elif changes.get('started'):
                response = self.generate_start_response(context)
            elif changes.get('status'):
                response = self.generate_status_response(context)
            elif changes.get('priority'):
                response = self.generate_priority_response(context)
            else:
                response = self.generate_general_response(context)
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return {"type": "error", "message": "Failed to generate response"}
    
    def generate_completion_response(self, context):
        """Generate response for completed action"""
        action_id = context['action_id']
        title = context['title']
        category = context['category']
        roi_potential = context['roi_potential']
        
        # Calculate estimated ROI achievement
        roi_mapping = {'High': 100, 'Medium': 50, 'Low': 25}
        estimated_roi = roi_mapping.get(roi_potential, 50)
        
        response = {
            "type": "completion",
            "message": f"🎉 Congratulations! Action {action_id} completed successfully!",
            "impact_analysis": {
                "roi_achieved": f"${estimated_roi}/month estimated",
                "category_progress": f"{category} category advanced",
                "next_recommendations": self.get_next_recommendations(category, action_id)
            },
            "celebration": f"✅ {title} - DONE! Moving forward with enhanced {category} capabilities.",
            "automation_update": "System will now utilize this completed capability in future operations."
        }
        
        # Update performance metrics
        self.update_performance_metrics("completion", estimated_roi)
        
        return response
    
    def generate_blocker_response(self, context):
        """Generate response for blocked action"""
        action_id = context['action_id']
        title = context['title']
        dependencies = context['dependencies']
        category = context['category']
        
        response = {
            "type": "blocker",
            "message": f"🚨 Action {action_id} is blocked - immediate assistance available!",
            "blocker_analysis": {
                "likely_causes": self.analyze_likely_blockers(context),
                "dependency_check": dependencies if dependencies else "No dependencies listed",
                "escalation_needed": "High" if context['roi_potential'] == "High" else "Medium"
            },
            "immediate_actions": self.generate_unblock_suggestions(context),
            "alternative_approach": f"Consider alternative implementation for {category} objectives"
        }
        
        return response
    
    def generate_start_response(self, context):
        """Generate response for started action"""
        action_id = context['action_id']
        title = context['title']
        effort = context['effort']
        implementation_notes = context['implementation_notes']
        
        response = {
            "type": "start",
            "message": f"🚀 Great! Action {action_id} started - here's your implementation guide!",
            "implementation_guide": {
                "estimated_duration": effort,
                "key_steps": implementation_notes,
                "success_criteria": self.generate_success_criteria(context),
                "potential_challenges": self.identify_potential_challenges(context)
            },
            "progress_tracking": "Will monitor for completion and provide assistance if needed",
            "encouragement": f"💪 You've got this! {title} will significantly improve system capabilities."
        }
        
        return response
    
    def generate_status_response(self, context):
        """Generate response for status change"""
        changes = context['changes']
        status_change = changes.get('status', {})
        
        response = {
            "type": "status_change",
            "message": f"📊 Status update detected: {status_change.get('from')} → {status_change.get('to')}",
            "analysis": self.analyze_status_change(context),
            "recommendations": self.get_status_recommendations(context)
        }
        
        return response
    
    def generate_priority_response(self, context):
        """Generate response for priority change"""
        changes = context['changes']
        priority_change = changes.get('priority', {})
        
        response = {
            "type": "priority_change",
            "message": f"🎯 Priority updated: {priority_change.get('from')} → {priority_change.get('to')}",
            "impact": self.analyze_priority_impact(context),
            "schedule_adjustment": self.suggest_schedule_adjustment(context)
        }
        
        return response
    
    def generate_general_response(self, context):
        """Generate general response for other changes"""
        response = {
            "type": "general",
            "message": f"🔄 Action {context['action_id']} updated",
            "status": "Monitoring for further changes",
            "support": "Ready to assist with implementation when needed"
        }
        
        return response
    
    def get_next_recommendations(self, category, completed_action_id):
        """Get next recommended actions based on completion"""
        recommendations = {
            "API_INTEGRATIONS": [
                "Test the new API integration",
                "Monitor API usage and costs",
                "Document API configuration for team"
            ],
            "SECURITY": [
                "Verify security implementation",
                "Update security documentation",
                "Schedule security audit"
            ],
            "TRADING_EXECUTION": [
                "Run paper trading tests",
                "Monitor execution performance",
                "Optimize execution parameters"
            ],
            "MONITORING": [
                "Configure alert thresholds",
                "Test monitoring systems",
                "Create monitoring dashboard"
            ]
        }
        
        return recommendations.get(category, ["Continue with related actions", "Monitor implementation results"])
    
    def analyze_likely_blockers(self, context):
        """Analyze likely causes of blockers"""
        category = context['category']
        dependencies = context['dependencies']
        
        common_blockers = {
            "API_INTEGRATIONS": ["API key issues", "Rate limiting", "Documentation unclear"],
            "SECURITY": ["Permission issues", "Configuration complexity", "Testing requirements"],
            "TRADING_EXECUTION": ["Exchange API issues", "Testing environment setup", "Risk management config"],
            "INFRASTRUCTURE": ["System permissions", "Backup configuration", "Storage space"]
        }
        
        blockers = common_blockers.get(category, ["Technical complexity", "Resource requirements"])
        
        if dependencies:
            blockers.append(f"Dependency not met: {dependencies}")
        
        return blockers
    
    def generate_unblock_suggestions(self, context):
        """Generate suggestions to unblock action"""
        category = context['category']
        
        suggestions = {
            "API_INTEGRATIONS": [
                "Verify API keys in .env file",
                "Check API documentation and rate limits",
                "Test API endpoints manually first"
            ],
            "SECURITY": [
                "Check file permissions",
                "Review security documentation",
                "Test in sandbox environment first"
            ],
            "TRADING_EXECUTION": [
                "Verify exchange connectivity",
                "Check testnet configuration",
                "Review trading logic step by step"
            ]
        }
        
        return suggestions.get(category, [
            "Review implementation notes carefully",
            "Check system logs for errors",
            "Break down into smaller steps"
        ])
    
    def generate_success_criteria(self, context):
        """Generate success criteria for action"""
        category = context['category']
        
        criteria = {
            "API_INTEGRATIONS": "API responds successfully and data is processed correctly",
            "SECURITY": "Security measures are active and tested without system disruption", 
            "TRADING_EXECUTION": "Orders execute successfully in testnet environment",
            "MONITORING": "Alerts trigger properly and dashboards display correct data"
        }
        
        return criteria.get(category, "Implementation works as specified and passes basic testing")
    
    def identify_potential_challenges(self, context):
        """Identify potential challenges during implementation"""
        category = context['category']
        effort = context['effort']
        
        challenges = {
            "API_INTEGRATIONS": ["Rate limiting", "Authentication issues", "Data format changes"],
            "SECURITY": ["Permission conflicts", "System compatibility", "Testing complexity"],
            "TRADING_EXECUTION": ["Market volatility during testing", "Order rejection handling", "Position sizing calculation"]
        }
        
        category_challenges = challenges.get(category, ["Configuration complexity", "Integration issues"])
        
        # Add effort-based challenges
        if "6 hours" in effort:
            category_challenges.append("Complex implementation - consider breaking into phases")
        
        return category_challenges
    
    def analyze_status_change(self, context):
        """Analyze the impact of status change"""
        changes = context['changes']
        status_change = changes.get('status', {})
        to_status = status_change.get('to')
        
        analysis = {
            "In Progress": "Active development phase - monitoring for completion",
            "Testing": "Validation phase - ensuring quality before deployment",
            "Blocked": "Immediate attention required to resolve obstacles",
            "Completed": "Success! ROI benefits now active in system"
        }
        
        return analysis.get(to_status, "Status change noted - continuing to monitor")
    
    def get_status_recommendations(self, context):
        """Get recommendations based on status"""
        changes = context['changes']
        status_change = changes.get('status', {})
        to_status = status_change.get('to')
        
        recommendations = {
            "In Progress": ["Set realistic milestones", "Document progress", "Ask for help if stuck"],
            "Testing": ["Test thoroughly", "Document test results", "Prepare for deployment"],
            "Blocked": ["Identify specific blocker", "Seek assistance", "Consider alternatives"],
            "Completed": ["Verify implementation", "Update documentation", "Move to next priority"]
        }
        
        return recommendations.get(to_status, ["Continue monitoring", "Update as needed"])
    
    def analyze_priority_impact(self, context):
        """Analyze impact of priority change"""
        changes = context['changes']
        priority_change = changes.get('priority', {})
        to_priority = priority_change.get('to')
        
        impact = {
            "Critical": "Immediate attention required - may need resource reallocation",
            "High": "Elevated importance - schedule accordingly",
            "Medium": "Standard priority - maintain current schedule",
            "Low": "Reduced urgency - can be deferred if needed"
        }
        
        return impact.get(to_priority, "Priority change noted")
    
    def suggest_schedule_adjustment(self, context):
        """Suggest schedule adjustments based on priority change"""
        changes = context['changes']
        priority_change = changes.get('priority', {})
        to_priority = priority_change.get('to')
        
        if to_priority == "Critical":
            return "Consider moving to top of queue and allocating immediate resources"
        elif to_priority == "High":
            return "Schedule within current week for optimal impact"
        elif to_priority == "Low":
            return "Can be scheduled after higher priority items are completed"
        else:
            return "Maintain current scheduling approach"
    
    def extract_action_id(self, page):
        """Extract action ID from page"""
        try:
            title_property = page.get('properties', {}).get('Action ID', {})
            if title_property.get('type') == 'title':
                title_array = title_property.get('title', [])
                if title_array:
                    return title_array[0].get('text', {}).get('content', '')
            return 'unknown'
        except:
            return 'unknown'
    
    def extract_property_value(self, page, property_name):
        """Extract property value from page"""
        try:
            prop = page.get('properties', {}).get(property_name, {})
            prop_type = prop.get('type')
            
            if prop_type == 'select':
                return prop.get('select', {}).get('name', '')
            elif prop_type == 'rich_text':
                rich_text = prop.get('rich_text', [])
                if rich_text:
                    return rich_text[0].get('text', {}).get('content', '')
                return ''
            elif prop_type == 'checkbox':
                return prop.get('checkbox', False)
            elif prop_type == 'date':
                date_obj = prop.get('date')
                if date_obj:
                    return date_obj.get('start', '')
                return ''
            else:
                return ''
        except:
            return ''
    
    def store_response(self, action_id, changes, response):
        """Store response in local database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO system_responses 
            (action_id, response_type, response_content, created_at)
            VALUES (?, ?, ?, ?)
            ''', (
                action_id,
                response.get('type', 'general'),
                json.dumps(response),
                datetime.now().isoformat()
            ))
            
            # Update response count
            cursor.execute('''
            UPDATE action_states 
            SET response_count = response_count + 1
            WHERE action_id = ?
            ''', (action_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"❌ Error storing response: {e}")
    
    def update_local_state(self, action_id, page):
        """Update local state tracking"""
        try:
            status = self.extract_property_value(page, 'Status')
            priority = self.extract_property_value(page, 'Priority')
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            completion_date = datetime.now().isoformat() if status == "Completed" else None
            
            cursor.execute('''
            UPDATE action_states 
            SET last_status = ?, last_priority = ?, last_updated = ?, completion_date = ?
            WHERE action_id = ?
            ''', (status, priority, datetime.now().isoformat(), completion_date, action_id))
            
            conn.commit()
            conn.close()
            
            # Update in-memory state
            self.known_items[action_id] = {
                'status': status,
                'priority': priority,
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error updating local state: {e}")
    
    def update_performance_metrics(self, metric_type, value=0):
        """Update performance metrics"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current metrics
            cursor.execute('SELECT * FROM performance_metrics WHERE date = ?', (today,))
            existing = cursor.fetchone()
            
            if existing:
                if metric_type == "completion":
                    cursor.execute('''
                    UPDATE performance_metrics 
                    SET actions_completed = actions_completed + 1,
                        total_roi_achieved = total_roi_achieved + ?
                    WHERE date = ?
                    ''', (value, today))
            else:
                # Create new entry
                cursor.execute('''
                INSERT INTO performance_metrics 
                (date, actions_completed, total_roi_achieved)
                VALUES (?, ?, ?)
                ''', (today, 1 if metric_type == "completion" else 0, value))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"❌ Error updating metrics: {e}")
    
    def display_response(self, action_id, title, changes, response):
        """Display response to user"""
        print("\n" + "="*80)
        print(f"🤖 INTELLIGENT RESPONSE - {action_id}")
        print("="*80)
        
        print(f"📋 Action: {title}")
        print(f"🔄 Changes: {list(changes.keys())}")
        print(f"💬 Response Type: {response.get('type', 'general').upper()}")
        
        print(f"\n📨 MESSAGE:")
        print(f"   {response.get('message', 'No message generated')}")
        
        # Display specific response content
        if response.get('type') == 'completion':
            impact = response.get('impact_analysis', {})
            print(f"\n💰 IMPACT ANALYSIS:")
            print(f"   ROI Achieved: {impact.get('roi_achieved', 'Calculating...')}")
            print(f"   Progress: {impact.get('category_progress', 'System enhanced')}")
            
            next_recs = impact.get('next_recommendations', [])
            if next_recs:
                print(f"\n🎯 NEXT RECOMMENDATIONS:")
                for i, rec in enumerate(next_recs[:3], 1):
                    print(f"   {i}. {rec}")
        
        elif response.get('type') == 'blocker':
            blocker_analysis = response.get('blocker_analysis', {})
            print(f"\n🚨 BLOCKER ANALYSIS:")
            causes = blocker_analysis.get('likely_causes', [])
            for cause in causes[:3]:
                print(f"   • {cause}")
            
            actions = response.get('immediate_actions', [])
            if actions:
                print(f"\n🔧 IMMEDIATE ACTIONS:")
                for i, action in enumerate(actions[:3], 1):
                    print(f"   {i}. {action}")
        
        elif response.get('type') == 'start':
            guide = response.get('implementation_guide', {})
            print(f"\n🚀 IMPLEMENTATION GUIDE:")
            print(f"   Duration: {guide.get('estimated_duration', 'Unknown')}")
            print(f"   Success Criteria: {guide.get('success_criteria', 'Complete as specified')}")
        
        print(f"\n⏰ Generated: {datetime.now().strftime('%H:%M:%S')}")
        print("="*80)

def main():
    """Run the Notion response loop"""
    loop = NotionResponseLoop()
    
    print("\n🤖 NOTION AUTOMATED RESPONSE LOOP")
    print("Monitoring your Notion database for updates...")
    print("Update action items in Notion and receive intelligent responses!")
    print("Press Ctrl+C to stop\n")
    
    try:
        loop.start_monitoring_loop()
    except KeyboardInterrupt:
        print("\n🛑 Stopping response loop...")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 