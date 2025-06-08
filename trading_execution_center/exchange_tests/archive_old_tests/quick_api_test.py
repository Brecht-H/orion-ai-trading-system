#!/usr/bin/env python3
import os
import time
import hmac
import hashlib
import requests
from datetime import datetime

print('🔧 PHEMEX & COINBASE API CREDENTIAL TESTER')
print('=' * 60)
print(f'📅 Test Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('🎯 Goal: Test Phemex after user trade + check Coinbase format')

# Test Phemex Account 1
print('\n🏛️ TESTING PHEMEX ACCOUNT 1...')
api_key_1 = 'TkXmB-wEDvVpsZuLljNUSss56jmzvbp7kIlJDPAscqNkODdhN2RhNi03ODc4LTQ0ZjQtYmU5MS0xMDgxMGIwYmU3Nzk'
api_id_1 = '1a2b91aa-25f8-4ecb-9854-87a3cf4030b4'

try:
    url = 'https://testnet-api.phemex.com/accounts/accountPositions'
    timestamp = str(int(time.time()))
    
    message = f'GET/accounts/accountPositions{timestamp}'
    signature = hmac.new(
        api_key_1.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        'x-phemex-access-token': api_key_1,
        'x-phemex-request-signature': signature,
        'x-phemex-request-timestamp': timestamp,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    print(f'📡 Phemex Account 1 Response: HTTP {response.status_code}')
    
    if response.status_code == 200:
        print('✅ Phemex Account 1: API Connected Successfully!')
    else:
        print(f'❌ Phemex Account 1: HTTP {response.status_code} - {response.text[:100]}')
        
except Exception as e:
    print(f'❌ Phemex Account 1: Error - {str(e)}')

# Test Phemex Account 2
print('\n🏛️ TESTING PHEMEX ACCOUNT 2...')
api_key_2 = 'lcUQ8Zc27h8wwHosHwpmmNGAOqAzg9v60SBswgvpYEoxOGRhNDk3ZS1hNzkyLTRkYmItOTBiZi1lYTA1NWU4ZmY2ZGY'
api_id_2 = '63b7a04c-5d06-49f3-b0f2-ed7970bdf3f1'

try:
    url = 'https://testnet-api.phemex.com/accounts/accountPositions'
    timestamp = str(int(time.time()))
    
    message = f'GET/accounts/accountPositions{timestamp}'
    signature = hmac.new(
        api_key_2.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        'x-phemex-access-token': api_key_2,
        'x-phemex-request-signature': signature,
        'x-phemex-request-timestamp': timestamp,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    print(f'📡 Phemex Account 2 Response: HTTP {response.status_code}')
    
    if response.status_code == 200:
        print('✅ Phemex Account 2: API Connected Successfully!')
    else:
        print(f'❌ Phemex Account 2: HTTP {response.status_code} - {response.text[:100]}')
        
except Exception as e:
    print(f'❌ Phemex Account 2: Error - {str(e)}')

# Check Coinbase Credentials Format
print('\n🪙 COINBASE CREDENTIAL FORMAT CHECK...')
print('=' * 50)

accounts = [
    {
        'name': 'Coinbase Testnet 1',
        'api_key': 'dkSh3SMN4QWET5gGiI+8L0rLURNfaFBcE1Rwskl5IUi8oGIryA6//VuYEEvXEYi19n6zk681Js3hguicSCyZoQ==',
        'passphrase': 'hlcz5rwa39t7'
    },
    {
        'name': 'Coinbase Testnet 2', 
        'api_key': 'TSEw2UuuxiYaTO1lMmnxz/aRNEG04Xt4olp1WSkY0nf0Yn+RGxzKmy1TOjW8ndF5gxUGk7flPIjyIYJT02KhCA==',
        'passphrase': 'p5xihrg7ezmm'
    },
    {
        'name': 'Coinbase Testnet 3',
        'api_key': 'PiF2MrOCWZW9xuG8XIg9Pxse9vlrmvtyTUj9Ori7DtyGofVi1LAXHimuV6PNL42EjZ+KKTY1ivSq6JwK7ORsnA==',
        'passphrase': '33xmm8vo7cyu'
    }
]

print('📋 CREDENTIAL STATUS:')
for account in accounts:
    print(f'\n{account["name"]}:')
    print(f'  ✅ API_KEY: {account["api_key"][:20]}...')
    print(f'  ✅ PASSPHRASE: {account["passphrase"]}')
    print(f'  ❌ API_SECRET: MISSING!')

print(f'\n🔧 FIX NEEDED for .env file:')
print('Add these lines with your actual API secrets:')
print('')
print('#Coinbase Testnet:')
print('API_KEY=dkSh3SMN4QWET5gGiI+8L0rLURNfaFBcE1Rwskl5IUi8oGIryA6//VuYEEvXEYi19n6zk681Js3hguicSCyZoQ==')
print('API_SECRET=YOUR_API_SECRET_1_HERE')
print('Passphrase=hlcz5rwa39t7')
print('')
print('#Coinbase Testnet2:')
print('API_KEY=TSEw2UuuxiYaTO1lMmnxz/aRNEG04Xt4olp1WSkY0nf0Yn+RGxzKmy1TOjW8ndF5gxUGk7flPIjyIYJT02KhCA==')
print('API_SECRET=YOUR_API_SECRET_2_HERE')
print('Passphrase=p5xihrg7ezmm')
print('')
print('#Coinbase Testnet3:')
print('API_KEY=PiF2MrOCWZW9xuG8XIg9Pxse9vlrmvtyTUj9Ori7DtyGofVi1LAXHimuV6PNL42EjZ+KKTY1ivSq6JwK7ORsnA==')
print('API_SECRET=YOUR_API_SECRET_3_HERE')
print('passphrase=33xmm8vo7cyu')

print('\n🏁 TESTING COMPLETE!')
print('=' * 60) 