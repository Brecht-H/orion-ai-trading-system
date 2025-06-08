#!/usr/bin/env python3
"""
Bybit V5 API Fixed Test - Correct signature method
"""

import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

def test_bybit_v5_fixed():
    """Test Bybit V5 API with correct signature method"""
    print("🟡 TESTING BYBIT V5 API (FIXED SIGNATURE)")
    
    api_key = os.getenv('BYBIT_API_KEY')
    secret = os.getenv('BYBIT_API_SECRET')
    
    if not api_key or not secret:
        print("❌ Missing credentials")
        return False
    
    try:
        base_url = "https://api-testnet.bybit.com"
        
        # Test connection first
        response = requests.get(f"{base_url}/v5/market/time", timeout=10)
        if response.status_code != 200:
            print(f"❌ Connection failed: {response.status_code}")
            return False
        
        print("✅ Connection: SUCCESS")
        
        # Correct V5 API signature method
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        # For GET request with query parameters
        query_params = "category=spot"
        
        # V5 signature: timestamp + api_key + recv_window + query_params
        param_str = timestamp + api_key + recv_window + query_params
        
        signature = hmac.new(
            secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window
        }
        
        # Test wallet balance
        balance_response = requests.get(
            f"{base_url}/v5/account/wallet-balance",
            headers=headers,
            params={'category': 'spot'},
            timeout=10
        )
        
        print(f"Response status: {balance_response.status_code}")
        print(f"Response: {balance_response.text}")
        
        if balance_response.status_code == 200:
            data = balance_response.json()
            if data.get('retCode') == 0:
                print("✅ Authentication: SUCCESS")
                
                # Extract balance
                balances = data.get('result', {}).get('list', [])
                total_usd = 0
                
                for account in balances:
                    for coin in account.get('coin', []):
                        if coin['coin'] == 'USDT':
                            total_usd += float(coin.get('walletBalance', 0))
                
                print(f"✅ Balance: ${total_usd:,.2f} USDT")
                return True
            else:
                print(f"❌ API Error: {data}")
                return False
        else:
            print(f"❌ HTTP Error: {balance_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_bybit_v5_fixed() 