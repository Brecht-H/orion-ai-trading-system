import logging
import random

from logging_utils import fetch_data, log_trade, analyze_position

symbol = "BTC/USDT"
position = None
entry_price = None

def run():
    global position, entry_price
    try:
        logging.info("🔥 Aggressieve strategie draait!")

        actie = random.choice(["BUY", "SELL"])
        prijs = round(random.uniform(25000, 50000), 2)
        winst = round(random.uniform(-200, 200), 2)

        logging.info(f"📊 Aggressieve trade: {actie} @ ${prijs} | Resultaat: {winst}")
        log_trade("strategy_aggressive", actie, prijs, winst)

        analyze_position(symbol, prijs, position=position, strategy="strategy_aggressive")

    except Exception as e:
        logging.exception(f"❌ Strategie aggressive fout: {e}")