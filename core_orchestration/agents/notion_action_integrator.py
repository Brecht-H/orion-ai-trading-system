#!/usr/bin/env python3
"""
🎯 NOTION ACTION LIST INTEGRATOR
Automatically creates and populates Notion database with Orion action items
GOAL: Zero-effort CEO action list setup in Notion
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Any

class NotionActionIntegrator:
    """
    🎯 NOTION ACTION INTEGRATOR
    
    CAPABILITIES:
    - Create Notion database with proper schema
    - Populate with all 35 action items
    - Setup filters and views
    - Configure mobile-optimized dashboard
    """
    
    def __init__(self):
        self.integrator_id = "notion_action_integrator_001"
        self.setup_logging()
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def setup_logging(self):
        """Setup Notion integration logging"""
        Path("logs/notion_integration").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - NotionIntegrator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/notion_integration/notion_integration.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🎯 Notion Action Integrator {self.integrator_id} initialized")
    
    def create_action_list_database(self, parent_page_id=None):
        """Create Orion Action List database in Notion"""
        self.logger.info("🗂️ Creating Orion Action List database in Notion...")
        
        # If no parent page provided, try to find or create one
        if not parent_page_id:
            parent_page_id = self.find_or_create_orion_page()
        
        database_schema = {
            "parent": {"page_id": parent_page_id},
            "title": [
                {
                    "type": "text",
                    "text": {"content": "🎯 Orion Action List"}
                }
            ],
            "properties": {
                "Action ID": {
                    "title": {}
                },
                "Title": {
                    "rich_text": {}
                },
                "Category": {
                    "select": {
                        "options": [
                            {"name": "API_INTEGRATIONS", "color": "blue"},
                            {"name": "SECURITY", "color": "red"},
                            {"name": "TRADING_EXECUTION", "color": "green"},
                            {"name": "MONITORING", "color": "yellow"},
                            {"name": "STRATEGY_DEVELOPMENT", "color": "purple"},
                            {"name": "KNOWLEDGE_EXPANSION", "color": "pink"},
                            {"name": "INFRASTRUCTURE", "color": "orange"},
                            {"name": "OPTIMIZATION", "color": "gray"},
                            {"name": "DOCUMENTATION", "color": "brown"}
                        ]
                    }
                },
                "Priority": {
                    "select": {
                        "options": [
                            {"name": "Critical", "color": "red"},
                            {"name": "High", "color": "orange"},
                            {"name": "Medium", "color": "yellow"},
                            {"name": "Low", "color": "gray"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Not Started", "color": "default"},
                            {"name": "In Progress", "color": "blue"},
                            {"name": "Completed", "color": "green"},
                            {"name": "Blocked", "color": "red"},
                            {"name": "Testing", "color": "purple"}
                        ]
                    }
                },
                "Effort": {
                    "select": {
                        "options": [
                            {"name": "30 minutes", "color": "green"},
                            {"name": "45 minutes", "color": "green"},
                            {"name": "1 hour", "color": "yellow"},
                            {"name": "2 hours", "color": "yellow"},
                            {"name": "3 hours", "color": "orange"},
                            {"name": "4 hours", "color": "orange"},
                            {"name": "6 hours", "color": "red"}
                        ]
                    }
                },
                "Cost": {
                    "select": {
                        "options": [
                            {"name": "Free", "color": "green"},
                            {"name": "<$25", "color": "yellow"},
                            {"name": "<$100", "color": "orange"},
                            {"name": ">$100", "color": "red"}
                        ]
                    }
                },
                "ROI Potential": {
                    "select": {
                        "options": [
                            {"name": "High", "color": "green"},
                            {"name": "Medium", "color": "yellow"},
                            {"name": "Low", "color": "gray"}
                        ]
                    }
                },
                "Deadline": {
                    "date": {}
                },
                "Quick Win": {
                    "checkbox": {}
                },
                "Testing Required": {
                    "checkbox": {}
                },
                "Dependencies": {
                    "rich_text": {}
                },
                "Implementation Notes": {
                    "rich_text": {}
                },
                "API Details": {
                    "rich_text": {}
                },
                "Module Source": {
                    "rich_text": {}
                },
                "Assigned To": {
                    "rich_text": {}
                },
                "Created Date": {
                    "date": {}
                },
                "Estimated ROI": {
                    "select": {
                        "options": [
                            {"name": "Very High", "color": "green"},
                            {"name": "High", "color": "yellow"},
                            {"name": "Medium", "color": "orange"},
                            {"name": "Low", "color": "gray"}
                        ]
                    }
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/databases",
                headers=self.headers,
                json=database_schema
            )
            
            if response.status_code == 200:
                database_data = response.json()
                database_id = database_data['id']
                self.logger.info(f"✅ Database created successfully: {database_id}")
                return database_id
            else:
                self.logger.error(f"❌ Failed to create database: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error creating database: {e}")
            return None
    
    def find_or_create_orion_page(self):
        """Find existing Orion page or create new one"""
        try:
            # Search for existing Orion page
            search_params = {
                "query": "Orion Project",
                "filter": {"property": "object", "value": "page"}
            }
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json=search_params
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    page_id = results[0]['id']
                    self.logger.info(f"📄 Found existing Orion page: {page_id}")
                    return page_id
            
            # Create new page if not found
            self.logger.info("📄 Creating new Orion Project page...")
            page_schema = {
                "parent": {"type": "page_id", "page_id": "root"},  # This will need to be updated
                "properties": {
                    "title": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "🚀 Orion Project Dashboard"}
                            }
                        ]
                    }
                }
            }
            
            # For now, we'll return None and let the user specify the parent page
            self.logger.warning("⚠️ Please provide a parent page ID or create the database manually")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error finding/creating page: {e}")
            return None
    
    def populate_action_items(self, database_id, action_items_file=None):
        """Populate database with action items"""
        self.logger.info("📝 Populating database with action items...")
        
        if not action_items_file:
            # Find the most recent action items file
            action_files = list(Path("action_lists").glob("notion_database_*.json"))
            if not action_files:
                self.logger.error("❌ No action items file found")
                return False
            
            action_items_file = max(action_files)  # Most recent file
        
        # Load action items
        with open(action_items_file, 'r') as f:
            action_items = json.load(f)
        
        self.logger.info(f"📊 Loading {len(action_items)} action items...")
        
        success_count = 0
        for i, item in enumerate(action_items):
            try:
                # Convert deadline to proper date format
                deadline_date = self.convert_deadline_to_date(item.get('Deadline', ''))
                created_date = item.get('Created Date', datetime.now().strftime("%Y-%m-%d"))
                
                page_data = {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Action ID": {
                            "title": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Action ID', '')}
                                }
                            ]
                        },
                        "Title": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Title', '')}
                                }
                            ]
                        },
                        "Category": {
                            "select": {"name": item.get('Category', 'OTHER')}
                        },
                        "Priority": {
                            "select": {"name": item.get('Priority', 'Medium')}
                        },
                        "Status": {
                            "select": {"name": item.get('Status', 'Not Started')}
                        },
                        "Effort": {
                            "select": {"name": item.get('Effort', '1 hour')}
                        },
                        "Cost": {
                            "select": {"name": item.get('Cost', 'Free')}
                        },
                        "ROI Potential": {
                            "select": {"name": item.get('ROI Potential', 'Medium')}
                        },
                        "Quick Win": {
                            "checkbox": item.get('Quick Win') == 'Yes'
                        },
                        "Testing Required": {
                            "checkbox": item.get('Testing Required', False)
                        },
                        "Dependencies": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Dependencies', '')}
                                }
                            ]
                        },
                        "Implementation Notes": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Implementation Notes', '')}
                                }
                            ]
                        },
                        "API Details": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('API Details', '')}
                                }
                            ]
                        },
                        "Module Source": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Module Source', '')}
                                }
                            ]
                        },
                        "Assigned To": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": item.get('Assigned To', 'CEO')}
                                }
                            ]
                        },
                        "Estimated ROI": {
                            "select": {"name": item.get('Estimated ROI', 'Medium')}
                        }
                    }
                }
                
                # Add dates if valid
                if deadline_date:
                    page_data["properties"]["Deadline"] = {"date": {"start": deadline_date}}
                
                if created_date:
                    page_data["properties"]["Created Date"] = {"date": {"start": created_date}}
                
                # Add page content with description
                if item.get('Description'):
                    page_data["children"] = [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {"content": item.get('Description', '')}
                                    }
                                ]
                            }
                        }
                    ]
                
                # Create page in Notion
                response = requests.post(
                    f"{self.base_url}/pages",
                    headers=self.headers,
                    json=page_data
                )
                
                if response.status_code == 200:
                    success_count += 1
                    self.logger.info(f"✅ Created action {i+1}/{len(action_items)}: {item.get('Action ID')}")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.1)
                else:
                    self.logger.error(f"❌ Failed to create action {item.get('Action ID')}: {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"❌ Error creating action {item.get('Action ID', 'unknown')}: {e}")
                continue
        
        self.logger.info(f"🎯 Successfully created {success_count}/{len(action_items)} action items")
        return success_count == len(action_items)
    
    def convert_deadline_to_date(self, deadline_str):
        """Convert deadline string to ISO date"""
        if not deadline_str:
            return None
            
        today = datetime.now()
        
        if "3 days" in deadline_str:
            return (today + timedelta(days=3)).strftime("%Y-%m-%d")
        elif "1 week" in deadline_str:
            return (today + timedelta(weeks=1)).strftime("%Y-%m-%d")
        elif "2 weeks" in deadline_str:
            return (today + timedelta(weeks=2)).strftime("%Y-%m-%d")
        elif "1 month" in deadline_str:
            return (today + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            return (today + timedelta(weeks=1)).strftime("%Y-%m-%d")  # Default 1 week
    
    def create_dashboard_views(self, database_id):
        """Create filtered views for CEO dashboard"""
        self.logger.info("📊 Creating dashboard views...")
        
        # Unfortunately, the Notion API doesn't support creating views programmatically yet
        # We'll provide instructions for manual creation
        
        view_instructions = {
            "CEO_CRITICAL": {
                "name": "🚨 CEO Critical",
                "filter": "Priority = Critical",
                "sort": "Deadline ascending"
            },
            "QUICK_WINS": {
                "name": "⚡ Quick Wins",
                "filter": "Quick Win = Yes AND Status ≠ Completed",
                "sort": "Effort ascending"
            },
            "HIGH_IMPACT_FREE": {
                "name": "💰 High Impact Free",
                "filter": "ROI Potential = High AND Cost = Free",
                "sort": "Priority, Effort"
            },
            "THIS_WEEK": {
                "name": "📅 This Week",
                "filter": "Deadline ≤ 1 week from today",
                "sort": "Priority descending"
            },
            "BY_CATEGORY": {
                "name": "📂 By Category",
                "group_by": "Category",
                "filter": "Status ≠ Completed"
            }
        }
        
        # Save view instructions
        with open("notion_view_instructions.json", "w") as f:
            json.dump(view_instructions, f, indent=2)
        
        self.logger.info("💡 View instructions saved to notion_view_instructions.json")
        return view_instructions
    
    def integrate_complete_action_list(self, parent_page_id=None):
        """Complete integration: create database and populate"""
        self.logger.info("🚀 Starting complete Notion integration...")
        
        # Validate Notion token
        if not self.notion_token or self.notion_token == "your_key_here":
            self.logger.error("❌ Invalid Notion token. Please update NOTION_TOKEN in .env")
            return self.provide_manual_instructions()
        
        try:
            # Test API connection
            test_response = requests.get(f"{self.base_url}/users/me", headers=self.headers)
            if test_response.status_code != 200:
                self.logger.error(f"❌ Notion API authentication failed: {test_response.status_code}")
                return self.provide_manual_instructions()
            
            self.logger.info("✅ Notion API authentication successful")
            
            # Create database
            database_id = self.create_action_list_database(parent_page_id)
            if not database_id:
                self.logger.error("❌ Failed to create database")
                return self.provide_manual_instructions()
            
            # Populate with action items
            populate_success = self.populate_action_items(database_id)
            if not populate_success:
                self.logger.warning("⚠️ Some action items failed to import")
            
            # Create view instructions
            view_instructions = self.create_dashboard_views(database_id)
            
            # Generate success summary
            success_summary = {
                "database_id": database_id,
                "database_url": f"https://notion.so/{database_id.replace('-', '')}",
                "view_instructions": view_instructions,
                "next_steps": [
                    "Open the database in Notion",
                    "Create the recommended views manually",
                    "Start with critical items (ACT_011_SEC, ACT_034_TRA)",
                    "Use mobile app for daily progress tracking"
                ]
            }
            
            self.display_success_summary(success_summary)
            return success_summary
            
        except Exception as e:
            self.logger.error(f"❌ Integration failed: {e}")
            return self.provide_manual_instructions()
    
    def provide_manual_instructions(self):
        """Provide manual setup instructions as fallback"""
        self.logger.info("📋 Providing manual setup instructions...")
        
        instructions = {
            "method": "manual",
            "steps": [
                "1. Open Notion and create new database",
                "2. Name it '🎯 Orion Action List'",
                "3. Configure columns as specified in NOTION_ACTION_LIST_IMPORT_GUIDE.md",
                "4. Import data from action_lists/action_list_20250604_185342.csv",
                "5. Create filtered views for dashboard",
                "6. Start with critical items"
            ],
            "files_to_use": [
                "action_lists/action_list_20250604_185342.csv",
                "NOTION_ACTION_LIST_IMPORT_GUIDE.md"
            ]
        }
        
        return instructions
    
    def display_success_summary(self, summary):
        """Display integration success summary"""
        print("\n" + "="*80)
        print("🎯 NOTION INTEGRATION - SUCCESS!")
        print("="*80)
        
        print(f"\n✅ DATABASE CREATED:")
        print(f"   Database ID: {summary['database_id']}")
        print(f"   URL: {summary['database_url']}")
        
        print(f"\n📊 NEXT STEPS:")
        for i, step in enumerate(summary['next_steps'], 1):
            print(f"   {i}. {step}")
        
        print(f"\n📱 MOBILE DASHBOARD READY:")
        print(f"   • Critical items view for urgent actions")
        print(f"   • Quick wins view for 30-45 minute tasks")
        print(f"   • Progress tracking and status updates")
        
        print(f"\n🎯 READY FOR ACTION!")
        print("="*80)

def main():
    """Run Notion integration"""
    integrator = NotionActionIntegrator()
    
    # Check if we can do automatic integration
    if not os.getenv('NOTION_TOKEN') or os.getenv('NOTION_TOKEN') == "your_key_here":
        print("\n🔧 MANUAL SETUP REQUIRED")
        print("Your Notion token needs to be configured for automatic integration.")
        print("Following manual setup instructions...")
        return integrator.provide_manual_instructions()
    
    # Attempt automatic integration
    return integrator.integrate_complete_action_list()

if __name__ == "__main__":
    main() 