import requests

def get_wallet_verdict(address):
    """Analyzes BTC address activity."""
    url = f"https://blockchain.info/rawaddr/{address}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"label1": "Unknown", "label2": "Invalid BTC", "details": "Check address format."}
        
        data = response.json()
        count = len(data.get("txs", []))
        
        if count > 20:
            return {"label1": "Whale", "label2": "HODLer", "details": f"Heavy BTC activity ({count} txs)."}
        return {"label1": "Small Fish", "label2": "Lurker", "details": f"Minimal BTC activity ({count} txs)."}
    except:
        return {"label1": "Error", "label2": "API Down", "details": "Bitcoin network unreachable."}
