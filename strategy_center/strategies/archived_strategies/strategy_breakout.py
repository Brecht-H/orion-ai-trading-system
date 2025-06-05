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

def initialize_strategy():
    logging.basicConfig(level=logging.INFO)
    logging.info(f"🚀 Strategie {strategy_name} initialiseren (Breakout)")

def should_buy(close, high_20):
    return close > high_20

def should_sell(close, low_20):
    return close < low_20

def analyze_market():
    # Simuleer prijs en high/low 20
    close = round(random.uniform(25000, 52000), 2)
    high_20 = close - random.uniform(-500, 500)
    low_20 = close - random.uniform(0, 1000)
    feedback = ""
    if should_buy(close, high_20):
        actie = "BUY"
        feedback = f"Breakout: Slotkoers {close} is boven high_20 ({high_20:.2f}), koopmoment."
    elif should_sell(close, low_20):
        actie = "SELL"
        feedback = f"Breakout: Slotkoers {close} is onder low_20 ({low_20:.2f}), verkoopmoment."
    else:
        actie = random.choice(["BUY", "SELL"])
        feedback = f"Breakout: Slotkoers {close} binnen range, geen duidelijk signaal."
    winst = round(random.uniform(-200, 250), 2)
    return {
        "actie": actie,
        "prijs": close,
        "winst": winst,
        "feedback": feedback
    }

def log_feedback(strategy_name, feedback):
    save_feedback(strategy_name, feedback)

def run_strategy():
    initialize_strategy()
    result = analyze_market()
    logging.info(f"🚀 Breakout trade: {result['actie']} @ ${result['prijs']} | Resultaat: {result['winst']}")
    log_trade(strategy_name, result['actie'], result['prijs'], result['winst'])
    analyze_position(symbol=symbol, price=result['prijs'], position=position, strategy=strategy_name)
    log_feedback(strategy_name, result['feedback'])