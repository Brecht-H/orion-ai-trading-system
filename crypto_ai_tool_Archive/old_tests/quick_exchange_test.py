#!/usr/bin/env python3
"""
Quick Exchange Status Test - December 2025
Testing current status with correct environment variable names
"""

import os
import sys
import json
import time
import hmac
import hashlib
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_bybit():
    """Test Bybit V5 API"""
    print("\n🟡 TESTING BYBIT V5 API")
    
    api_key = os.getenv('BYBIT_API_KEY')
    secret = os.getenv('BYBIT_API_SECRET')
    
    if not api_key or not secret:
        print(f"❌ Missing credentials: API_KEY={bool(api_key)}, SECRET={bool(secret)}")
        return False
    
    try:
        # Test connection
        base_url = "https://api-testnet.bybit.com"
        response = requests.get(f"{base_url}/v5/market/time", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Connection failed: {response.status_code}")
            return False
        
        print("✅ Connection: SUCCESS")
        
        # Test authentication
        timestamp = str(int(time.time() * 1000))
        params = f"category=spot&timestamp={timestamp}"
        
        signature = hmac.new(
            secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': '5000'
        }
        
        balance_response = requests.get(
            f"{base_url}/v5/account/wallet-balance",
            headers=headers,
            params={'category': 'spot'},
            timeout=10
        )
        
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
                print(f"❌ Authentication failed: {data}")
                return False
        else:
            print(f"❌ Balance check failed: {balance_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_binance():
    """Test Binance Testnet"""
    print("\n🟡 TESTING BINANCE TESTNET")
    
    api_key = os.getenv('BINANCE_API_KEY')
    secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not secret:
        print(f"❌ Missing credentials: API_KEY={bool(api_key)}, SECRET={bool(secret)}")
        return False
    
    try:
        base_url = "https://testnet.binance.vision"
        
        # Test connection
        response = requests.get(f"{base_url}/api/v3/time", timeout=10)
        if response.status_code != 200:
            print(f"❌ Connection failed: {response.status_code}")
            return False
        
        print("✅ Connection: SUCCESS")
        
        # Test authentication
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        
        signature = hmac.new(
            secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {'X-MBX-APIKEY': api_key}
        params = {'timestamp': timestamp, 'signature': signature}
        
        account_response = requests.get(
            f"{base_url}/api/v3/account",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if account_response.status_code == 200:
            data = account_response.json()
            print("✅ Authentication: SUCCESS")
            
            # Extract USDT balance
            usdt_balance = 0
            for balance in data.get('balances', []):
                if balance['asset'] == 'USDT':
                    usdt_balance = float(balance['free'])
                    break
            
            print(f"✅ Balance: ${usdt_balance:,.2f} USDT")
            return True
        else:
            print(f"❌ Authentication failed: {account_response.status_code} - {account_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_coinbase():
    """Test Coinbase Advanced Trade API"""
    print("\n🟡 TESTING COINBASE ADVANCED TRADE")
    
    api_key = os.getenv('COINBASE_API_KEY')
    secret = os.getenv('COINBASE_SECRET')
    passphrase = os.getenv('COINBASE_PASSPHRASE')
    
    if not api_key or not secret or not passphrase:
        print(f"❌ Missing credentials: API_KEY={bool(api_key)}, SECRET={bool(secret)}, PASSPHRASE={bool(passphrase)}")
        return False
    
    try:
        base_url = "https://api.coinbase.com"
        
        # Test connection
        response = requests.get(f"{base_url}/api/v2/time", timeout=10)
        if response.status_code != 200:
            print(f"❌ Connection failed: {response.status_code}")
            return False
        
        print("✅ Connection: SUCCESS")
        
        # Test authentication with proper + character handling
        timestamp = str(int(time.time()))
        method = 'GET'
        request_path = '/api/v2/accounts'
        body = ''
        
        message = timestamp + method + request_path + body
        
        # Properly decode the secret (it contains + character)
        try:
            secret_decoded = base64.b64decode(secret)
        except Exception as e:
            print(f"❌ Secret decoding failed: {e}")
            return False
        
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
        
        accounts_response = requests.get(
            f"{base_url}/api/v2/accounts",
            headers=headers,
            timeout=10
        )
        
        if accounts_response.status_code == 200:
            data = accounts_response.json()
            print("✅ Authentication: SUCCESS")
            
            # Extract USD balance
            usd_balance = 0
            for account in data.get('data', []):
                if account.get('currency') == 'USD':
                    usd_balance = float(account.get('balance', {}).get('amount', 0))
                    break
            
            print(f"✅ Balance: ${usd_balance:,.2f} USD")
            return True
        else:
            print(f"❌ Authentication failed: {accounts_response.status_code} - {accounts_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_phemex():
    """Test Phemex Testnet"""
    print("\n🟡 TESTING PHEMEX TESTNET")
    
    api_key = os.getenv('PHEMEX_API_KEY')
    secret = os.getenv('PHEMEX_API_SECRET')
    
    if not api_key or not secret:
        print(f"❌ Missing credentials: API_KEY={bool(api_key)}, SECRET={bool(secret)}")
        return False
    
    try:
        base_url = "https://testnet-api.phemex.com"
        
        # Test connection
        response = requests.get(f"{base_url}/public/products", timeout=10)
        if response.status_code != 200:
            print(f"❌ Connection failed: {response.status_code}")
            return False
        
        print("✅ Connection: SUCCESS")
        
        # Test authentication
        timestamp = str(int(time.time()))
        method = 'GET'
        request_path = '/accounts/accountPositions'
        query_string = f'currency=USD'
        
        message = request_path + query_string + timestamp
        
        signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'x-phemex-access-token': api_key,
            'x-phemex-request-signature': signature,
            'x-phemex-request-timestamp': timestamp
        }
        
        account_response = requests.get(
            f"{base_url}/accounts/accountPositions",
            headers=headers,
            params={'currency': 'USD'},
            timeout=10
        )
        
        if account_response.status_code == 200:
            data = account_response.json()
            print("✅ Authentication: SUCCESS")
            
            # Extract balance
            usd_balance = 0
            if 'data' in data and 'account' in data['data']:
                account = data['data']['account']
                usd_balance = account.get('accountBalanceEv', 0) / 10000  # Phemex uses scaled integers
            
            print(f"✅ Balance: ${usd_balance:,.2f} USD")
            return True
        else:
            print(f"❌ Authentication failed: {account_response.status_code} - {account_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_kraken():
    """Test Kraken Public API"""
    print("\n🟡 TESTING KRAKEN PUBLIC API")
    
    try:
        base_url = "https://api.kraken.com"
        
        # Test connection and market data
        response = requests.get(f"{base_url}/0/public/Ticker?pair=XBTUSD", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                print("✅ Connection: SUCCESS")
                
                # Extract BTC price
                btc_price = 0
                if 'XXBTZUSD' in data['result']:
                    btc_price = float(data['result']['XXBTZUSD']['c'][0])
                
                print(f"✅ Market Data: BTC ${btc_price:,.2f}")
                return True
            else:
                print(f"❌ Invalid response: {data}")
                return False
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 QUICK EXCHANGE STATUS TEST")
    print("=" * 50)
    
    results = {}
    
    # Test all exchanges
    results['bybit'] = test_bybit()
    results['binance'] = test_binance()
    results['coinbase'] = test_coinbase()
    results['phemex'] = test_phemex()
    results['kraken'] = test_kraken()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    working_count = sum(results.values())
    total_count = len(results)
    
    for exchange, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {exchange.upper()}: {'WORKING' if status else 'FAILED'}")
    
    print(f"\n🎯 WORKING EXCHANGES: {working_count}/{total_count}")
    
    if working_count >= 2:
        print("🟢 READY FOR MULTI-EXCHANGE TRADING")
    elif working_count >= 1:
        print("🟡 LIMITED TRADING POSSIBLE")
    else:
        print("🔴 NO EXCHANGES WORKING - NEED FIXES")

if __name__ == "__main__":
    main() 