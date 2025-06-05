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
    logging.info(f"🔄 Strategie {strategy_name} initialiseren (Mean Reversion)")

def should_buy(price):
    # Simuleer mean reversion: koop als prijs onder een drempel
    threshold = 30000
    return price < threshold

def should_sell(price):
    # Simuleer mean reversion: verkoop als prijs boven een drempel
    threshold = 45000
    return price > threshold

def analyze_market():
    prijs = round(random.uniform(24000, 52000), 2)
    feedback = ""
    if should_buy(prijs):
        actie = "BUY"
        feedback = f"Mean Reversion: Prijs {prijs} is onder {30000}, koopmoment."
    elif should_sell(prijs):
        actie = "SELL"
        feedback = f"Mean Reversion: Prijs {prijs} is boven {45000}, verkoopmoment."
    else:
        actie = random.choice(["BUY", "SELL"])
        feedback = f"Mean Reversion: Prijs {prijs} in neutraal gebied, willekeurige actie."
    winst = round(random.uniform(-180, 250), 2)
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
    logging.info(f"📊 Mean Reversion trade: {result['actie']} @ ${result['prijs']} | Resultaat: {result['winst']}")
    log_trade(strategy_name, result['actie'], result['prijs'], result['winst'])
    analyze_position(symbol=symbol, price=result['prijs'], position=position, strategy=strategy_name)
    log_feedback(strategy_name, result['feedback'])