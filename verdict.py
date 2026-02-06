def get_verdict(transactions):
    if not transactions:
        return "GHOST WALLET", "No activity detected in the last 7 days.", "#808080" # Gray

    tx_count = len(transactions)
    
    # Part A: Activity Level
    if tx_count > 40:
        activity = "DEGEN TRADER"
        color = "#FF4B4B" # Red
    elif tx_count > 10:
        activity = "ACTIVE TRADER"
        color = "#FFA500" # Orange
    else:
        activity = "PATIENT HOLDER"
        color = "#00FF41" # Green (Matrix Green)

    # Part B: Behavior (Selling vs Holding)
    # Checking for 'from' field to see if they are the sender
    sent_count = sum(1 for tx in transactions if 'from' in tx)
    
    if sent_count > (tx_count * 0.6):
        behavior = "🧻 PAPER HANDS"
    else:
        behavior = "💎 DIAMOND HANDS"

    return f"{activity} | {behavior}", f"Found {tx_count} transactions this week.", color
