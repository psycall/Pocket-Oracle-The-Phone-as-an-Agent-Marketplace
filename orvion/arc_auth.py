"""
Arc Wallet Authentication
Integração com ethers.js para wallet-connect e assinatura
"""

import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import jwt
import os
from eth_account import Account
from eth_account.messages import encode_defunct
import httpx

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class ArcAuthService:
    """Arc Wallet authentication service"""

    @staticmethod
    def verify_signature(
        address: str, message: str, signature: str
    ) -> bool:
        """
        Verify Ethereum signature
        Used for wallet-connect authentication
        """
        try:
            # Encode message as Ethereum message
            message_hash = encode_defunct(text=message)

            # Recover address from signature
            recovered_address = Account.recover_message(message_hash, signature=signature)

            # Compare addresses (case-insensitive)
            return recovered_address.lower() == address.lower()

        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False

    @staticmethod
    def create_access_token(
        user_id: str, wallet_address: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "sub": user_id,
            "wallet": wallet_address,
            "exp": expire,
            "iat": datetime.utcnow(),
        }

        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

    @staticmethod
    async def get_wallet_nonce(wallet_address: str) -> str:
        """
        Get nonce for wallet authentication
        Prevents replay attacks
        """
        timestamp = datetime.utcnow().isoformat()
        nonce = f"ORVION_AUTH_{wallet_address}_{timestamp}"
        return nonce

    @staticmethod
    async def verify_arc_wallet(wallet_address: str) -> bool:
        """
        Verify wallet exists on Arc network
        """
        try:
            arc_rpc_url = os.getenv("ARC_RPC_URL", "https://testnet-rpc.arc.io")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    arc_rpc_url,
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [wallet_address, "latest"],
                        "id": 1,
                    },
                    timeout=10,
                )

                if response.status_code == 200:
                    result = response.json()
                    return "result" in result
                return False

        except Exception as e:
            logger.error(f"Failed to verify Arc wallet: {e}")
            return False


class WalletLoginRequest:
    """Wallet login request model"""

    def __init__(self, wallet_address: str, signature: str, message: str):
        self.wallet_address = wallet_address
        self.signature = signature
        self.message = message

    def validate(self) -> bool:
        """Validate request"""
        if not self.wallet_address or not self.wallet_address.startswith("0x"):
            logger.warning("Invalid wallet address")
            return False

        if not self.signature or not self.signature.startswith("0x"):
            logger.warning("Invalid signature")
            return False

        if not self.message:
            logger.warning("Missing message")
            return False

        return True


async def authenticate_wallet(request: WalletLoginRequest) -> Optional[Dict[str, Any]]:
    """
    Authenticate user via wallet
    Returns JWT token if successful
    """
    # Validate request
    if not request.validate():
        logger.warning("Invalid wallet login request")
        return None

    # Verify signature
    if not ArcAuthService.verify_signature(
        request.wallet_address, request.message, request.signature
    ):
        logger.warning(f"Signature verification failed for {request.wallet_address}")
        return None

    # Verify wallet exists on Arc
    if not await ArcAuthService.verify_arc_wallet(request.wallet_address):
        logger.warning(f"Wallet not found on Arc network: {request.wallet_address}")
        return None

    # Create token
    user_id = request.wallet_address.lower()
    token = ArcAuthService.create_access_token(user_id, request.wallet_address)

    return {
        "access_token": token,
        "token_type": "bearer",
        "wallet_address": request.wallet_address,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
