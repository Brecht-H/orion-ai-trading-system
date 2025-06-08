#!/usr/bin/env python3
"""
Test Coinbase met IP whitelist (192.168.68.255)
"""

import os
import hmac
import hashlib
import time
import base64
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def test_coinbase_whitelist():
    # Use Coinbase testnet2 (f85e7f17b44f06f5dea11e229b314803)
    passphrase = "p5xihrg7ezmm"
    api_key = "f85e7f17b44f06f5dea11e229b314803"
    secret_key = "TSEw2UuuxiYaTO1lMmnxz/aRNEG04Xt4olp1WSkY0nf0Yn+RGxzKmy1TOjW8ndF5gxUGk7flPIjyIYJT02KhCA=="
    
    print(f"🔑 Testing Coinbase API Key: {api_key}")
    print(f"🔒 IP Whitelist: 192.168.68.255")
    
    try:
        timestamp = str(time.time())
        path = '/accounts'
        method = 'GET'
        body = ''
        
        # Create message for signature
        message = f"{timestamp}{method}{path}{body}"
        
        # Decode base64 secret
        secret_decoded = base64.b64decode(secret_key)
        
        # Create signature
        signature = hmac.new(
            secret_decoded,
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        headers = {
            'CB-ACCESS-KEY': api_key,
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': passphrase,
            'Content-Type': 'application/json'
        }
        
        url = f"https://api-public.sandbox.exchange.coinbase.com{path}"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ COINBASE SANDBOX SUCCESS!")
            data = response.json()
            print(f"💰 Found {len(data)} accounts")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Coinbase IP Whitelist")
    print("=" * 40)
    test_coinbase_whitelist() 