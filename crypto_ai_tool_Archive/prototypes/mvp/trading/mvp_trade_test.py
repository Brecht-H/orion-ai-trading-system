#!/usr/bin/env python3
"""
🧪 MVP TRADE TEST - Force trading scenarios to validate logic
"""

from mvp_trading_system import MVPTradingSystem
import time

def test_trading_logic():
    """Test buy/sell logic by forcing RSI values"""
    print("🧪 TESTING MVP TRADING LOGIC")
    print("=" * 50)
    
    mvp = MVPTradingSystem()
    
    # Get real price for testing
    current_price = mvp.get_btc_price()
    if not current_price:
        print("❌ Could not get BTC price")
        return
    
    print(f"Testing with BTC price: ${current_price:,.2f}")
    print(f"Starting portfolio: ${mvp.portfolio_value:,.2f}")
    
    # Test 1: Force BUY signal (oversold)
    print("\n--- TEST 1: FORCED BUY SIGNAL (RSI 25) ---")
    buy_signal = mvp.generate_signal(25)  # Force oversold
    print(f"Signal generated: {buy_signal}")
    
    if buy_signal == "BUY":
        trade_executed = mvp.execute_trade("BUY", current_price)
        if trade_executed:
            print("✅ BUY trade executed successfully")
            total_value = mvp.portfolio_value + (mvp.position_size * current_price)
            print(f"New portfolio state:")
            print(f"  Cash: ${mvp.portfolio_value:,.2f}")
            print(f"  BTC: {mvp.position_size:.6f} BTC")
            print(f"  Total: ${total_value:,.2f}")
        else:
            print("❌ BUY trade failed")
    
    # Record the trade
    mvp.record_trade(current_price, 25, buy_signal)
    
    # Wait a moment
    print("\n⏳ Waiting for price update...")
    time.sleep(2)
    
    # Get updated price
    new_price = mvp.get_btc_price()
    if not new_price:
        new_price = current_price * 1.01  # Simulate 1% increase
        print(f"Using simulated price: ${new_price:,.2f}")
    
    # Test 2: Force SELL signal (overbought)
    print("\n--- TEST 2: FORCED SELL SIGNAL (RSI 75) ---")
    sell_signal = mvp.generate_signal(75)  # Force overbought
    print(f"Signal generated: {sell_signal}")
    
    if sell_signal == "SELL" and mvp.position_size > 0:
        old_total = mvp.portfolio_value + (mvp.position_size * mvp.last_price)
        trade_executed = mvp.execute_trade("SELL", new_price)
        if trade_executed:
            print("✅ SELL trade executed successfully")
            new_total = mvp.portfolio_value
            pnl = new_total - 1000  # Calculate total P&L from starting $1000
            print(f"Final portfolio state:")
            print(f"  Cash: ${mvp.portfolio_value:,.2f}")
            print(f"  BTC: {mvp.position_size:.6f} BTC")
            print(f"  Total P&L: ${pnl:,.2f}")
        else:
            print("❌ SELL trade failed")
    elif mvp.position_size == 0:
        print("⚠️ No BTC position to sell")
    
    # Record the sell trade
    mvp.record_trade(new_price, 75, sell_signal)
    
    # Show final summary
    print("\n📊 TRADING TEST SUMMARY")
    print("-" * 30)
    mvp.show_trade_history()

if __name__ == "__main__":
    test_trading_logic() 