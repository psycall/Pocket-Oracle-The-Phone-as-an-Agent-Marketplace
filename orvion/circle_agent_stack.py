import requests
import uuid
from .config import CIRCLE_API_KEY, ENTITY_SECRET, WALLET_SET_ID

class CircleAgentStack:
    def __init__(self):
        self.base_url = "https://api.circle.com/v1/w3s"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CIRCLE_API_KEY}"
        }

    def create_agent_wallet(self, agent_id: str):
        """
        Cria uma carteira programável para um agente.
        """
        endpoint = f"{self.base_url}/developer/wallets"
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "entitySecret": ENTITY_SECRET,
            "walletSetId": WALLET_SET_ID,
            "blockchain": "MATIC-AMOY", # Usando Amoy como padrão para teste/Arc
            "count": 1
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()

    def get_wallet_balance(self, wallet_id: str):
        """
        Consulta o saldo de USDC na carteira do agente.
        """
        endpoint = f"{self.base_url}/wallets/{wallet_id}/balances"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def transfer_between_agents(self, source_wallet_id: str, destination_address: str, amount: str):
        """
        Realiza transferência autônoma entre agentes.
        """
        endpoint = f"{self.base_url}/developer/transactions/transfer"
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "entitySecret": ENTITY_SECRET,
            "walletId": source_wallet_id,
            "destinationAddress": destination_address,
            "amount": [amount],
            "tokenId": "USDC", # ID do token USDC na rede selecionada
            "feeLevel": "MEDIUM"
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()

agent_stack_service = CircleAgentStack()
