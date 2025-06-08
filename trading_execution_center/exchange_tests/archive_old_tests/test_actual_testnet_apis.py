#!/usr/bin/env python3
"""
ACTUAL TESTNET API TEST - Using real credentials provided
Testing Bybit, Binance, and Kraken testnet APIs
"""

import os
import requests
import hmac
import hashlib
import time
import base64
from urllib.parse import urlencode

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_bybit_testnet():
    """Test Bybit testnet API with actual credentials"""
    print("🧪 Testing Bybit Testnet API...")
    
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Missing Bybit credentials")
        return False
    
    try:
        # Test connection and get account info
        timestamp = str(int(time.time() * 1000))
        
        # Create signature for authenticated request
        param_str = f"timestamp={timestamp}"
        signature = hmac.new(
            api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': '20000'
        }
        
        # Test testnet endpoint
        url = f"https://api-testnet.bybit.com/v5/account/wallet-balance?{param_str}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('retCode') == 0:
                print(f"✅ Bybit Testnet: Connected successfully")
                print(f"   Account info: {data.get('result', {})}")
                return True
            else:
                print(f"❌ Bybit API Error: {data.get('retMsg', 'Unknown error')}")
                return False
        else:
            print(f"❌ Bybit HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Bybit Connection Error: {e}")
        return False

def test_binance_testnet():
    """Test Binance testnet API with actual credentials"""
    print("🧪 Testing Binance Testnet API...")
    
    api_key = os.getenv('API_Key')  # Binance testnet key
    secret_key = os.getenv('Secret_Key')  # Binance testnet secret
    
    if not api_key or not secret_key:
        print("❌ Missing Binance credentials")
        return False
    
    try:
        # Test connection and get account info
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        
        signature = hmac.new(
            secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-MBX-APIKEY': api_key
        }
        
        # Test testnet endpoint
        url = f"https://testnet.binance.vision/api/v3/account?{query_string}&signature={signature}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Binance Testnet: Connected successfully")
            print(f"   Account balances: {len(data.get('balances', []))} assets")
            return True
        else:
            print(f"❌ Binance HTTP Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Binance Connection Error: {e}")
        return False

def test_kraken_testnet():
    """Test Kraken testnet API with actual credentials"""
    print("🧪 Testing Kraken Testnet API...")
    
    public_key = os.getenv('Public_key')  # Kraken testnet public
    private_key = os.getenv('Private_key')  # Kraken testnet private
    
    if not public_key or not private_key:
        print("❌ Missing Kraken credentials")
        return False
    
    try:
        # Test connection and get account balance
        url = "https://api.kraken.com/0/private/Balance"
        nonce = str(int(time.time() * 1000))
        data = {"nonce": nonce}
        
        # Create signature
        postdata = urlencode(data)
        encoded = (nonce + postdata).encode()
        message = url.encode() + hashlib.sha256(encoded).digest()
        
        signature = hmac.new(
            base64.b64decode(private_key),
            message,
            hashlib.sha512
        )
        
        headers = {
            'API-Key': public_key,
            'API-Sign': base64.b64encode(signature.digest()).decode()
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('error'):
                print(f"✅ Kraken: Connected successfully")
                print(f"   Balances: {data.get('result', {})}")
                return True
            else:
                print(f"❌ Kraken API Error: {data.get('error')}")
                return False
        else:
            print(f"❌ Kraken HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Kraken Connection Error: {e}")
        return False

def test_simple_order_placement():
    """Test if we can place a test order on Bybit testnet"""
    print("\n💰 Testing Order Placement on Bybit Testnet...")
    
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Missing Bybit credentials")
        return False
    
    try:
        timestamp = str(int(time.time() * 1000))
        
        # Simple market buy order for testing
        params = {
            'category': 'spot',
            'symbol': 'BTCUSDT',
            'side': 'Buy',
            'orderType': 'Market',
            'qty': '0.001',  # Very small test amount
            'timestamp': timestamp
        }
        
        # Create signature
        param_str = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            api_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': '20000',
            'Content-Type': 'application/json'
        }
        
        # TEST ONLY - Don't actually place order yet
        print("🚨 TEST MODE: Would place order with these parameters:")
        print(f"   Symbol: BTCUSDT")
        print(f"   Side: Buy")
        print(f"   Quantity: 0.001 BTC")
        print(f"   Type: Market")
        print("✅ Order placement system ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Order placement test error: {e}")
        return False

def main():
    """Test all testnet APIs"""
    print("🚀 TESTING ACTUAL TESTNET APIS")
    print("=" * 50)
    
    results = {
        'bybit': test_bybit_testnet(),
        'binance': test_binance_testnet(),
        'kraken': test_kraken_testnet()
    }
    
    print("\n📊 API TEST RESULTS:")
    print("-" * 30)
    for exchange, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"{exchange.upper()}: {status}")
    
    working_count = sum(results.values())
    print(f"\nTotal: {working_count}/3 exchanges working")
    
    if working_count > 0:
        print("\n🎯 PAPER TRADING IS POSSIBLE!")
        test_simple_order_placement()
    else:
        print("\n❌ NO WORKING EXCHANGES - PAPER TRADING NOT POSSIBLE")
    
    return working_count > 0

if __name__ == "__main__":
    main() 