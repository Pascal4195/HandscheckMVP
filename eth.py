"""
Ethereum Blockchain Data Module
Fetches ETH wallet data from Etherscan API (requires API key)
"""

import httpx
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta


class ETHAnalyzer:
    """Analyzes Ethereum wallet addresses using Etherscan API"""
    
    def __init__(self):
        self.api_key = os.getenv('ETHERSCAN_API_KEY')
        self.base_url = 'https://api.etherscan.io/api'
        
        if not self.api_key or self.api_key == 'YOUR_KEY_HERE':
            raise ValueError("Etherscan API key not configured. Please add your key to .env file.")
    
    async def get_wallet_data(self, address: str) -> Dict[str, Any]:
        """
        Fetch wallet data for the last 24 hours.
        
        Args:
            address: Ethereum wallet address
            
        Returns:
            Dict with transactions and balance info
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get balance
                balance = await self._get_balance(client, address)
                
                # Get normal transactions
                transactions = await self._get_transactions(client, address)
                
                # Filter transactions from last 24 hours
                cutoff_time = datetime.now() - timedelta(hours=24)
                recent_transactions = self._filter_recent_transactions(
                    transactions, 
                    cutoff_time,
                    address
                )
                
                return {
                    'transactions': recent_transactions,
                    'balance_info': {
                        'balance': balance,
                        'address': address
                    }
                }
                
        except httpx.HTTPError as e:
            raise Exception(f"Error fetching ETH data: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def _get_balance(self, client: httpx.AsyncClient, address: str) -> float:
        """
        Get ETH balance for address.
        
        Args:
            client: HTTP client
            address: Wallet address
            
        Returns:
            Balance in ETH
        """
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': self.api_key
        }
        
        response = await client.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != '1':
            raise Exception(f"Etherscan API error: {data.get('message', 'Unknown error')}")
        
        # Convert Wei to ETH
        balance_wei = int(data['result'])
        return balance_wei / 1e18
    
    async def _get_transactions(self, client: httpx.AsyncClient, address: str) -> List[Dict]:
        """
        Get transaction list for address.
        
        Args:
            client: HTTP client
            address: Wallet address
            
        Returns:
            List of transactions
        """
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': 100,  # Last 100 transactions
            'sort': 'desc',  # Most recent first
            'apikey': self.api_key
        }
        
        response = await client.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != '1':
            # If no transactions found, return empty list
            if 'No transactions found' in data.get('message', ''):
                return []
            raise Exception(f"Etherscan API error: {data.get('message', 'Unknown error')}")
        
        return data['result']
    
    def _filter_recent_transactions(
        self, 
        transactions: List[Dict], 
        cutoff_time: datetime,
        address: str
    ) -> List[Dict[str, Any]]:
        """
        Filter and format transactions from last 24 hours.
        
        Args:
            transactions: List of all transactions
            cutoff_time: Datetime cutoff for filtering
            address: The wallet address being analyzed
            
        Returns:
            List of formatted recent transactions
        """
        recent_txs = []
        address_lower = address.lower()
        
        for tx in transactions:
            # Convert timestamp to datetime
            tx_time = datetime.fromtimestamp(int(tx['timeStamp']))
            
            # Only include transactions from last 24 hours
            if tx_time < cutoff_time:
                continue
            
            # Determine transaction type
            from_addr = tx['from'].lower()
            to_addr = tx['to'].lower()
            
            if from_addr == address_lower:
                tx_type = 'out'
            elif to_addr == address_lower:
                tx_type = 'in'
            else:
                continue  # Skip if address is not directly involved
            
            # Convert value from Wei to ETH
            value_wei = int(tx['value'])
            value_eth = value_wei / 1e18
            
            recent_txs.append({
                'type': tx_type,
                'value': value_eth,
                'timestamp': tx_time.isoformat(),
                'hash': tx['hash']
            })
        
        return recent_txs