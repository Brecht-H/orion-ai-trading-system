#!/usr/bin/env python3
"""
⏸️ ADD WAIT STATUS
Adds 'Wait' status option to Notion database
"""

import os
import json
import requests
from datetime import datetime
import logging

class NotionStatusUpdater:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = "208cba76-1065-8185-bad8-f0f1aeb99ecf"
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def add_wait_status(self):
        """Add 'Wait' option to the Status field"""
        print("⏸️ Adding 'Wait' status option to Notion database...")
        
        try:
            # Get current database schema
            response = requests.get(
                f"{self.base_url}/databases/{self.database_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                database = response.json()
                print("✅ Retrieved database schema")
                
                # Find Status property
                properties = database.get('properties', {})
                status_prop = properties.get('Status', {})
                
                if status_prop.get('type') == 'select':
                    current_options = status_prop.get('select', {}).get('options', [])
                    print(f"📊 Current status options: {[opt['name'] for opt in current_options]}")
                    
                    # Check if 'Wait' already exists
                    wait_exists = any(opt['name'] == 'Wait' for opt in current_options)
                    
                    if not wait_exists:
                        # Add 'Wait' option
                        new_options = current_options + [{
                            "name": "Wait",
                            "color": "yellow"
                        }]
                        
                        # Update database schema
                        update_data = {
                            "properties": {
                                "Status": {
                                    "select": {
                                        "options": new_options
                                    }
                                }
                            }
                        }
                        
                        update_response = requests.patch(
                            f"{self.base_url}/databases/{self.database_id}",
                            headers=self.headers,
                            json=update_data
                        )
                        
                        if update_response.status_code == 200:
                            print("✅ Successfully added 'Wait' status option!")
                            print("📊 New status options available:")
                            print("  • Complete")
                            print("  • In Progress") 
                            print("  • Blocked")
                            print("  • Wait ⏸️ (NEW)")
                            return True
                        else:
                            print(f"❌ Failed to update database: {update_response.status_code}")
                            print(f"Response: {update_response.text}")
                            return False
                    else:
                        print("⏭️ 'Wait' status already exists!")
                        return True
                else:
                    print("❌ Status property not found or not a select field")
                    return False
            else:
                print(f"❌ Failed to get database: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding Wait status: {e}")
            return False

def main():
    """Main function"""
    print("⏸️ NOTION STATUS UPDATER")
    print("="*50)
    print("Adding 'Wait' status option for CEO workflow...")
    
    updater = NotionStatusUpdater()
    success = updater.add_wait_status()
    
    if success:
        print(f"\n🎯 STATUS UPDATE COMPLETE!")
        print(f"✅ CEOs can now use 'Wait' status for preparation without implementation")
        print(f"📋 CEO can now use all workflow options:")
        print(f"   🎯 Complete → Immediate implementation")
        print(f"   ⏸️ Wait → Prepare but hold for approval") 
        print(f"   🚫 Blocked → Analyze blockers")
        print(f"   🔄 In Progress → Monitor and support")
    
    return success

if __name__ == "__main__":
    main() 