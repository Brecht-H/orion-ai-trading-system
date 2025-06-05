import os
import logging
import random
from logging_utils import log_trade, analyze_position, save_feedback

# Enhanced Signal Detection Integration
# Auto-generated integration for v2_enhanced signals
import sys
sys.path.append('src/signal_detection')

try:
    from crypto_signal_detector_v2_enhanced import CryptoSignalDetector, integrate_enhanced_sources
    
    def get_enhanced_market_signals():
        """Get enhanced market signals for strategy optimization"""
        try:
            detector = CryptoSignalDetector()
            signals = detector.get_current_signals()
            return {
                "signal_strength": signals.get("strength", "WEAK"),
                "sentiment_score": signals.get("sentiment", 0.5),
                "data_sources_count": signals.get("sources", 0),
                "recommendation": signals.get("action", "HOLD")
            }
        except Exception as e:
            print(f"⚠️ Enhanced signals unavailable: {e}")
            return {
                "signal_strength": "WEAK",
                "sentiment_score": 0.5,
                "data_sources_count": 0,
                "recommendation": "HOLD"
            }
    
    # Auto-integration on import
    enhanced_signals = get_enhanced_market_signals()
    print(f"📡 Enhanced signals loaded: {enhanced_signals['data_sources_count']} sources")
    
except ImportError as e:
    print(f"⚠️ Enhanced signal integration not available: {e}")
    enhanced_signals = None



strategy_name = os.path.basename(__file__)
symbol = "ETH/USDT"
position = None
entry_price = None

def initialize_strategy():
    logging.basicConfig(level=logging.INFO)
    logging.info(f"📉 Strategie {strategy_name} initialiseren (MACD Signal)")

def should_buy(macd, signal):
    return macd > signal

def should_sell(macd, signal):
    return macd < signal

def analyze_market():
    prijs = round(random.uniform(26000, 49000), 2)
    macd = random.uniform(-2, 2)
    signal = random.uniform(-2, 2)
    feedback = ""
    if should_buy(macd, signal):
        actie = "BUY"
        feedback = f"MACD Signal: MACD ({macd:.2f}) > Signaal ({signal:.2f}), koopmoment."
    elif should_sell(macd, signal):
        actie = "SELL"
        feedback = f"MACD Signal: MACD ({macd:.2f}) < Signaal ({signal:.2f}), verkoopmoment."
    else:
        actie = random.choice(["BUY", "SELL"])
        feedback = f"MACD Signal: MACD ({macd:.2f}) ≈ Signaal ({signal:.2f}), geen duidelijk signaal."
    winst = round(random.uniform(-160, 200), 2)
    return {
        "actie": actie,
        "prijs": prijs,
        "winst": winst,
        "feedback": feedback
    }

def log_feedback(strategy_name, feedback):
    save_feedback(strategy_name, feedback)

def run_strategy():
    initialize_strategy()
    result = analyze_market()
    logging.info(f"📊 MACD Signal trade: {result['actie']} @ ${result['prijs']} | Resultaat: {result['winst']}")
    log_trade(strategy_name, result['actie'], result['prijs'], result['winst'])
    analyze_position(symbol=symbol, price=result['prijs'], position=position, strategy=strategy_name)
    log_feedback(strategy_name, result['feedback'])