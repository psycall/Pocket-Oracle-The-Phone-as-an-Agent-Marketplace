from web3 import Web3
from .config import ARC_RPC_URL, PRIVATE_KEY, ESCROW_CONTRACT_ADDRESS
from .circle_service_real import circle_service
import json
import asyncio

class OrvionSettlementEngine:
    """
    Motor de escala industrial para liquidação atômica e em lote.
    """
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(ARC_RPC_URL))
        self.account = self.w3.eth.account.from_key(PRIVATE_KEY)
        
        # ABI completa para OrvionEscrow
        self.abi = [
            {"inputs":[{"name":"_settlementId","type":"bytes32"}],"name":"releaseSettlement","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"name":"_settlementId","type":"bytes32"}],"name":"settlements","outputs":[{"name":"employer","type":"address"},{"name":"agent","type":"address"},{"name":"amount","type":"uint256"},{"name":"isReleased","type":"bool"},{"name":"isDisputed","type":"bool"},{"name":"taskId","type":"string"}],"stateMutability":"view","type":"function"}
        ]
        self.contract = self.w3.eth.contract(address=ESCROW_CONTRACT_ADDRESS, abi=self.abi)

    def process_atomic_settlement(self, settlement_id: str, agent_wallet_id: str):
        """
        Executa o fluxo atômico individual.
        """
        settlement_data = self.contract.functions.settlements(settlement_id).call()
        if settlement_data[3]: # isReleased
            return {"status": "error", "message": "Already released"}

        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.contract.functions.releaseSettlement(settlement_id).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 250000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        amount_str = str(settlement_data[2] / 10**6)
        circle_res = circle_service.initiate_settlement_payment(
            wallet_id=agent_wallet_id,
            destination_address=settlement_data[1],
            amount=amount_str
        )

        return {
            "status": "success",
            "arc_tx_hash": tx_hash.hex(),
            "circle_response": circle_res
        }

    async def process_batch_settlement(self, requests: list):
        """
        Processa múltiplos pagamentos em paralelo para escala massiva.
        """
        tasks = []
        for req in requests:
            tasks.append(asyncio.to_thread(
                self.process_atomic_settlement, 
                req["settlement_id"], 
                req["agent_wallet_id"]
            ))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

settlement_engine = OrvionSettlementEngine()
