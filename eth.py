import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY", "").replace('"', '').replace("'", "").strip()

def get_wallet_verdict(address):
    address = address.strip()
    
    if not API_KEY:
        return {"label1": "System Error", "label2": "Key Missing", "details": "Please check your Render Environment Variables."}
    
    # MENDED: Updated to Etherscan API V2 Endpoint
    url = f"https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=100&sort=desc&apikey={API_KEY}"
    
    try:
        r = requests.get(url, timeout=12)
        data = r.json()
        
        # Etherscan V2 sometimes wraps results differently
        result = data.get("result", [])

        if isinstance(result, str) or not result:
            return {"label1": "Void Wallet", "label2": "No History", "details": "This address has no recorded moves on Ethereum."}

        # Analysis Logic for your specific write-ups
        total_count = len(result)
        sells = [t for t in result if str(t.get('from', '')).lower() == address.lower()]
        sell_count = len(sells)

        if sell_count == 0 and total_count > 0:
            return {"label1": "💎 Diamond Hands", "label2": "“Didn’t flinch. Didn’t sell. Respect.”", "details": f"Pure accumulation detected over {total_count} transactions."}
        
        elif sell_count > 15:
            return {"label1": "🚪 Exit Liquidity", "label2": "“Someone needed liquidity — and this wallet provided it.”", "details": "High-frequency selling behavior detected."}
            
        elif sell_count > 5:
            return {"label1": "😬 Weak Conviction", "label2": "“In, out, in, out… pick a side.”", "details": "Frequent flip-flopping between positions."}
            
        else:
            return {"label1": "🧻 Paper Hands", "label2": "“Sold the dip. Bought the fear. Classic.”", "details": "Detected recent sell pressure from this wallet."}
            
    except Exception as e:
        return {"label1": "Scan Failed", "label2": "Timeout", "details": "Etherscan V2 is busy. Try again in a moment."}
