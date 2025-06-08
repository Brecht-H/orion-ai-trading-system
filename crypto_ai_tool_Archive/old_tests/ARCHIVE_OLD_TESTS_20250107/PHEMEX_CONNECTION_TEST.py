import os
import ccxt
from dotenv import load_dotenv

def test_phemex_connection():
    """
    Tests the connection to Phemex using API keys from the .env file.
    """
    print("🚀 Starting Phemex Connection Test...")

    # Load environment variables from .env file
    load_dotenv()

    # --- Get Phemex credentials ---
    phemex_api_key = os.getenv("PHEMEX_API_KEY")
    phemex_api_secret = os.getenv("PHEMEX_API_SECRET")

    if not phemex_api_key or not phemex_api_secret:
        print("❌ ERROR: PHEMEX_API_KEY or PHEMEX_API_SECRET not found in .env file.")
        return

    print("🔑 API Key found. Attempting to connect to Phemex Testnet...")

    # --- Initialize Phemex exchange with ccxt for TESTNET ---
    exchange = ccxt.phemex({
        'apiKey': phemex_api_key,
        'secret': phemex_api_secret,
    })
    exchange.set_sandbox_mode(True) # IMPORTANT: Use the testnet

    # --- Test Connection by Fetching Balance ---
    try:
        print("\n🔄 Fetching balance to verify connection and credentials...")
        balance = exchange.fetch_balance()
        print("\n✅ SUCCESS: Phemex connection is working!")
        print("   Successfully authenticated and fetched balance from Testnet.")
        
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
        print("   This means your API Key or Secret is incorrect for the **Testnet**.")
        print("   Please ensure the keys are for the Phemex Testnet.")
        print(f"   Full Error: {e}")
    except ccxt.NetworkError as e:
        print("\n❌ FAILED: Network Error.")
        print("   Could not connect to Phemex. Check your internet connection.")
        print(f"   Full Error: {e}")
    except Exception as e:
        print(f"\n❌ FAILED: An unexpected error occurred.")
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_phemex_connection() 