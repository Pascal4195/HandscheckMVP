import requests

def get_btc_transactions(address):
    url = f"https://blockchain.info/rawaddr/{address}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    data = response.json()
    all_txs = data.get('tx', [])
    
    # 7 days of Bitcoin blocks is roughly 1,008
    latest_block_url = "https://blockchain.info/q/getblockcount"
    latest_height = int(requests.get(latest_block_url).text)
    cutoff_height = latest_height - 1008
    
    return [tx for tx in all_txs if tx.get('block_height', 0) >= cutoff_height]
