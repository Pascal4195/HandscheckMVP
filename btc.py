import requests

def get_wallet_verdict(address):
    address = address.strip()
    url = f"https://blockchain.info/rawaddr/{address}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"label1": "Unknown Entity", "label2": "Address Mismatch", "details": "Bitcoin path unreadable."}
        
        data = response.json()
        txs = data.get("txs", [])
        # Detect outgoing BTC (sells/transfers out)
        sells = [t for t in txs[:10] if any(i['prev_out']['addr'] == address for i in t.get('inputs', []) if 'prev_out' in i)]
        sell_count = len(sells)

        if sell_count == 0:
            return {"label1": "💎 Diamond Hands", "label2": "“Didn’t flinch. Didn’t sell. Respect.”", "details": "No Bitcoin sells detected."}
        elif sell_count > 7:
            return {"label1": "🚪 Exit Liquidity", "label2": "“Someone needed liquidity — and this wallet provided it.”", "details": "Over 70% of recent moves were exits."}
        elif sell_count > 2:
            return {"label1": "😬 Weak Conviction", "label2": "“In, out, in, out… pick a side.”", "details": "Mixed behavior on the BTC chain."}
        else:
            return {"label1": "🧻 Paper Hands", "label2": "“Sold the dip. Bought the fear. Classic.”", "details": "Panic sold into weakness."}
    except:
        return {"label1": "Node Offline", "label2": "Connection Lost", "details": "Could not reach Bitcoin network."}
