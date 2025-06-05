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
symbol = "BNB/USDT"
position = None
entry_price = None

def initialize_strategy():
    logging.basicConfig(level=logging.INFO)
    logging.info(f"📈 Strategie {strategy_name} initialiseren (EMA Cross)")

def should_buy(ema_short, ema_long):
    return ema_short > ema_long

def should_sell(ema_short, ema_long):
    return ema_short < ema_long

def analyze_market():
    prijs = round(random.uniform(26000, 51000), 2)
    ema_short = random.uniform(20000, 52000)
    ema_long = random.uniform(20000, 52000)
    feedback = ""
    if should_buy(ema_short, ema_long):
        actie = "BUY"
        feedback = f"EMA Cross: EMA kort ({ema_short:.2f}) > EMA lang ({ema_long:.2f}), koopmoment."
    elif should_sell(ema_short, ema_long):
        actie = "SELL"
        feedback = f"EMA Cross: EMA kort ({ema_short:.2f}) < EMA lang ({ema_long:.2f}), verkoopmoment."
    else:
        actie = random.choice(["BUY", "SELL"])
        feedback = f"EMA Cross: EMA's zijn gelijk, geen duidelijk signaal."
    winst = round(random.uniform(-190, 230), 2)
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
    logging.info(f"📊 EMA Cross trade: {result['actie']} @ ${result['prijs']} | Resultaat: {result['winst']}")
    log_trade(strategy_name, result['actie'], result['prijs'], result['winst'])
    analyze_position(symbol=symbol, price=result['prijs'], position=position, strategy=strategy_name)
    log_feedback(strategy_name, result['feedback'])