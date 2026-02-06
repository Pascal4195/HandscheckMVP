import requests
import os

def get_eth_transactions(address):
    api_key = os.getenv('ETHERSCAN_API_KEY')
    # 1. Get latest block
    latest_url = f"https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={api_key}"
    response = requests.get(latest_url).json()
    latest_block = int(response['result'], 16)

    # 2. Go back 7 days (~50,400 blocks)
    start_block = latest_block - 50400 

    # 3. Fetch data
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={latest_block}&sort=desc&apikey={api_key}"
    
    data = requests.get(url).json()
    return data.get('result', [])
