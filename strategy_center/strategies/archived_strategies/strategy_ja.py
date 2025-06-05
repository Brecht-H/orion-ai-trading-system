"""
Strategie: ja
Gegenereerd door strategy_dev_agent.py op 2025-05-18T15:23:43.904093
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
