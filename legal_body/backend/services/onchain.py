"""
Thin web3.py wrapper for AgentPersona.sol.
Falls back to a 'dry-run' mode (returns deterministic fake tx hashes)
when web3 or RPC are not configured — so the UI is always usable
during development and demos.
"""
from __future__ import annotations
import os
import hashlib
from typing import Optional

JURISDICTION_ENUM = {
    "WYOMING_DAO_LLC": 0,
    "DELAWARE_SERIES_LLC": 1,
    "NEW_YORK_LLC": 2,
    "MARSHALL_ISLANDS_DAO": 3,
}


class OnChainClient:
    def __init__(self,
                 rpc_url: Optional[str] = None,
                 contract_address: Optional[str] = None,
                 private_key: Optional[str] = None):
        self.rpc_url = rpc_url or os.getenv("ORVION_ARC_RPC", "")
        self.contract_address = contract_address or os.getenv("ORVION_PERSONA_CONTRACT", "")
        self.private_key = private_key or os.getenv("ORVION_DEPLOYER_KEY", "")
        self.enabled = bool(self.rpc_url and self.contract_address and self.private_key)
        self._w3 = None
        if self.enabled:
            try:
                from web3 import Web3  # type: ignore
                self._w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            except ImportError:
                self.enabled = False

    def _dry_tx(self, salt: str) -> str:
        return "0x" + hashlib.sha256(salt.encode()).hexdigest()

    def incorporate(self,
                    agent_wallet: str,
                    jurisdiction: str,
                    legal_name: str,
                    oa_hash: str,
                    registered_agent_uri: str = "") -> dict:
        if not self.enabled:
            return {
                "tx_hash": self._dry_tx(f"{agent_wallet}|{legal_name}"),
                "persona_id": abs(hash(agent_wallet)) % 10_000 + 1,
                "dry_run": True,
            }
        # Real path (requires deployed contract + ABI):
        # contract = self._w3.eth.contract(address=self.contract_address, abi=AGENT_PERSONA_ABI)
        # tx = contract.functions.incorporate(...).build_transaction(...)
        # signed = self._w3.eth.account.sign_transaction(tx, self.private_key)
        # tx_hash = self._w3.eth.send_raw_transaction(signed.rawTransaction)
        # receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash)
        # return {"tx_hash": tx_hash.hex(), "persona_id": <decode from event>, "dry_run": False}
        raise NotImplementedError("Wire ABI + transaction builder before production use.")
