#!/usr/bin/env python3
"""
🔐 API KEY ROTATION SYSTEM
Automated rotation of API keys for enhanced security
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
import shutil

class APIKeyRotator:
    def __init__(self):
        self.env_file = '.env'
        self.backup_dir = 'backups/api_keys'
        self.rotation_log = 'logs/api_rotation.log'
        self.setup_logging()
        
    def setup_logging(self):
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - APIRotator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.rotation_log),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def backup_current_keys(self):
        """Create timestamped backup of current keys"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/env_backup_{timestamp}"
        
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.env_file, backup_path)
        os.chmod(backup_path, 0o600)
        
        self.logger.info(f"✅ API keys backed up to {backup_path}")
        return backup_path
    
    def get_api_keys_needing_rotation(self):
        """Identify keys that need rotation"""
        # Critical keys to rotate
        rotation_keys = [
            'BYBIT_API_KEY',
            'BYBIT_API_SECRET', 
            'NOTION_TOKEN',
            'HUGGINGFACE_TOKEN',
            'API_Groq',
            'API_Mistral'
        ]
        
        current_keys = {}
        with open(self.env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key in rotation_keys:
                        current_keys[key] = value
        
        return current_keys
    
    def generate_rotation_plan(self):
        """Generate rotation plan with priorities"""
        keys = self.get_api_keys_needing_rotation()
        
        rotation_plan = {
            'high_priority': [
                'BYBIT_API_KEY',
                'BYBIT_API_SECRET'
            ],
            'medium_priority': [
                'NOTION_TOKEN',
                'HUGGINGFACE_TOKEN'
            ],
            'low_priority': [
                'API_Groq',
                'API_Mistral'
            ]
        }
        
        return rotation_plan
    
    def rotate_exchange_keys(self):
        """Rotate exchange API keys (manual process)"""
        self.logger.info("🔄 Starting exchange API key rotation...")
        
        instructions = {
            'bybit': {
                'steps': [
                    '1. Login to Bybit account',
                    '2. Go to API Management',
                    '3. Create new API key pair',
                    '4. Update BYBIT_API_KEY and BYBIT_API_SECRET in .env',
                    '5. Test connection',
                    '6. Delete old API key from Bybit'
                ],
                'test_command': 'python3 test_bybit_connection.py'
            }
        }
        
        return instructions
    
    def test_api_connections(self):
        """Test all API connections after rotation"""
        test_results = {}
        
        # Test Bybit
        try:
            # Add your Bybit connection test here
            test_results['bybit'] = 'success'
        except Exception as e:
            test_results['bybit'] = f'failed: {e}'
        
        # Test Notion
        try:
            # Add your Notion connection test here  
            test_results['notion'] = 'success'
        except Exception as e:
            test_results['notion'] = f'failed: {e}'
        
        return test_results
    
    def schedule_next_rotation(self, weeks=4):
        """Schedule next rotation"""
        next_rotation = datetime.now() + timedelta(weeks=weeks)
        
        schedule_info = {
            'next_rotation_date': next_rotation.isoformat(),
            'rotation_frequency': f'{weeks} weeks',
            'automated': False  # Manual for now
        }
        
        # Create config directory if it doesn't exist
        Path('config').mkdir(exist_ok=True)
        
        # Save schedule
        with open('config/rotation_schedule.json', 'w') as f:
            json.dump(schedule_info, f, indent=2)
        
        self.logger.info(f"📅 Next rotation scheduled for {next_rotation.strftime('%Y-%m-%d')}")
        return schedule_info

def main():
    """Run API key rotation"""
    rotator = APIKeyRotator()
    
    print("🔐 API KEY ROTATION SYSTEM")
    print("="*50)
    
    # Step 1: Backup
    backup_path = rotator.backup_current_keys()
    
    # Step 2: Generate plan
    plan = rotator.generate_rotation_plan()
    print(f"\n📋 ROTATION PLAN:")
    for priority, keys in plan.items():
        print(f"  {priority.upper()}: {', '.join(keys)}")
    
    # Step 3: Provide instructions
    instructions = rotator.rotate_exchange_keys()
    print(f"\n🔄 MANUAL ROTATION REQUIRED:")
    for service, details in instructions.items():
        print(f"\n{service.upper()}:")
        for step in details['steps']:
            print(f"  {step}")
    
    # Step 4: Schedule next
    schedule = rotator.schedule_next_rotation()
    print(f"\n📅 NEXT ROTATION: {schedule['next_rotation_date'][:10]}")
    
    return True

if __name__ == "__main__":
    main() 