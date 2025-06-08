#!/usr/bin/env python3
"""
🔍 BYBIT MINIMUM ORDER VALUE TEST
Find the exact minimum order value and test automation

GOAL: Determine minimum order size for automated trading
"""

import os
import requests
import json
import time
import hmac
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BybitMinimumOrderTest:
    def __init__(self):
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.secret = os.getenv('BYBIT_API_SECRET')
        self.base_url = "https://api-testnet.bybit.com"
        
        print("🔍 BYBIT MINIMUM ORDER VALUE TEST")
        print("=" * 50)
    
    def create_signature_for_post(self, order_params):
        """Signature for POST requests (orders)"""
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        json_body = json.dumps(order_params, separators=(',', ':'), sort_keys=True)
        sign_string = timestamp + self.api_key + recv_window + json_body
        
        signature = hmac.new(
            self.secret.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature, timestamp, recv_window, json_body
    
    def get_btc_price(self):
        """Get current BTC price"""
        response = requests.get(
            f"{self.base_url}/v5/market/tickers",
            params={'category': 'spot', 'symbol': 'BTCUSDT'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('retCode') == 0:
                price = float(data['result']['list'][0]['lastPrice'])
                return price
        return 0
    
    def test_order_amount(self, usdt_amount):
        """Test order with specific USDT amount"""
        print(f"\n🧪 Testing ${usdt_amount:.2f} order...")
        
        btc_price = self.get_btc_price()
        if btc_price == 0:
            print("❌ Cannot get BTC price")
            return False
        
        btc_qty = round(usdt_amount / btc_price, 6)
        
        print(f"   📊 BTC Price: ${btc_price:,.2f}")
        print(f"   📈 BTC Quantity: {btc_qty}")
        print(f"   💰 Order Value: ${usdt_amount:.2f}")
        
        # Order parameters
        order_params = {
            'category': 'spot',
            'symbol': 'BTCUSDT',
            'side': 'Buy',
            'orderType': 'Market',
            'qty': str(btc_qty)
        }
        
        # Create signature
        signature, timestamp, recv_window, json_body = self.create_signature_for_post(order_params)
        
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'Content-Type': 'application/json'
        }
        
        # Execute order
        response = requests.post(
            f"{self.base_url}/v5/order/create",
            headers=headers,
            data=json_body,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('retCode') == 0:
                order_id = data.get('result', {}).get('orderId', 'N/A')
                print(f"   ✅ SUCCESS! Order ID: {order_id}")
                return True
            else:
                error_msg = data.get('retMsg', 'Unknown error')
                print(f"   ❌ FAILED: {error_msg}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
    
    def find_minimum_order(self):
        """Find minimum order value by testing different amounts"""
        print(f"\n🔍 FINDING MINIMUM ORDER VALUE")
        print("=" * 50)
        
        # Test different amounts
        test_amounts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        for amount in test_amounts:
            success = self.test_order_amount(amount)
            if success:
                print(f"\n🎉 MINIMUM ORDER FOUND: ${amount:.2f}")
                print(f"✅ Bybit automation possible with ${amount:.2f}+ orders")
                return amount
            
            # Wait between tests
            time.sleep(1)
        
        print(f"\n❌ Could not find working minimum (tested up to $100)")
        return None
    
    def test_automation_with_minimum(self, min_amount):
        """Test automation with the found minimum amount"""
        if min_amount is None:
            print("\n❌ Cannot test automation - no working minimum found")
            return False
        
        print(f"\n🤖 TESTING AUTOMATION WITH ${min_amount:.2f}")
        print("=" * 50)
        
        # Test with minimum + buffer
        test_amount = min_amount + 10
        success = self.test_order_amount(test_amount)
        
        if success:
            print(f"\n🎉 AUTOMATION CONFIRMED!")
            print(f"✅ Bybit ready for automated trading")
            print(f"💰 Minimum order: ${min_amount:.2f}")
            print(f"🎯 Recommended amount: ${test_amount:.2f}+")
            return True
        else:
            print(f"\n❌ Automation failed even with ${test_amount:.2f}")
            return False

def main():
    """Main execution"""
    tester = BybitMinimumOrderTest()
    
    if not tester.api_key or not tester.secret:
        print("❌ Missing API credentials")
        return
    
    # Find minimum order value
    min_amount = tester.find_minimum_order()
    
    # Test automation with minimum
    automation_ready = tester.test_automation_with_minimum(min_amount)
    
    print(f"\n🎯 FINAL RESULTS:")
    if automation_ready:
        print(f"🟢 BYBIT AUTOMATION READY")
        print(f"💰 Minimum order: ${min_amount:.2f}")
        print(f"🎯 Use ${min_amount + 10:.2f}+ for reliable automation")
    else:
        print(f"🔴 BYBIT AUTOMATION NOT READY")
        print(f"🔧 Investigate order requirements")

if __name__ == "__main__":
    main() 