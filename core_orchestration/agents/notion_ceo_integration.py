#!/usr/bin/env python3
"""
🔗 NOTION CEO INTEGRATION
Connects CEO Action Flow with existing Notion Response Loop
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

class NotionCEOIntegration:
    def __init__(self):
        self.setup_logging()
        self.ceo_flow = None
        self.load_ceo_flow()
        
    def setup_logging(self):
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - NotionCEO - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/notion_ceo_integration.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_ceo_flow(self):
        """Load the CEO Action Flow system"""
        try:
            from core_orchestration.agents.ceo_action_flow import CEOActionFlow
            self.ceo_flow = CEOActionFlow()
            self.logger.info("✅ CEO Action Flow loaded successfully")
        except Exception as e:
            self.logger.error(f"❌ Failed to load CEO Action Flow: {e}")

    def detect_action_id(self, item_title, item_id=None):
        """Detect action ID from Notion item title"""
        # Common action patterns
        action_patterns = [
            'ACT_011_SEC', 'ACT_034_TRA', 'ACT_045_OPT', 'ACT_067_MON',
            'ACT_089_INT', 'ACT_012_BAC', 'ACT_023_API', 'ACT_056_DAT',
            'ACT_078_REP', 'ACT_090_DEP'
        ]
        
        title_upper = item_title.upper()
        
        for pattern in action_patterns:
            if pattern in title_upper:
                return pattern
        
        # Check for generic ACT_ pattern
        import re
        match = re.search(r'ACT_\d{3}_[A-Z]{3}', title_upper)
        if match:
            return match.group(0)
        
        return None

    def handle_notion_status_change(self, item_data):
        """Handle status change from Notion Response Loop"""
        try:
            item_title = item_data.get('title', '')
            new_status = item_data.get('status', '')
            item_id = item_data.get('id', '')
            
            self.logger.info(f"🔄 Notion status change detected: {item_title} → {new_status}")
            
            # Detect action ID
            action_id = self.detect_action_id(item_title, item_id)
            
            if action_id:
                self.logger.info(f"🎯 Action detected: {action_id}")
                
                # Process through CEO Action Flow
                if self.ceo_flow:
                    result = self.ceo_flow.process_action_status_change(
                        action_id, new_status, item_data
                    )
                    
                    # Log result
                    self.logger.info(f"✅ {action_id} processed: {result.get('status', 'unknown')}")
                    
                    return {
                        'processed': True,
                        'action_id': action_id,
                        'result': result
                    }
                else:
                    self.logger.error("❌ CEO Action Flow not available")
                    return {'processed': False, 'error': 'CEO Flow not loaded'}
            else:
                self.logger.info(f"📝 Non-action item: {item_title}")
                return {'processed': False, 'reason': 'Not an action item'}
                
        except Exception as e:
            self.logger.error(f"❌ Error handling Notion status change: {e}")
            return {'processed': False, 'error': str(e)}

    def create_action_response(self, action_id, status, result):
        """Create formatted response for Notion"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if status.lower() == 'complete':
            if result.get('status') == 'implementation_complete':
                return f"""
🎯 **{action_id} IMPLEMENTATION COMPLETE**

✅ **Status**: Successfully implemented
🕐 **Time**: {timestamp}

**Results**:
{self.format_results(result.get('results', []))}

**Next Steps**: {result.get('next_steps', 'Monitor for 24h')}

---
*Automated by Orion CEO Action Flow*
                """.strip()
            else:
                return f"""
⚠️ **{action_id} IMPLEMENTATION PENDING**

📋 **Status**: Waiting for prerequisites
🕐 **Time**: {timestamp}

**Missing Requirements**:
{self.format_list(result.get('missing', []))}

**Action Required**: Complete requirements then change status to Complete again

---
*Automated by Orion CEO Action Flow*
                """.strip()
        
        elif status.lower() == 'wait':
            return f"""
⏸️ **{action_id} READY FOR IMPLEMENTATION**

✅ **Status**: Prepared and waiting
🕐 **Time**: {timestamp}

**Preparation Complete**: All systems ready
**Action Required**: Change status to Complete when ready to implement

---
*Automated by Orion CEO Action Flow*
            """.strip()
        
        elif status.lower() == 'blocked':
            return f"""
🚫 **{action_id} BLOCKER ANALYSIS**

🔍 **Status**: Blockers identified
🕐 **Time**: {timestamp}

**Blockers Found**:
{self.format_list(result.get('blockers', []))}

**Unblock Options**:
{self.format_list(result.get('unblock_options', []))}

**Recommended Action**: {result.get('recommendation', 'Contact support')}

---
*Automated by Orion CEO Action Flow*
            """.strip()
        
        else:
            return f"""
📊 **{action_id} STATUS UPDATE**

🔄 **Status**: {status}
🕐 **Time**: {timestamp}

**Current State**: {result.get('state', 'Monitoring')}

**Available Actions**: Complete | Wait | Blocked

---
*Automated by Orion CEO Action Flow*
            """.strip()

    def format_results(self, results):
        """Format results list for display"""
        if not results:
            return "• No specific results"
        
        formatted = ""
        for result in results:
            if isinstance(result, dict):
                formatted += f"• {result.get('service', 'Unknown')}: {result.get('status', 'Unknown')}\n"
            else:
                formatted += f"• {result}\n"
        
        return formatted.strip()

    def format_list(self, items):
        """Format list items for display"""
        if not items:
            return "• None identified"
        
        return "\n".join([f"• {item}" for item in items])

    def get_integration_status(self):
        """Get current integration status"""
        return {
            'ceo_flow_loaded': self.ceo_flow is not None,
            'integration_active': True,
            'supported_actions': [
                'ACT_011_SEC', 'ACT_034_TRA', 'ACT_045_OPT', 'ACT_067_MON',
                'ACT_089_INT', 'ACT_012_BAC', 'ACT_023_API', 'ACT_056_DAT',
                'ACT_078_REP', 'ACT_090_DEP'
            ],
            'workflow': 'Complete → Implement | Wait → Prepare | Blocked → Analyze'
        }

def main():
    """Test the integration"""
    integration = NotionCEOIntegration()
    
    print("🔗 NOTION CEO INTEGRATION")
    print("="*40)
    
    # Test status
    status = integration.get_integration_status()
    print(f"\n📊 Integration Status:")
    print(f"  CEO Flow Loaded: {'✅' if status['ceo_flow_loaded'] else '❌'}")
    print(f"  Integration Active: {'✅' if status['integration_active'] else '❌'}")
    print(f"  Supported Actions: {len(status['supported_actions'])}")
    
    # Test action detection
    test_items = [
        "ACT_011_SEC: API Key Rotation Implementation",
        "ACT_034_TRA: Trading Engine Deployment", 
        "Regular task: Update documentation"
    ]
    
    print(f"\n🔍 Action Detection Test:")
    for item in test_items:
        action_id = integration.detect_action_id(item)
        icon = "🎯" if action_id else "📝"
        print(f"  {icon} '{item}' → {action_id or 'Not an action'}")
    
    return integration

if __name__ == "__main__":
    main() 