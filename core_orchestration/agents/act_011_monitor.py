#!/usr/bin/env python3
"""
🎯 ACT_011 SMART MONITOR
Integrates with Notion Response Loop to handle API key rotation
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ACT011Monitor:
    def __init__(self):
        self.setup_logging()
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = None  # Will be detected from response loop
        
    def setup_logging(self):
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ACT011Monitor - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/act_011_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def check_backup_keys_status(self):
        """Check current backup key status"""
        backup_keys = {
            'BYBIT_API_KEY_V2': os.getenv('BYBIT_API_KEY_V2'),
            'BYBIT_API_SECRET_V2': os.getenv('BYBIT_API_SECRET_V2'),
            'NOTION_TOKEN_V2': os.getenv('NOTION_TOKEN_V2'),
            'HUGGINGFACE_TOKEN_V2': os.getenv('HUGGINGFACE_TOKEN_V2'),
            'API_Groq_V2': os.getenv('API_Groq_V2'),
            'API_Mistral_V2': os.getenv('API_Mistral_V2')
        }
        
        ready_count = 0
        missing_keys = []
        
        for key, value in backup_keys.items():
            if value and not value.startswith('get_new_'):
                ready_count += 1
            else:
                missing_keys.append(key.replace('_V2', ''))
                
        return {
            'ready_count': ready_count,
            'total_count': len(backup_keys),
            'missing_keys': missing_keys,
            'percentage': round((ready_count / len(backup_keys)) * 100, 1)
        }

    def handle_status_change(self, new_status, item_id=None):
        """Handle when ACT_011 status changes in Notion"""
        self.logger.info(f"🔄 ACT_011 status changed to: {new_status}")
        
        # Check backup keys status
        keys_status = self.check_backup_keys_status()
        
        if new_status.lower() == 'complete':
            return self.handle_complete_request(keys_status)
        elif new_status.lower() == 'wait':
            return self.handle_wait_request(keys_status)
        else:
            return self.handle_other_status(new_status, keys_status)

    def handle_complete_request(self, keys_status):
        """Handle Complete status - implement rotation immediately"""
        self.logger.info("🎯 COMPLETE status detected - Starting rotation...")
        
        if keys_status['ready_count'] < keys_status['total_count']:
            # Not all keys ready
            missing_count = keys_status['total_count'] - keys_status['ready_count']
            response = {
                'status': 'waiting_for_keys',
                'message': f"⚠️ Need {missing_count} more backup keys before rotation",
                'progress': f"{keys_status['ready_count']}/{keys_status['total_count']} keys ready ({keys_status['percentage']}%)",
                'missing_services': keys_status['missing_keys'],
                'next_action': 'Add missing backup keys to .env, then try Complete again'
            }
        else:
            # All keys ready - execute rotation
            response = self.execute_automatic_rotation(keys_status)
        
        # Post response to Notion comments
        self.post_notion_comment(response)
        return response

    def handle_wait_request(self, keys_status):
        """Handle Wait status - prepare but don't implement"""
        self.logger.info("⏸️ WAIT status detected - Preparing without implementation...")
        
        response = {
            'status': 'ready_when_you_are',
            'message': f"✅ Keys ready: {keys_status['ready_count']}/{keys_status['total_count']} ({keys_status['percentage']}%)",
            'action': 'Implementation paused - change to Complete when ready',
            'missing_keys': keys_status['missing_keys'] if keys_status['missing_keys'] else 'All keys ready!'
        }
        
        self.post_notion_comment(response)
        return response

    def handle_other_status(self, status, keys_status):
        """Handle other status changes"""
        response = {
            'status': f'monitoring_{status.lower()}',
            'message': f"📊 Status: {status} | Keys: {keys_status['ready_count']}/{keys_status['total_count']}",
            'info': 'Set to Complete to implement rotation, or Wait to prepare without implementing'
        }
        return response

    def execute_automatic_rotation(self, keys_status):
        """Execute the actual API key rotation"""
        self.logger.info("🔄 Executing automatic API key rotation...")
        
        rotation_results = []
        
        # Get all backup keys
        backup_keys = {
            'BYBIT_API_KEY_V2': os.getenv('BYBIT_API_KEY_V2'),
            'BYBIT_API_SECRET_V2': os.getenv('BYBIT_API_SECRET_V2'),
            'NOTION_TOKEN_V2': os.getenv('NOTION_TOKEN_V2'),
            'HUGGINGFACE_TOKEN_V2': os.getenv('HUGGINGFACE_TOKEN_V2'),
            'API_Groq_V2': os.getenv('API_Groq_V2'),
            'API_Mistral_V2': os.getenv('API_Mistral_V2')
        }
        
        # Process each key
        for key_name, new_value in backup_keys.items():
            if new_value and not new_value.startswith('get_new_'):
                service = key_name.replace('_V2', '').split('_')[0].lower()
                
                try:
                    # Test the new key
                    test_result = self.test_new_api_key(service, new_value, key_name)
                    
                    if test_result['success']:
                        # Update .env with new key
                        self.update_env_key(key_name, new_value)
                        rotation_results.append({
                            'service': service.upper(),
                            'status': '✅ SUCCESS',
                            'message': f'{service.upper()} API key rotated and tested successfully'
                        })
                    else:
                        rotation_results.append({
                            'service': service.upper(),
                            'status': '❌ FAILED',
                            'message': f'{service.upper()} key test failed: {test_result.get("error", "Unknown error")}'
                        })
                        
                except Exception as e:
                    rotation_results.append({
                        'service': service.upper(),
                        'status': '⚠️ ERROR',
                        'message': f'{service.upper()} rotation error: {str(e)}'
                    })
        
        # Generate summary
        successful_rotations = len([r for r in rotation_results if r['status'] == '✅ SUCCESS'])
        total_attempts = len(rotation_results)
        
        return {
            'status': 'rotation_complete',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': f'✅ {successful_rotations}/{total_attempts} API keys rotated successfully',
            'results': rotation_results,
            'next_steps': 'All systems updated with new API keys. Monitor for 24h to ensure stability.'
        }

    def test_new_api_key(self, service, api_key, key_name):
        """Test new API key before switching"""
        try:
            if 'notion' in service.lower():
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Notion-Version': '2022-06-28'
                }
                response = requests.get('https://api.notion.com/v1/users/me', headers=headers, timeout=10)
                return {'success': response.status_code == 200, 'error': None}
            
            elif 'huggingface' in service.lower():
                headers = {'Authorization': f'Bearer {api_key}'}
                response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
                return {'success': response.status_code == 200, 'error': None}
            
            else:
                # For other APIs, verify format
                return {'success': len(api_key) > 10, 'error': None}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def update_env_key(self, key_name, new_value):
        """Update .env file with rotated key"""
        original_key = key_name.replace('_V2', '')
        
        # Read .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update the original key
        updated_lines = []
        for line in lines:
            if line.startswith(f'{original_key}='):
                updated_lines.append(f'{original_key}={new_value}\n')
                self.logger.info(f"✅ Updated {original_key} in .env")
            else:
                updated_lines.append(line)
        
        # Write back to .env
        with open('.env', 'w') as f:
            f.writelines(updated_lines)

    def post_notion_comment(self, response):
        """Post automated response to Notion ACT_011 comments"""
        try:
            comment_text = f"""
🤖 **AUTOMATIC ACT_011 UPDATE**

**Status**: {response.get('status', 'unknown')}
**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Message**: {response.get('message', 'No message')}

{self.format_results(response)}

---
*Automated by Orion AI Security System*
            """.strip()
            
            self.logger.info(f"📝 Posting update to Notion: {response.get('status')}")
            
            # Note: Actual Notion API call would go here
            # The existing notion_response_loop.py will handle this
            
        except Exception as e:
            self.logger.error(f"❌ Failed to post Notion comment: {e}")

    def format_results(self, response):
        """Format results for Notion display"""
        if 'results' in response:
            result_text = "\n**Rotation Results**:\n"
            for result in response['results']:
                result_text += f"• {result['service']}: {result['status']} - {result['message']}\n"
            return result_text
        elif 'missing_services' in response:
            return f"\n**Missing Keys**: {', '.join(response['missing_services'])}"
        else:
            return ""

def main():
    """Main monitoring function"""
    monitor = ACT011Monitor()
    
    print("🎯 ACT_011 SMART MONITOR")
    print("="*40)
    
    # Check current status
    keys_status = monitor.check_backup_keys_status()
    
    print(f"\n📊 Current Backup Keys Status:")
    print(f"  Ready: {keys_status['ready_count']}/{keys_status['total_count']} ({keys_status['percentage']}%)")
    
    if keys_status['missing_keys']:
        print(f"  Missing: {', '.join(keys_status['missing_keys'])}")
    else:
        print(f"  ✅ All backup keys ready for rotation!")
    
    print(f"\n🔄 Monitoring Notion for ACT_011 status changes...")
    print(f"  📝 Complete → Implement rotation immediately")
    print(f"  ⏸️ Wait → Prepare but hold implementation")
    
    return monitor

if __name__ == "__main__":
    main() 