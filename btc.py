from datetime import datetime, timedelta, timezone

# ... (inside BTCAnalyzer class) ...

    def _determine_tx_type(self, tx: Dict, address: str) -> str:
        """Accurately determines if the NET flow is in or out."""
        net_value = self._calculate_net_satoshis(tx, address)
        return 'in' if net_value > 0 else 'out'

    def _calculate_tx_value(self, tx: Dict, address: str) -> float:
        """Calculates the absolute net change for the wallet in BTC."""
        net_sats = self._calculate_net_satoshis(tx, address)
        return abs(net_sats) / 100_000_000

    def _calculate_net_satoshis(self, tx: Dict, address: str) -> int:
        """
        Calculates net change in Satoshis. 
        Positive = Received, Negative = Sent.
        """
        address_received = 0
        address_sent = 0

        # 1. How much did this address receive in this TX?
        for vout in tx.get('vout', []):
            if vout.get('scriptpubkey_address') == address:
                address_received += vout.get('value', 0)

        # 2. How much did this address contribute to the inputs?
        for vin in tx.get('vin', []):
            prevout = vin.get('prevout')
            if prevout and prevout.get('scriptpubkey_address') == address:
                address_sent += prevout.get('value', 0)

        # Net Change = Received - Sent
        return address_received - address_sent
