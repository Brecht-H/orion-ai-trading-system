#!/usr/bin/env python3
"""
🚀 NEW COMPREHENSIVE EXCHANGE TEST 2025
Specifically designed to handle all current API issues and perform actual trades

TARGETS:
✅ BYBIT: Fix signature issues, test trading
✅ COINBASE: Handle + character in SECRET properly  
✅ PHEMEX: Test new keys with IP whitelist
✅ BINANCE: Test with current working credentials
✅ KRAKEN: Public API market data testing
"""

import os
import requests
import json
import time
import hmac
import hashlib
import base64
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NewExchangeTest:
    def __init__(self):
        print("🚀 NEW COMPREHENSIVE EXCHANGE TEST 2025")
        print("=" * 60)
        self.results = {}
        self.setup_results_db()
    
    def setup_results_db(self):
        """Setup results database"""
        self.db_path = f"exchange_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            exchange TEXT,
            test_type TEXT,
            status TEXT,
            balance_usd REAL,
            details TEXT,
            recommendation TEXT
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            exchange TEXT,
            symbol TEXT,
            side TEXT,
            quantity REAL,
            price REAL,
            order_id TEXT,
            status TEXT
        )''')
        
        conn.commit()
        conn.close()
        print(f"📊 Results database: {self.db_path}")
    
    def log_result(self, exchange, test_type, status, balance_usd=0, details="", recommendation=""):
        """Log test result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO test_results (timestamp, exchange, test_type, status, balance_usd, details, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), exchange, test_type, status, balance_usd, details, recommendation))
        conn.commit()
        conn.close()
    
    def test_binance(self):
        """Test Binance with current working credentials"""
        print("\n🟡 TESTING BINANCE (Currently working with $109k)")
        
        try:
            # Use the working credentials from .env
            api_key = os.getenv('BINANCE_API_KEY') or os.getenv('API_Key')
            secret = os.getenv('BINANCE_API_SECRET') or os.getenv('Secret_Key')
            
            if not api_key or not secret:
                print("❌ Missing Binance credentials")
                return {'status': 'FAILED', 'reason': 'Missing credentials'}
            
            print(f"🔍 Using API Key: {api_key[:8]}...")
            
            # Test connection
            base_url = "https://testnet.binance.vision/api/v3"
            ping = requests.get(f"{base_url}/ping", timeout=10)
            
            if ping.status_code != 200:
                print("❌ Connection failed")
                return {'status': 'FAILED', 'reason': 'Connection failed'}
            
            print("✅ Connection: SUCCESS")
            
            # Test account balance
            timestamp = int(time.time() * 1000)
            query_string = f"timestamp={timestamp}"
            signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
            
            headers = {'X-MBX-APIKEY': api_key}
            params = {'timestamp': timestamp, 'signature': signature}
            
            account_response = requests.get(f"{base_url}/account", headers=headers, params=params, timeout=10)
            
            if account_response.status_code == 200:
                account_data = account_response.json()
                balances = account_data.get('balances', [])
                
                usdt_balance = 0
                btc_balance = 0
                
                for balance in balances:
                    if balance['asset'] == 'USDT':
                        usdt_balance = float(balance['free'])
                    elif balance['asset'] == 'BTC':
                        btc_balance = float(balance['free'])
                
                total_value = usdt_balance + (btc_balance * 100000)  # Estimate BTC value
                
                print(f"✅ Balance: ${total_value:,.2f} ({usdt_balance:,.2f} USDT + {btc_balance:.8f} BTC)")
                
                # Test small trade if balance allows
                if usdt_balance >= 15:
                    trade_result = self.execute_binance_trade(api_key, secret, base_url)
                    if trade_result['success']:
                        print("✅ Test trade: SUCCESS")
                        recommendation = "🟢 READY FOR AUTOMATED TRADING"
                    else:
                        print(f"❌ Test trade failed: {trade_result['error']}")
                        recommendation = "🟡 Balance OK, trade issues"
                else:
                    recommendation = f"🟡 Need more USDT: ${usdt_balance:.2f} available"
                
                self.log_result('BINANCE', 'FULL_TEST', 'SUCCESS', total_value, 
                              f"USDT: ${usdt_balance:.2f}, BTC: {btc_balance:.8f}", recommendation)
                
                return {
                    'status': 'SUCCESS',
                    'balance_usd': total_value,
                    'usdt': usdt_balance,
                    'btc': btc_balance,
                    'recommendation': recommendation
                }
            else:
                error_msg = account_response.text
                print(f"❌ Account access failed: {error_msg}")
                self.log_result('BINANCE', 'AUTHENTICATION', 'FAILED', details=error_msg)
                return {'status': 'FAILED', 'reason': 'Authentication failed'}
                
        except Exception as e:
            print(f"❌ Binance error: {str(e)}")
            self.log_result('BINANCE', 'EXCEPTION', 'FAILED', details=str(e))
            return {'status': 'FAILED', 'reason': str(e)}
    
    def execute_binance_trade(self, api_key, secret, base_url):
        """Execute small test trade on Binance"""
        try:
            # Get current BTC price
            ticker = requests.get(f"{base_url}/ticker/price?symbol=BTCUSDT").json()
            btc_price = float(ticker['price'])
            
            # Calculate small trade amount
            trade_usdt = 12
            btc_qty = round(trade_usdt / btc_price, 5)
            
            # Prepare order
            timestamp = int(time.time() * 1000)
            order_params = {
                'symbol': 'BTCUSDT',
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': btc_qty,
                'timestamp': timestamp
            }
            
            query_string = '&'.join([f"{k}={v}" for k, v in order_params.items()])
            signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
            
            order_params['signature'] = signature
            headers = {'X-MBX-APIKEY': api_key}
            
            # Execute order
            order_response = requests.post(f"{base_url}/order", headers=headers, data=order_params, timeout=10)
            
            if order_response.status_code == 200:
                order_data = order_response.json()
                order_id = order_data.get('orderId', 'N/A')
                
                # Log trade
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO trades (timestamp, exchange, symbol, side, quantity, price, order_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (datetime.now().isoformat(), 'BINANCE', 'BTCUSDT', 'BUY', btc_qty, btc_price, order_id, 'FILLED'))
                conn.commit()
                conn.close()
                
                return {'success': True, 'order_id': order_id, 'quantity': btc_qty}
            else:
                return {'success': False, 'error': order_response.text}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_bybit_fixed(self):
        """Test Bybit with corrected signature"""
        print("\n🟡 TESTING BYBIT (Fixed signature method)")
        
        try:
            api_key = os.getenv('BYBIT_API_KEY')
            secret = os.getenv('BYBIT_API_SECRET')
            
            if not api_key or not secret:
                print("❌ Missing Bybit credentials")
                return {'status': 'FAILED', 'reason': 'Missing credentials'}
            
            print(f"🔍 Using API Key: {api_key[:8]}...")
            
            base_url = "https://api-testnet.bybit.com"
            
            # Test connection
            time_response = requests.get(f"{base_url}/v5/market/time", timeout=10)
            if time_response.status_code != 200:
                print("❌ Connection failed")
                return {'status': 'FAILED', 'reason': 'Connection failed'}
            
            print("✅ Connection: SUCCESS")
            
            # Fixed authentication method for V5 API
            timestamp = str(int(time.time() * 1000))
            recv_window = "5000"
            
            # Corrected parameter string for wallet balance
            param_str = f"category=spot&timestamp={timestamp}"
            
            # Create signature - this is the corrected method
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
                f"{base_url}/v5/account/wallet-balance?category=spot",
                headers=headers,
                timeout=10
            )
            
            if balance_response.status_code == 200:
                data = balance_response.json()
                
                if data.get('retCode') == 0:
                    print("✅ Authentication: SUCCESS")
                    
                    # Extract balance
                    accounts = data.get('result', {}).get('list', [])
                    total_usd = 0
                    
                    for account in accounts:
                        for coin in account.get('coin', []):
                            if coin['coin'] == 'USDT':
                                total_usd += float(coin.get('walletBalance', 0))
                    
                    print(f"✅ Balance: ${total_usd:,.2f} USDT")
                    
                    if total_usd >= 15:
                        # Test trade
                        trade_result = self.execute_bybit_trade(api_key, secret, base_url)
                        if trade_result['success']:
                            recommendation = "🟢 READY FOR AUTOMATED TRADING"
                        else:
                            recommendation = f"🟡 Balance OK, trade issue: {trade_result['error']}"
                    else:
                        recommendation = f"🟡 Need funding: ${total_usd:.2f} available"
                    
                    self.log_result('BYBIT', 'FULL_TEST', 'SUCCESS', total_usd, 
                                  f"USDT Balance: ${total_usd:.2f}", recommendation)
                    
                    return {
                        'status': 'SUCCESS',
                        'balance_usd': total_usd,
                        'recommendation': recommendation
                    }
                else:
                    error_msg = data.get('retMsg', 'Unknown error')
                    print(f"❌ API Error: {error_msg}")
                    self.log_result('BYBIT', 'API_ERROR', 'FAILED', details=error_msg)
                    return {'status': 'FAILED', 'reason': error_msg}
            else:
                print(f"❌ HTTP Error: {balance_response.status_code}")
                print(f"Response: {balance_response.text}")
                self.log_result('BYBIT', 'HTTP_ERROR', 'FAILED', details=balance_response.text)
                return {'status': 'FAILED', 'reason': f'HTTP {balance_response.status_code}'}
                
        except Exception as e:
            print(f"❌ Bybit error: {str(e)}")
            self.log_result('BYBIT', 'EXCEPTION', 'FAILED', details=str(e))
            return {'status': 'FAILED', 'reason': str(e)}
    
    def execute_bybit_trade(self, api_key, secret, base_url):
        """Execute test trade on Bybit V5"""
        try:
            # Get BTC price
            ticker_response = requests.get(f"{base_url}/v5/market/tickers?category=spot&symbol=BTCUSDT")
            ticker_data = ticker_response.json()
            
            if ticker_data.get('retCode') != 0:
                return {'success': False, 'error': 'Cannot get price'}
                
            btc_price = float(ticker_data['result']['list'][0]['lastPrice'])
            
            # Calculate trade
            trade_usdt = 12
            btc_qty = round(trade_usdt / btc_price, 6)
            
            # Prepare order parameters
            timestamp = str(int(time.time() * 1000))
            order_params = {
                'category': 'spot',
                'symbol': 'BTCUSDT',
                'side': 'Buy',
                'orderType': 'Market',
                'qty': str(btc_qty),
                'timestamp': timestamp
            }
            
            # Create parameter string
            param_str = '&'.join([f"{k}={v}" for k, v in sorted(order_params.items())])
            
            # Create signature
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
                'X-BAPI-RECV-WINDOW': '5000',
                'Content-Type': 'application/json'
            }
            
            # Execute order
            order_response = requests.post(
                f"{base_url}/v5/order/create",
                headers=headers,
                json=order_params,
                timeout=10
            )
            
            if order_response.status_code == 200:
                order_data = order_response.json()
                if order_data.get('retCode') == 0:
                    order_id = order_data.get('result', {}).get('orderId', 'N/A')
                    
                    # Log trade
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('''
                    INSERT INTO trades (timestamp, exchange, symbol, side, quantity, price, order_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (datetime.now().isoformat(), 'BYBIT', 'BTCUSDT', 'BUY', btc_qty, btc_price, order_id, 'FILLED'))
                    conn.commit()
                    conn.close()
                    
                    return {'success': True, 'order_id': order_id, 'quantity': btc_qty}
                else:
                    return {'success': False, 'error': order_data.get('retMsg', 'Unknown error')}
            else:
                return {'success': False, 'error': f'HTTP {order_response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_coinbase_plus_fix(self):
        """Test Coinbase with proper + character handling"""
        print("\n🟡 TESTING COINBASE (+ character fix)")
        
        try:
            # Try multiple credential formats
            api_key = os.getenv('CB_ACCESS_KEY') or os.getenv('COINBASE_API_KEY') or os.getenv('API')
            secret = os.getenv('CB_ACCESS_SECRET') or os.getenv('COINBASE_API_SECRET') or os.getenv('SECRET_KEY')
            passphrase = os.getenv('CB_ACCESS_PASSPHRASE') or os.getenv('COINBASE_PASSPHRASE') or os.getenv('passphrase')
            
            if not all([api_key, secret, passphrase]):
                print("❌ Missing Coinbase credentials")
                print(f"API Key: {'✅' if api_key else '❌'}")
                print(f"Secret: {'✅' if secret else '❌'}")
                print(f"Passphrase: {'✅' if passphrase else '❌'}")
                return {'status': 'FAILED', 'reason': 'Missing credentials'}
            
            print(f"🔍 Using API Key: {api_key[:8]}...")
            print(f"🔍 Secret has + characters: {'YES' if '+' in secret else 'NO'}")
            
            base_url = "https://api-public.sandbox.exchange.coinbase.com"
            
            # Test connection
            time_response = requests.get(f"{base_url}/time", timeout=10)
            if time_response.status_code != 200:
                print("❌ Connection failed")
                return {'status': 'FAILED', 'reason': 'Connection failed'}
            
            print("✅ Connection: SUCCESS")
            
            # Authentication test with proper + handling
            timestamp = str(int(time.time()))
            method = 'GET'
            path = '/accounts'
            body = ''
            
            message = timestamp + method + path + body
            
            # Proper base64 decoding of secret (handles + characters)
            try:
                secret_decoded = base64.b64decode(secret)
            except Exception as e:
                print(f"❌ Secret decoding failed: {e}")
                return {'status': 'FAILED', 'reason': 'Invalid secret format'}
            
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
            
            # Test accounts endpoint
            accounts_response = requests.get(f"{base_url}/accounts", headers=headers, timeout=10)
            
            if accounts_response.status_code == 200:
                accounts = accounts_response.json()
                total_usd = 0
                
                for account in accounts:
                    if account.get('currency') == 'USD':
                        total_usd += float(account.get('balance', 0))
                
                print(f"✅ Authentication: SUCCESS")
                print(f"✅ Balance: ${total_usd:,.2f} USD")
                
                if total_usd >= 15:
                    recommendation = "🟢 READY FOR TRADING"
                else:
                    recommendation = f"🟡 Need funding: ${total_usd:.2f} available"
                
                self.log_result('COINBASE', 'FULL_TEST', 'SUCCESS', total_usd, 
                              f"USD Balance: ${total_usd:.2f}", recommendation)
                
                return {
                    'status': 'SUCCESS',
                    'balance_usd': total_usd,
                    'recommendation': recommendation
                }
            else:
                error_text = accounts_response.text
                print(f"❌ Authentication failed: HTTP {accounts_response.status_code}")
                print(f"Response: {error_text[:200]}...")
                self.log_result('COINBASE', 'AUTHENTICATION', 'FAILED', details=error_text[:100])
                return {'status': 'FAILED', 'reason': f'HTTP {accounts_response.status_code}'}
                
        except Exception as e:
            print(f"❌ Coinbase error: {str(e)}")
            self.log_result('COINBASE', 'EXCEPTION', 'FAILED', details=str(e))
            return {'status': 'FAILED', 'reason': str(e)}
    
    def test_phemex_new(self):
        """Test Phemex with new API keys and IP whitelist"""
        print("\n🟡 TESTING PHEMEX (New keys + IP whitelist)")
        
        try:
            api_key = os.getenv('PHEMEX_API_KEY') or os.getenv('ID')
            secret = os.getenv('PHEMEX_API_SECRET') or os.getenv('API_SECRET')
            
            if not api_key or not secret:
                print("❌ Missing Phemex credentials")
                return {'status': 'FAILED', 'reason': 'Missing credentials'}
            
            print(f"🔍 Using API Key: {api_key[:8]}...")
            
            base_url = "https://testnet-api.phemex.com"
            
            # Test connection
            time_response = requests.get(f"{base_url}/public/md/time", timeout=10)
            if time_response.status_code != 200:
                print("❌ Connection failed")
                return {'status': 'FAILED', 'reason': 'Connection failed'}
            
            print("✅ Connection: SUCCESS")
            
            # Test authentication
            timestamp = str(int(time.time()))
            path = "/accounts/accountPositions"
            query_string = "currency=USD"
            
            message = path + query_string + timestamp
            signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
            
            headers = {
                'x-phemex-access-token': api_key,
                'x-phemex-request-signature': signature,
                'x-phemex-request-timestamp': timestamp
            }
            
            balance_response = requests.get(
                f"{base_url}/accounts/accountPositions?{query_string}",
                headers=headers,
                timeout=10
            )
            
            if balance_response.status_code == 200:
                data = balance_response.json()
                if data.get('code') == 0:
                    account_data = data.get('data', {})
                    balance_value = account_data.get('totalTradingBalanceValue', 0) / 10000
                    
                    print(f"✅ Authentication: SUCCESS")
                    print(f"✅ Balance: ${balance_value:,.2f} USD")
                    
                    if balance_value >= 15:
                        recommendation = "🟢 READY FOR TRADING"
                    else:
                        recommendation = f"🟡 Need funding: ${balance_value:.2f} available"
                    
                    self.log_result('PHEMEX', 'FULL_TEST', 'SUCCESS', balance_value, 
                                  f"Balance: ${balance_value:.2f}", recommendation)
                    
                    return {
                        'status': 'SUCCESS',
                        'balance_usd': balance_value,
                        'recommendation': recommendation
                    }
                else:
                    error_msg = data.get('msg', 'Unknown error')
                    print(f"❌ API Error: {error_msg}")
                    self.log_result('PHEMEX', 'API_ERROR', 'FAILED', details=error_msg)
                    return {'status': 'FAILED', 'reason': error_msg}
            else:
                print(f"❌ HTTP Error: {balance_response.status_code}")
                self.log_result('PHEMEX', 'HTTP_ERROR', 'FAILED', details=balance_response.text)
                return {'status': 'FAILED', 'reason': f'HTTP {balance_response.status_code}'}
                
        except Exception as e:
            print(f"❌ Phemex error: {str(e)}")
            self.log_result('PHEMEX', 'EXCEPTION', 'FAILED', details=str(e))
            return {'status': 'FAILED', 'reason': str(e)}
    
    def test_kraken_public(self):
        """Test Kraken public API (no testnet available)"""
        print("\n🟡 TESTING KRAKEN PUBLIC API")
        
        try:
            base_url = "https://api.kraken.com"
            
            # Test time endpoint
            time_response = requests.get(f"{base_url}/0/public/Time", timeout=10)
            if time_response.status_code != 200:
                print("❌ Connection failed")
                return {'status': 'FAILED', 'reason': 'Connection failed'}
            
            print("✅ Connection: SUCCESS")
            
            # Test market data
            ticker_response = requests.get(f"{base_url}/0/public/Ticker?pair=BTCUSD", timeout=10)
            
            if ticker_response.status_code == 200:
                ticker_data = ticker_response.json()
                if not ticker_data.get('error'):
                    btc_price = float(ticker_data['result']['XXBTZUSD']['c'][0])
                    
                    print(f"✅ Market Data: BTC ${btc_price:,.2f}")
                    
                    recommendation = "🟢 MARKET DATA READY (No testnet, live only)"
                    
                    self.log_result('KRAKEN', 'MARKET_DATA', 'SUCCESS', 0, 
                                  f"BTC Price: ${btc_price:.2f}", recommendation)
                    
                    return {
                        'status': 'SUCCESS',
                        'btc_price': btc_price,
                        'recommendation': recommendation
                    }
                else:
                    print(f"❌ Market data error: {ticker_data['error']}")
                    return {'status': 'FAILED', 'reason': 'Market data error'}
            else:
                print(f"❌ Market data failed: HTTP {ticker_response.status_code}")
                return {'status': 'FAILED', 'reason': 'Market data failed'}
                
        except Exception as e:
            print(f"❌ Kraken error: {str(e)}")
            self.log_result('KRAKEN', 'EXCEPTION', 'FAILED', details=str(e))
            return {'status': 'FAILED', 'reason': str(e)}
    
    def run_all_tests(self):
        """Run all exchange tests"""
        print("\n🔥 RUNNING ALL EXCHANGE TESTS")
        print("=" * 60)
        
        # Test all exchanges
        self.results = {
            'BINANCE': self.test_binance(),
            'BYBIT': self.test_bybit_fixed(),
            'COINBASE': self.test_coinbase_plus_fix(),
            'PHEMEX': self.test_phemex_new(),
            'KRAKEN': self.test_kraken_public()
        }
        
        # Generate final report
        self.generate_report()
        
        return self.results
    
    def generate_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("🎯 FINAL EXCHANGE TEST REPORT")
        print("=" * 60)
        
        working_exchanges = []
        trading_ready = []
        total_capital = 0
        
        for exchange, result in self.results.items():
            if result['status'] == 'SUCCESS':
                working_exchanges.append(exchange)
                balance = result.get('balance_usd', 0)
                total_capital += balance
                
                if balance >= 15:
                    trading_ready.append(exchange)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Working: {len(working_exchanges)}/5 exchanges ({', '.join(working_exchanges)})")
        print(f"   Trading Ready: {len(trading_ready)}/5 exchanges ({', '.join(trading_ready)})")
        print(f"   Total Capital: ${total_capital:,.2f}")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for exchange, result in self.results.items():
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            print(f"   {status_icon} {exchange}: {result.get('recommendation', result.get('reason', 'Unknown'))}")
        
        print(f"\n🚀 DEPLOYMENT STATUS:")
        if len(trading_ready) >= 2:
            print("   ✅ READY FOR MULTI-EXCHANGE DEPLOYMENT")
            print("   🔄 Can start automated trading immediately")
        elif len(trading_ready) >= 1:
            print("   🟡 LIMITED DEPLOYMENT POSSIBLE")
            print("   📈 Single exchange trading available")
        else:
            print("   ❌ NOT READY FOR DEPLOYMENT")
            print("   🔧 Fix exchange issues first")
        
        # Save final summary
        self.log_result('SUMMARY', 'FINAL_REPORT', 'COMPLETED', total_capital, 
                       f"Working: {len(working_exchanges)}/5, Ready: {len(trading_ready)}/5",
                       f"Deployment status: {'READY' if len(trading_ready) >= 2 else 'LIMITED' if len(trading_ready) >= 1 else 'NOT_READY'}")
        
        print(f"\n📄 Full results saved to: {self.db_path}")

def main():
    """Main execution"""
    tester = NewExchangeTest()
    results = tester.run_all_tests()
    
    print("\n🎯 TEST COMPLETED!")
    print("Ready for automated trading setup based on working exchanges.")
    
    return results

if __name__ == "__main__":
    main() 