import os
import ccxt
from dotenv import load_dotenv

def test_binance_connection():
    """
    Tests the connection to the Binance Spot Testnet using API keys from the .env file.
    """
    print("🚀 Starting Binance Connection Test...")

    # Load environment variables from .env file
    load_dotenv()

    # --- Get Binance credentials ---
    # Using the primary Binance keys from .env
    binance_api_key = os.getenv("BINANCE_API_KEY")
    binance_api_secret = os.getenv("BINANCE_API_SECRET")

    if not binance_api_key or not binance_api_secret:
        print("❌ ERROR: BINANCE_API_KEY or BINANCE_API_SECRET not found in .env file.")
        return

    print("🔑 API Key found. Attempting to connect to Binance Spot Testnet...")

    # --- Initialize Binance exchange with ccxt for TESTNET ---
    # As per documentation, ccxt handles the testnet URL switch.
    exchange = ccxt.binance({
        'apiKey': binance_api_key,
        'secret': binance_api_secret,
    })
    exchange.set_sandbox_mode(True) # IMPORTANT: Use the testnet

    # --- Test Connection by Fetching Balance ---
    try:
        print("\n🔄 Fetching balance to verify connection and credentials...")
        balance = exchange.fetch_balance()
        print("\n✅ SUCCESS: Binance connection is working!")
        print("   Successfully authenticated and fetched balance from Testnet.")
        
        print("\n💰 Account Balance:")
        total_balance = balance.get('total', {})
        if not total_balance or all(value == 0 for value in total_balance.values()):
            print("   - No funds found or all balances are zero.")
            print("   - NOTE: This could be due to a recent Binance Testnet data reset.")
        else:
            for currency, value in total_balance.items():
                if value > 0:
                    print(f"   - {currency}: {value}")

    except ccxt.AuthenticationError as e:
        print("\n❌ FAILED: Authentication Error.")
        print("   This means your API Key or Secret is incorrect or has been invalidated.")
        print("   This is the expected error if the keys were reset during a Testnet wipe.")
        print("   SOLUTION: Generate new keys at https://testnet.binance.vision and update .env")
        print(f"   Full Error: {e}")
    except ccxt.NetworkError as e:
        print("\n❌ FAILED: Network Error.")
        print("   Could not connect to Binance. Check your internet connection.")
        print(f"   Full Error: {e}")
    except Exception as e:
        print(f"\n❌ FAILED: An unexpected error occurred.")
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_binance_connection() 