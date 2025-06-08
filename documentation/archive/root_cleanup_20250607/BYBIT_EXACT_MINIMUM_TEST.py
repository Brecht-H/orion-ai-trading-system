#!/usr/bin/env python3
"""
🎯 BYBIT EXACT MINIMUM TEST
Test with the exact minimum quantity from instrument info

GOAL: Test with 0.000048 BTC minimum quantity
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

class BybitExactMinimumTest:
    def __init__(self):
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.secret = os.getenv('BYBIT_API_SECRET')
        self.base_url = "https://api-testnet.bybit.com"
        
        print("🎯 BYBIT EXACT MINIMUM TEST")
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
    
    def test_exact_minimum(self):
        """Test with exact minimum quantity"""
        print(f"\n🧪 Testing with exact minimum quantity...")
        
        btc_price = self.get_btc_price()
        if btc_price == 0:
            print("❌ Cannot get BTC price")
            return False
        
        # Use exact minimum from instrument info
        btc_qty = 0.000048
        usdt_value = btc_qty * btc_price
        
        print(f"   📊 BTC Price: ${btc_price:,.2f}")
        print(f"   📈 BTC Quantity: {btc_qty} (exact minimum)")
        print(f"   💰 Order Value: ${usdt_value:.2f}")
        
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
        
        print(f"\n🚀 Executing order with exact minimum...")
        
        # Execute order
        response = requests.post(
            f"{self.base_url}/v5/order/create",
            headers=headers,
            data=json_body,
            timeout=10
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Full Response: {json.dumps(data, indent=2)}")
            
            if data.get('retCode') == 0:
                order_id = data.get('result', {}).get('orderId', 'N/A')
                print(f"✅ SUCCESS! Order ID: {order_id}")
                print(f"🎉 AUTOMATION CONFIRMED WORKING!")
                return True
            else:
                error_msg = data.get('retMsg', 'Unknown error')
                print(f"❌ Order failed: {error_msg}")
                
                # Check for specific error types
                if "lower limit" in error_msg.lower():
                    print("🔍 This suggests there's a higher minimum notional value")
                elif "insufficient" in error_msg.lower():
                    print("🔍 This suggests balance issues")
                elif "precision" in error_msg.lower():
                    print("🔍 This suggests quantity precision issues")
                
                return False
        else:
            error_msg = response.text
            print(f"❌ HTTP error: {error_msg}")
            return False
    
    def test_higher_quantities(self):
        """Test with progressively higher quantities"""
        print(f"\n🔍 Testing higher quantities...")
        
        btc_price = self.get_btc_price()
        if btc_price == 0:
            return False
        
        # Test different multiples of minimum
        test_quantities = [0.000048, 0.0001, 0.0005, 0.001, 0.002, 0.005, 0.01]
        
        for qty in test_quantities:
            usdt_value = qty * btc_price
            print(f"\n🧪 Testing {qty} BTC (${usdt_value:.2f})...")
            
            order_params = {
                'category': 'spot',
                'symbol': 'BTCUSDT',
                'side': 'Buy',
                'orderType': 'Market',
                'qty': str(qty)
            }
            
            signature, timestamp, recv_window, json_body = self.create_signature_for_post(order_params)
            
            headers = {
                'X-BAPI-API-KEY': self.api_key,
                'X-BAPI-SIGN': signature,
                'X-BAPI-SIGN-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': recv_window,
                'Content-Type': 'application/json'
            }
            
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
                    print(f"   🎉 Working minimum: {qty} BTC (${usdt_value:.2f})")
                    return qty, usdt_value
                else:
                    error_msg = data.get('retMsg', 'Unknown error')
                    print(f"   ❌ FAILED: {error_msg}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
            
            # Wait between tests
            time.sleep(1)
        
        print("❌ No working quantity found")
        return None, None

def main():
    """Main execution"""
    tester = BybitExactMinimumTest()
    
    if not tester.api_key or not tester.secret:
        print("❌ Missing API credentials")
        return
    
    # Test exact minimum
    success = tester.test_exact_minimum()
    
    if not success:
        print("\n🔍 Exact minimum failed, testing higher quantities...")
        working_qty, working_value = tester.test_higher_quantities()
        
        if working_qty:
            print(f"\n🎉 FOUND WORKING MINIMUM!")
            print(f"✅ Quantity: {working_qty} BTC")
            print(f"💰 Value: ${working_value:.2f}")
            print(f"🤖 Bybit automation possible with ${working_value:.2f}+ orders")
        else:
            print(f"\n❌ Could not find working minimum")
            print(f"🔧 May need to investigate further or use different approach")
    else:
        print(f"\n🎉 EXACT MINIMUM WORKS!")
        print(f"🤖 Bybit automation ready with ~$5 orders")

if __name__ == "__main__":
    main() 