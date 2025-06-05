#!/usr/bin/env python3
"""
🎯 CEO ACTION ENHANCER
Adds CEO descriptions and completion guides to all Notion actions
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import logging

class CEOActionEnhancer:
    def __init__(self):
        self.setup_logging()
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = "208cba76-1065-8185-bad8-f0f1aeb99ecf"
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def setup_logging(self):
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - CEOEnhancer - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/ceo_action_enhancer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_action_templates(self):
        """Get CEO action templates with descriptions and completion guides"""
        return {
            'ACT_011_SEC': {
                'ceo_description': '🔐 **API Key Rotation**: Secure all API keys with automated rotation system',
                'completion_guide': {
                    'what_happens': 'System will automatically rotate ALL API keys and test connections',
                    'prerequisites': ['Add 6 backup API keys to .env file', 'Backup keys must be real (not placeholders)'],
                    'duration': '5-10 minutes',
                    'risk_level': 'Low (testnet keys, automatic rollback)',
                    'success_criteria': 'All API connections tested and working with new keys'
                }
            },
            'ACT_034_TRA': {
                'ceo_description': '⚡ **Trading Engine**: Deploy automated trading execution system',
                'completion_guide': {
                    'what_happens': 'System will deploy trading engine with risk management and monitoring',
                    'prerequisites': ['API keys configured', 'Risk parameters set', 'Backtesting completed'],
                    'duration': '15-30 minutes',
                    'risk_level': 'Medium (real trading, monitored)',
                    'success_criteria': 'Trading engine operational with first successful trade'
                }
            },
            'ACT_045_OPT': {
                'ceo_description': '🚀 **System Optimization**: Improve performance and reduce costs',
                'completion_guide': {
                    'what_happens': 'System will analyze bottlenecks and implement optimizations',
                    'prerequisites': ['Current system analysis completed', 'Optimization plan reviewed'],
                    'duration': '10-20 minutes',
                    'risk_level': 'Low (performance improvements only)',
                    'success_criteria': 'System performance improved by 20%+'
                }
            },
            'ACT_067_MON': {
                'ceo_description': '📊 **Monitoring System**: Deploy comprehensive system monitoring',
                'completion_guide': {
                    'what_happens': 'System will set up real-time monitoring and alerting',
                    'prerequisites': ['Monitoring metrics defined', 'Alert thresholds set'],
                    'duration': '10-15 minutes', 
                    'risk_level': 'Very Low (monitoring only)',
                    'success_criteria': 'All systems monitored with real-time alerts'
                }
            },
            'ACT_089_INT': {
                'ceo_description': '🔗 **Integration Hub**: Connect all external services and APIs',
                'completion_guide': {
                    'what_happens': 'System will integrate and test all external connections',
                    'prerequisites': ['Integration list finalized', 'API credentials available'],
                    'duration': '20-30 minutes',
                    'risk_level': 'Medium (external dependencies)',
                    'success_criteria': 'All integrations connected and data flowing'
                }
            },
            'ACT_012_BAC': {
                'ceo_description': '💾 **Backup System**: Implement automated data backup and recovery',
                'completion_guide': {
                    'what_happens': 'System will set up automated backups with recovery testing',
                    'prerequisites': ['Backup storage configured', 'Recovery procedures defined'],
                    'duration': '15-25 minutes',
                    'risk_level': 'Very Low (backup implementation)',
                    'success_criteria': 'Automated backups running with verified recovery'
                }
            },
            'ACT_023_API': {
                'ceo_description': '🌐 **API Management**: Deploy API gateway and management system',
                'completion_guide': {
                    'what_happens': 'System will deploy API management with rate limiting and monitoring',
                    'prerequisites': ['API specifications complete', 'Security policies defined'],
                    'duration': '20-30 minutes',
                    'risk_level': 'Medium (API security)',
                    'success_criteria': 'API gateway operational with proper security'
                }
            }
        }

    def create_ceo_status_guide(self):
        """Create universal CEO status guide"""
        return {
            'Complete': {
                'icon': '🎯',
                'action': 'IMPLEMENT IMMEDIATELY',
                'description': 'System will execute this action automatically right now',
                'timeline': 'Implementation starts within 30 seconds',
                'safety': 'Automatic testing and rollback if issues detected'
            },
            'Wait': {
                'icon': '⏸️', 
                'action': 'PREPARE BUT HOLD',
                'description': 'System will prepare everything but wait for your final approval',
                'timeline': 'Preparation completed, ready for implementation',
                'safety': 'No changes made until you change status to Complete'
            },
            'Blocked': {
                'icon': '🚫',
                'action': 'ANALYZE BLOCKERS',
                'description': 'System will analyze what\'s preventing implementation',
                'timeline': 'Blocker analysis provided with unblock options',
                'safety': 'No implementation attempted while blocked'
            },
            'In Progress': {
                'icon': '🔄',
                'action': 'MONITOR PROGRESS',
                'description': 'System will track progress and provide updates',
                'timeline': 'Real-time progress monitoring and assistance',
                'safety': 'Continuous monitoring with support available'
            }
        }

    def generate_action_enhancement(self, action_id, title):
        """Generate CEO enhancement for a specific action"""
        templates = self.get_action_templates()
        status_guide = self.create_ceo_status_guide()
        
        # Get template or create intelligent generic one based on title
        if action_id in templates:
            template = templates[action_id]
        else:
            # Create intelligent template based on title keywords
            template = self.create_smart_generic_template(title, action_id)
        
        # Create enhanced description
        enhanced_description = f"""
{template['ceo_description']}

