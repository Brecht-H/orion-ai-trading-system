import os
import logging
import random
from logging_utils import log_trade, analyze_position, save_feedback

strategy_name = os.path.basename(__file__)
symbol = "BTC/USDT"
position = None
entry_price = None

def initialize_strategy():
    logging.basicConfig(level=logging.INFO)
    logging.info(f"📊 Strategie {strategy_name} initialiseren (RSI Trend)")

def should_buy(rsi):
    return rsi < 30

def should_sell(rsi):
    return rsi > 70

def analyze_market():
    prijs = round(random.uniform(25000, 47000), 2)
    rsi = random.randint(10, 90)
    feedback = ""
    if should_buy(rsi):
        actie = "BUY"
        feedback = f"RSI Trend: RSI {rsi} is laag, koopmoment."
    elif should_sell(rsi):
        actie = "SELL"
        feedback = f"RSI Trend: RSI {rsi} is hoog, verkoopmoment."
    else:
        actie = random.choice(["BUY", "SELL"])
        feedback = f"RSI Trend: RSI {rsi} is neutraal, geen duidelijk signaal."
    winst = round(random.uniform(-140, 210), 2)
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
    logging.info(f"📈 RSI Trend trade: {result['actie']} @ ${result['prijs']} | Resultaat: {result['winst']}")
    log_trade(strategy_name, result['actie'], result['prijs'], result['winst'])
    analyze_position(symbol=symbol, price=result['prijs'], position=position, strategy=strategy_name)
    log_feedback(strategy_name, result['feedback'])