import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_verdict(address):
    if not API_KEY:
        return {"label1": "Error", "label2": "Config Missing", "details": "API Key not set in Render."}
    
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("status") != "1":
            return {"label1": "Unknown", "label2": "Invalid Address", "details": "Check address or network status."}
        
        count = len(data.get("result", []))
        if count > 50: return {"label1": "Active Trader", "label2": "Diamond Hands", "details": f"High activity ({count} txs)."}
        return {"label1": "Casual", "label2": "Paper Hands", "details": f"Low activity ({count} txs)."}
    except:
        return {"label1": "Error", "label2": "Network", "details": "Etherscan unreachable."}
