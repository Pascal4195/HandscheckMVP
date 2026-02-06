import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Force pull from environment and strip any accidental quotes
API_KEY = os.getenv("ETHERSCAN_API_KEY", "").replace('"', '').replace("'", "").strip()

def get_wallet_verdict(address):
    address = address.strip()
    
    if not API_KEY or len(API_KEY) < 5:
        return {"label1": "System Error", "label2": "Key Missing", "details": "Check Render Environment Variables for ETHERSCAN_API_KEY."}
    
    # Updated URL format for better compatibility
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&apikey={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        # Log the specific Etherscan error for debugging
        status = data.get("status")
        message = data.get("message", "")
        result = data.get("result", [])

        if status == "0" and message == "NOTOK":
            return {"label1": "API Error", "label2": "Limit Reached", "details": f"Etherscan says: {result}"}

        if not result or len(result) == 0:
            return {"label1": "Ghost Wallet", "label2": "Void Address", "details": "No transaction history found on Ethereum Mainnet."}

        # Analysis Logic
        sells = [t for t in result if t['from'].lower() == address.lower()]
        sell_count = len(sells)

        if sell_count == 0:
            return {"label1": "💎 Diamond Hands", "label2": "“Didn’t flinch. Didn’t sell. Respect.”", "details": "No sells detected in recent activity."}
        elif sell_count > 10:
            return {"label1": "🚪 Exit Liquidity", "label2": "“Someone needed liquidity — and this wallet provided it.”", "details": f"Massive volume: {sell_count} recent sells."}
        elif sell_count > 3:
            return {"label1": "😬 Weak Conviction", "label2": "“In, out, in, out… pick a side.”", "details": "Frequent flip-flopping detected."}
        else:
            return {"label1": "🧻 Paper Hands", "label2": "“Sold the dip. Bought the fear. Classic.”", "details": "Recent sell activity detected."}
            
    except Exception as e:
        return {"label1": "Network Lag", "label2": "Syncing...", "details": f"Connection error: {str(e)[:30]}"}
