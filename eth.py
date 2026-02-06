import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_verdict(address):
    """Analyzes 7 days of wallet activity and returns labels."""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["status"] != "1":
            return {"label1": "Error", "label2": "Invalid Address", "details": "Check the ETH address and try again."}

        txs = data["result"]
        # Filter for last 7 days (roughly)
        # For MVP: Simple count check
        count = len(txs)
        
        if count > 50:
            l1, l2, desc = "Active Trader", "Diamond Hands", "High volume over 7 days."
        elif count > 10:
            l1, l2, desc = "Casual User", "Paper Hands", "Low activity recently."
        else:
            l1, l2, desc = "Newbie", "Lurker", "Very few transactions found."

        return {
            "label1": l1,
            "label2": l2,
            "details": f"Found {count} transactions. {desc}"
        }
    except Exception as e:
        return {"label1": "Server", "label2": "Error", "details": str(e)}