📋 **CEO WORKFLOW GUIDE**

🎯 **COMPLETE** → {status_guide['Complete']['description']}
⏸️ **WAIT** → {status_guide['Wait']['description']}  
🚫 **BLOCKED** → {status_guide['Blocked']['description']}

📊 **WHAT HAPPENS WHEN YOU CLICK COMPLETE:**

✅ **Action**: {template['completion_guide']['what_happens']}
⏱️ **Duration**: {template['completion_guide']['duration']}
🛡️ **Risk Level**: {template['completion_guide']['risk_level']}
🎯 **Success**: {template['completion_guide']['success_criteria']}

📋 **Prerequisites Needed:**
{self.format_prerequisites(template['completion_guide']['prerequisites'])}

📝 **NEXT STEPS AFTER COMPLETION:**
{self.format_next_steps(template['completion_guide'])}

🔒 **Safety Features:**
• Automatic testing before deployment
• Rollback capability if issues detected  
• Real-time monitoring during implementation
• Immediate alerts for any problems

---
*Powered by Orion CEO Action Flow System*
        """.strip()
        
        return enhanced_description

    def create_smart_generic_template(self, title, action_id):
        """Create intelligent template based on action title keywords"""
        title_lower = title.lower() if title else ""
        
        # Analyze title for keywords and create appropriate template
        if any(word in title_lower for word in ['api', 'key', 'security', 'auth']):
            return {
                'ceo_description': f'🔐 **{action_id}**: {title} - Security & API Management',
                'completion_guide': {
                    'what_happens': 'System will implement security measures with API configuration and testing',
                    'prerequisites': ['Security requirements reviewed', 'API credentials available', 'Testing environment ready'],
                    'duration': '10-20 minutes',
                    'risk_level': 'Medium (security changes, tested)',
                    'success_criteria': 'Security implementation verified and all connections tested',
                    'next_steps': ['Monitor security metrics', 'Verify all integrations working', 'Update documentation']
                }
            }
        elif any(word in title_lower for word in ['trading', 'strategy', 'execution']):
            return {
                'ceo_description': f'⚡ **{action_id}**: {title} - Trading & Strategy',
                'completion_guide': {
                    'what_happens': 'System will deploy trading strategies with risk management and monitoring',
                    'prerequisites': ['Strategy backtested', 'Risk parameters set', 'Capital allocation confirmed'],
                    'duration': '15-30 minutes',
                    'risk_level': 'Medium-High (live trading, monitored)',
                    'success_criteria': 'Trading system operational with successful test trades',
                    'next_steps': ['Monitor trading performance', 'Track P&L metrics', 'Adjust parameters if needed']
                }
            }
        elif any(word in title_lower for word in ['monitor', 'alert', 'notification']):
            return {
                'ceo_description': f'📊 **{action_id}**: {title} - Monitoring & Alerts',
                'completion_guide': {
                    'what_happens': 'System will set up comprehensive monitoring with real-time alerts',
                    'prerequisites': ['Monitoring metrics defined', 'Alert thresholds configured', 'Notification channels ready'],
                    'duration': '10-15 minutes',
                    'risk_level': 'Very Low (monitoring only)',
                    'success_criteria': 'All systems monitored with alerts functioning',
                    'next_steps': ['Verify alert delivery', 'Monitor system health', 'Fine-tune thresholds']
                }
            }
        elif any(word in title_lower for word in ['backup', 'recovery', 'data']):
            return {
                'ceo_description': f'💾 **{action_id}**: {title} - Data & Backup',
                'completion_guide': {
                    'what_happens': 'System will implement data management and backup procedures',
                    'prerequisites': ['Data sources identified', 'Storage configured', 'Recovery procedures defined'],
                    'duration': '15-25 minutes',
                    'risk_level': 'Low (data protection)',
                    'success_criteria': 'Data backup and recovery verified working',
                    'next_steps': ['Test recovery procedures', 'Monitor backup status', 'Verify data integrity']
                }
            }
        elif any(word in title_lower for word in ['optimization', 'performance', 'improve']):
            return {
                'ceo_description': f'🚀 **{action_id}**: {title} - System Optimization',
                'completion_guide': {
                    'what_happens': 'System will analyze and implement performance improvements',
                    'prerequisites': ['Performance baseline established', 'Optimization targets defined', 'Testing plan ready'],
                    'duration': '10-20 minutes',
                    'risk_level': 'Low (performance improvements)',
                    'success_criteria': 'System performance improved with metrics verification',
                    'next_steps': ['Monitor performance gains', 'Measure efficiency improvements', 'Document changes']
                }
            }
        else:
            # Generic template for any other action
            return {
                'ceo_description': f'📋 **{action_id}**: {title} - System Implementation',
                'completion_guide': {
                    'what_happens': 'System will implement this action with standard automation and testing',
                    'prerequisites': ['Requirements reviewed', 'Dependencies checked', 'Implementation plan confirmed'],
                    'duration': '10-20 minutes',
                    'risk_level': 'Medium (standard implementation)',
                    'success_criteria': 'Action completed successfully with verification and testing',
                    'next_steps': ['Verify implementation working', 'Monitor for any issues', 'Update related systems']
                }
            }

    def format_prerequisites(self, prerequisites):
        """Format prerequisites list"""
        if not prerequisites:
            return "• No special prerequisites required"
        
        return "\n".join([f"• {prereq}" for prereq in prerequisites])

    def format_next_steps(self, completion_guide):
        """Format next steps after completion"""
        next_steps = completion_guide.get('next_steps', [])
        if not next_steps:
            return "• Implementation complete - system will monitor and maintain automatically"
        
        return "\n".join([f"• {step}" for step in next_steps])

    def enhance_all_actions(self):
        """Enhance all actions in the Notion database"""
        self.logger.info("🚀 Starting CEO Action Enhancement for all actions...")
        
        try:
            # Query all pages in the database
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json={}
            )
            
            if response.status_code == 200:
                pages = response.json().get('results', [])
                self.logger.info(f"📊 Found {len(pages)} actions to enhance")
                
                enhanced_count = 0
                
                for page in pages:
                    try:
                        title = self.extract_property_value(page, 'Title')
                        print(f"🔍 Processing: {title}")
                        
                        # Enhanced to work with ANY action, not just specific patterns
                        action_id = self.detect_action_id(title) or f"ACT_{enhanced_count:03d}_GEN"
                        
                        # Generate enhancement for ALL actions
                        enhanced_description = self.generate_action_enhancement(action_id, title)
                        
                        # Check if already has CEO description
                        current_notes = self.extract_property_value(page, 'Implementation Notes') or ""
                        print(f"📝 Current notes length: {len(current_notes)}")
                        
                        if "CEO WORKFLOW GUIDE" not in current_notes:
                            # Add enhancement to Implementation Notes
                            updated_notes = f"{current_notes}\n\n{enhanced_description}".strip()
                            
                            # Update the page
                            success = self.update_page_notes(page['id'], updated_notes)
                            if success:
                                enhanced_count += 1
                                print(f"✅ Enhanced: {title}")
                                self.logger.info(f"✅ Enhanced {action_id}: {title}")
                            else:
                                print(f"❌ Failed to enhance: {title}")
                        else:
                            print(f"⏭️ Already enhanced: {title}")
                            self.logger.info(f"⏭️ Skipped {action_id}: Already enhanced")
                        
                    except Exception as e:
                        print(f"❌ Error processing page: {e}")
                        self.logger.error(f"❌ Error enhancing page: {e}")
                
                self.logger.info(f"🎯 Enhancement complete: {enhanced_count} actions enhanced")
                
                return {
                    'total_actions': len(pages),
                    'enhanced_count': enhanced_count,
                    'status': 'success'
                }
                
            else:
                self.logger.error(f"❌ Failed to query database: {response.status_code}")
                print(f"❌ Failed to query database: {response.status_code}")
                return {'status': 'error', 'message': 'Failed to query database'}
                
        except Exception as e:
            self.logger.error(f"❌ Error enhancing actions: {e}")
            print(f"❌ Error enhancing actions: {e}")
            return {'status': 'error', 'message': str(e)}

    def detect_action_id(self, title):
        """Detect action ID from title"""
        if not title:
            return None
            
        title_upper = title.upper()
        
        # Check for specific patterns
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

    def extract_property_value(self, page, property_name):
        """Extract property value from Notion page"""
        try:
            properties = page.get('properties', {})
            prop = properties.get(property_name, {})
            
            if not prop:
                return None
                
            prop_type = prop.get('type')
            
            if prop_type == 'title':
                title_array = prop.get('title', [])
                if title_array:
                    return title_array[0].get('text', {}).get('content', '')
            elif prop_type == 'rich_text':
                text_array = prop.get('rich_text', [])
                if text_array:
                    return text_array[0].get('text', {}).get('content', '')
            elif prop_type == 'select':
                select_obj = prop.get('select')
                if select_obj:
                    return select_obj.get('name', '')
            elif prop_type == 'multi_select':
                multi_select = prop.get('multi_select', [])
                return [item.get('name', '') for item in multi_select]
            elif prop_type == 'number':
                return prop.get('number')
            elif prop_type == 'checkbox':
                return prop.get('checkbox', False)
                
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting property {property_name}: {e}")
            return None

    def update_page_notes(self, page_id, notes):
        """Update Implementation Notes field for a page"""
        try:
            update_data = {
                "properties": {
                    "Implementation Notes": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": notes
                                }
                            }
                        ]
                    }
                }
            }
            
            response = requests.patch(
                f"{self.base_url}/pages/{page_id}",
                headers=self.headers,
                json=update_data
            )
            
            if response.status_code == 200:
                return True
            else:
                self.logger.error(f"❌ Failed to update page: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error updating page notes: {e}")
            return False

def main():
    """Main enhancement function"""
    enhancer = CEOActionEnhancer()
    
    print("🎯 CEO ACTION ENHANCER")
    print("="*50)
    print("Adding CEO descriptions and completion guides to all actions...")
    
    result = enhancer.enhance_all_actions()
    
    print(f"\n📊 Enhancement Results:")
    print(f"  Total Actions: {result.get('total_actions', 0)}")
    print(f"  Enhanced: {result.get('enhanced_count', 0)}")
    print(f"  Status: {result.get('status', 'unknown')}")
    
    if result.get('status') == 'success':
        print(f"\n✅ All actions now have CEO workflow guides!")
        print(f"🎯 You can now see what happens when you click 'Complete' for any action")
    
    return result

if __name__ == "__main__":
    main() 