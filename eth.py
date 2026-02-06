import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_verdict(address):
    address = address.strip()
    if not API_KEY:
        return {"label1": "System Error", "label2": "API Missing", "details": "Set ETHERSCAN_API_KEY in Render."}
    
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("status") != "1":
            return {"label1": "Ghost Wallet", "label2": "Void Address", "details": "Invalid ETH address or no history found."}

        txs = data.get("result", [])
        # Simplified logic for 'Sell' detection (Outgoing Transactions)
        sells = [t for t in txs[:20] if t['from'].lower() == address.lower()]
        sell_count = len(sells)

        if sell_count == 0:
            return {"label1": "💎 Diamond Hands", "label2": "“Didn’t flinch. Didn’t sell. Respect.”", "details": "No sells detected in recent activity."}
        elif sell_count > 10:
            return {"label1": "🚪 Exit Liquidity", "label2": "“Someone needed liquidity — and this wallet provided it.”", "details": "Massive sell volume detected recently."}
        elif sell_count > 3:
            return {"label1": "😬 Weak Conviction", "label2": "“In, out, in, out… pick a side.”", "details": "Frequent flip-flopping and partial sells."}
        else:
            return {"label1": "🧻 Paper Hands", "label2": "“Sold the dip. Bought the fear. Classic.”", "details": "Sold into local weakness."}
            
    except Exception:
        return {"label1": "Network Lag", "label2": "Syncing...", "details": "Etherscan is taking too long."}
