import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_wallet_verdict(address):
    """Analyzes Bitcoin wallet activity using Blockchain.info API."""
    # Using Blockchain.info API (doesn't require a key for basic lookups)
    url = f"https://blockchain.info/rawaddr/{address}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"label1": "Error", "label2": "Invalid BTC", "details": "Address not found on Bitcoin network."}
        
        data = response.json()
        txs = data.get("txs", [])
        count = len(txs)
        
        # 7-day logic simulation for BTC
        if count > 30:
            l1, l2, desc = "Whale", "HODLer", "Heavy transaction volume detected."
        elif count > 5:
            l1, l2, desc = "Active", "Sats Stacker", "Regular activity found."
        else:
            l1, l2, desc = "Small Fish", "Newbie", "Very few Bitcoin moves."

        return {
            "label1": l1,
            "label2": l2,
            "details": f"Found {count} BTC transactions. {desc}"
        }
    except Exception as e:
        return {"label1": "Server", "label2": "Error", "details": "Bitcoin API is currently unreachable."}
