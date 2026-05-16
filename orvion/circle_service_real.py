import requests
import uuid
from typing import Dict, Any
from .config import CIRCLE_API_KEY, CIRCLE_ENTITY_SECRET

class CircleService:
    """
    Integração real com Circle Programmable Wallets para a camada de liquidação ORVION.
    """
    def __init__(self):
        self.base_url = "https://api.circle.com/v1/w3s"
        self.headers = {
            "Authorization": f"Bearer {CIRCLE_API_KEY}",
            "Content-Type": "application/json"
        }

    def create_agent_wallet(self, agent_id: str) -> Dict[str, Any]:
        """
        Cria uma nova Programmable Wallet para um agente.
        """
        endpoint = f"{self.base_url}/developer/wallets"
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "accountType": "SCA",
            "blockchains": ["MATIC-AMOY"], # Exemplo usando Polygon Amoy para compatibilidade Arc
            "metadata": {"agentId": agent_id, "project": "ORVION"}
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def initiate_settlement_payment(self, wallet_id: str, destination_address: str, amount: str) -> Dict[str, Any]:
        """
        Inicia uma transferência de USDC via Circle API para liquidação.
        """
        endpoint = f"{self.base_url}/developer/transactions/transfer"
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "walletId": wallet_id,
            "destinationAddress": destination_address,
            "amount": [amount],
            "tokenId": "USD-TOKEN-ID", # Substituir pelo ID real do USDC na rede
            "blockchain": "MATIC-AMOY",
            "feeLevel": "MEDIUM"
        }

        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Consulta o status de uma transação de liquidação.
        """
        endpoint = f"{self.base_url}/transactions/{transaction_id}"
        try:
            response = requests.get(endpoint, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

circle_service = CircleService()
