#!/usr/bin/env python3
"""
🔧 PHEMEX & COINBASE API CREDENTIAL FIXER & TESTER
Updated after user's Phemex trade - testing all connections
"""

import os
import sys
import time
import hmac
import hashlib
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APICredentialTester:
    def __init__(self):
        self.results = {}
        
    def test_phemex_connection(self):
        """Test Phemex API connection with both accounts"""
        print("\n🏛️ TESTING PHEMEX APIs...")
        print("=" * 50)
        
        # Phemex Account 1
        api_key_1 = "TkXmB-wEDvVpsZuLljNUSss56jmzvbp7kIlJDPAscqNkODdhN2RhNi03ODc4LTQ0ZjQtYmU5MS0xMDgxMGIwYmU3Nzk"
        api_id_1 = "1a2b91aa-25f8-4ecb-9854-87a3cf4030b4"
        
        # Phemex Account 2  
        api_key_2 = "lcUQ8Zc27h8wwHosHwpmmNGAOqAzg9v60SBswgvpYEoxOGRhNDk3ZS1hNzkyLTRkYmItOTBiZi1lYTA1NWU4ZmY2ZGY"
        api_id_2 = "63b7a04c-5d06-49f3-b0f2-ed7970bdf3f1"
        
        results = []
        
        for account_num, (api_key, api_id) in enumerate([(api_key_1, api_id_1), (api_key_2, api_id_2)], 1):
            if not api_key or not api_id:
                results.append(f"❌ Phemex Account {account_num}: Missing credentials")
                continue
                
            try:
                # Phemex testnet API - simplified balance check
                url = "https://testnet-api.phemex.com/accounts/accountPositions"
                timestamp = str(int(time.time()))
                
                # Create signature for Phemex
                message = f"GET/accounts/accountPositions{timestamp}"
                signature = hmac.new(
                    api_key.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = {
                    'x-phemex-access-token': api_key,
                    'x-phemex-request-signature': signature,
                    'x-phemex-request-timestamp': timestamp,
                    'Content-Type': 'application/json'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"📡 Phemex Account {account_num} Response: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"📦 Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not dict'}")
                    
                    if 'error' not in data:
                        results.append(f"✅ Phemex Account {account_num}: API Connected Successfully!")
                        self.results[f'phemex_account_{account_num}'] = {
                            'status': 'success',
                            'response_code': response.status_code,
                            'api_id': api_id
                        }
                    else:
                        results.append(f"❌ Phemex Account {account_num}: API Error - {data.get('msg', 'Unknown error')}")
                else:
                    error_text = response.text[:200] if response.text else "No error details"
                    results.append(f"❌ Phemex Account {account_num}: HTTP {response.status_code} - {error_text}")
                    
            except requests.exceptions.RequestException as e:
                results.append(f"❌ Phemex Account {account_num}: Connection failed - {str(e)}")
            except Exception as e:
                results.append(f"❌ Phemex Account {account_num}: Error - {str(e)}")
        
        for result in results:
            print(result)
        
        return results

    def check_coinbase_credentials_format(self):
        """Check Coinbase credential format and show what's missing"""
        print("\n🪙 COINBASE CREDENTIAL FORMAT CHECK...")
        print("=" * 50)
        
        accounts = [
            {
                'name': 'Coinbase Testnet 1',
                'api_key': 'dkSh3SMN4QWET5gGiI+8L0rLURNfaFBcE1Rwskl5IUi8oGIryA6//VuYEEvXEYi19n6zk681Js3hguicSCyZoQ==',
                'passphrase': 'hlcz5rwa39t7',
                'api_secret': None  # Missing!
            },
            {
                'name': 'Coinbase Testnet 2', 
                'api_key': 'TSEw2UuuxiYaTO1lMmnxz/aRNEG04Xt4olp1WSkY0nf0Yn+RGxzKmy1TOjW8ndF5gxUGk7flPIjyIYJT02KhCA==',
                'passphrase': 'p5xihrg7ezmm',
                'api_secret': None  # Missing!
            },
            {
                'name': 'Coinbase Testnet 3',
                'api_key': 'PiF2MrOCWZW9xuG8XIg9Pxse9vlrmvtyTUj9Ori7DtyGofVi1LAXHimuV6PNL42EjZ+KKTY1ivSq6JwK7ORsnA==',
                'passphrase': '33xmm8vo7cyu',
                'api_secret': None  # Missing!
            }
        ]
        
        print("📋 CREDENTIAL STATUS:")
        for account in accounts:
            print(f"\n{account['name']}:")
            print(f"  ✅ API_KEY: {account['api_key'][:20]}...")
            print(f"  ✅ PASSPHRASE: {account['passphrase']}")
            print(f"  ❌ API_SECRET: MISSING!")
            
        print(f"\n🔧 FIX NEEDED:")
        print("You need to add API_SECRET for each Coinbase account in .env file:")
        print("")
        print("#Coinbase Testnet:")
        print("API_KEY=dkSh3SMN4QWET5gGiI+8L0rLURNfaFBcE1Rwskl5IUi8oGIryA6//VuYEEvXEYi19n6zk681Js3hguicSCyZoQ==")
        print("API_SECRET=YOUR_API_SECRET_1_HERE")
        print("Passphrase=hlcz5rwa39t7")
        print("")
        print("#Coinbase Testnet2:")
        print("API_KEY=TSEw2UuuxiYaTO1lMmnxz/aRNEG04Xt4olp1WSkY0nf0Yn+RGxzKmy1TOjW8ndF5gxUGk7flPIjyIYJT02KhCA==")
        print("API_SECRET=YOUR_API_SECRET_2_HERE")
        print("Passphrase=p5xihrg7ezmm")
        print("")
        print("#Coinbase Testnet3:")
        print("API_KEY=PiF2MrOCWZW9xuG8XIg9Pxse9vlrmvtyTUj9Ori7DtyGofVi1LAXHimuV6PNL42EjZ+KKTY1ivSq6JwK7ORsnA==")
        print("API_SECRET=YOUR_API_SECRET_3_HERE")
        print("passphrase=33xmm8vo7cyu")
        
        return accounts

    def test_working_exchanges(self):
        """Test exchanges we know are working"""
        print("\n✅ TESTING WORKING EXCHANGES...")
        print("=" * 50)
        
        # Test Binance (we know this works)
        try:
            binance_key = os.getenv('API_Key')
            binance_secret = os.getenv('Secret_Key')
            
            if binance_key and binance_secret:
                url = "https://testnet.binance.vision/api/v3/account"
                timestamp = int(time.time() * 1000)
                query_string = f"timestamp={timestamp}"
                
                signature = hmac.new(
                    binance_secret.encode('utf-8'),
                    query_string.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = {'X-MBX-APIKEY': binance_key}
                params = {'timestamp': timestamp, 'signature': signature}
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    usdt_balance = 0
                    for balance in data.get('balances', []):
                        if balance['asset'] == 'USDT':
                            usdt_balance = float(balance['free'])
                            break
                    
                    print(f"✅ Binance Testnet: ${usdt_balance:,.2f} USDT available")
                    self.results['binance'] = {'status': 'success', 'balance': usdt_balance}
                else:
                    print(f"❌ Binance Testnet: HTTP {response.status_code}")
            else:
                print("❌ Binance: Missing credentials")
                
        except Exception as e:
            print(f"❌ Binance Test Error: {str(e)}")

    def generate_summary_report(self):
        """Generate final assessment summary"""
        print("\n📊 FINAL API ASSESSMENT SUMMARY")
        print("=" * 60)
        
        working_count = sum(1 for r in self.results.values() if r.get('status') == 'success')
        total_tested = len(self.results)
        
        print(f"✅ WORKING EXCHANGES: {working_count}")
        print(f"🔧 NEEDS FIXING: {total_tested - working_count}")
        print(f"📋 TOTAL ASSESSED: {total_tested}")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        if 'phemex_account_1' in self.results or 'phemex_account_2' in self.results:
            phemex_working = any(self.results.get(f'phemex_account_{i}', {}).get('status') == 'success' for i in [1, 2])
            if phemex_working:
                print("• ✅ Phemex: NOW WORKING! Ready for trading deployment")
            else:
                print("• ❌ Phemex: Still needs fixing")
        print("• ❌ Coinbase: Add API_SECRET fields to .env file")
        print("• ✅ Binance: Continue using for immediate trading (proven working)")
        
        return self.results

def main():
    """Main testing function"""
    print("🔧 API CREDENTIAL FIXER & COMPREHENSIVE TESTER")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Goal: Fix Phemex + Coinbase credential format issues")
    
    tester = APICredentialTester()
    
    # Test Phemex (now that user did a trade)
    tester.test_phemex_connection()
    
    # Check Coinbase format
    tester.check_coinbase_credentials_format()
    
    # Test working exchanges for comparison
    tester.test_working_exchanges()
    
    # Generate final report
    tester.generate_summary_report()
    
    print(f"\n🏁 TESTING COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main() 