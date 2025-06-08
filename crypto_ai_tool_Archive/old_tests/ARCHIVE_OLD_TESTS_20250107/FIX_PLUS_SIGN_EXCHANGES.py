import os
import ccxt
from dotenv import load_dotenv

def test_exchange_with_plus_in_secret(exchange_name):
    """
    Tests a connection to an exchange that is known to have issues
    with '+' characters in the API secret.
    """
    load_dotenv()
    print(f"--- TESTING: {exchange_name.upper()} ---")

    api_key = os.getenv(f"{exchange_name.upper()}_API_KEY")
    secret = os.getenv(f"{exchange_name.upper()}_SECRET_KEY")
    if exchange_name == 'coinbase':
        # Coinbase uses different var names in this project's .env
        api_key = os.getenv("COINBASE_API_KEY")
        secret = os.getenv("COINBASE_SECRET")
    
    if not api_key or not secret:
        print(f"❌ SKIPPED: Missing API credentials for {exchange_name.upper()} in .env file.\n")
        return

    print(f"🔑 API Key found for {exchange_name.upper()}.")
    if '+' in secret:
        print("⚠️  Secret contains a '+' character. This is the likely cause of auth issues.")
    
    try:
        # Initialize the exchange using ccxt
        exchange_class = getattr(ccxt, exchange_name)
        
        config = {'apiKey': api_key, 'secret': secret}
        if exchange_name == 'coinbase':
            config['password'] = os.getenv("COINBASE_PASSPHRASE")

        exchange = exchange_class(config)

        # For some exchanges, you might need to specify the sandbox/testnet URL
        if hasattr(exchange, 'set_sandbox_mode'):
            exchange.set_sandbox_mode(True)

        # The crucial test: fetch balance
        print("🔄 Fetching balance...")
        balance = exchange.fetch_balance()
        
        print(f"✅ SUCCESS: Connected to {exchange_name.upper()} and fetched balance.")
        
        # Print a summary of the balance
        total_balance = balance.get('total', {})
        found_assets = False
        for currency, value in total_balance.items():
            if value > 0:
                print(f"   - {currency}: {value}")
                found_assets = True
        if not found_assets:
            print("   - No positive balances found.")

    except ccxt.AuthenticationError as e:
        print(f"❌ FAILED: Authentication Error.")
        print("   This confirms the standard ccxt implementation fails with this secret.")
        print("   A custom signature implementation is likely needed if this persists.")
        print(f"   Error: {e}\n")
    except Exception as e:
        print(f"❌ FAILED: An unexpected error occurred.")
        print(f"   Error: {e}\n")


if __name__ == "__main__":
    print("🚀 Running Connection Fixer for Exchanges with '+' in Secret Key...\n")
    
    # We test Coinbase and Kraken as identified
    test_exchange_with_plus_in_secret('coinbase')
    test_exchange_with_plus_in_secret('kraken')

    print("\n--- TEST COMPLETE ---")
    print("If tests failed with AuthenticationError, it confirms the '+' sign issue.")
    print("The next step is to find the signing code for these exchanges and fix the encoding.") 