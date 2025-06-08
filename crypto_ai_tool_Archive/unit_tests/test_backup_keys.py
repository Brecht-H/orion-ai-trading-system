#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()
import os

backup_keys = {
    'BYBIT_API_KEY_V2': os.getenv('BYBIT_API_KEY_V2'),
    'BYBIT_API_SECRET_V2': os.getenv('BYBIT_API_SECRET_V2'),
    'NOTION_TOKEN_V2': os.getenv('NOTION_TOKEN_V2'),
    'HUGGINGFACE_TOKEN_V2': os.getenv('HUGGINGFACE_TOKEN_V2'),
    'API_Groq_V2': os.getenv('API_Groq_V2'),
    'API_Mistral_V2': os.getenv('API_Mistral_V2')
}

ready_count = 0
for key, value in backup_keys.items():
    if value and not value.startswith('get_new_'):
        ready_count += 1
        print(f'✅ {key}: Ready')
    else:
        print(f'❌ {key}: {value or "Missing"}')

print(f'\nTotal Ready: {ready_count}/6 ({round(ready_count/6*100, 1)}%)')

if ready_count == 6:
    print("🎯 ALL BACKUP KEYS READY - ACT_011 can now be implemented!")
else:
    print(f"⚠️ Still need {6-ready_count} more backup keys for ACT_011") 