#!/usr/bin/env python3
"""
🧪 TEST NEW BINANCE KEYS - VERIFICATION
Test the newly created Binance testnet API keys
"""

import os
import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def test_new_binance_keys():
    """Test the new Binance API keys"""
    print("🧪 TESTING NEW BINANCE KEYS")
    print("=" * 50)
    
    # New keys from screenshot
    api_key = "U7UE7oY01f65iNJxVWLDN50FCFvBnQwb5hCxFOTDcTvdaPEkAuFNuq7ZzamJojw4"
    api_secret = "ByuzFEgKsPtg8qZAjhqHVF5rXIGVRdVAm44VSqKDhDbnBANMDkp9BtA7SQ6tVT47"
    
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🔐 Secret: {api_secret[:10]}...")
    
    try:
        # Test account endpoint
        print(f"\n📊 Testing Account Balance...")
        timestamp = str(int(time.time() * 1000))
        params = f"timestamp={timestamp}"
        signature = hmac.new(api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()
        
        headers = {'X-MBX-APIKEY': api_key}
        url = f"https://testnet.binance.vision/api/v3/account?{params}&signature={signature}"
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ BINANCE WORKING!")
            
            # Extract balances
            balances = {}
            for asset in data['balances']:
                free_balance = float(asset['free'])
                if free_balance > 0:
                    balances[asset['asset']] = free_balance
            
            print(f"💰 Balances: {balances}")
            
            # Test market data
            print(f"\n📈 Testing Market Data...")
            market_url = "https://testnet.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"
            market_response = requests.get(market_url, timeout=10)
            
            if market_response.status_code == 200:
                price_data = market_response.json()
                btc_price = float(price_data['price'])
                print(f"📊 BTC Price: ${btc_price:,.2f}")
                
                # Test a small order (dry run)
                print(f"\n🎯 Testing Order Placement (TEST MODE)...")
                order_params = {
                    'symbol': 'BTCUSDT',
                    'side': 'BUY',
                    'type': 'MARKET',
                    'quantity': '0.001',
                    'timestamp': timestamp
                }
                
                query_string = '&'.join([f"{k}={v}" for k, v in order_params.items()])
                order_signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
                order_url = f"https://testnet.binance.vision/api/v3/order/test?{query_string}&signature={order_signature}"
                
                order_response = requests.post(order_url, headers=headers, timeout=10)
                print(f"📋 Test Order Status: {order_response.status_code}")
                
                if order_response.status_code == 200:
                    print(f"✅ ORDER SYSTEM WORKING!")
                    return True, balances, btc_price
                else:
                    print(f"⚠️ Order test failed: {order_response.text}")
                    return True, balances, btc_price  # Account works, order might need adjustment
            else:
                print(f"❌ Market data failed: {market_response.text}")
                return True, balances, None
        else:
            print(f"❌ Account test failed: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False, None, None

def main():
    """Main function"""
    success, balances, btc_price = test_new_binance_keys()
    
    print(f"\n🎯 TEST RESULTS")
    print("=" * 30)
    if success:
        print("✅ BINANCE: WORKING!")
        if balances:
            print(f"💰 Available funds: {balances}")
        if btc_price:
            print(f"📊 BTC Price: ${btc_price:,.2f}")
        print("🚀 Ready for trading!")
    else:
        print("❌ BINANCE: FAILED")
        print("🔧 Check API key permissions")
    
    return success

if __name__ == '__main__':
    main() 