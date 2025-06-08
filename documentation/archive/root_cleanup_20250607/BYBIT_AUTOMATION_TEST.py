#!/usr/bin/env python3
"""
🤖 BYBIT AUTOMATION TEST
Test actual automated trading capability on Bybit with $10,000 balance

GOAL: Verify automated trading without approval
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

class BybitAutomationTest:
    def __init__(self):
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.secret = os.getenv('BYBIT_API_SECRET')
        self.base_url = "https://api-testnet.bybit.com"
        
        print("🤖 BYBIT AUTOMATION TEST")
        print("=" * 50)
        print(f"🔍 API Key: {self.api_key[:8]}..." if self.api_key else "❌ No API Key")
        print(f"💰 Target: Test automated trade with $10,000 balance")
    
    def create_signature_for_get(self, params_dict):
        """Signature for GET requests (balance queries)"""
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        param_str = '&'.join([f"{k}={v}" for k, v in sorted(params_dict.items())])
        sign_string = timestamp + self.api_key + recv_window + param_str
        
        signature = hmac.new(
            self.secret.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature, timestamp, recv_window
    
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
    
    def get_balance(self):
        """Get current balance"""
        print("\n🔄 Checking balance...")
        
        params = {
            'accountType': 'UNIFIED',
            'coin': 'USDT'
        }
        
        signature, timestamp, recv_window = self.create_signature_for_get(params)
        
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window
        }
        
        response = requests.get(
            f"{self.base_url}/v5/account/wallet-balance",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('retCode') == 0:
                accounts = data.get('result', {}).get('list', [])
                for account in accounts:
                    for coin in account.get('coin', []):
                        if coin['coin'] == 'USDT':
                            balance = float(coin.get('walletBalance', 0))
                            print(f"✅ USDT Balance: ${balance:,.2f}")
                            return balance
        
        print("❌ Failed to get balance")
        return 0
    
    def get_btc_price(self):
        """Get current BTC price"""
        print("\n🔄 Getting BTC price...")
        
        response = requests.get(
            f"{self.base_url}/v5/market/tickers",
            params={'category': 'spot', 'symbol': 'BTCUSDT'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('retCode') == 0:
                price = float(data['result']['list'][0]['lastPrice'])
                print(f"📊 BTC Price: ${price:,.2f}")
                return price
        
        print("❌ Failed to get BTC price")
        return 0
    
    def execute_automated_trade(self, balance):
        """Execute automated test trade"""
        print(f"\n🤖 EXECUTING AUTOMATED TRADE")
        print("=" * 40)
        
        # Get BTC price
        btc_price = self.get_btc_price()
        if btc_price == 0:
            return False
        
        # Calculate trade amount (use $30 to be safe above minimum)
        trade_usdt = 30
        btc_qty = round(trade_usdt / btc_price, 6)
        
        print(f"🎯 Automated Trade Plan:")
        print(f"   💰 Amount: ${trade_usdt:.2f} USDT")
        print(f"   📈 Quantity: {btc_qty} BTC")
        print(f"   💵 Price: ${btc_price:,.2f}")
        
        if balance < trade_usdt:
            print(f"❌ Insufficient balance: ${balance:.2f} < ${trade_usdt:.2f}")
            return False
        
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
        
        print(f"\n🚀 Executing order...")
        
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
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            if data.get('retCode') == 0:
                order_id = data.get('result', {}).get('orderId', 'N/A')
                print(f"✅ AUTOMATED ORDER SUCCESSFUL!")
                print(f"🆔 Order ID: {order_id}")
                print(f"🎉 AUTOMATION CONFIRMED WORKING!")
                return True
            else:
                error_msg = data.get('retMsg', 'Unknown error')
                print(f"❌ Order failed: {error_msg}")
                return False
        else:
            error_msg = response.text
            print(f"❌ HTTP error: {error_msg}")
            return False
    
    def run_automation_test(self):
        """Run complete automation test"""
        print(f"\n🚀 STARTING AUTOMATION TEST")
        print("=" * 50)
        
        # Check balance
        balance = self.get_balance()
        if balance == 0:
            print("❌ Cannot get balance - automation not possible")
            return False
        
        if balance < 30:
            print(f"❌ Insufficient balance for automation: ${balance:.2f}")
            return False
        
        print(f"✅ Sufficient balance: ${balance:,.2f}")
        
        # Execute automated trade
        success = self.execute_automated_trade(balance)
        
        if success:
            print(f"\n🎉 AUTOMATION TEST RESULT: SUCCESS")
            print(f"✅ Bybit is ready for automated trading")
            print(f"💰 Available capital: ${balance:,.2f}")
            return True
        else:
            print(f"\n❌ AUTOMATION TEST RESULT: FAILED")
            print(f"🔧 Needs investigation before automation")
            return False

def main():
    """Main execution"""
    tester = BybitAutomationTest()
    
    if not tester.api_key or not tester.secret:
        print("❌ Missing API credentials")
        return
    
    success = tester.run_automation_test()
    
    print(f"\n🎯 FINAL VERDICT:")
    if success:
        print("🟢 BYBIT READY FOR AUTOMATED TRADING")
    else:
        print("🔴 BYBIT NOT READY FOR AUTOMATION")

if __name__ == "__main__":
    main() 