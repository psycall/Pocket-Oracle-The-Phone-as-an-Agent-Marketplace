# Copyright © 2026 ORVION. All rights reserved.
# Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

"""
Enhanced authentication module with signature verification and token blacklist.
Provides secure wallet login and token management.
"""

import hashlib
import hmac
import logging
from datetime import datetime, timedelta
from typing import Optional, Set
from web3 import Web3
from web3.exceptions import InvalidAddress
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)

# In-memory token blacklist (in production, use Redis)
_TOKEN_BLACKLIST: Set[str] = set()


class SignatureVerifier:
    """Verifies Ethereum signatures for wallet-based authentication."""
    
    @staticmethod
    def verify_signature(message: str, signature: str, address: str) -> bool:
        """
        Verify that a message was signed by the given Ethereum address.
        
        Args:
            message: Original message that was signed
            signature: Hex-encoded signature
            address: Ethereum address that allegedly signed the message
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Ensure address is checksummed
            address = Web3.to_checksum_address(address)
            
            # Encode message with Ethereum prefix
            message_hash = encode_defunct(text=message)
            
            # Recover signer from signature
            recovered_address = Web3.eth.account.recover_message(message_hash, signature=signature)
            
            # Compare recovered address with provided address
            return Web3.to_checksum_address(recovered_address) == address
        except (InvalidAddress, ValueError, Exception) as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    @staticmethod
    def create_challenge(address: str, nonce: int) -> str:
        """
        Create a challenge message for wallet login.
        
        Args:
            address: Ethereum address
            nonce: Unique nonce (timestamp or random)
            
        Returns:
            Challenge message to be signed
        """
        return f"ORVION Authentication\nAddress: {address}\nNonce: {nonce}\nTimestamp: {datetime.utcnow().isoformat()}"


class TokenManager:
    """Manages token lifecycle including blacklist and expiration."""
    
    @staticmethod
    def blacklist_token(token: str) -> None:
        """Add token to blacklist (e.g., on logout)."""
        _TOKEN_BLACKLIST.add(token)
        logger.info(f"Token blacklisted: {token[:20]}...")
    
    @staticmethod
    def is_token_blacklisted(token: str) -> bool:
        """Check if token is blacklisted."""
        return token in _TOKEN_BLACKLIST
    
    @staticmethod
    def clear_expired_tokens(max_age_hours: int = 24) -> None:
        """
        Clear old tokens from blacklist (in production, use Redis TTL).
        This is a simple implementation; use Redis for production.
        """
        # In production: use Redis EXPIRE or similar
        pass
    
    @staticmethod
    def compute_token_hash(token: str, secret: str) -> str:
        """
        Compute HMAC of token for secure storage.
        
        Args:
            token: Token to hash
            secret: Secret key
            
        Returns:
            HMAC hex digest
        """
        return hmac.new(
            secret.encode(),
            token.encode(),
            hashlib.sha256
        ).hexdigest()


class WalletAuthenticationFlow:
    """Orchestrates wallet-based authentication flow."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.verifier = SignatureVerifier()
        self.token_manager = TokenManager()
    
    def create_login_challenge(self, address: str) -> dict:
        """
        Generate a challenge for wallet login.
        
        Returns:
            {
                "challenge": "ORVION Authentication\n...",
                "nonce": 1234567890,
                "expires_in": 300  # seconds
            }
        """
        nonce = int(datetime.utcnow().timestamp())
        challenge = self.verifier.create_challenge(address, nonce)
        
        return {
            "challenge": challenge,
            "nonce": nonce,
            "expires_in": 300,  # 5 minutes
            "address": Web3.to_checksum_address(address)
        }
    
    def verify_wallet_login(self, address: str, message: str, signature: str) -> bool:
        """
        Verify wallet login signature.
        
        Args:
            address: User's Ethereum address
            message: Original challenge message
            signature: User's signature
            
        Returns:
            True if signature is valid
        """
        return self.verifier.verify_signature(message, signature, address)
    
    def revoke_token(self, token: str) -> None:
        """Revoke (blacklist) a token."""
        self.token_manager.blacklist_token(token)
    
    def is_token_valid(self, token: str) -> bool:
        """Check if token is still valid (not blacklisted)."""
        return not self.token_manager.is_token_blacklisted(token)
