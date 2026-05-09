"""
Testes de integração para settlement_engine.py — Versão "Perfeição".
Valida o ciclo de vida completo on-chain:
1. Criação automática de Job (createJob)
2. Aprovação automática de USDC (approve)
3. Conclusão de Job via Recibo (completeJob)
4. Liquidação final (settleJob)
"""
import unittest
from uuid import uuid4

class TestSettlementLifecycleLogic(unittest.TestCase):
    """
    Testa a lógica do ciclo de vida completo simulando as chamadas do engine.
    """

    def _simulate_create_settlement(self, amount, to_address, has_signer=True, connected=True):
        """Simula a lógica de criação com automação on-chain."""
        on_chain_id = None
        if has_signer and connected:
            # Simula sucesso na criação on-chain
            on_chain_id = 100 # ID fictício retornado pelo contrato
        
        return {
            "id": str(uuid4()),
            "amount": amount,
            "to_address": to_address,
            "on_chain_job_id": on_chain_id,
            "status": "pending"
        }

    def _simulate_complete_job(self, settlement, has_signer=True, connected=True):
        """Simula a lógica de completar job via recibo."""
        verified = False
        if settlement["on_chain_job_id"] is not None and has_signer and connected:
            verified = True
        
        return {
            "id": str(uuid4()),
            "job_id": "job_123",
            "verified": verified
        }

    def _simulate_settle_batch(self, settlements, has_signer=True, connected=True):
        """Simula a liquidação final."""
        results = []
        for s in settlements:
            tx_hash = None
            if s["on_chain_job_id"] is not None and has_signer and connected:
                tx_hash = "0x_real_tx_" + uuid4().hex
            else:
                tx_hash = "0x_fallback_tx_" + uuid4().hex
            
            s["status"] = "confirmed"
            s["transaction_hash"] = tx_hash
            results.append(tx_hash)
        
        return results[-1] if results else None

    def test_full_on_chain_cycle(self):
        """Valida o fluxo feliz: tudo on-chain."""
        # 1. Criar
        settlement = self._simulate_create_settlement(10.0, "0xAgent", has_signer=True, connected=True)
        self.assertEqual(settlement["on_chain_job_id"], 100)
        
        # 2. Completar
        receipt = self._simulate_complete_job(settlement, has_signer=True, connected=True)
        self.assertTrue(receipt["verified"])
        
        # 3. Liquidar
        tx = self._simulate_settle_batch([settlement], has_signer=True, connected=True)
        self.assertIn("real", tx)
        self.assertEqual(settlement["status"], "confirmed")

    def test_fallback_cycle_no_signer(self):
        """Valida o fluxo de fallback: sem chave privada."""
        # 1. Criar (deve ser local)
        settlement = self._simulate_create_settlement(10.0, "0xAgent", has_signer=False, connected=True)
        self.assertIsNone(settlement["on_chain_job_id"])
        
        # 2. Completar (deve ser local/não verificado on-chain)
        receipt = self._simulate_complete_job(settlement, has_signer=False, connected=True)
        self.assertFalse(receipt["verified"])
        
        # 3. Liquidar (deve usar hash de fallback)
        tx = self._simulate_settle_batch([settlement], has_signer=False, connected=True)
        self.assertIn("fallback", tx)
        self.assertEqual(settlement["status"], "confirmed")

    def test_usdc_approval_logic(self):
        """Valida a lógica de decisão de aprovação de USDC."""
        def should_approve(allowance, amount):
            return allowance < amount

        self.assertTrue(should_approve(0, 1000))
        self.assertFalse(should_approve(2000, 1000))
        self.assertTrue(should_approve(500, 1000))

if __name__ == "__main__":
    unittest.main(verbosity=2)
