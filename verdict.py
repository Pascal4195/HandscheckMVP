"""
Verdict Logic Module
Determines wallet behavior based on transaction patterns
"""

from typing import Dict, Any


def calculate_verdict(transactions: list, balance_info: Dict[str, Any]) -> Dict[str, str]:
    """
    Analyze transactions and return a verdict about wallet behavior.
    
    Args:
        transactions: List of transaction data
        balance_info: Current balance and holding information
        
    Returns:
        Dict with 'verdict' (emoji + label) and 'description'
    """
    
    # Handle empty or insufficient data
    if not transactions or len(transactions) == 0:
        return {
            "verdict": "💎 Diamond Hands",
            "description": "Didn't flinch. Didn't sell. Respect."
        }
    
    # Calculate metrics
    total_value_sold = 0
    total_value_bought = 0
    sell_transactions = 0
    buy_transactions = 0
    total_transactions = len(transactions)
    
    # Analyze transactions
    for tx in transactions:
        value = float(tx.get('value', 0))
        
        if tx.get('type') == 'out':
            total_value_sold += value
            sell_transactions += 1
        elif tx.get('type') == 'in':
            total_value_bought += value
            buy_transactions += 1
    
    # Current balance
    current_balance = float(balance_info.get('balance', 0))
    
    # Calculate sell percentage
    # If wallet had holdings and sold a significant portion
    total_holdings = current_balance + total_value_sold
    
    if total_holdings > 0:
        sell_percentage = (total_value_sold / total_holdings) * 100
    else:
        sell_percentage = 0
    
    # Verdict Logic
    
    # Rule 1: Sold >70% of holdings → Exit Liquidity
    if sell_percentage > 70:
        return {
            "verdict": "🚪 Exit Liquidity",
            "description": "Someone needed liquidity — and this wallet provided it."
        }
    
    # Rule 2: Made sells (paper hands behavior)
    if sell_transactions > 0 and total_value_sold > 0:
        return {
            "verdict": "🧻 Paper Hands",
            "description": "Sold the dip. Bought the fear. Classic."
        }
    
    # Rule 3: No sells → Diamond Hands
    if sell_transactions == 0:
        return {
            "verdict": "💎 Diamond Hands",
            "description": "Didn't flinch. Didn't sell. Respect."
        }
    
    # Rule 4: Multiple in/out transactions → Weak Conviction
    if buy_transactions > 0 and sell_transactions > 0 and total_transactions >= 3:
        return {
            "verdict": "😬 Weak Conviction",
            "description": "In, out, in, out… pick a side."
        }
    
    # Default: Diamond Hands
    return {
        "verdict": "💎 Diamond Hands",
        "description": "Didn't flinch. Didn't sell. Respect."
    }