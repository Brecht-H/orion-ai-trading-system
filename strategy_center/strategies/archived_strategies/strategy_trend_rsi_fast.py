"""
Strategie: trend_rsi_fast
Gegenereerd door strategy_dev_agent.py op 2025-05-18T15:27:45.883254
"""

def run_strategy(data):
    # Placeholder: voeg je logica toe
    signals = []
    for row in data:
        if row["close"] > row["open"]:
            signals.append("buy")
        else:
            signals.append("sell")
    return signals
