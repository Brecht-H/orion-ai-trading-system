#!/usr/bin/env python3
"""
🔧 FIX FIELD PLACEMENT
Updates CEO workflow guide to correct field in Notion
"""

import os
import json
import requests
from datetime import datetime
import logging

class NotionFieldFixer:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = "208cba76-1065-8185-bad8-f0f1aeb99ecf"
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json", 
            "Notion-Version": "2022-06-28"
        }

    def check_page_structure(self, page_id):
        """Check all fields in a specific page"""
        try:
            response = requests.get(
                f"{self.base_url}/pages/{page_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                page = response.json()
                properties = page.get('properties', {})
                
                print("📋 Available fields in this page:")
                for field_name, field_data in properties.items():
                    field_type = field_data.get('type', 'unknown')
                    print(f"  • {field_name} ({field_type})")
                    
                    # Show content for text fields
                    if field_type in ['rich_text', 'title']:
                        content = self.extract_property_value(page, field_name)
                        if content:
                            preview = content[:50] + "..." if len(content) > 50 else content
                            print(f"    Content: {preview}")
                
                return properties
            else:
                print(f"❌ Failed to get page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error checking page structure: {e}")
            return None

    def find_defipulse_action(self):
        """Find the DeFiPulse action to examine its structure"""
        try:
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json={
                    "filter": {
                        "property": "Title",
                        "title": {
                            "contains": "DeFiPulse"
                        }
                    }
                }
            )
            
            if response.status_code == 200:
                pages = response.json().get('results', [])
                if pages:
                    page = pages[0]
                    page_id = page['id']
                    title = self.extract_property_value(page, 'Title')
                    
                    print(f"🔍 Found DeFiPulse action: {title}")
                    print(f"📋 Page ID: {page_id}")
                    
                    # Check its structure
                    self.check_page_structure(page_id)
                    
                    return page_id, page
                else:
                    print("❌ DeFiPulse action not found")
                    return None, None
            else:
                print(f"❌ Failed to search: {response.status_code}")
                return None, None
                
        except Exception as e:
            print(f"❌ Error finding DeFiPulse action: {e}")
            return None, None

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
                    
            return None
            
        except Exception as e:
            print(f"❌ Error extracting property {property_name}: {e}")
            return None

    def update_correct_field(self, page_id, field_name, content):
        """Update the correct field with CEO workflow guide"""
        try:
            update_data = {
                "properties": {
                    field_name: {
                        "rich_text": [
                            {
                                "text": {
                                    "content": content
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
                print(f"✅ Updated {field_name} field successfully!")
                return True
            else:
                print(f"❌ Failed to update {field_name}: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating {field_name}: {e}")
            return False

def main():
    """Main function"""
    print("🔧 NOTION FIELD FIXER")
    print("="*50)
    print("Checking DeFiPulse action structure and fixing field placement...")
    
    fixer = NotionFieldFixer()
    
    # Find and examine the DeFiPulse action
    page_id, page = fixer.find_defipulse_action()
    
    if page_id:
        print(f"\n📊 Current field contents:")
        properties = page.get('properties', {})
        
        # Check common field names that might contain the comment
        potential_fields = [
            'Comments', 'Notes', 'Description', 'Details', 
            'Implementation Notes', 'Progress Notes', 'Status Notes'
        ]
        
        found_field = None
        for field_name in potential_fields:
            if field_name in properties:
                content = fixer.extract_property_value(page, field_name)
                if content and ("defipulse" in content.lower() or "defi" in content.lower()):
                    print(f"🎯 Found target field: {field_name}")
                    print(f"   Current content: {content}")
                    found_field = field_name
                    break
        
        if found_field:
            # Generate CEO workflow guide for DeFiPulse
            ceo_guide = """🔐 **ACT_017_GEN**: Add DeFiPulse API - Security & API Management

📋 **CEO WORKFLOW GUIDE**

🎯 **COMPLETE** → System will execute this action automatically right now
⏸️ **WAIT** → System will prepare everything but wait for your final approval
🚫 **BLOCKED** → System will analyze what's preventing implementation

📊 **WHAT HAPPENS WHEN YOU CLICK COMPLETE:**

✅ **Action**: System will implement security measures with API configuration and testing
⏱️ **Duration**: 10-20 minutes
🛡️ **Risk Level**: Medium (security changes, tested)
🎯 **Success**: Security implementation verified and all connections tested

📋 **Prerequisites Needed:**
• Security requirements reviewed
• API credentials available
• Testing environment ready

📝 **NEXT STEPS AFTER COMPLETION:**
• Monitor security metrics
• Verify all integrations working
• Update documentation

🔒 **Safety Features:**
• Automatic testing before deployment
• Rollback capability if issues detected
• Real-time monitoring during implementation
• Immediate alerts for any problems

---
*Powered by Orion CEO Action Flow System*"""
            
            # Update the field
            success = fixer.update_correct_field(page_id, found_field, ceo_guide)
            
            if success:
                print(f"\n🎉 FIELD PLACEMENT FIXED!")
                print(f"✅ CEO workflow guide added to {found_field} field")
                print(f"🎯 Ready to continue with next steps!")
                return True
        else:
            print("❌ Could not find the field containing DeFiPulse comment")
            return False
    
    return False

if __name__ == "__main__":
    main() 