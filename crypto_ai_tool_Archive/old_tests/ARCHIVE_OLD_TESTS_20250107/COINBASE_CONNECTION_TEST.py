import os
import ccxt
from dotenv import load_dotenv
import urllib.parse

def test_coinbase_connection():
    """
    Tests the connection to Coinbase Advanced Trade API using keys from the .env file.
    Highlights the common '+' character issue in secrets.
    """
    print("🚀 Starting Coinbase Connection Test...")
    load_dotenv()

    # --- Get Coinbase credentials ---
    api_key = os.getenv("COINBASE_API_KEY")
    secret = os.getenv("COINBASE_SECRET")
    passphrase = os.getenv("COINBASE_PASSPHRASE")

    if not all([api_key, secret, passphrase]):
        print("❌ ERROR: Coinbase credentials (KEY, SECRET, PASSPHRASE) not found in .env.")
        return

    if '+' in secret:
        print("\n⚠️ WARNING: Your COINBASE_SECRET contains a '+' character.")
        print("   This is a known cause for authentication failures if not handled correctly.")
        print("   The script will now test the connection. If it fails, this is the likely cause.\n")
    
    print("🔑 API Key found. Attempting to connect to Coinbase...")

    # --- Initialize Coinbase exchange with ccxt ---
    exchange = ccxt.coinbase({
        'apiKey': api_key,
        'secret': secret,
        'password': passphrase,
    })

    # --- Test Connection by Fetching Balance ---
    try:
        print("\n🔄 Fetching balance to verify connection and credentials...")
        balance = exchange.fetch_balance()
        print("\n✅ SUCCESS: Coinbase connection is working!")
        print("   This means your environment correctly handles the API secret.")
        
        print("\n💰 Account Balance:")
        total_balance = balance.get('total', {})
        if not total_balance or all(value == 0 for value in total_balance.values()):
            print("   - No funds found or all balances are zero.")
        else:
            for currency, value in total_balance.items():
                if value > 0:
                    print(f"   - {currency}: {value}")

    except ccxt.AuthenticationError as e:
        print("\n❌ FAILED: Authentication Error.")
        print("   This is the expected error when the '+' in the secret is mishandled.")
        print("   SOLUTION: The signing mechanism in the core code needs to be fixed to ensure")
        print("   the raw secret is used for hashing, not a URL-encoded version.")
        print(f"   Full Error: {e}")
    except Exception as e:
        print(f"\n❌ FAILED: An unexpected error occurred.")
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_coinbase_connection() 