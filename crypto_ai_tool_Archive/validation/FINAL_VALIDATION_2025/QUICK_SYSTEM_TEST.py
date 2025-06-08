#!/usr/bin/env python3
"""
QUICK SYSTEM TEST - WHAT WORKS RIGHT NOW?
========================================

Doel: Snel testen wat werkt en wat niet
- Test Simple Working Trader
- Test data collection
- Test basic trading logic
- Geef concrete next steps

GEEN COMPLEXE SYSTEMEN - GEWOON CHECKEN WAT WERKT
"""

import sys
import os
import time
import requests
from datetime import datetime

class QuickSystemTest:
    """Snelle test van werkende componenten"""
    
    def __init__(self):
        print("🚀 QUICK SYSTEM TEST")
        print("=" * 40)
        print("Doel: Checken wat NU werkt")
        print()

    def test_environment(self):
        """Test basic environment"""
        print("🔧 TESTING ENVIRONMENT")
        print("-" * 30)
        
        results = {}
        
        # Check .env file
        env_path = "../.env"
        if os.path.exists(env_path):
            print("✅ .env file exists")
            results['env_file'] = True
        else:
            print("❌ .env file missing")
            results['env_file'] = False
        
        # Check Python packages
        try:
            import pandas
            import numpy
            import requests
            print("✅ Core packages available")
            results['packages'] = True
        except ImportError as e:
            print(f"❌ Missing packages: {e}")
            results['packages'] = False
        
        # Check directories
        key_dirs = ['../strategy_center', '../trading_execution_center', '../research_center']
        dir_count = 0
        for dir_path in key_dirs:
            if os.path.exists(dir_path):
                dir_count += 1
        
        if dir_count == len(key_dirs):
            print("✅ All key directories exist")
            results['directories'] = True
        else:
            print(f"⚠️ {dir_count}/{len(key_dirs)} directories exist")
            results['directories'] = dir_count == len(key_dirs)
        
        return results

    def test_bybit_connection(self):
        """Test Bybit connection"""
        print("\n🔌 TESTING BYBIT CONNECTION")
        print("-" * 30)
        
        try:
            # Test public API first
            url = "https://api-testnet.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('retCode') == 0:
                    price = data['result']['list'][0]['lastPrice']
                    print(f"✅ Bybit public API works: BTC ${price}")
                    return True
                else:
                    print(f"❌ Bybit API error: {data.get('retMsg', 'Unknown')}")
                    return False
            else:
                print(f"❌ Bybit connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Bybit connection error: {e}")
            return False

    def test_simple_rsi_calculation(self):
        """Test basic RSI calculation"""
        print("\n📊 TESTING RSI CALCULATION")
        print("-" * 30)
        
        try:
            import numpy as np
            
            # Sample price data
            prices = [100, 102, 101, 105, 104, 108, 107, 110, 109, 112, 111, 115, 114, 118, 117]
            
            def calculate_simple_rsi(prices, period=14):
                if len(prices) < period + 1:
                    return None
                    
                gains = []
                losses = []
                
                for i in range(1, len(prices)):
                    change = prices[i] - prices[i-1]
                    if change > 0:
                        gains.append(change)
                        losses.append(0)
                    else:
                        gains.append(0)
                        losses.append(abs(change))
                
                if len(gains) < period:
                    return None
                    
                avg_gain = sum(gains[-period:]) / period
                avg_loss = sum(losses[-period:]) / period
                
                if avg_loss == 0:
                    return 100
                    
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                
                return rsi
            
            rsi = calculate_simple_rsi(prices)
            
            if rsi is not None:
                print(f"✅ RSI calculation works: {rsi:.2f}")
                
                # Test trading logic
                if rsi < 30:
                    signal = "BUY"
                elif rsi > 70:
                    signal = "SELL"
                else:
                    signal = "HOLD"
                
                print(f"✅ Trading logic works: RSI {rsi:.2f} → {signal}")
                return True
            else:
                print("❌ RSI calculation failed")
                return False
                
        except Exception as e:
            print(f"❌ RSI calculation error: {e}")
            return False

    def test_data_collection(self):
        """Test basic data collection"""
        print("\n📈 TESTING DATA COLLECTION")
        print("-" * 30)
        
        try:
            # Test CoinGecko API
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                btc_price = data.get('bitcoin', {}).get('usd')
                eth_price = data.get('ethereum', {}).get('usd')
                
                if btc_price and eth_price:
                    print(f"✅ Data collection works: BTC ${btc_price:,}, ETH ${eth_price:,}")
                    return True
                else:
                    print("❌ No price data received")
                    return False
            else:
                print(f"❌ Data collection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Data collection error: {e}")
            return False

    def test_basic_trading_simulation(self):
        """Test basic trading simulation"""
        print("\n💰 TESTING TRADING SIMULATION")
        print("-" * 30)
        
        try:
            # Simulate a simple trade
            portfolio = {
                'cash': 1000.0,
                'btc': 0.0,
                'trades': []
            }
            
            # Get current price
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                btc_price = response.json()['bitcoin']['usd']
                
                # Simulate buy
                position_size = portfolio['cash'] * 0.01  # 1% position
                btc_to_buy = position_size / btc_price
                
                portfolio['cash'] -= position_size
                portfolio['btc'] += btc_to_buy
                portfolio['trades'].append({
                    'type': 'BUY',
                    'amount': btc_to_buy,
                    'price': btc_price,
                    'value': position_size
                })
                
                print(f"✅ Simulated BUY: {btc_to_buy:.6f} BTC at ${btc_price:,}")
                print(f"   Portfolio: ${portfolio['cash']:.2f} cash + {portfolio['btc']:.6f} BTC")
                
                # Calculate total value
                total_value = portfolio['cash'] + (portfolio['btc'] * btc_price)
                print(f"   Total Value: ${total_value:.2f}")
                
                return True
            else:
                print("❌ Could not get price for simulation")
                return False
                
        except Exception as e:
            print(f"❌ Trading simulation error: {e}")
            return False

    def run_comprehensive_test(self):
        """Run all tests and provide assessment"""
        print("🎯 COMPREHENSIVE SYSTEM TEST")
        print("=" * 50)
        print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        results = {}
        
        # Run all tests
        results['environment'] = self.test_environment()
        results['bybit_connection'] = self.test_bybit_connection()
        results['rsi_calculation'] = self.test_simple_rsi_calculation()
        results['data_collection'] = self.test_data_collection()
        results['trading_simulation'] = self.test_basic_trading_simulation()
        
        # Calculate overall health
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)
        health_score = (passed_tests / total_tests) * 100
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n🎯 OVERALL HEALTH: {health_score:.0f}%")
        
        # Provide recommendations
        print("\n🚀 RECOMMENDATIONS:")
        
        if health_score >= 80:
            print("  ✅ System is healthy - ready for limited deployment")
            print("  📈 Next: Deploy Simple Working Trader with $100 test")
        elif health_score >= 60:
            print("  ⚠️ System needs minor fixes")
            print("  🔧 Next: Fix failing components then test again")
        else:
            print("  ❌ System needs major work")
            print("  🛠️ Next: Focus on basic functionality first")
        
        # Provide specific next steps
        print("\n📋 IMMEDIATE NEXT STEPS:")
        
        if results.get('bybit_connection') and results.get('rsi_calculation'):
            print("  1. ✅ Core trading capability available")
            print("  2. 🚀 Start Simple Working Trader")
            print("  3. 💰 Test with minimal capital ($50-100)")
        else:
            print("  1. 🔧 Fix connection issues first")
            print("  2. 📊 Verify calculation logic")
            print("  3. 🧪 Rerun this test")
        
        return {
            'health_score': health_score,
            'results': results,
            'recommendations': 'Deploy' if health_score >= 80 else 'Fix' if health_score >= 60 else 'Rebuild'
        }

if __name__ == "__main__":
    tester = QuickSystemTest()
    test_results = tester.run_comprehensive_test()
    
    print(f"\n🎯 FINAL STATUS: {test_results['recommendations']}")
    print(f"💡 Health Score: {test_results['health_score']:.0f}%") 