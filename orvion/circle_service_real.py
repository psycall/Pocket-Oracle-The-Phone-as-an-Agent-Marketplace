"""
Circle CCTP Real Integration
Programmable Wallets SDK para USDC cross-chain settlements
"""

import os
import logging
from typing import Dict, Optional, Any
from decimal import Decimal
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)


class CircleCCTPService:
    """
    Real Circle CCTP integration using Programmable Wallets SDK
    Supports USDC transfers across 12+ blockchain networks
    """

    def __init__(self):
        self.api_key = os.getenv("CIRCLE_API_KEY")
        self.entity_secret = os.getenv("CIRCLE_ENTITY_SECRET")
        self.wallet_set_id = os.getenv("CIRCLE_WALLET_SET_ID")
        self.base_url = "https://api.circle.com/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

        if not all([self.api_key, self.entity_secret, self.wallet_set_id]):
            logger.warning(
                "Circle credentials not fully configured. Using mock mode."
            )
            self.mock_mode = True
        else:
            self.mock_mode = False

    async def create_wallet(self, user_id: str) -> Dict[str, Any]:
        """Create a new Circle wallet for user"""
        if self.mock_mode:
            return {
                "id": f"wallet_{user_id}",
                "address": f"0x{user_id[:40]}",
                "blockchain": "arc",
                "status": "ACTIVE",
            }

        try:
            payload = {
                "idempotencyKey": f"{user_id}_{datetime.now().timestamp()}",
                "walletSetId": self.wallet_set_id,
                "blockchains": ["ARC", "ETHEREUM", "POLYGON", "OPTIMISM"],
            }

            response = await self.client.post(
                f"{self.base_url}/w3/wallets", json=payload
            )
            response.raise_for_status()
            return response.json()["data"]

        except Exception as e:
            logger.error(f"Failed to create wallet: {e}")
            raise

    async def get_wallet_balance(
        self, wallet_id: str, blockchain: str = "ARC"
    ) -> Decimal:
        """Get USDC balance for wallet"""
        if self.mock_mode:
            return Decimal("1000.00")

        try:
            response = await self.client.get(
                f"{self.base_url}/w3/wallets/{wallet_id}/balances",
                params={"blockchain": blockchain},
            )
            response.raise_for_status()
            balances = response.json()["data"]["balances"]

            # Find USDC balance
            for balance in balances:
                if balance["token"]["symbol"] == "USDC":
                    return Decimal(balance["amount"])

            return Decimal("0")

        except Exception as e:
            logger.error(f"Failed to get wallet balance: {e}")
            raise

    async def transfer_usdc(
        self,
        from_wallet_id: str,
        to_address: str,
        amount: Decimal,
        source_blockchain: str = "ARC",
        destination_blockchain: str = "ARC",
    ) -> Dict[str, Any]:
        """
        Transfer USDC using Circle CCTP
        Supports cross-chain transfers
        """
        if self.mock_mode:
            return {
                "id": f"tx_{datetime.now().timestamp()}",
                "status": "PENDING",
                "from": from_wallet_id,
                "to": to_address,
                "amount": str(amount),
                "token": "USDC",
                "sourceBlockchain": source_blockchain,
                "destinationBlockchain": destination_blockchain,
                "transactionHash": f"0x{'0' * 64}",
            }

        try:
            payload = {
                "idempotencyKey": f"{from_wallet_id}_{to_address}_{datetime.now().timestamp()}",
                "walletId": from_wallet_id,
                "tokenId": "USDC",
                "destinationAddress": to_address,
                "amounts": [str(amount)],
                "blockchain": source_blockchain,
            }

            # If cross-chain, use CCTP
            if source_blockchain != destination_blockchain:
                payload["destinationBlockchain"] = destination_blockchain

            response = await self.client.post(
                f"{self.base_url}/w3/wallets/{from_wallet_id}/transfers",
                json=payload,
            )
            response.raise_for_status()
            return response.json()["data"]

        except Exception as e:
            logger.error(f"Failed to transfer USDC: {e}")
            raise

    async def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """Get status of a transaction"""
        if self.mock_mode:
            return {
                "id": transaction_id,
                "status": "CONFIRMED",
                "confirmations": 12,
                "transactionHash": f"0x{'0' * 64}",
            }

        try:
            response = await self.client.get(
                f"{self.base_url}/w3/transactions/{transaction_id}"
            )
            response.raise_for_status()
            return response.json()["data"]

        except Exception as e:
            logger.error(f"Failed to get transaction status: {e}")
            raise

    async def estimate_gas(
        self, from_address: str, to_address: str, amount: Decimal, blockchain: str
    ) -> Dict[str, Any]:
        """Estimate gas fees for transfer"""
        if self.mock_mode:
            return {
                "gasPrice": "50",
                "gasLimit": "21000",
                "totalGas": "1050000000000000",  # 0.00105 ETH
                "estimatedTime": "~2 minutes",
            }

        try:
            payload = {
                "from": from_address,
                "to": to_address,
                "amount": str(amount),
                "blockchain": blockchain,
            }

            response = await self.client.post(
                f"{self.base_url}/w3/estimate-gas", json=payload
            )
            response.raise_for_status()
            return response.json()["data"]

        except Exception as e:
            logger.error(f"Failed to estimate gas: {e}")
            raise

    async def get_supported_blockchains(self) -> list:
        """Get list of supported blockchains"""
        if self.mock_mode:
            return [
                "ARC",
                "ETHEREUM",
                "POLYGON",
                "OPTIMISM",
                "ARBITRUM",
                "AVALANCHE",
                "BASE",
                "SOLANA",
                "PHAROS",
            ]

        try:
            response = await self.client.get(f"{self.base_url}/configuration/networks")
            response.raise_for_status()
            networks = response.json()["data"]["networks"]
            return [n["blockchain"] for n in networks if n["enabled"]]

        except Exception as e:
            logger.error(f"Failed to get supported blockchains: {e}")
            raise

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_circle_service: Optional[CircleCCTPService] = None


async def get_circle_service() -> CircleCCTPService:
    """Get or create Circle service instance"""
    global _circle_service
    if _circle_service is None:
        _circle_service = CircleCCTPService()
    return _circle_service


async def close_circle_service():
    """Close Circle service"""
    global _circle_service
    if _circle_service:
        await _circle_service.close()
        _circle_service = None
